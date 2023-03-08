# CS262 Design Exercise 2: Logical Clocks

This repository implements a 3-machine logical clock system. It runs on python3. 

Installation: 

`pip install -r requirements.txt`

(Note: the required are mainly for analyzing the logs, not actually running th emachines)

## Usage

To run this program, run `python3 logical_clocks_lab.py`. Parameters such as tick rate, amount of run time, and maximum random action variable can be set in the main function.

## Implementation

For our implementation, we used sockets for communication and simulated the creation of a machine by creating a socket for each machine within a Process, and creating two threads within the process -- one that connects to the ports of other machines and sends them messages on clock ticks (the producer), and one that constantly receives messages and stores them in the queue (the consumer). 

## Experiments

For our experiments, we ran 5 iterations of `logical_clocks_lab.py` with 3 machines and default maximum tick speed of 6 actions/second and default internal event probability of 70% for 1 minute. We then ran 3 iterations with a lower maximum tick speed and internal event probability. The results are descriped in `logical_clock_analysis`.pdf, and plots and logs can be found in `normal_logs` (for the 5 default runs) and `exp_logs` (for the changed tick speed/event probability).

Our results can be recreated by running `python3 analyze_logs.py`. 

