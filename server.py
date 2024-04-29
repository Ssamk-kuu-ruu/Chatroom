import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode(FORMAT))
            nicknames.remove(nickname)
            break

def receive_message():
    while True:
        client, address = server.accept()
        print(f"[LISTENING]     Connected with {str(address)}")

        client.send('MYNAME'.encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'[NEW CONNECTION]     {nickname} joined the chat!'.encode(FORMAT))
        client.send('Connected to the server!'.encode(FORMAT))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]     {threading.active_count() - 1}")

print("[STARTING]     Server is Starting...")
receive_message()