import socket

port = 53
ip = "127.0.0.1"
data = (
    b"D\xcb\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07"
    b"example\x03com\x00\x00\x01\x00\x01"
)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(data, (ip, port))
reply = sock.recv(512)
print(reply)
