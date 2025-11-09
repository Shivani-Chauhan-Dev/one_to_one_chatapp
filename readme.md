# 🗨️ One-to-One Chat App (WebSocket)

A simple **Python WebSocket-based chat application** that allows two users to chat with each other in real-time — directly via the terminal.  
This project includes both a WebSocket **server** and **clients** that communicate over the same WebSocket connection.

---

## 🚀 Features

- Real-time one-to-one chat between two users  
- Uses WebSocket protocol for persistent connections  
- Lightweight and easy to extend  
- Terminal-based message input and output  
- JSON message format with sender/receiver info  

---


---

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/one_to_one_chat.git
cd one_to_one_chat

python3 -m venv venv
source venv/bin/activate


pip install -r requirements.txt

python3 server.py

python3 client1.py

python3 client2.py
