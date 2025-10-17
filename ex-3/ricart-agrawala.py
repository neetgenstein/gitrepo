import socket
import threading
import time
import sys

# List of all process ports
PROCESS_PORTS = [5001, 5002, 5003]

# Set to keep track of REPLY messages received
RECEIVED_REPLIES = set()


def listen(my_port):
    """
    Thread function to listen for incoming messages.
    Handles REQUEST and REPLY messages.
    """
    global RECEIVED_REPLIES
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', my_port))
    server.listen()
    print(f"[{my_port}] Listening for messages...")

    while True:
        conn, addr = server.accept()
        try:
            msg = conn.recv(1024).decode()

            if msg.startswith("REQUEST"):
                sender_port = int(msg.split(":")[1])
                print(f"[{my_port}] Received REQUEST from {sender_port}")
                conn.send(f"REPLY:{my_port}".encode())

            elif msg.startswith("REPLY"):
                sender_port = int(msg.split(":")[1])
                print(f"[{my_port}] Received REPLY from {sender_port}")
                RECEIVED_REPLIES.add(sender_port)

        except Exception as e:
            print(f"[{my_port}] Error while receiving message: {e}")
        finally:
            conn.close()


def request_cs(my_port):
    """
    Request access to the Critical Section (CS).
    Sends REQUEST to all other processes and waits for REPLYs.
    """
    global RECEIVED_REPLIES
    RECEIVED_REPLIES = set()
    print(f"[{my_port}] Requesting Critical Section...")

    for port in PROCESS_PORTS:
        if port != my_port:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('localhost', port))
                s.send(f"REQUEST:{my_port}".encode())

                reply = s.recv(1024).decode()
                if reply.startswith("REPLY"):
                    sender_port = int(reply.split(":")[1])
                    print(f"[{my_port}] Received REPLY from {sender_port}")
                    RECEIVED_REPLIES.add(sender_port)

            except Exception as e:
                print(f"[{my_port}] Could not connect to {port}: {e}")
            finally:
                s.close()

    # Wait until all REPLYs received
    while len(RECEIVED_REPLIES) < len(PROCESS_PORTS) - 1:
        print(f"[{my_port}] Waiting... Received replies: {RECEIVED_REPLIES}")
        time.sleep(0.5)

    # Entering and exiting critical section
    print(f"[{my_port}] Entering Critical Section...")
    time.sleep(2)
    print(f"[{my_port}] Exiting Critical Section...")


def run(my_port):
    """
    Start listening thread and wait for user input to request CS.
    """
    threading.Thread(target=listen, args=(my_port,), daemon=True).start()
    while True:
        input(f"[{my_port}] Press Enter to request CS...")
        request_cs(my_port)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    if port not in PROCESS_PORTS:
        print(f"Port {port} not recognized. Use one of {PROCESS_PORTS}.")
        sys.exit(1)

    run(port)


# python ricart_agrawala.py 5001
# python ricart_agrawala.py 5002
# python ricart_agrawala.py 5003

# python token_ring.py 5002
# python token_ring.py 5003
# python token_ring.py 5001 start

# python coordinator.py

# python centralized_client.py P1
# python centralized_client.py P1