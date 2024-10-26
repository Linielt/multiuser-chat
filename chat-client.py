import sys
import socket
import json


def usage():
    print("usage: chat-client.py nickname host port", file=sys.stderr)

def create_hello_packet(nickname):
    hello_object = {
        "type": "hello",
        "nickname": nickname,
    }

    hello_bytes = json.dumps(hello_object).encode("utf-8")
    hello_len_bytes = len(hello_bytes).to_bytes(2, byteorder='big')
    hello_packet = hello_len_bytes + hello_bytes
    return hello_packet

def main(argv):
    try:
        nickname = argv[1]
        host = argv[2]
        port = int(argv[3])
    except:
        usage()
        sys.exit(1)

    client_socket = socket.socket()
    client_socket.connect((host, port))

    for i in range(5):
        client_socket.sendall(create_hello_packet(nickname))

    while True:
        print("waiting")

    client_socket.close()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
