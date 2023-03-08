import unittest
from unittest.mock import Mock, patch, MagicMock
import time
import logging
import os

from logical_clocks_lab import producer, consumer, logging_util

class TestProducer(unittest.TestCase):
    def setUp(self):
        self.host = 'localhost'
        self.ports = [8000, 8001, 8002]
        self.run_time = 5
        self.tick_range = 5
        self.rand_range = 10
        self.id = 0
        global global_time
        global_time = time.time()
        
        self.mock_socket = Mock()
        self.mock_conn = Mock()
        self.mock_socket.return_value = self.mock_conn
        
        self.mock_msg_queue = MagicMock()
        
        self.expected_log = [
            f'{global_time} Machine: 0 Clock Rate: 3',
            f'{global_time} Sent a message to Machine 2; Logical Clock: 1'
        ]
        
    def test_producer(self):        
        conns = []
        for i in range(len(self.ports)):
            conns.append(self.mock_conn)

        self.assertEqual(len(conns), 3)
        print("Successfully connects to all other ports")
        self.assertEqual(self.mock_msg_queue.empty.call_count, 0)
        print("No messages were sent to queue")
    
    
class TestConsumer(unittest.TestCase):
    def setUp(self):
        self.mock_conn = Mock()
        self.mock_conn.recv.return_value = b'1'
        self.mock_msg_queue = MagicMock()

    def test_consumer(self):
        data = int(self.mock_conn.recv(1024).decode('ascii'))
        self.mock_conn.close()
        self.assertEqual(data, 1)
        print("Data is successfully retrieved")
        self.assertEqual(self.mock_conn.close.call_count, 1)
        print("Connection is successfully closed")

class TestSetupLogger(unittest.TestCase):
    def test_setup_logger(self):
        logger_name = 'test_logger'
        log_file = 'test.log'
        logging_util(logger_name, log_file)
        logger = logging.getLogger(logger_name)
        self.assertTrue(os.path.exists(log_file))
        print("Log file is successfully created")

    def tearDown(self):
        os.remove("test.log")


if __name__ == '__main__':
    unittest.main()
