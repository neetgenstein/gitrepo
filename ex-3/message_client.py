import socket
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print("\nReceived:", msg)
                print("You: ", end='', flush=True)
            else:
                break
        except:
            break
    sock.close()

def start_client(host='localhost', port=5000):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
    except ConnectionRefusedError:
        print(f"Unable to connect to server at {host}:{port}")
        return

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
    print(f"Connected to server at {host}:{port}. Type 'exit' to disconnect.")
    
    try:
        while True:
            msg = input("You: ")
            if msg.lower() == "exit":
                break
            client.send(msg.encode())
    except KeyboardInterrupt:
        print("\nDisconnected from server.")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()