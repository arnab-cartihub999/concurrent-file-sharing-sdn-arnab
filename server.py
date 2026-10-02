import socket
import threading
import os

HOST = "0.0.0.0"
PORT = 5000
SHARED_FOLDER = "shared_files"

os.makedirs(SHARED_FOLDER, exist_ok=True)


def handle_client(conn, addr):
    print("Client connected:", addr)

    try:
        conn.sendall(b"Welcome to the File Sharing Server\n")

        while True:
            data = conn.recv(1024).decode().strip()

            if not data:
                break

            if data == "LIST":
                files = os.listdir(SHARED_FOLDER)

                if files:
                    response = "\n".join(files)
                else:
                    response = "No files available"

                conn.sendall(response.encode())

            elif data.startswith("DOWNLOAD "):
                filename = data[9:].strip()
                filepath = os.path.join(SHARED_FOLDER, filename)

                if os.path.isfile(filepath):
                    conn.sendall(b"OK")

                    with open(filepath, "rb") as f:
                        while True:
                            chunk = f.read(4096)

                            if not chunk:
                                break

                            conn.sendall(chunk)

                    conn.sendall(b"\nEND")
                else:
                    conn.sendall(b"ERROR: File not found")

            elif data == "QUIT":
                break

            else:
                conn.sendall(b"Invalid command")

    except Exception as e:
        print("Error:", e)

    finally:
        conn.close()
        print("Client disconnected:", addr)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(5)

print("File Sharing Server started")
print("Listening on port", PORT)

while True:
    conn, addr = server.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(conn, addr)
    )

    thread.start()