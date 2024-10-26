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

    client_set = {listener_sock}

    while True:
        ready_to_read, _, _ = select.select(client_set, {}, {})
        for client_sock in ready_to_read:
            if client_sock == listener_sock:
                new_client_sock, client_address = listener_sock.accept()
                client_set.add(new_client_sock)
                print(f"{new_client_sock.getpeername()}: connected")
            elif client_sock != listener_sock:
                data = client_sock.recv(1024)

                if len(data) == 0:
                    print(f"{client_sock.getpeername()}: disconnected")
                    client_sock.close()
                    client_set.remove(client_sock)
                else:
                    client_sock.sendall(data)
                    print(f"{client_sock.getpeername()}: {data}")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
