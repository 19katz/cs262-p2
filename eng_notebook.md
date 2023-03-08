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
        - Val = 1: send to one of the other machines a message that is the local logical clock time, update it’s own logical clock, and update the log with the send, the system time, and the logical clock time
        - Val = 2: send to the other virtual machine a message that is the local logical clock time, update it’s own logical clock, and update the log with the send, the system time, and the logical clock time.
        - Val = 3: send to both of the other virtual machines a message that is the logical clock time, update it’s own logical clock, and update the log with the send, the system time, and the logical clock time.
        - Val = 4-10: treat the cycle as an internal event; update the local logical clock, and log the internal event, the system time, and the logical clock value.

Testing/ Logging
1. Unit Tests
2. Run the scale model >5 times for at at least 1 min each time and discuss on at least 3 virtual machines:
    - size of jumps in values for logical clocks
    - drift in values of local logical clocks in different machines (use system time)
    - impact of different timings on things such as gaps in logical clock values and length of message queue
3. Run same experiment above with smaller variation in clock cycles and smaller probability of event being internal

## Implementing Logical Clocks
- Decided to use the general structure described in Lab by TF
- We have threads that listen to the other machines, and threads that send messages
to the other machines
- Each machine runs as a Process
- Tried to organize things in a class structure, but this caused Threading issues
- Going to remove things from classes to make it work
- Decided to completely go with the structure laid out in lab, with a consumer and producer thread -- this seems to work well

## Experimental Runs
- had some trouble figuring out how exactly to measure drift: eventually, we settled on comparing the time in machine seconds to the time in real seconds
- measure avg/stdev jump, max jump, max drift, and max queue length for each machine
- expecting bigger jumps with more tick variance
- use matplotlib to plot histogram