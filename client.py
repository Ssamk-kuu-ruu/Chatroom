import socket
import threading

PORT = 5050
FORMAT = 'utf-8'
SERVER = "192.168.189.37"
ADDR = (SERVER, PORT)

print("Create your desired nickname...")
nickname = input("> ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send_message():
    while True:
        message = f'\n{nickname}: {input("")}'
        client.send(message.encode(FORMAT))

def recieve_message():
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            if message == "MYNAME":
                client.send(nickname.encode(FORMAT))
            else:
                print(message)

        except:
            print("An error occured!!")
            client.close()
            break

recieve_thread = threading.Thread(target=recieve_message)
recieve_thread.start()

send_thread = threading.Thread(target=send_message)
send_thread.start()
