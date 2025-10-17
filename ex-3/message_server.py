import socket
import threading

clients = []

def handle_client(conn, addr):
    print(f"Client connected: {addr}")
    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(f"{addr}: {msg}")
            broadcast(msg, conn)
        except:
            break
    conn.close()
    if conn in clients:
        clients.remove(conn)
    print(f"Client disconnected: {addr}")

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message.encode())
            except:
                client.close()
                if client in clients:
                    clients.remove(client)

def start_server(host='localhost', port=5000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()
    print(f"Server running on {host}:{port}")
    while True:
        try:
            conn, addr = server.accept()
            clients.append(conn)
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
        except KeyboardInterrupt:
            print("Server shutting down...")
            break
        except Exception as e:
            print(f"Server error: {e}")

    server.close()

if __name__ == "__main__":
    start_server()