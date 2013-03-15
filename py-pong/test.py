#test
import socket
clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clisock.connect(('127.123.0.1', 20000 ))
clisock.send("hello")
print clisock.recv(100)
clisock.close()
