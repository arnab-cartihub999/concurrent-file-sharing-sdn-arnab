import socket
import os

HOST = "127.0.0.1"
PORT = 5000
DOWNLOAD_FOLDER = "downloads"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print(client.recv(1024).decode())

while True:
    command = input("Enter command: ")

    client.sendall(command.encode())

    if command == "QUIT":
        break

    if command.startswith("DOWNLOAD "):
        filename = command[9:].strip()

        response = client.recv(2)

        if response == b"OK":
            filepath = os.path.join(DOWNLOAD_FOLDER, filename)

            with open(filepath, "wb") as f:
                while True:
                    data = client.recv(4096)

                    if data.endswith(b"\nEND"):
                        f.write(data[:-4])
                        break

                    f.write(data)

            print("File downloaded successfully")

        else:
            print(response.decode())

    else:
        response = client.recv(4096)
        print(response.decode())

client.close()