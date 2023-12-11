import socket

HOST, PORT = "localhost", 10000

# Create a TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allocate the host and port
s.bind((HOST, PORT))

# Listen up to 1 client
s.listen(1)

# Wait for the incoming messages
connection, address = s.accept()

# Get 64 bytes from the socket buffer
data = connection.recv(64)

print(data)
