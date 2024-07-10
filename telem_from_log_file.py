import socket
from datetime import datetime
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Set the log file path
log_file_path = "logs/07-07-2024_17-33-59.csv"

# Initialize InfluxDB client
token = "7xfcpLvj2jf7RYh8snjXjJeNWagDQlKxugw7aDl5ee_pqh4SrL8q3KbjgVP2R-57hIDjDXayBApCHlLA8cHa2A=="  # os.environ.get("INFLUXDB_TOKEN")
org = "Stanford Solar Car Project"
url = "http://localhost:8086"
bucket = "Telemetry"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

# Read CSV header from the log file
with open(log_file_path, "r") as file:
    CSV_HEADER = file.readline().strip()

# with open("desired_headers.txt", "r") as file:
#     desired_headers = list(map(lambda x: x.strip("\n "), file.readlines()))
# print(f"Printing: {desired_headers}")

# Open the log file for reading
log_file = open(log_file_path, "r")
log_file.readline()  # Skip the header line

while True:
    strdata = log_file.readline().strip()
    if not strdata:
        # Reached end of file, wait before trying again
        time.sleep(1)
        continue

    dataDict = {}
    headers = CSV_HEADER.split(",")
    datas = strdata.split(",")
    printstr = ""
    for i in range(len(headers)):
        dataDict[headers[i]] = datas[i]
        data = dataDict[headers[i]]
        if "On" in headers[i]:
            data = data[2:]
        try:
            data = float(data)
        except ValueError:
            pass
        if "CellVoltages_" in headers[i]:
            point = (
                Point(headers[i])
                .tag("cell_number",int(headers[i][13:]))
                .field("output_value", data)
            )

        else:
            point = (
                Point(headers[i])
                .field("output_value", data)
            )
        write_api.write(bucket=bucket, org=org, record=point)

    for i in range(len(headers)):
        header = headers[i]
        blank = ' ' * (30 - len(header))
        blank2 = ' ' * (6 - len(dataDict[header]))
        printstr = printstr + f"{header}:{blank}{dataDict[header]}{blank2}"
        if (i % 3 == 0):
            printstr += "\n"
        else:
            printstr += "\t"
    print(printstr, end="\r")
    time.sleep(1)

# Close the log file when done
log_file.close()
