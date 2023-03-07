import time
import threading
import queue
import os
import socket
from random import randint
from multiprocessing import Process, Manager
from _thread import * 
from threading import Thread
from select import select
from signal import signal, SIGPIPE, SIG_DFL

global global_time
global_time = time.time()

signal(SIGPIPE,SIG_DFL)

# logger
def logging_util():
    pass

# https://stackoverflow.com/questions/1540822/dumping-a-multiprocessing-queue-into-a-list
def dump_queue(q):
    q.put(None)
    item = list(iter(lambda : q.get(timeout=0.00001), None))
    print(item)
    return item

class SocketUtil(Process):
    def __init__(self, host, port, queue):
        Process.__init__(self)
        self.host = host
        self.port = port
        self.queue = queue

        # init server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(10)
    
    def run(self):
        conn, addr = self.server.accept()
        print("Connection accepted: " + str(conn))
        data = conn.recv(1024)
        data_msg = data.decode('ascii')
        print("Received message " + data_msg)
        # add to queue
        self.queue.put((data_msg)) 

def send_msg(host, port, id, machine_count, run_time):
    queue = Manager().Queue()
    sock = SocketUtil(host, port[id], queue)
    sock.start()

    ticks = randint(1, 6)
    logical_clock = 0

    #logger
    machine_connections = {}
    for machine in range(machine_count - 1):
        rec = (id + machine + 1) % 3
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host, port[rec]))
        machine_connections[rec] = conn
    
    for i in range(run_time):
        for j in range(ticks):
            logical_clock += 1
            start_time = time.time()
            if not queue.empty():
                # get the logical clock time that was sent to you
                rec_logical_clock = int(queue.get())
                logical_clock = max(rec_logical_clock, logical_clock)
                # TODO: update log that it got a message, the global time (from system), length of message queue, and the machine logical clock time
                print("Queue is not empty!")
                dump_queue(queue)
            else:
                global val
                val = randint(1,10)
                if val == 1:
                    print("val:", val)
                    # m0 sends to m1, m1 sends to m2, m2 sends to m0
                    rec = (id + 1) % 3
                    print("id", id)
                    print("receiver:", rec)
                    print(machine_connections)
                    data = str(logical_clock).encode('ascii')
                    machine_connections[rec].send(data)
                    print("sent ", data)
                    dump_queue(queue)
                    # TODO: update log with the send, the system time, and the logical clock time
                elif val == 2:
                    print("val:", val)
                    # m0 sends to m2, m1 sends to m0, m2 sends to m1
                    rec = (id + 2) % 3
                    print("id", id)
                    print("receiver:", rec)
                    print(machine_connections)
                    data = str(logical_clock).encode('ascii')
                    machine_connections[rec].send(data)
                    print("sent ", data)
                    dump_queue(queue)
                    # TODO: update log with the send, the system time, and the logical clock time
                elif val == 3:
                    print("val:", val)
                    # m0 sends to m1/2, m1 sends to m2/0, m2 sends to m0/1
                    rec = [(id + 1)%3, (id + 2)%3]
                    data = str(logical_clock).encode('ascii')
                    for r in rec:
                        print("id", id)
                        print("receiver:", rec)
                        print(machine_connections)
                        machine_connections[r].send(data)
                    print("sent ", data)
                    dump_queue(queue)
                    # TODO: update log with the send, the system time, and the logical clock time
                else:
                    # TODO: update log with internal event, the system time, and the logical clock value.
                    pass

        time.sleep(1/ticks - (time.time() - start_time))
    
    for connection in machine_connections.values():
        connection.close()

if __name__ == "__main__":
    host = "localhost"
    ports = [2048, 3048, 4048]
    machine_count = 3
    global_time = time.time()
    run_time = 10

    thread1 = Process(target=send_msg, args=(host, ports, 0, machine_count, run_time))
    thread2 = Process(target=send_msg, args=(host, ports, 1, machine_count, run_time))
    thread3 = Process(target=send_msg, args=(host, ports, 2, machine_count, run_time))

    thread1.start()
    print("Started 1")
    thread2.start()
    print("Started 2")
    thread3.start()
    print("Started 3")

    thread1.join()
    thread2.join()
    thread3.join()