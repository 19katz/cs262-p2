import time
import threading
import queue
import os
import socket
from random import randint
from multiprocessing import Process
from _thread import * 
from threading import Thread
import logging

class VirtualMachine:
    """Class that represents an individual machine."""
    def __init__(self, host, port, machine_count, id):
        self.machine_count = machine_count
        # host name for this machine
        self.host = host
        # port number for this machine
        self.port = port
        # will store the socket that is used to connect to/with other machines
        self.socket = None
        # set ID for the machine to be added to queue
        self.id = id
        # set a random clock rate (randint 1-6, number of ticks per real world seconds)
        self.ticks = randint(1, 6)
        # dictionary of queues to hold messages for all virtual machines
        self.system_queue = self.gen_queues()
        # queue to hold incoming messages for this id
        self.id_queue = self.system_queue[self.id]
        # init logical clock
        self.logical_clock = 0
        # init logs and clear logs each run 
    
    def consumer(conn):
        print("Connection accepted: " + str(conn))
        while True:
            data = conn.recv(1024)
            data_msg = data.decode('ascii')
            print("Received message " + data_msg)
            # add to queue 
            # -- i'm not sure how the current queue system works?
            # is it strictly necessary for every machine to hold every other machine's queue?
    
    def producer(self, other_port):
        success = False
        while not success:
            try:
                self.socket.connect((self.host, other_port))
                print("Successfully connected to " + str(other_port))
            except:
                pass
        
        while True:
            # based on the global variable val, send a message to this connection
            # read message off queue here i guess?
            # send_msg() 
            pass
    
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
            global val
            val = randint(1,10)
            if val == 1:
                # m0 sends to m1, m1 sends to m2, m2 sends to m0
                rec = [(self.id + 1) % 3]
                self.system_queue[rec].put(self.logical_clock)
                # TODO: update log with the send, the system time, and the logical clock time
            elif val == 2:
                # m0 sends to m2, m1 sends to m0, m2 sends to m1
                rec = [(self.id + 2) % 3]
                self.system_queue[rec].put(self.logical_clock)
                # TODO: update log with the send, the system time, and the logical clock time
            elif val == 3:
                # m0 sends to m1/2, m1 sends to m2/0, m2 sends to m0/1
                rec = [(self.id + 1)%3, (self.id + 2)%3]
                self.system_queue[rec].put(self.logical_clock)
                # TODO: update log with the send, the system time, and the logical clock time
            else:
                # TODO: update log with internal event, the system time, and the logical clock value.
                pass

    def start_machine(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.lostin()
        while True:
            conn, addr = self.socket.accept()
            start_new_thread(self.consumer, (conn,))


# will run each server -- loop and solicit messages, randomly
# select ints to determine if messages are sent
def run_server():
    # this can contain the "machine" function as in the demo code
    pass 

if __name__ == "__main__":
    vm = VirtualMachine(1, 3, 1)
    #vm.print_vals()
    vm.send_msg()