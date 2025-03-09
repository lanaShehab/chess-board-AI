import socket

# Create a client socket
clientSocket = socket.socket()
clientSocket.connect(("127.0.0.1", 9999))  # Connect to the server

while(True):
    
    # Receive a message from the server
    message = clientSocket.recv(1024).decode()
    
    if not message:
        break
    
    print(f"{message}")
    
    if message.startswith("Time"):
        time = int(float(message[5:]) * 60)
        print(f"You got:{time} minutes to play.")
        msg = str.encode("OK")
        clientSocket.send(msg)
    
    elif message == "begin":
        print("Game is starting")
        

# Close connection
clientSocket.close()
