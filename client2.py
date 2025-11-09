import websocket
import json
import threading
import time


def on_message(ws, message):
    data = json.loads(message)
    print(f"New message from {data['from']}: {data['message']}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

def on_open(ws):
    recipient = {"username": "shivani","id": 2}
    ws.send(json.dumps(recipient))

    def send_messages():
        while True:
            message = input("Enter your message: ")
            reciver_recipient = {"username": "sagar", "id": 1}
            msg_data = {
                "type": "chat",
                "sender": recipient,
                "to": reciver_recipient,
                "message": message,
            }
            ws.send(json.dumps(msg_data))
            time.sleep(1)

    threading.Thread(target=send_messages).start()

if __name__ == "__main__":
    ws_url = "ws://localhost:4000"  
    ws = websocket.WebSocketApp(
        ws_url, on_message=on_message, on_error=on_error, on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()
