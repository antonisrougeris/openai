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
