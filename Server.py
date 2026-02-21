import socket
import threading


def main():
    host = "127.0.0.1"
    port = 9000
    buffer_size = 1024
    encoding = "utf-8"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()

    clients = []
    nicknames = []

# sends a message to all connected clients. if it can't recieve its marked for removal
    def broadcast(message):
        dead_clients = []
        for client in clients:
            try:
                client.send(message)
            except Exception:
                dead_clients.append(client)

        for dead_client in dead_clients:
            remove_client(dead_client)

# Removes disconnected clients
    def remove_client(client):
        if client not in clients:
            return

        index = clients.index(client)
        nickname = nicknames[index]

        clients.pop(index)
        nicknames.pop(index)

        try:
            client.close()
        except Exception:
            pass

        broadcast(f"{nickname} left the chat".encode(encoding))
        print(f"{nickname} disconnected")


# constantly recieves message from specific client handles commands, removes clients if they disconnect
    def handle(client):
        while True:
            try:
                message = client.recv(buffer_size)
                if not message:
                    remove_client(client)
                    break

                if message.decode(encoding).strip().lower() == "/users":
                    user_list = ", ".join(nicknames) if nicknames else "No users connected"
                    client.send(f"Online users: {user_list}".encode(encoding))
                    continue

                broadcast(message)

            except Exception:
                remove_client(client)
                break

# accepts new client connections infinitely. starts new thread to handle messages
    def receive():
        print(f"Server is listening on {host}:{port}")

        while True:
            client, address = sock.accept()
            print(f"Connected with {address}")

            client.send("NICK".encode(encoding))
            nickname = client.recv(buffer_size).decode(encoding).strip()

            if not nickname:
                nickname = f"Guest{len(clients) + 1}"

            clients.append(client)
            nicknames.append(nickname)

            print(f"Client name is {nickname}")
            broadcast(f"{nickname} joined the chat".encode(encoding))
            client.send("Connected to the server".encode(encoding))

            thread = threading.Thread(target=handle, args=(client,), daemon=True)
            thread.start()

    receive()


if __name__ == "__main__":
    main()