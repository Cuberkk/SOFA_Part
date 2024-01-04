import socket

def Receive_Data():
   server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server_socket.bind(('localhost', 12345))
   server_socket.listen()
   print("Server Starts, Waiting for connection")

   while True:
      connection, address = server_socket.accept()
      print(f"Receive the connection from {address}")
      
      try:
            while True:
                data = connection.recv(1024)
                if not data:
                    # If there is no data recieved, break
                    break
                print("Received data:", data.decode())
      except Exception as e:
         print(f"Error: {e}")
         
if __name__ == "__main__":
    Receive_Data()