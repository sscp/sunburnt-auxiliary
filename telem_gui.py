import socket
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

# Set up the socket for receiving data
UDP_IP = socket.gethostbyname_ex(socket.gethostname())[2][-1]
UDP_PORT = 6000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet, UDP
sock.bind((UDP_IP, UDP_PORT))
print(UDP_IP, UDP_PORT)

if UDP_IP[:3] != "192":
    print("Incorrect IP!")
while UDP_IP[:3] != "192":
    pass

# Read the CSV header 
with open("headers.txt", "r") as file:
    CSV_HEADER = file.readline().strip()

with open("desired_headers.txt", "r") as file:
    desired_headers = list(map(lambda x: x.strip("\n "), file.readlines()))
print(f"Printing: {' '.join(desired_headers)}")

# Create the main window
root = tk.Tk()
root.title("Telemetry Data")

# Create a smaller font
small_font = Font(root, size=8)

# Create a canvas to hold the Treeview
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add scrollbars
vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
vsb.pack(side=tk.RIGHT, fill="y")
hsb = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
hsb.pack(side=tk.BOTTOM, fill="x")
canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

# Create a frame to hold the Treeview and headers
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Function to update the scroll region
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_frame_configure)

# Function to split headers into rows
def split_headers(headers, splits):
    i = 0
    for k in splits:
        yield headers[i:i + k]
        i += k

# Split desired headers into rows specified below - see desired_headers to get numbers
splits = [10, 8, 5, 5, 5, 5, 5, 5, 8, 8, 8, 8]
header_rows = list(split_headers(desired_headers, splits))

treeviews = []

# Create multiple Treeview widgets for different rows of headers
for header_row in header_rows:
    tree = ttk.Treeview(frame, columns=header_row, show='headings')
    for header in header_row:
        tree.heading(header, text=header)
        tree.column(header, width=100)
    tree.pack(fill=tk.X, expand=True)
    treeviews.append(tree)
    tree.configure(height=1)  # Adjust row height
    tree.tag_configure('small_font', font=small_font)

def update_data():
    dataDict = {}
    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes

    strdata = data.decode("utf-8").strip()

    headers = CSV_HEADER.split(",")
    datas = strdata.split(",")
    for i in range(len(headers)):
        dataDict[headers[i]] = datas[i]

    # Clear existing data in Treeviews
    for tree in treeviews:
        tree.delete(*tree.get_children())

    # Insert new data into respective Treeviews
    for i, header_row in enumerate(header_rows):
        values = [dataDict.get(header, "") for header in header_row]
        treeviews[i].insert("", tk.END, values=values, tags=('small_font',))

    # Schedule the update_data function to be called again after 1000 ms (1 second)
    root.after(1000, update_data)

# Schedule the first call to update_data
root.after(1000, update_data)

# Start the GUI event loop
root.mainloop()
