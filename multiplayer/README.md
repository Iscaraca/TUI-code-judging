# TUI-code-judging (Multiplayer Mode)

Features of multiplayer mode:
- Allows users to compete against the coding speed of others (Everyone knows that typing speed is proportional to programming prowess)
- Lines of code are executed in the context of a larger block of code, allowing problem setters to test different programming concepts (e.g. socket programming, in the example case)
- Intuitive customisability in creating new challenges

## Instructions
Run `server.py`, inputting a valid IP address and port to accept connections. Run two instances of `codejudge.py` and when prompted with an address and a port, input in the same values you used for the server. 

At every step, look at the prompt at the top of the screen and type the code into the provided editor below. MacOS and Linux useres might have to use either Ctrl+H or Ctrl+BACKSPACE respectively as backspace, because of limitations with the curses library. We'll find a way to fix this soon enough (in like a year or 6).

## Creating your own challenges
When a user submits their code, an exec() function on the server side(yeah I know) will run the input together with code before and after it. These extra code blocks are defined in the `config.json` file. The layout of code to be executed will look something like this:

```python
"""Instruction: Create an object 'my_socket'"""

import socket # Prepended statement, invisible to students

{input here} # my_socket = socket.socket()

# Appended statement, invisible to students
if isinstance(my_socket, socket.socket):
  test = True
else:
  test = False

my_socket.close()
```

This is an example from the sample `config.json` file in the repository.

Notice how we have assigned a boolean value to a `test` variable. This boolean will be used to test whether the code has produced the intended outcome or not.
