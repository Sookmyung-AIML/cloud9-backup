from fastapi import FastAPI, WebSocket
from mangum import Mangum

app = FastAPI()

@app.websocket("wss://sa79u8gqgf.execute-api.ap-northeast-2.amazonaws.com/production/")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

handler = Mangum(app)
