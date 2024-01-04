import socket

def send_data(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))  # 连接到服务端

    client_socket.sendall(data.encode())
    print("Sent")
    socket.close()
    
if __name__ == "__main__":
    while True:
        data = input([1,1])
        if data.lower() == 'exit':
            break
        send_data(data)