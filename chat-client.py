import json
import socket
import sys
import threading

import chatui
from chatui import init_windows


def usage():
    print("usage: chat-client.py nickname host port")

def send_hello_payload(client_socket, nickname):
    """
    Sends payload to allow server to associate the client socket with a nickname
    This MUST be sent before any other packet
    :param client_socket:
    :param nickname:
    :return:
    """
    hello_payload = {
        "type": "hello",
        "nick": nickname,
    }
    hello_bytes = json.dumps(hello_payload).encode("utf-8")
    client_socket.sendall(hello_bytes)

def send_chat_payload(client_socket, message):
    """
    Sends a payload representing a chat message to the server
    :param client_socket:
    :param message:
    :return:
    """
    chat_payload = {
        "type": "chat",
        "message": message,
    }
    chat_bytes = json.dumps(chat_payload).encode("utf-8")
    client_socket.sendall(chat_bytes)

def send_messages(client_socket, nickname):
    """
    Reads messages sent by the client and sends them to the server as chat packet
    or performs special actions for inputs beginning with '/'
    :param client_socket:
    :param nickname:
    :return:
    """
    while True:
        message = chatui.read_command(f"{nickname}> ")
        if message == "/q":
            client_socket.close()
            chatui.end_windows()
            sys.exit(0)
        else:
            send_chat_payload(client_socket, message)

def receive_data(client_socket):
    """
    Receives data sent by the server, processes them and displays an appropriate message
    to the client
    :param client_socket:
    :return:
    """
    while True:
        data = client_socket.recv(1024)

        if data:
            payload = json.loads(data.decode("utf-8"))

            if payload['type'] == "chat":
                chatui.print_message(f"{payload['nick']}: {payload['message']}")
            elif payload['type'] == "join":
                chatui.print_message(f"*** {payload['nick']} has joined the chat")
            elif payload['type'] == "leave":
                chatui.print_message(f"*** {payload['nick']} has left the chat")
        else:
            client_socket.close()
            break

def main(argv):
    try:
        nickname = argv[1]
        host = argv[2]
        port = int(argv[3])
    except:
        usage()
        sys.exit(1)

    threads = []

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    init_windows()
    send_hello_payload(client_socket, nickname)

    sending_thread = threading.Thread(target=send_messages, args=(client_socket, nickname,))
    receiving_thread = threading.Thread(target=receive_data, args=(client_socket,))

    sending_thread.start()
    receiving_thread.start()
    threads.append(sending_thread)
    threads.append(receiving_thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
