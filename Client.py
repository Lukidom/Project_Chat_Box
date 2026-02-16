import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 9000))

def recieve():
    while True:
        msg = sock.recv(1024)
        print(msg)

        