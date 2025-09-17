import socket
import time

def request_cs(pid):
    s = socket.socket()
    s.connect(('localhost', 6000))
    s.send("REQUEST".encode())
    reply = s.recv(1024).decode()
    s.close()
    return reply

def release_cs():
    s = socket.socket()
    s.connect(('localhost', 6000))
    s.send("RELEASE".encode())
    s.close()

def run(pid):
    while True:
        input(f"[{pid}] Press Enter to request CS...")
        reply = request_cs(pid)
        if reply == "GRANT":
            print(f"[{pid}] Entering CS...")
            time.sleep(2)
            print(f"[{pid}] Exiting CS...")
            release_cs()
        else:
            print(f"[{pid}] Access Denied. Try again later.")

if __name__ == "__main__":
    import sys
    run(sys.argv[1])
