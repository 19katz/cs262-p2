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

# Setup logging
def logging_util():
    pass

# Read messages
class SocketUtil(Process):
    def __init__(self, host, port, event):
        Process.__init__(self)
        self.host = host
        self.port = port
        self.event = event
    
    # Create socket and bind to port
    def start_machine(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(self.host, self.port)
        server.listen(10)
    
    def consumer(self):
        server = self.start_machine()
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
           

class VirtualMachine():
    def __init__(self, host, port, id, machine_count, global_time, run_time):
        self.host = host
        self.port = port
        self.id = id
        self.machine_count = machine_count
        self.event = threading.Event()
        self.event.set()
        self.queue = queue.Queue()
        self.ticks = randint(1, 6)
        self.global_time = global_time
        self.run_time = run_time
        self.logical_clock = 0
        self.sock = SocketUtil(self.host, self.port[self.id], self.queue, self.event)
        self.sock.start()
    
        # Set up logger
    
    # Connect to other machines
    def connections(self):
        machine_connections = {}
        for machine in range(self.machine_count - 1):
            rec = (self.id + machine) % 3
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect(self.host, self.port[rec])
            machine_connections[rec] = conn
        return machine_connections


    def send_msg(self):
        # increment logical clock by 1
        connections = self.connections() 
        for i in range(self.run_time):
            for j in range(self.ticks):
                self.logical_clock += 1
                start_time = time.time()
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
                        data = self.logical_clock.encode()
                        connections[rec].send(data)
                        # TODO: update log with the send, the system time, and the logical clock time
                    elif val == 2:
                        # m0 sends to m2, m1 sends to m0, m2 sends to m1
                        rec = [(self.id + 2) % 3]
                        data = self.logical_clock.encode()
                        connections[rec].send(data)
                        # TODO: update log with the send, the system time, and the logical clock time
                    elif val == 3:
                        # m0 sends to m1/2, m1 sends to m2/0, m2 sends to m0/1
                        rec = [(self.id + 1)%3, (self.id + 2)%3]
                        data = self.logical_clock.encode()
                        connections[rec].send(data)
                        # TODO: update log with the send, the system time, and the logical clock time
                    else:
                        # TODO: update log with internal event, the system time, and the logical clock value.
                        pass
            time.sleep(1/self.ticks - (time.time() - start_time))
        
        for connection in connections.values():
            connection.close()
    
    # how do i close this socket lmao i cant reinit the socket oop

if __name__ == "__main__":
    host = "localhost"
    ports = [2048, 3048, 4048]
    # still need to generate ticks randomly from 1-6
    v1 = VirtualMachine(host, ports[0], ticks, 3, 1)
    v2 = VirtualMachine(host, ports[1], ticks, 3, 2)
    v2 = VirtualMachine(host, ports[2], ticks, 3, 3)

    p1 = Process(target=v1.machine([3048, 4048]))
    p2 = Process(target=v1.machine([2048, 4048]))
    p3 = Process(target=v1.machine([2048, 3048]))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
    #vm.print_vals()
    #vm.send_msg()