import pyfiglet
import sys
import socket
import threading
from queue import Queue
from datetime import datetime


# Using the fancy figlet banner
ascii_banner = pyfiglet.figlet_format("Swiss Scanner")
print(ascii_banner)

# Input target IP address or hostname

print_lock = threading.Lock()
target = input(str("Target IP or hostname: "))


# Resolve hostname if necessary
try:
    target_ip = socket.gethostbyname(target)
    print("Target IP:", target_ip)
except socket.gaierror:
    print("Hostname could not be resolved.")
    sys.exit()


# Scanning Banner

print("Scanning Target: " + target_ip)
print("X" * 30)

# Scanning for open ports

def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connection = s.connect((target_ip,port))
        with print_lock:
            print("\033[92mOpen Port:",port, "\033[0m")
        connection.close()
    except:
        pass

def threader():
    while True:
        worker = que.get()
        portscan(worker)
        que.task_done()

que = Queue()

# Scan for specific ports
for openPort in [20,21,22,23,25,53,69,80,137,139,443,445,8443,8080]:
    thread = threading.Thread(target=threader)
    thread.daemon = True
    thread.start()

for worker in range(1, 65535):
    que.put(worker)

que.join()

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
