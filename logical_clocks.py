import time
import threading
import queue
import os
import socket
from random import randint
from multiprocessing import Process
from _thread import * 
from threading import Thread
from select import select

global global_time
global_time = time.time()

# logger
def logging_util():
    pass

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
    
    def consumer(self):
        server = [self.server]
        while self.event.is_set():
            sock_list = select(server, [], server, 0.01)
            for sock in sock_list:
                if sock == server:
                    conn, addr = sock.accept()
                    print("Connection accepted: " + str(conn))
                    sock_list.append(conn)
                else:
                    data = conn.recv(1024)
                    data_msg = data.decode('ascii')
                    print("Received message " + data_msg)
                    # add to queue
                    self.queue.put((data_msg)) 
        for sock in server:
            sock.close()
        print("Servers closed")

def connections(machine_count, id, host, port):
    machine_connections = {}
    for machine in range(machine_count - 1):
        rec = (id + machine) % 3
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(host, port[rec])
        machine_connections[rec] = conn
    return machine_connections

def send_msg(host, port, id, machine_count, run_time):
    queue = queue.Queue()
    sock = SocketUtil(host, port[id], queue)
    sock.start()

    ticks = randint(1, 6)
    logical_clock = 0

    #logger
    connections = connections(machine_count, id, host, port)
    for i in range(run_time):
        for j in range(ticks):
            logical_clock += 1
            start_time = time.time()
            if not queue.empty():
                # get the logical clock time that was sent to you
                rec_logical_clock = queue.get()
                queue.pop()
                logical_clock = max(rec_logical_clock, logical_clock)
                # TODO: update log that it got a message, the global time (from system), length of message queue, and the machine logical clock time
                print("Queue is not empty!")
            else:
                global val
                val = randint(1,10)
                if val == 1:
                    # m0 sends to m1, m1 sends to m2, m2 sends to m0
                    rec = [(id + 1) % 3]
                    data = logical_clock.encode()
                    connections[rec].send(data)
                    print(data)
                    # TODO: update log with the send, the system time, and the logical clock time
                elif val == 2:
                    # m0 sends to m2, m1 sends to m0, m2 sends to m1
                    rec = [(id + 2) % 3]
                    data = logical_clock.encode()
                    connections[rec].send(data)
                    print(data)
                    # TODO: update log with the send, the system time, and the logical clock time
                elif val == 3:
                    # m0 sends to m1/2, m1 sends to m2/0, m2 sends to m0/1
                    rec = [(id + 1)%3, (id + 2)%3]
                    data = logical_clock.encode()
                    connections[rec].send(data)
                    print(data)
                    # TODO: update log with the send, the system time, and the logical clock time
                else:
                    # TODO: update log with internal event, the system time, and the logical clock value.
                    pass
        time.sleep(1/ticks - (time.time() - start_time))
    
    for connection in connections.values():
        connection.close()

if __name__ == "__main__":
    host = "localhost"
    ports = [2048, 3048, 4048]
    machine_count = 3
    global_time = time.time()
    run_time = 10
    threads = []

    for i in range(0, machine_count-1):
        thread = Process(target=send_msg, args=(host, ports, i, machine_count, run_time))
        thread.start()
        threads.append(thread)
        print("whoo")