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
