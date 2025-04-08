# Runway SDK

Open Source LLM Observability Platform

## Installation 
```bash
pip install runway-sdk
```

## Usage
```python 
from runway import RunwayApp
from runway.sdks import RunwayOpenAI
from os import getenv

app = RunwayApp(api_key="<NotImportantForNow>", title="My App", log_to="console")
client = RunwayOpenAI()

@app.serve(route="/")
def get_4o():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello, how are you?"}]
    )
    return response.choices[0].message.content

app.run()
```