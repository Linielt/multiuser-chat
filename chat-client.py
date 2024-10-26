import json


def usage():
    print("usage: chat-client.py nickname host port")

def send_hello_payload(client_socket, nickname):
    hello_packet = b""
    hello_payload = {
        "type": "hello",
        "nickname": nickname,
    }
    hello_bytes = json.dumps(hello_payload).encode("utf-8")
    hello_len_bytes = len(hello_bytes).to_bytes(2, byteorder="big")
    hello_packet += hello_len_bytes + hello_bytes

    client_socket.sendall(hello_packet)

def send_chat_payload(client_socket, message):
    chat_packet = b""
    chat_payload = {
        "type": "chat",
        "message": message,
    }
    chat_bytes = json.dumps(chat_payload).encode("utf-8")
    chat_len_bytes = len(chat_bytes).to_bytes(2, byteorder="big")
    chat_packet += chat_len_bytes + chat_bytes
    client_socket.sendall(chat_packet)

