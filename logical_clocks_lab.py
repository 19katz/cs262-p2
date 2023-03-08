import time
import socket
from random import randint
import multiprocessing
from multiprocessing import Process, Manager
from _thread import * 
from threading import Thread
import logging
import queue

"""
File that runs 3 machines with 3 different clock rates according to
parameters given in the main function. The actions of these machines
will be logged along with the starting real-time timestamp in text files.
"""

# global variable representing the current time in each process
global global_time
global_time = time.time()

# logger utility function
def logging_util(name, file):
    """
    name: name of logger
    file: name of file to log to
    """
    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.setLevel('INFO')
    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

# Consumer thread, which accepts connections from other machines
# and puts the received messages in queues
def consumer(conn):
    """
    conn: a connection request from another socket/machine
    """
    print("Connection accepted: " + str(conn))
    while True:
        data = conn.recv(1024)
        data_msg = data.decode('ascii')
        if len(data_msg) == 0:
            print("Dropped")
            # connection has dropped
            break
        print("Received message " + data_msg)
        # add to queue, which is a global variable per process
        msg_queue.put(data_msg)
    if conn:
        conn.close()

# Producer thread, which connects to all other ports, and then rolls a 10-sided die
# for the type of action to take at each tick. 
def producer(id, host, ports, run_time, tick_range, rand_range):
    """
    id: id of the machine (0, 1, or 2)
    host: name of the host
    ports: list of all the ports, declared in main
    run_time: number of seconds to run for
    tick_range: maximum possible tick value (actions / second)
    rand_range: maximum possible value for random action (can be adjusted to change
    the frequency of an internal event)
    """

    success = False
    # stores all the connections by id
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

    # randomly generate tick value given range
    ticks = randint(1, tick_range)
    # start logical clock
    logical_clock = 0

    # start logging, using the time of logging in seconds as an identifier
    cur_time = time.time()
    log_name = f'machine_{id}'
    logging_util(log_name, f'machine_{round(cur_time)}_{id}_{tick_range}_{rand_range}.log')
    log = logging.getLogger(log_name)
    log.info(f'{global_time} Machine: {id} Clock Rate: {ticks}')
    
    for i in range(run_time):
        for j in range(ticks):
            # increment the logical clock
            logical_clock += 1
            start_time = time.time()
            # calculate the time that the next tick should happen
            next_time = start_time + 1.0 / ticks
            if not msg_queue.empty():
                # get the logical clock time that was sent to you if there is such a message
                rec_logical_clock = msg_queue.get()
                length = msg_queue.qsize()
                logical_clock = max(int(rec_logical_clock), logical_clock)
                # write in the log that it received a message, the global time (gotten from the system), the length of the message queue, and the logical clock time
                log.info(f'{global_time} Received a message; Logical Clock: {logical_clock}; Queue Length: {length}')
            else:
                global val
                val = randint(1, rand_range)
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
    # close all the connections
    for connection in machine_connections.values():
        if connection is not None:
            print("CLOSING")
            connection.close()

# Thread that initializes this machine's socket and the consumer thread,
# which listens for connections
def init_machine(host, port):
    """
    host: name of host
    port: number of this machine's port
    """
    # bind and listen on this socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    print("Bound to port " + str(port))
    while True:
        # accept any other connections
        conn, addr = s.accept()
        start_new_thread(consumer, (conn,))

# Method invoked by each machine's Process that starts the entire system
def machine(host, ports, id, run_time, tick_range, rand_range):
    """
    host: name of the host
    ports: list of all ports for all machines
    id: id of this machine
    run_time: number of seconds to run for
    tick_range: maximum number of ticks per second
    rand_range: maximum opcode for machine action
    """
    rec = id % 3 

    # declare the queue to be a global variable. Each Process has an independent
    # queue that is accessible by all threads in the process. 
    global msg_queue
    msg_queue = queue.Queue()

    # initialize the machine and start listening/accepting connections
    init_thread = Thread(target=init_machine, args=(host, ports[rec]))
    init_thread.start()
    # sleep to allow some time for all machines to instantiate
    time.sleep(5)
    # it's awake!
    print("i'm awake")

    # create producer thread, which starts the logical clock and begins
    # performing operations
    prod_thread = Thread(target=producer, args=(id, host, ports, run_time, tick_range, rand_range))
    prod_thread.start()


if __name__ == "__main__":
    host = "localhost"
    ports = [2048, 3048, 4048]
    machine_count = 3
    global_time = time.time()
    run_time = 60
    tick_range = 3
    rand_range = 5

    thread1 = Process(target=machine, args=(host, ports, 0, run_time, tick_range, rand_range))
    thread2 = Process(target=machine, args=(host, ports, 1, run_time, tick_range, rand_range))
    thread3 = Process(target=machine, args=(host, ports, 2, run_time, tick_range, rand_range))

    thread1.start()
    print("Started 1")
    thread2.start()
    print("Started 2")
    thread3.start()
    print("Started 3")

    thread1.join()
    thread2.join()
    thread3.join()