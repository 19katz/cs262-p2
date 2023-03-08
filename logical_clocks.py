import time
import socket
from random import randint
from multiprocessing import Process, Manager
from _thread import * 
from threading import Thread
from select import select
from signal import signal, SIGPIPE, SIG_DFL
import logging

global global_time
global_time = time.time()

signal(SIGPIPE,SIG_DFL)

# logger
def logging_util(name, file):
    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.setLevel('INFO')
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

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
    log_name = f'machine_{id}'
    logging_util(log_name, f'machine_{id}.log')
    log = logging.getLogger(log_name)
    log.info(f'{global_time} Machine: {id} Clock Rate: {ticks}')

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
                rec_logical_clock = queue.get()
                length = queue.qsize()
                logical_clock = max(int(rec_logical_clock), logical_clock)
                # write in the log that it received a message, the global time (gotten from the system), the length of the message queue, and the logical clock time
                log.info(f'{global_time} Received a message; Logical Clock: {logical_clock}; Queue Length: {length}')
            else:
                global val
                val = randint(1,10)
                if val == 1:
                    # m0 sends to m1, m1 sends to m2, m2 sends to m0
                    rec = (id + 1) % 3
                    data = str(logical_clock).encode('ascii')
                    machine_connections[rec].send(data)
                    log.info(f'{global_time} Sent a message to Machine {rec}; Logical Clock: {logical_clock}')
                elif val == 2:
                    # m0 sends to m2, m1 sends to m0, m2 sends to m1
                    rec = (id + 2) % 3
                    data = str(logical_clock).encode('ascii')
                    machine_connections[rec].send(data)
                    log.info(f'{global_time} Sent a message to Machine {rec}; Logical Clock: {logical_clock}')
                elif val == 3:
                    # m0 sends to m1/2, m1 sends to m2/0, m2 sends to m0/1
                    rec = [(id + 1)%3, (id + 2)%3]
                    data = str(logical_clock).encode('ascii')
                    for r in rec:
                        machine_connections[r].send(data)
                        log.info(f'{global_time} Sent a message to Machine {r}; Logical Clock: {logical_clock}')
                else:
                    log.info(f'{global_time} Internal Event!; Logical Clock: {logical_clock}')

        time.sleep(1/ticks - (time.time() - start_time))
    
    for connection in machine_connections.values():
        connection.close()

if __name__ == "__main__":
    host = "localhost"
    ports = [2048, 3048, 4048]
    machine_count = 3
    global_time = time.time()
    run_time = 50

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