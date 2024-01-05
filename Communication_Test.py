import socket
import json
import time

def Receive_Data():
   server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server_socket.bind(('localhost', 12345))
   server_socket.listen()
   server_socket.settimeout(60) #Set 60s timeout
   
   print("Server Starts, Waiting for connection")
   
   try:
       while True:
           try:
               connection, address = server_socket.accept()
               print(f"Receive the conncetion from {address}")
               
               while True:
                   try:
                       data = connection.recv(1024)
                       if not data:
                           break
                       data_arr = json.loads(data.decode())
                       target1 = data_arr[0][0]
                       target2 = data_arr[1][0]
                       print("Target1:", target1, "Target2:", target2)
                   
                   except Exception as e:
                       print(f"Error: {e}")
                       break
               
           except socket.timeout:
               print("Server shutdown due to timeout")
               break
           
           finally:
               connection.close()
               
#    except KeyboardInterrupt:
#        print("Server shutdown via KeyboardInterrupt")
       
   finally:
       server_socket.close()
       print("Server Stopped")
         
if __name__ == "__main__":
    Receive_Data()