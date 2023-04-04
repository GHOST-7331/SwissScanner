import pyfiglet
import sys
import socket
import threading
from queue import Queue
import re


# Creating the fancy swiss scanner banner with pyfiglet library

ascii_banner = pyfiglet.figlet_format("Swiss Scanner")
print(ascii_banner)

# Create a lock object from the threading module and set the target ip as a input

print_lock = threading.Lock()
target = input(str("Target IP or hostname: "))


# Tries to resolve a hostname to an IP address
try:
    target_ip = socket.gethostbyname(target)
    print("Target IP:", target_ip)
except socket.gaierror:
    print("Hostname could not be resolved.")
    sys.exit()


# Banner

print("Scanning Target: " + target_ip)
print("X" * 30)

# function that takes a port number, and attempts to connect using s.connect((target_ip,port))

def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connection = s.connect((target_ip,port))
        with print_lock:
            # send HTTP request to extract version info
            s.send(b"HEAD / HTTP/1.1\r\nHost: " + bytes(target, 'utf-8') + b"\r\n\r\n")
            response = s.recv(4096)
            version = re.search(b"Server: (.*)\r\n", response).group(1)
            print("\033[92mOpen Port: " + str(port) + "/tcp (" + version.decode() + ")\033[0m")
        connection.close()
    except:
        pass

# Function used to create and manage threads, using the Queue module 

def threader():
    while True:
        worker = que.get()
        portscan(worker)
        que.task_done()

que = Queue()

# Loop through common ports, creating a thread for each port until loop is resolved.

for openPort in [20,21,22,23,25,53,69,80,137,139,443,445,8443,8080]:
    thread = threading.Thread(target=threader)
    thread.daemon = True
    thread.start()

# This loop adds each port number 1 through 65535 to the que and waits for all the workers to resolve.

for worker in range(1, 65535):
    que.put(worker)

que.join()

# Used to handle potential exceptions when running the program.

try:
    pass

except KeyboardInterrupt:
    print("\nExiting program.")
    sys.exit()

except socket.error:
    print("\nServer not responding.")
    sys.exit()

except:
    print("\nAn error occurred.")
    sys.exit()

