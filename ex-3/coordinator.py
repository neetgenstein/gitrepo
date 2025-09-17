import socket
import threading

CS_LOCKED = False

def handle_client(conn):
    global CS_LOCKED
    msg = conn.recv(1024).decode()
    if msg == "REQUEST":
        if not CS_LOCKED:
            conn.send("GRANT".encode())
            CS_LOCKED = True
        else:
            conn.send("DENY".encode())
    elif msg == "RELEASE":
        CS_LOCKED = False
    conn.close()

def run():
    s = socket.socket()
    s.bind(('localhost', 6000))  # Coordinator fixed at port 6000
    s.listen()
    print("[Coordinator] Running...")
    while True:
        conn, _ = s.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    run()
