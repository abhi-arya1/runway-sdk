import logging
from datetime import datetime
from pathlib import Path
import sys
from runway.errors import RunwayError
from typing import Literal


LogTo = Literal["console", "file", "both"]


class RunwayLogger:
    def __init__(self, name: str = "runway", log_to: LogTo = "both"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d")
        file_handler = logging.FileHandler(f"logs/runway_{timestamp}.log")
        file_handler.setLevel(logging.INFO)
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(log_format)   
        console_handler.setFormatter(log_format)
        
        if log_to == "file":
            self.logger.addHandler(file_handler)
        elif log_to == "console":
            self.logger.addHandler(console_handler)
        else:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def error(self, message: str, error: RunwayError = None):
        if error:
            error_message = f"{message} - {str(error)}"
            if error.traceback:
                error_message += f"\nTraceback:\n{error.traceback}"
        else:
            error_message = message
        self.logger.error(error_message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def debug(self, message: str):
        self.logger.debug(message)