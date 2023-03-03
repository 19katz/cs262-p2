import multiprocessing
import time
import threading
import queue
from random import randint

class VirtualMachine():
    def __init__(self, ticks, machine_count, id):
        self.machine_count = machine_count
        # set ID for the machine to be added to queue
        self.id = id
        # set a random clock rate (randint 1-6, number of ticks per real world seconds)
        self.ticks = ticks
        # dictionary of queues to hold messages for all virtual machines
        self.system_queue = self.gen_queues()
        # queue to hold incoming messages for this id
        self.id_queue = self.system_queue[self.id]
        # init logical clock
        self.logical_clock = 0
        # init logs and clear logs each run 
    
    def gen_queues(self):
        system_queue = []
        for i in range(self.machine_count):
            system_queue.append(queue.Queue())
        return system_queue
    
    def send_msg(self):
        global_time = time.time()
        # increment logical clock by 1
        self.logical_clock += 1

        if not self.queue.empty():
            # get the logical clock time that was sent to you
            rec_logical_clock = self.id_queue.get()
            self.id_queue.pop()
            self.logical_clock = max(rec_logical_clock, self.logical_clock)
            # TODO: update log that it got a message, the global time (from system), length of message queue, and the machine logical clock time
            print("Queue is not empty!")
        else:
            val = randint(1,10)
            if val == 1:
                # m0 sends to m1, m1 sends to m2, m2 sends to m0
                rec = [(self.id + 1) % 3]
                self.system_queue[rec].put(self.logical_clock)
                # TODO: update log
            elif val == 2:
                # m0 sends to m2, m1 sends to m0, m2 sends to m1
                rec = [(self.id + 2) % 3]
                self.system_queue[rec].put(self.logical_clock)
                # TODO: update log
            elif val == 3:
                # m0 sends to m1/2, m1 sends to m2/0, m2 sends to m0/1
                rec = [(self.id + 1)%3, (self.id + 2)%3]
                self.system_queue[rec].put(self.logical_clock)
                # TODO: update log
            else:
                pass

# will run each server -- loop and solicit messages, randomly
# select ints to determine if messages are sent
def run_server():
    pass 

if __name__ == "__main__":
    vm = VirtualMachine(1, 3, 1)
    #vm.print_vals()
    vm.send_msg()