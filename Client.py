import socket
import threading
nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9000))

running = True

""" The Recieve function is used to recieve messages from the server and other clients

NICK handshake allows the server to know who is sending message so it can format the message correctly

nickname: message

"""
def recieve():
    global running

    while running:
        try:
            message = client.recv(1024).decode("utf-8")

            if not message:
                print("Disconnected from server")
                running = False
                break

            if message == "NICK":
                client.send(nickname.encode("utf-8"))
            else:
                print(message)

        except Exception:
            if running:
                print("An error occurred!")
            running = False
            client.close()
            break


""" The Write function is used to send messages and commands to server

/quit = disconnect from server. 
"""

def write():
    global running

    print("Type /quit to leave")

    while running:
        try:
            text = input("").strip()
        except (EOFError, KeyboardInterrupt):
            text = "/quit"

        if not text:
            continue

        if text.lower() == "/quit":
            try:
                client.send("/quit".encode("utf-8"))
            except Exception:
                pass

            running = False
            client.close()
            print("Disconnected")
            break

        message = f"{nickname}: {text}"
        try:
            client.send(message.encode("utf-8"))
        except Exception:
            print("Could not send message")
            running = False
            client.close()
            break


recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

