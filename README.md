# TUI-code-judging
A TUI implementation of online code judging for Python code, using curses.

### About requirements:
If you're on a windows machine, run

```
pip install -r requirements.txt
```

Otherwise, you don't need to do anything.


### About safety:
This code is 100% certified to be very very unsafe for your machine. If you're planning on hosting this, **MAKE SURE YOUR USERS ARE TRUSTED**. The exec() function runs on the server side, and I'd hate to see your 1TB porn folder leaked for all your friends to see.

### About the project requirements
1. Purpose is explained clearly: Start and end of messages can be detected unambiguously, so that data sent will not be incomplete

- Yes.

2. Characters used to indicate start/end of transmission, (eg: agree beforehand that any data we transmit will always end with a character ""eg \n"".)

- server 19
- client 26

3. Characters used to trigger different events ("player wins")

- server 22 25
- client 29 32

4. Characters used to indicate that the data attached contains certain information (eg: the accuracy score of the opponent)

- client 43

5. The data itself will never contain the above signalling characters to confuse the recipient

- server 114 115

6. Allows users to agree on valid Port + IP Address

- client 12
- server 133

7. Manages starting and abrupt ending of game if either client/server leaves suddenly

- server 110
- server 143
- client 17
