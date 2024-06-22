import socket
from datetime import datetime

UDP_IP = "192.168.0.100"
UDP_PORT = 10000
CSV_HEADER = "alive_0,bus_current_0,bus_voltage_0,heatsink_temp_0,motor_temp_0,rail_15v_0,rail_3v3_0,rail_1v9_0,dsp_temp_0,error_flags_0,limit_flags_0,rx_error_count_0,tx_error_count_0,motor_velocity_0,vehicle_velocity_0,phase_current_b_0,alive_1,bus_current_1,bus_voltage_1,heatsink_temp_1,motor_temp_1,rail_15v_1,rail_3v3_1,rail_1v9_1,dsp_temp_1,error_flags_1,limit_flags_1,rx_error_count_1,tx_error_count_1,motor_velocity_1,vehicle_velocity_1,phase_current_b_1"

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
