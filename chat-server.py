import json


def usage():
    print("usage: chat-server.py port")

def send_chat_payload(server_socket, nickname, message):
    chat_packet = b""
    chat_payload = {
        "type": "chat",
        "nick": nickname,
        "message": message
    }

    chat_bytes = json.dumps(chat_payload).encode("utf-8")
    chat_len_bytes = len(chat_payload).to_bytes(2, byteorder="big")
    chat_packet += chat_len_bytes + chat_bytes

    server_socket.sendall(chat_packet)

def send_join_payload(server_socket, nickname):
    join_packet = b""
    join_payload = {
        "type": "join",
        "nick": nickname
    }
    join_bytes = json.dumps(join_payload).encode("utf-8")
    join_len_bytes = len(join_payload).to_bytes(2, byteorder="big")
    join_packet += join_len_bytes + join_bytes

    server_socket.sendall(join_packet)

def send_leave_payload(server_socket, nickname):
    leave_packet = b""
    leave_payload = {
        "type": "leave",
        "nick": nickname
    }
    leave_bytes = json.dumps(leave_payload).encode("utf-8")
    leave_len_bytes = len(leave_payload).to_bytes(2, byteorder="big")
    leave_packet += leave_len_bytes + leave_bytes

    server_socket.sendall(leave_packet)