import socket

HOST, PORT = "localhost", 10000
data = b"Redes~I"

# Create a TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
s.connect((HOST, PORT))

# Send the data
s.send(data)
