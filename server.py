import socket


clients = []

# Create a server socket
serverSocket = socket.socket()
serverSocket.bind(("127.0.0.1", 9999))  # Bind to localhost, port 9999
serverSocket.listen(2)  # Wait for clients
print("Server is listening...")


count = 0

while (True):

    # wait for the two agents to connect

    (clientConnection, clientAddress) = serverSocket.accept()

    count = count + 1

    clients.append(clientConnection)

    (clientConnection, clientAddress) = serverSocket.accept()

    count = count + 1

    clients.append(clientConnection)

    print("Accepted {} connections".format(count))

    msg = str.encode("Connected to the server")

    #send the msg to both agents
    clients[0].send(msg)
    clients[1].send(msg)
    
    
    Time = input("Enter game time: ")
    Time = f"Time:{Time}"
    msg = str.encode(Time)
    clients[0].send(msg)
    clients[1].send(msg)
    print("Game time sent to both players.")
    
    msg = str.encode("Begin")
    clients[0].send(msg)
    clients[1].send(msg)       
        
    while True:
        for i, client in enumerate(clients):
            try:
                message = client.recv(1024).decode()
                if not message:
                    continue

                print(f"Player {i+1} says: {message}")

                # If a player sends "exit", stop the game
                if message.lower() == "exit":
                    print("Game is ending.")
                    for c in clients:
                        c.send(str.encode("exit"))
                    break

            except Exception as e:
                 print(f"Error receiving data from Player {i+1}: {e}")
                 break
        
        break
    break
# Close connection
serverSocket.close()
