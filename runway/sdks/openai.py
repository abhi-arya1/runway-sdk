import openai
from runway.logs import RunwayLogger
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class RunwayOpenAI(openai.OpenAI):
    def __init__(self, *args, **kwargs):
        if getenv("OPENAI_API_KEY"):
            super().__init__(api_key=getenv("OPENAI_API_KEY"), *args, **kwargs)
        else: 
            super().__init__(*args, **kwargs)
        self.logger = RunwayLogger(name="runway.openai")
    
    def _request(self, *args, **kwargs):
        """
        Override the base _request method to log usage information for all endpoints.
        
        This method intercepts all API requests and logs usage information.
        """
        response = super()._request(*args, **kwargs)

        model = kwargs.get('options', {}).json_data.get('model', 'unknown')
        
        if hasattr(response, 'usage'):
            usage = response.usage
            self.logger.info(f"\nOpenAI API Usage\n- Model: {model}"
                            f"- Prompt Tokens: {usage.prompt_tokens}\n"
                            f"- Completion Tokens: {usage.completion_tokens}\n"
                            f"- Total Tokens: {usage.total_tokens}")
        else:
            self.logger.info(f"OpenAI API Request - Endpoint: {kwargs.get('url', 'unknown')}, Method: {kwargs.get('method', 'unknown')}")
        
        return response

    
