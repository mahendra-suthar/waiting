from fastapi import WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.routing import APIRouter
from typing import List
from collections import deque, defaultdict
import json
import os

router = APIRouter()


class WaitingListManager:
    def __init__(self, volume_path: str):
        self.volume_path = volume_path
        self.load_waiting_list_from_volume()
        self.websocket_clients: List[WebSocket] = []

    def load_waiting_list_from_volume(self):
        file_path = os.path.join(self.volume_path, "waiting_lists.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.waiting_lists = defaultdict(dict)
                for queue_id, dates_data in data.items():
                    self.waiting_lists[queue_id] = {date: deque(positions) for date, positions in dates_data.items()}
        else:
            self.waiting_lists = defaultdict(dict)

    def save_waiting_lists_to_volume(self):
        file_path = os.path.join(self.volume_path, "waiting_lists.json")
        temp_file_path = file_path + '.temp'
        try:
            # Create directory structure if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(temp_file_path, 'w') as file:
                data_to_write = {queue_id: {date: list(positions) for date, positions in dates_data.items()}
                                 for queue_id, dates_data in self.waiting_lists.items()}
                json.dump(data_to_write, file)
            # Rename temp file to actual file
            os.replace(temp_file_path, file_path)
        except Exception as e:
            # Handle errors, e.g., log the error
            print(f"Error saving waiting lists to volume: {e}")
            # Remove temp file if it exists
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def get_waiting_list(self, queue_id: str, date: str = None):
        if date:
            return list(self.waiting_lists.get(queue_id, {}).get(date, deque()))
        return list(self.waiting_lists.get(queue_id, {}).values())

    def add_customer(self, queue_id: str, position: int, date: str = None):
        if date:
            if queue_id not in self.waiting_lists:
                self.waiting_lists[queue_id] = {}
            if date not in self.waiting_lists[queue_id]:
                self.waiting_lists[queue_id][date] = deque()
            self.waiting_lists[queue_id][date].append(position)
        else:
            print("---------[Please add date]----------")
        self.update_waiting_list(queue_id)

    def remove_customer(self, queue_id: str, date: str = None):
        if queue_id in self.waiting_lists and date in self.waiting_lists[queue_id]:
            self.waiting_lists[queue_id][date].popleft()
            self.update_waiting_list(queue_id)

    def clear_queue(self, queue_id: str, date: str = None):
        if queue_id in self.waiting_lists and date in self.waiting_lists[queue_id]:
            self.waiting_lists[queue_id][date].clear()
        else:
            self.waiting_lists[queue_id].clear()
        self.update_waiting_list(queue_id)

    async def connect_websocket(self, websocket: WebSocket):
        await websocket.accept()
        self.websocket_clients.append(websocket)

    def disconnect_websocket(self, websocket: WebSocket):
        try:
            self.websocket_clients.remove(websocket)
        except ValueError:
            pass  # Handle the case where the websocket is not in the list

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


# from collections import defaultdict, deque
# from typing import List, Optional
# from fastapi import WebSocket
# import json
# import os
#
# class WaitingListManager:
#     def __init__(self, volume_path: str):
#         self.volume_path = volume_path
#         self.load_waiting_list_from_volume()
#         self.websocket_clients: List[WebSocket] = []
#
#     def load_waiting_list_from_volume(self):
#         file_path = f"{self.volume_path}/waiting_lists.json"
#         if os.path.exists(file_path):
#             with open(file_path, 'r') as file:
#                 self.waiting_lists = defaultdict(deque, json.load(file))
#         else:
#             self.waiting_lists = defaultdict(deque)
#
#     def save_waiting_lists_to_volume(self):
#         try:
#             with open(f"{self.volume_path}/waiting_lists.json", 'w') as file:
#                 json.dump(dict(self.waiting_lists), file)
#         except Exception as e:
#             print(f"Error saving waiting lists: {e}")
#
#     def get_waiting_list(self, queue_id: str, date: Optional[str] = None) -> List[str]:
#         if date:
#             return list(self.waiting_lists.get(queue_id, {}).get(date, deque()))
#         return list(self.waiting_lists.get(queue_id, {}))
#
#     def add_customer(self, queue_id: str, position: str, date: Optional[str] = None):
#         if date:
#             if queue_id not in self.waiting_lists:
#                 self.waiting_lists[queue_id] = defaultdict(deque)
#             self.waiting_lists[queue_id][date].append(position)
#             self.update_waiting_list(queue_id)
#         else:
#             self.waiting_lists[queue_id].append(position)
#             self.update_waiting_list(queue_id)
#
#     def remove_customer(self, queue_id: str, date: Optional[str] = None):
#         if queue_id in self.waiting_lists:
#             if date and date in self.waiting_lists[queue_id]:
#                 self.waiting_lists[queue_id][date].popleft()
#             elif not date and self.waiting_lists[queue_id]:
#                 self.waiting_lists[queue_id].popleft()
#             self.update_waiting_list(queue_id)
#
#     def clear_queue(self, queue_id: str, date: Optional[str] = None):
#         if queue_id in self.waiting_lists:
#             if date and date in self.waiting_lists[queue_id]:
#                 self.waiting_lists[queue_id][date].clear()
#             elif not date and self.waiting_lists[queue_id]:
#                 self.waiting_lists[queue_id].clear()
#             self.update_waiting_list(queue_id)
#
#     async def connect_websocket(self, websocket: WebSocket):
#         await websocket.accept()
#         self.websocket_clients.append(websocket)
#
#     def disconnect_websocket(self, websocket: WebSocket):
#         self.websocket_clients.remove(websocket)
#
#     def update_waiting_list(self, queue_id: str):
#         self.save_waiting_lists_to_volume()
#         for client in self.websocket_clients:
#             try:
#                 client.send_text("update")
#             except Exception as e:
#                 print(f"Error updating waiting list for client: {e}")
#
# waiting_list_manager = WaitingListManager(volume_path="/app/data")
#
# @router.websocket("/ws/{queue_id}")
# async def websocket_endpoint(queue_id: str, websocket: WebSocket):
#     await waiting_list_manager.connect_websocket(websocket)
#     try:
#         while True:
#             await websocket.receive_text()
#     except WebSocketDisconnect:
#         waiting_list_manager.disconnect_websocket(websocket)
