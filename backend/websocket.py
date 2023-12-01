from fastapi import WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.routing import APIRouter
from typing import List
from collections import deque
import json
import os

router = APIRouter()


class WaitingListManager:
    def __init__(self, volume_path: str):
        self.volume_path = volume_path
        self.load_waiting_list_from_volume()
        self.websocket_clients: List[WebSocket] = []

    def load_waiting_list_from_volume(self):
        file_path = f"{self.volume_path}/waiting_lists.json"
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.waiting_lists = {queue_id: deque(data[queue_id]) for queue_id in data}
        else:
            self.waiting_lists = {}

    def save_waiting_lists_to_volume(self):
        with open(f"{self.volume_path}/waiting_lists.json", 'w') as file:
            print("-------saving-----")
            json.dump({queue_id: list(self.waiting_lists[queue_id]) for queue_id in self.waiting_lists}, file)

    def get_waiting_list(self, queue_id: str):
        return list(self.waiting_lists.get(queue_id, deque()))

    def add_customer(self, queue_id: str, position: str):
        if queue_id not in self.waiting_lists:
            self.waiting_lists[queue_id] = deque()
        self.waiting_lists[queue_id].append(position)
        self.update_waiting_list(queue_id)

    def remove_customer(self, queue_id: str):
        if queue_id in self.waiting_lists and self.waiting_lists[queue_id]:
            self.waiting_lists[queue_id].popleft()
            self.update_waiting_list(queue_id)

    async def connect_websocket(self, websocket: WebSocket):
        await websocket.accept()
        self.websocket_clients.append(websocket)

    def disconnect_websocket(self, websocket: WebSocket):
        self.websocket_clients.remove(websocket)

    def update_waiting_list(self, queue_id: str):
        self.save_waiting_lists_to_volume()
        for client in self.websocket_clients:
            try:
                client.send_text("update")
            except Exception as e:
                print(e)


waiting_list_manager = WaitingListManager(volume_path="/app/data")


@router.websocket("/ws/{queue_id}")
async def websocket_endpoint(queue_id: str, websocket: WebSocket):
    await waiting_list_manager.connect_websocket(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        waiting_list_manager.disconnect_websocket(websocket)

# Uncomment the following route if you want to use the commented-out POST endpoint
# @router.post("/add-to-queue/{queue_id}/{position}")
# async def add_to_queue(queue_id: str, position: str, waiting_list_manager: WaitingListManager = Depends()):
#     waiting_list_manager.add_customer(queue_id, position)
#     return {"message": f"User {position} added to the waiting list for employee {queue_id}."}
