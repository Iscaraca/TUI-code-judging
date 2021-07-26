import socket
from multiprocessing import *
import time
import json
import sys
from random import randint

players = []


def send(player, string, endRequired=False, instructionRequired=False):
    """Appends appropriate event identifier string to transmission

    Args:
        player (tuple<socket, address>): Target of transmission
        string (string): Transmission data
        endRequired (bool, optional): Triggers end of game event. Defaults to False.
        instructionRequired (bool, optional): Routes transmission data to the instructions window. Defaults to False.
    """
    string += "&&ENDL"

    if instructionRequired:
        string += "&&INSTRUCTION"

    if endRequired:
        string += "&&ENDG"

    # player is a tuple (socket, address)
    print(f"sent {string} to player {player}")

    try:
        player[0].sendall(string.encode())
    except:
        del player[0]
        sendAll("Something went wrong with the connection", endRequired=True)
        sys.exit(1)


def sendAll(string, endRequired=False, instructionRequired=False):
    """Broadcasts transmission to all players

    Args:
        string (string): Transmission data
        endRequired (bool, optional): Triggers end of game event. Defaults to False.
        instructionRequired (bool, optional): Routes transmission data to the instructions window. Defaults to False.
    """
    for player in players:
        send(player, string, endRequired, instructionRequired)
        time.sleep(0.1)  # A result of blocking sockets, so we don't have to deal with any race conditions


def acceptPlayers(s):
    """Accepts connection requests from two clients

    Args:
        s (socket object): The socket object
    """
    while len(players) < 2:
        sock, addr = s.accept()
        players.append([sock, addr, 0, 0.0])  # socket, address, score, timing
        send([sock], f"You are connected. You are player number {len(players)}")


def parseConfig(filename):
    """Parses data from config file, namely:
        	line (integer): Unique challenge identifier
			skip (bool): Indicates whether a question will appear in a challenge
			prepend (string): Code block to run before input executes
			append (string): Code block to run after input executes
			instructions (string): Prompt that displays on instruction window

        and parses data from the answer file

    Args:
        filename (string): Path to config file

    Returns:
        tuple<dict, list>: Loaded config file and list of recommended answers
    """
    config_file = open(str(filename), "r")
    config = json.loads(config_file.read())
    code_file = open(str(config["file"]), "r")
    code = code_file.read().splitlines()
    return config["config"], code


def findCase(config, line):
    return [case for case in config if case["line"] == int(line)][0]


def check(case, response):
    if case["skip"]:
        return True

    random_int = randint(12345, 22221)
    prepend = case['prepend'].replace("REPLACE_RANDINT", str(random_int))
    append = case['append'].replace("REPLACE_RANDINT", str(random_int))

    try:
        loc = {}
        exec(f"{prepend}{response}{append}", globals(), loc)
        return loc["test"]
    except Exception as e:
        print("something went wrong with execution of check. ")
        print(e)
        return False


def receive():
    """Receives time and code from clients

    Returns:
        list: 2D array with each element representing time and code data
    """
    responses = []

    for index, player in enumerate(players):
        response = b""
        while b"&&ENDL" not in response:
            try:
                response += player[0].recv(1024)
            except:
                print("Receiving failed.")
                sendAll("Something went wrong with the connection", endRequired=True)
                sys.exit(1)

        timing = response[response.find(b"&&TIME=") + 7 :].decode()
        response = response[: response.find(b"&&ENDL")].decode()

        responses.append([index, timing, response])

    return responses


def battle(filename):
    """Main function for the server, executes received code in the context of a larger code block
    and checks for sanity in execution

    Args:
        filename (string): Path to config file

    Returns:
        bool: Execution status
    """
    s = socket.socket()
    addr = input("Valid IP address of server (e.g. 127.0.0.1): ")
    port = int(input("Port number (e.g. 22222): "))
    try:
        s.bind((addr, port))
        print("Bind successful")
        s.listen()
        print("Listening...")
    except socket.error as exc:
            s.close()
            s = None
    if s is None:
        print('could not open socket')
        sys.exit(1)

    acceptPlayers(s)

    if len(players) < 2:
        return False

    config, codes = parseConfig(filename)

    for line, code in enumerate(codes):
        case = findCase(config, line)

        sendAll(case["instructions"], instructionRequired=True)

        responses = receive()
        print(responses)
        for [index, timing, response] in responses:
            print(response)
            result = check(case, response)
            print(result, response)
            players[index][3] += float(timing)
            if result:
                players[index][2] += 1
            send(
                players[index],
                f"Your code is {('correct' if result else 'wrong')}.\n\nYou took {float(timing)/1000:.2f}s\n\nFor your reference, the model answer is:\n\t{code}"
            )

    sendAll(
        f"Here are the scores:\n\nPlayer 1:\n\tScore:{players[0][2]}\n\tTiming:{float(players[0][3])/1000:.2f}s\n\nPlayer 2:\n\tScore:{players[1][2]}\n\tTiming:{float(players[1][3])/1000:.2f}s",
        endRequired=True,
    )

    # clean up
    for player in players:
        player[0].close()
    s.close()

    return True


if __name__ == "__main__":
    print("Server Online!")
    battle("./config.json")
    print("Server Terminated.")
