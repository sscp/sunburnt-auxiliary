import socket
from datetime import datetime

UDP_IP = "192.168.0.100"
UDP_PORT = 10000
CSV_HEADER = ""
with open("headers.txt","r") as file:
    CSV_HEADER = ",".join(list(map(lambda x:x.strip("\n "),file.readlines())))
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
path = "logs/" + time + ".csv"

with open(path, "a") as file:
    file.write(CSV_HEADER)

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

    strdata = data.decode("utf-8")
    
    with open(path, "a") as file:
        file.write(strdata)

    # cleaner print if one string printed all at once, then carriage return
    headers = CSV_HEADER.split(",")
    datas = strdata.split(",")
    printstr = ""
    for i in range(len(headers)):
        printstr = printstr + f"{headers[i]}: {datas[i]}\n"
    print(printstr, end="\r")
