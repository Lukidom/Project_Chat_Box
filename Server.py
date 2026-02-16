import socket

def Main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    socket.bind(("127.0.0.1", 9000))
    socket.listen()
    socket

