import multiprocessing
import time
import threading
import socket
import Queue

class VirtualMachine():
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.host = host
        self.port = port
        # for holding incoming messages
        self.queue = Queue()

# will run each server -- loop and solicit messages, randomly
# select ints to determine if messages are sent
def run_server():
    pass 

if __name__ == "__main__":
    ports = [2048, 2049, 2050]
    # create three VM/servers with each of the ports
