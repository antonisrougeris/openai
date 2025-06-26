# main.py
from fastapi import FastAPI, WebSocket
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.websocket("/ws/tts")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            async with openai.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice="coral",
                input=data,
                response_format="pcm",
            ) as response:
                async for chunk in response.iter_bytes():
                    await websocket.send_bytes(chunk)
    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()

# requirements.txt
fastapi
uvicorn
openai

# Dockerfile
FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

# .dockerignore
__pycache__
*.pyc
.env

# Railway Deployment Instructions
# 1. Create a Railway account at https://railway.app
# 2. New Project -> Deploy from GitHub -> Connect this repo
# 3. Add Environment Variable: OPENAI_API_KEY=sk-xxxxxxx
# 4. Deploy project
# 5. Get the deployed URL, use: wss://your-app-name.up.railway.app/ws/tts in your Flutter app
