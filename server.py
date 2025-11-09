import asyncio
import json
import websockets
from datetime import datetime

connected_clients = {}      
offline_messages = {} 

async def handle_connection(websocket):
    try:
        
        data = await websocket.recv()  #Login data
        print("Initial connection data:", data)

        try:
            user = json.loads(data)
        except json.JSONDecodeError:
            await websocket.send(json.dumps({"error": "Invalid JSON"}))
            return

        user_id = user.get("id")
        username = user.get("username")

        if not user_id or not username:
            await websocket.send(json.dumps({"error": "Missing id or username"}))
            return

        connected_clients[user_id] = websocket
        print(f"User '{username}' (ID: {user_id}) connected.")
        print(f"Connected clients: {list(connected_clients.keys())}")

        
        if user_id in offline_messages:  # stored offline messages 
            for msg in offline_messages[user_id]:
                await websocket.send(json.dumps(msg))
            del offline_messages[user_id]

       
        while True:   # Message Handling Loop 
            data = await websocket.recv()
            print("Received message:", data)

            try:
                msg_data = json.loads(data)
            except json.JSONDecodeError:
                await websocket.send(json.dumps({"error": "Invalid JSON"}))
                continue

            msg_type = msg_data.get("type")

            
            if msg_type == "chat": #Chat Message
                sender = msg_data.get("sender")  
                receiver = msg_data.get("to")    
                message_text = msg_data.get("message")

                if not sender or not receiver or not message_text:
                    await websocket.send(json.dumps({"error": "Incomplete chat message"}))
                    continue

                timestamp = datetime.utcnow().isoformat()
                response_payload = {
                    "type": "chat",
                    "from": sender,
                    "message": message_text,
                    "timestamp": timestamp
                }

                recipient_ws = connected_clients.get(receiver["id"])
                if recipient_ws:
                    await recipient_ws.send(json.dumps(response_payload))
                else:
                    print(f"User {receiver['username']} (ID: {receiver['id']}) is offline, storing message.")
                    offline_messages.setdefault(receiver["id"], []).append(response_payload)

            
            elif msg_type == "typing":  #Typing Indicator
                sender = msg_data.get("sender")
                receiver = msg_data.get("to")

                if sender and receiver:
                    recipient_ws = connected_clients.get(receiver["id"])
                    if recipient_ws:
                        await recipient_ws.send(json.dumps({
                            "type": "typing",
                            "from": sender
                        }))

            else:
                await websocket.send(json.dumps({"error": "Unknown message type"}))

    except websockets.exceptions.ConnectionClosed:
        print(f"User {username if 'username' in locals() else 'Unknown'} disconnected.")
    finally:
        if 'user_id' in locals() and user_id in connected_clients:
            del connected_clients[user_id]
        print(f"Connected clients after disconnection: {list(connected_clients.keys())}")

async def main():
    port = 4000
    print(f"WebSocket server running at ws://localhost:{port}")
    async with websockets.serve(handle_connection, "localhost", port):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
