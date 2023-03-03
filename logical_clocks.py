import multiprocessing
import time
import threading
import queue
from random import randint

class VirtualMachine():
    def __init__(self, ticks):
        # set ID for the machine to be added to queue
        self.id = id
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
                # m0 sends to m1, m1 sends to m2, m2 sends to m0
                rec = [(self.id + 1) % 3]
            elif val == 2:
                # m0 sends to m2, m1 sends to m0, m2 sends to m1
                rec = [(self.id + 2) % 3]
            elif val == 3:
                # m0 sends to m1/2, m1 sends to m2/0, m2 sends to m0/1
                rec = [(self.id + 1)%3, (self.id + 2)%3]
            else:
                pass

# will run each server -- loop and solicit messages, randomly
# select ints to determine if messages are sent
def run_server():
    pass 

if __name__ == "__main__":
    ports = [2048, 2049, 2050]
    # create three VM/servers with each of the ports
