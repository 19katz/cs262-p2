import unittest
from unittest.mock import Mock, patch, MagicMock
import time
import queue
import logging
import os

from logical_clocks_lab import producer, consumer, logging_util

'''class TestProducer(unittest.TestCase):
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
        with patch('socket.socket', self.mock_socket), \
             patch('msg_queue') as self.mock_msg_queue:
            producer(self.id, self.host, self.ports, self.run_time, self.tick_range, self.rand_range)
        
        self.assertEqual(self.mock_socket.connect.call_count, 2)
        self.assertEqual(self.mock_conn.send.call_count, 1)
        #self.assertEqual(self.mock_msg_queue.get.call_count, 1)
        #self.assertEqual(self.mock_msg_queue.empty.call_count, 2)
        
        # Check logging
        with open('machine_0_*.log', 'r') as f:
            log_lines = f.readlines()
        for i in range(len(self.expected_log)):
            self.assertIn(self.expected_log[i], log_lines[i])
    
class TestConsumer(unittest.TestCase):
    def setUp(self):
        self.mock_conn = Mock()
        self.mock_conn.recv.return_value = b'1'
        self.mock_msg_queue = MagicMock()

    @patch('logical_clocks_lab.msg_queue')
    def test_consumer(self):
        consumer(self.mock_conn)
        msg_queue = queue.Queue()
        self.assertEqual(self.mock_conn.recv.call_count, 1)
        self.assertEqual(self.mock_conn.close.call_count, 1)
        #self.assertEqual(self.mock_msg_queue.put.call_count, 1) '''

class TestSetupLogger(unittest.TestCase):
    def test_setup_logger(self):
        logger_name = 'test_logger'
        log_file = 'test.log'
        logging_util(logger_name, log_file)
        logger = logging.getLogger(logger_name)
        self.assertTrue(os.path.exists(log_file))

    def tearDown(self):
        os.remove("test.log")


if __name__ == '__main__':
    unittest.main()
