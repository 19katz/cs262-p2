import time
import socket
from random import randint
import multiprocessing
from multiprocessing import Process, Manager
from _thread import * 
from threading import Thread
from select import select
from signal import signal, SIGPIPE, SIG_DFL
import logging
import queue

global global_time
global_time = time.time()

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
    
def consumer(conn):
    print("Connection accepted: " + str(conn))
    while True:
        data = conn.recv(1024)
        data_msg = data.decode('ascii')
        if len(data_msg) == 0:
            break
        print("Received message " + data_msg)
        # add to queue
        msg_queue.put(data_msg)

def producer(id, host, ports, run_time, tick_range):
    success = False
    machine_connections = {}
    while not success:
        # keep trying to connect to ports until it fails
        try:
            for i in range(len(ports)):
                if i == id:
                    # don't connect to its own port
                    machine_connections[i] = None
                    continue
                # get current port and create a socket connection to it
                port = ports[i]
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.connect((host, port))
                print("Successfully connected to " + str(port))
                machine_connections[i] = conn
            success = True
        except Exception as e:
            print(e)

    # randomly generate tick value
    ticks = randint(1, tick_range)
    logical_clock = 0

    print("Machines: " + str(machine_connections))

    #logger
    cur_time = time.time()
    log_name = f'machine_{id}'
    logging_util(log_name, f'machine_{id}_{cur_time}.log')
    log = logging.getLogger(log_name)
    log.info(f'{global_time} Machine: {id} Clock Rate: {ticks}')
    
    for i in range(run_time):
        for j in range(ticks):
            logical_clock += 1
            start_time = time.time()
            next_time = start_time + 1.0 / ticks
            if not msg_queue.empty():
                # get the logical clock time that was sent to you
                rec_logical_clock = msg_queue.get()
                length = msg_queue.qsize()
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
                    log.info(f'{global_time} Sent a message to Machines {rec}; Logical Clock: {logical_clock}')
                else:
                    log.info(f'{global_time} Internal Event!; Logical Clock: {logical_clock}')
            time.sleep(max(next_time - time.time(), 0))
    for connection in machine_connections.values():
        if connection is not None:
            print("CLOSING")
            connection.close()

def init_machine(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    print("Bound to port " + str(port))
    while True:
        conn, addr = s.accept()
        start_new_thread(consumer, (conn,))

def machine(host, ports, id, run_time, tick_range):
    rec = id % 3 
    global msg_queue
    msg_queue = queue.Queue()
    init_thread = Thread(target=init_machine, args=(host, ports[rec]))
    init_thread.start()
    time.sleep(5)
    # it's awake!
    print("i'm awake")
    prod_thread = Thread(target=producer, args=(id, host, ports, run_time, tick_range))
    prod_thread.start()


if __name__ == "__main__":
    host = "localhost"
    ports = [2048, 3048, 4048]
    machine_count = 3
    global_time = time.time()
    run_time = 60
    tick_range = 6

    thread1 = Process(target=machine, args=(host, ports, 0, run_time, tick_range))
    thread2 = Process(target=machine, args=(host, ports, 1, run_time, tick_range))
    thread3 = Process(target=machine, args=(host, ports, 2, run_time, tick_range))

    thread1.start()
    print("Started 1")
    thread2.start()
    print("Started 2")
    thread3.start()
    print("Started 3")

    thread1.join()
    thread2.join()
    thread3.join()

    print("exited")