from typing import List

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles


app = FastAPI()


# FIXME вот такой формат сообщения, пока что это dict
class Message(BaseModel):
    type: str  # 'PLAYER' or 'MESSAGE'
    message: str  # 'START', 'STOP' or message text
    author: int


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id):
        del self.active_connections[client_id]

    # async def send_personal_message(self, message: dict, websocket: WebSocket):
    #     await websocket.send_json(message)

    async def broadcast(self, message: dict):
        for client_id, connection in self.active_connections.items():
            if client_id == message['author']:
                continue
            await connection.send_json(message)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            # await manager.send_personal_message(data, websocket)
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast(
            {
                'type': 'MESSAGE',
                'message': 'disconnected',
                'author': client_id
            }
        )


app.mount("/", StaticFiles(directory="static"), name="static")


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
