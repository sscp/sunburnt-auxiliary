import socket
from datetime import datetime

UDP_IP = socket.gethostbyname_ex(socket.gethostname())[2][-1]
UDP_PORT = 6000
CSV_HEADER = ""
with open("headers.txt","r") as file:
    CSV_HEADER = ",".join(list(map(lambda x:x.strip("\n "),file.readlines())))
    
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
print(UDP_IP, UDP_PORT)

# print(CSV_HEADER)

time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
path = "logs/" + time + ".csv"

with open(path, "a") as file:
    file.write(CSV_HEADER+"\n")

with open("desired_headers.txt","r") as file:
    desired_headers = ",".join(list(map(lambda x:x.strip("\n "),file.readlines())))
print(f"Printing: {desired_headers}")
while True:
    dataDict = {}
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

    strdata = data.decode("utf-8")
    
    with open(path, "a") as file:
        file.write(strdata)

    # cleaner print if one string printed all at once, then carriage return
    headers = CSV_HEADER.split(",")
    datas = strdata.split(",")
    printstr = ""
    dataDict[headers[i]] = datas[i]
    for i in range(len(desired_headers)):
        header = desired_headers[i]
        blank = ' ' * (25 - len(header))   
        blank2 = ' ' * (6 - len(dataDict[header]))    
        printstr = printstr + f"{header}:{blank}{dataDict[header]}{blank2}"
        if (i%3 == 0):
            printstr+="\n"
        else:
            printstr+="\t"
    print(printstr, end="\r")
