import socket
import json

UDP_IP = "192.168.0.100"
UDP_PORT = 10000

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    
    decodeddat = json.loads(data)
    for i in decodeddat:
        print(i)
        outputstring = ""
        for j in decodeddat[i]:
            outputstring = outputstring + "\t" + j + ": " + str(decodeddat[i][j]) + "\n"
        print(outputstring, end="\r")
    print("\n")
