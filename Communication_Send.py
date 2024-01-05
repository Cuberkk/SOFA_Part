import socket
import json
import time

def send_data(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))  # Connect to the Server
    
    try:
        while True:
            data_str = json.dumps(data)
            client_socket.sendall(data_str.encode())
            print("Sent")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down the connection.")
    finally:
        client_socket.close()
    
if __name__ == "__main__":
    data = [1,1]
    send_data(data)