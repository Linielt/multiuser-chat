import sys
import socket
import select


def usage():
    print("usage: chat-server.py port")

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        sys.exit(1)

    listener_sock = socket.socket()
    listener_sock.bind(('', port))
    listener_sock.listen()

    connected_clients = {listener_sock}

    while True:
        connected_clients, _, _ = select.select(connected_clients, {}, {})
        for client_sock in connected_clients:
            if client_sock == listener_sock:
                new_client_sock, client_address = listener_sock.accept()
                connected_clients.add(new_client_sock)
                print(f"{new_client_sock.getpeername()}: connected")
            elif client_sock != listener_sock:
                data = client_sock.recv(1024)

                if len(data) == 0:
                    print(f"{client_sock.getpeername()}: disconnected")
                    client_sock.close()
                    connected_clients.remove(client_sock)
                else:
                    print(f"{client_sock.getpeername()}: {data}")
