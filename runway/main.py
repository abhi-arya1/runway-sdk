import fastapi
from fastapi.responses import JSONResponse
import gunicorn.app.base
from typing import Any, Callable
from pathlib import Path
from os import getenv
from dotenv import load_dotenv
from runway.errors import RunwayError, APIKeyError, ConfigurationError, \
    RouteError, ServerError
from runway.logs import RunwayLogger, LogTo
from runway.pytypes import StatusCode



class RunwayApp(fastapi.FastAPI):
    def __init__(self, 
        api_key: str = None, 
        env_path: str = ".env", 
        log_to: LogTo = "both",
        **kwargs: Any # FastAPI Kwargs
    ):
        super().__init__(**kwargs)
        self._env_path = Path(env_path)
        self.logger = RunwayLogger(log_to=log_to)
        self.logger.info("Initializing RunwayApp")
        
        if api_key is not None:
            self._api_key = api_key
            self.logger.info(f"Using provided API key")
        else: 
            try: 
                load_dotenv(self._env_path)
                self._api_key = getenv("RUNWAY_API_KEY")
                if not self._api_key:
                    raise APIKeyError("RUNWAY_API_KEY not found in environment")
                self.logger.info("Loaded API key from environment")
            except FileNotFoundError:
                error = ConfigurationError("Environment file not found")
                self.logger.error("Failed to load environment file", error)
                raise error



    def serve(self, func: Callable = None, route: str = "/"):
        """
        Register a route handler function.
        
        This method can be used in two ways:
        1. As a decorator: @app.serve(route="/path")
        2. As a regular method: app.serve(func, route="/path")
        """
        def decorator(f):
            @self.get(route)
            def get():
                try:
                    result = f()
                    self.logger.info(f"HTTP GET {StatusCode.SUCCESS.value} OK: {route}")
                    return JSONResponse(content={
                        "hello": result
                    }, status_code=StatusCode.SUCCESS.value)
                except RunwayError as e:
                    self.logger.error(f"Runway error in route {route}", e)
                    return JSONResponse(
                        content={
                            "error": str(e),
                            "error_code": e.error_code,
                            "details": e.details
                        },
                        status_code=StatusCode.INTERNAL_SERVER_ERROR.value
                    )
                except Exception as e:
                    error = RouteError(f"Unexpected error in route {route}: {str(e)}")
                    self.logger.error("Route execution failed", error)
                    return JSONResponse(
                        content={
                            "error": str(error),
                            "error_code": error.error_code
                        },
                        status_code=StatusCode.INTERNAL_SERVER_ERROR.value
                    )
            return f
        
        if func is not None:
            return decorator(func)
        
        return decorator



    def run(self, host: str = "127.0.0.1", port: int = 8000):
        self.logger.info(f"Starting server on http://{host}:{port}")
        
        class StandaloneApplication(gunicorn.app.base.BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()

            def load_config(self):
                for key, value in self.options.items():
                    self.cfg.set(key.lower(), value)

            def load(self):
                return self.application

        options = {
            'bind': f'{host}:{port}',
            'workers': 4,
            'worker_class': 'uvicorn.workers.UvicornWorker',
            'accesslog': 'logs/access.log',
            'errorlog': 'logs/error.log',
            'loglevel': 'info'
        }
        
        # self.logger.info("Starting Gunicorn server with configuration:")
        # self.logger.info(f"Workers: {options['workers']}")
        # self.logger.info(f"Worker Class: {options['worker_class']}")
        self.logger.info(f"Server up!")
        
        try:
            StandaloneApplication(self, options).run()
            self.logger.info("Server started.")
        except Exception as e:
            error = ServerError(f"Failed to start server: {str(e)}")
            self.logger.error("Server startup failed", error)
            raise error
