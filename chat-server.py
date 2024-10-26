import json
import sys
import socket

import select


def usage():
    print("usage: chat-server.py port")


def create_chat_payload(nickname, message):
    """
    Creates payload containing data related to message sent by the client
    to rebroadcast to all other clients
    :param nickname:
    :param message:
    :return:
    """
    chat_payload = {"type": "chat", "nick": nickname, "message": message}
    chat_bytes = json.dumps(chat_payload).encode("utf-8")
    return chat_bytes


def create_join_payload(nickname):
    """
    Creates payload to send to clients when a new client joins the server
    :param nickname:
    :return:
    """
    join_payload = {"type": "join", "nick": nickname}
    join_bytes = json.dumps(join_payload).encode("utf-8")
    return join_bytes


def create_leave_payload(nickname):
    """
    Creates payload to send to clients when a client leaves the server
    :param nickname:
    :return:
    """
    leave_payload = {"type": "leave", "nick": nickname}
    leave_bytes = json.dumps(leave_payload).encode("utf-8")
    return leave_bytes


def create_list_payload(nicknames):
    """
    Create payload containing list of nicknames of clients connected to the server
    :return:
    """
    list_payload = {"type": "list", "nicknames": list(nicknames.values())}
    list_bytes = json.dumps(list_payload).encode("utf-8")
    return list_bytes


def broadcast(sender_socket, list_of_clients, data):
    """
    Sends given data to all clients on list_of_clients
    :param sender_socket:
    :param list_of_clients:
    :param data:
    :return:
    """
    for client in list_of_clients:
        if client != sender_socket:
            # Checks if client is not the sender
            client.sendall(data)


def run_server(port):
    """
    Main process that starts the server on the given port number
    :param port:
    :return:
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", port))
    server_socket.listen(5)

    read_set = {server_socket}
    nicknames = {}

    while True:
        ready_to_read, _, _ = select.select(read_set, {}, {})
        for sock in ready_to_read:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                read_set.add(client_socket)
                print(f"{client_socket.getpeername()}: connected")
            elif sock != server_socket:
                try:
                    data = sock.recv(1024)
                except ConnectionError:
                    print(f"Connection lost: {sock.getpeername()}")
                    if sock in read_set:
                        read_set.remove(sock)
                    broadcast(
                        server_socket, read_set, create_leave_payload(nicknames[sock])
                    )
                    if sock in nicknames:
                        nicknames.pop(sock)
                    continue

                if data:
                    payload = json.loads(data.decode("utf-8"))
                    try:
                        if payload["type"] == "hello":
                            nicknames[sock] = payload["nick"]
                            join_payload = create_join_payload(payload["nick"])
                            broadcast(server_socket, read_set, join_payload)
                        elif payload["type"] == "chat":
                            chat_nick = nicknames[sock]
                            chat_payload = create_chat_payload(
                                chat_nick, payload["message"]
                            )
                            broadcast(server_socket, read_set, chat_payload)
                        elif payload["type"] == "list":
                            sock.sendall(create_list_payload(nicknames))
                    except ConnectionError:
                        print(f"Connection lost: {sock.getpeername()}")
                        if sock in read_set:
                            read_set.remove(sock)
                        broadcast(
                            server_socket,
                            read_set,
                            create_leave_payload(nicknames[sock]),
                        )
                        if sock in nicknames:
                            nicknames.pop(sock)
                elif data is None:
                    read_set.remove(sock)
                    nicknames.pop(sock)
                    sock.close()
                    leave_payload = create_leave_payload(nicknames[sock])
                    broadcast(server_socket, read_set, leave_payload)


def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        sys.exit(1)

    run_server(port)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
