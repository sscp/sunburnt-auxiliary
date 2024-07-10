import socket
from datetime import datetime
IP_List = socket.gethostbyname_ex(socket.gethostname())[2]
UDP_IP = -1
for ip in IP_List:
    if int(ip[:3]) == 192:
        UDP_IP = ip
if UDP_IP == -1:
    print("Incorrect IP!")
while UDP_IP == -1:
    pass
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
    desired_headers = list(map(lambda x:x.strip("\n "),file.readlines()))
print(f"Printing: {desired_headers}")
while True:
    dataDict = {}
    data, addr = sock.recvfrom(2048) # buffer size is 2048 bytes

    strdata = data.decode("utf-8")
    
    with open(path, "a") as file:
        file.write(strdata)
    print("\n"*25)
    # cleaner print if one string printed all at once, then carriage return
    headers = CSV_HEADER.split(",")
    datas = strdata.split(",")
    printstr = ""
    print(len(headers), len(datas))
    for i in range(len(headers)):
        dataDict[headers[i]] = datas[i]
    for i in range(len(desired_headers)):
        header = desired_headers[i]
        blank = ' ' * (30 - len(header))   
        blank2 = ' ' * (6 - len(dataDict[header]))    
        printstr = printstr + f"{header}:{blank}{dataDict[header]}{blank2}"
        if (i%3 == 0):
            printstr+="\n"
        else:
            printstr+="\t"
    print(printstr, end="\r")


"""

enum BMSFlags
{
  NONE = 0;
  UNDER_2_VOLTS_FLAG        = 0x1;
  UNDER_2_5_VOLTS_FLAG      = 0x2;
  OVER_4_4_VOLTS_FLAG    = 0x4;
  OVER_4_2_VOLTS_FLAG          = 0x8;
  OVER_TEMP_SHORT_FLAG     = 0x10;
  OVER_TEMP_LONG_FLAG      = 0x20;
  PACK_OVERCURRENT_SHORT_FLAG  = 0x80;
  PACK_OVERCURRENT_LONG_FLAG  = 0x100;
  PRE_FAIL_FLAG     = 0x200;
  EXTERNAL_KILL = 0x400;
  LTC_CHIP_FAILED = 0x800;
}
enum State
{
  STARTUP          = 0;
  LV_SWITCH_ENABLE = 1;
  PRECHARGE_ENABLE        = 2;
  LOWSIDE_SHUT    = 3;
  HIGHSIDE_SHUT          = 4;
  LV_BUCK_ENABLE     = 5;
  PACK_NORMAL      = 6;
  FAULTED     = 7;
  HIGHSIDE_OPEN = 8;
  LOWSIDE_OPEN  = 9;
  PRECHARGE_DISABLE = 10;
}


"""