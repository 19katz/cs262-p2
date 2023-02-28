# Design Exercise 2 Eng Notebook

## Initial Notes

- model of a simple distributed system where the systems work at different speeds
- 3 processes (at minimum) on a single machine (or multiple)
- given number of instructions/second
- sometimes, they will send a message or two, and also look at any waiting messages
- sometimes, they will just wake up and go back to sleep
    - randomly generate what each machine does
- any time you wake up, you read from the message queue
- how often you wake up is also determined randomly (sleep for 1, 2, or 3 seconds)
- sockets queue messages automatically
- how to send the messages is dependent on what we want -- recommended use sockets, can use other things

## Implementation Details
Machine Details
1. Runs at a random clock rate (choose a random number 1-6 which will be the number of clock ticks per real world seconds), only this many operations can occur during that time
2. Each will have a network queue which can hold incoming messages but this isn't bound by the clock rate
3. Should be able to connect to all the other VMs so messages can be passed between (happens during initialization), not contrained by clock rate
4. Each should open a file as a log
5. Each should have a logical clock


Runtime Details
1. During each clock cycle, if there is a message in the queue then machine should: 
    - Pop a message from queue
    - Update local logical clock
    - Write in log that it got a message, the global time (from system), length of message queue, and the machine logical clock time
2. If no message in queue, machine should:
    - Generate random number in range 1-10

if the value is 1, send to one of the other machines a message that is the local logical clock time, update it’s own logical clock, and update the log with the send, the system time, and the logical clock time
if the value is 2, send to the other virtual machine a message that is the local logical clock time, update it’s own logical clock, and update the log with the send, the system time, and the logical clock time.
if the value is 3, send to both of the other virtual machines a message that is the logical clock time, update it’s own logical clock, and update the log with the send, the system time, and the logical clock time.
if the value is other than 1-3, treat the cycle as an internal event; update the local logical clock, and log the internal event, the system time, and the logical clock value.
While working on this, keep a lab notebook in which you note the design decisions you have made. Then, run the scale model at least 5 times for at least one minute each time. Examine the logs, and discuss (in the lab book) the size of the jumps in the values for the logical clocks, drift in the values of the local logical clocks in the different machines (you can get a god’s eye view because of the system time), and the impact different timings on such things as gaps in the logical clock values and length of the message queue. Observations and reflections about the model and the results of running the model are more than welcome.

Once you have run this on three virtual machines that can vary their internal times by an order of magnitude, try running it with a smaller variation in the clock cycles and a smaller probability of the event being internal. What differences do those variations make? Add these observations to your lab notebook. Play around, and see if you can find something interesting.

You may use whatever packages or support code for the construction of the model machines and for the communication between the processes. 

You will turn in both the code (or a pointer to your repo containing the code) and the lab notebook. You will also demo this, presenting your code and choices, during demo day 2.
