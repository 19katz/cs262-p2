import multiprocessing
import time
import threading
import socket
import queue
from random import randint

class VirtualMachine():
    def __init__(self, host, port, ticks):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.host = host
        self.port = port
        # set a random clock rate (randint 1-6, number of ticks per real world seconds)
        self.ticks = ticks
        # for holding incoming messages
        self.queue = queue.Queue()
        # init logs and clear logs each run
    
    def send_msg(self):
        global_time = time.time()
        if not self.queue.empty():
            print("Queue is not empty!")
        else:
            val = randint(1,10)
            if val == 1:
                #send to machine 2
                pass
            elif val == 2:
                #send to machine 3
                pass
            elif val == 3:
                #send to machine 2 and 3
                pass
            else:
                pass

# will run each server -- loop and solicit messages, randomly
# select ints to determine if messages are sent
def run_server():
    pass 

if __name__ == "__main__":
    ports = [2048, 2049, 2050]
    # create three VM/servers with each of the ports
