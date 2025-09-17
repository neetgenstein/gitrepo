import socket
import threading
import time

NEXT_PORT = {5001: 5002, 5002: 5003, 5003: 5001,}

def listen(my_port, has_token):
    server = socket.socket()
    server.bind(('localhost', my_port))
    server.listen()
    print(f"[{my_port}] Listening...")

    while True:
        conn, _ = server.accept()
        msg = conn.recv(1024).decode()
        if msg == "TOKEN":
            print(f"[{my_port}] Received TOKEN.")
            enter_cs(my_port)
            send_token(NEXT_PORT[my_port])
        conn.close()

def enter_cs(my_port):
    print(f"[{my_port}] Entering CS...")
    time.sleep(2)
    print(f"[{my_port}] Exiting CS.")

def send_token(next_port):
    time.sleep(1)
    s = socket.socket()
    s.connect(('localhost', next_port))
    s.send("TOKEN".encode())
    s.close()

def run(my_port, start_token=False):
    threading.Thread(target=listen, args=(my_port, False), daemon=True).start()
    if start_token:
        time.sleep(2)
        send_token(my_port)

    while True:
        time.sleep(1)

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1])
    is_start = len(sys.argv) > 2 and sys.argv[2] == "start"
    run(port, is_start)
