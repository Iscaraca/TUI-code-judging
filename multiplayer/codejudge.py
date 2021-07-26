import curses
from curses.textpad import Textbox, rectangle
import timeit
import socket
import time

# Connection with server
s = socket.socket()

while True:
    addr = input("Valid IP address of server (e.g. 127.0.0.1): ")
    port = int(input("Port number (e.g. 22222): "))
    try:
        s.connect((addr, port))
        break
    except socket.error as exc:
        print("Connection error: %s" % exc)


def receive(s):
    data = b""
    instructionRequired = False
    endRequired = False

    while b"&&ENDL" not in data:
        data += s.recv(1024)

    if data.find(b"&&INSTRUCTION") != -1:
        instructionRequired = True

    if data.find(b"&&ENDG") != -1:
        endRequired = True

    # '&&ENDL' comes before other flags
    data = data[: data.find(b"&&ENDL")]

    return (data.decode(), instructionRequired, endRequired)


def submit(s, timing, message):
    message += "&&ENDL"
    message += f"&&TIME={timing}"
    s.sendall(message.encode())


def draw_menu(stdscr):
    stdscr.clear()
    stdscr.refresh()

    # Instructions box
    helpOutlineULY = int(stdscr.getbegyx()[0])
    helpOutlineULX = int(stdscr.getbegyx()[1])
    helpOutlineLRY = int(stdscr.getbegyx()[0]) + 2
    helpOutlineLRX = int(stdscr.getmaxyx()[1] - 1)

    rectangle(stdscr, helpOutlineULY, helpOutlineULX, helpOutlineLRY, helpOutlineLRX)

    # Editor box
    writeboxOutlineULY = int(stdscr.getbegyx()[0]) + 3
    writeboxOutlineULX = int(stdscr.getbegyx()[1])
    writeboxOutlineLRY = int(stdscr.getmaxyx()[0] * 0.7) + 7
    writeboxOutlineLRX = int(stdscr.getmaxyx()[1] - 1) - 49

    rectangle(
        stdscr,
        writeboxOutlineULY,
        writeboxOutlineULX,
        writeboxOutlineLRY,
        writeboxOutlineLRX,
    )

    stdscr.refresh()

    writeboxH = int(stdscr.getmaxyx()[0] * 0.7) - int(stdscr.getbegyx()[0]) + 3
    writeboxW = int(stdscr.getmaxyx()[1] - 1) - int(stdscr.getbegyx()[1]) - 51
    writeboxURY = int(stdscr.getbegyx()[0]) + 4
    writeboxURX = int(stdscr.getbegyx()[1]) + 1

    writebox = curses.newwin(writeboxH, writeboxW, writeboxURY, writeboxURX)

    # Results box
    resultsOutlineULY = int(stdscr.getbegyx()[0]) + 3
    resultsOutlineULX = int(stdscr.getmaxyx()[1] - 1) - 47
    resultsOutlineLRY = int(stdscr.getmaxyx()[0] * 0.7) + 7
    resultsOutlineLRX = int(stdscr.getmaxyx()[1] - 1)

    rectangle(
        stdscr,
        resultsOutlineULY,
        resultsOutlineULX,
        resultsOutlineLRY,
        resultsOutlineLRX,
    )

    resultsH = int(stdscr.getmaxyx()[0] * 0.7) - int(stdscr.getbegyx()[0]) + 2
    resultsW = int(stdscr.getmaxyx()[1] - 1) - int(stdscr.getmaxyx()[1] - 1) + 45
    resultsURY = int(stdscr.getbegyx()[0]) + 4
    resultsURX = int(stdscr.getmaxyx()[1] - 1) - 46

    results = curses.newwin(resultsH, resultsW, resultsURY, resultsURX)

    stdscr.refresh()

    helpH = 1
    helpW = int(stdscr.getmaxyx()[1] - 2)
    helpURY = 1
    helpURX = 1

    helpbox = curses.newwin(helpH, helpW, helpURY, helpURX)

    helpbox.addstr(0, 0, f"{receive(s)[0]}. The game will start shortly.")
    helpbox.refresh()
    time.sleep(3)

    while True:
        response, instructionRequired, endRequired = receive(s)
        if instructionRequired:  # new question.
            helpbox.clear()
            helpbox.addstr(0, 0, f"{response}(CTRL-G to submit)")
            helpbox.refresh()

            results.clear()
            results.refresh()

            startCode = timeit.default_timer()

            # Allow for text input
            writebox.clear()
            writebox.refresh()
            box = Textbox(writebox)
            box.edit()

            message = box.gather()

            endCode = timeit.default_timer()

            submit(s, ((endCode - startCode) * 1000.0), message)

            helpbox.clear()
            helpbox.addstr(0, 0, "Code has been submitted. Please wait for a while.")
            helpbox.refresh()

        elif endRequired:  # end game
            results.addstr(0, 0, response)
            results.refresh()
            k = stdscr.getch()
            break

        else:  # display results for that question
            results.addstr(0, 0, f"{response}\n\n(Press any key to continue)")
            results.refresh()
            k = stdscr.getch()


def main():
    curses.wrapper(draw_menu)


if __name__ == "__main__":
    main()

    # # Test code
    # # Test cases, [input, output]
    # cases = [
    #     [[5, 4, 3, 2, 1, 0], [0, 1, 2, 3, 4, 5]],
    #     [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]],
    #     [[1, 6, 6, 5, 3, 4], [1, 3, 4, 5, 6, 6]]]

    # sorted_l = []

    # times = []

    # correctCases = 0

    # for case in cases:
    #     messageNew = f"sorted_l = []\nl = {str(case[0])}\n" + message

    #     startExec = timeit.default_timer()

    #     loc = {}
    #     exec(messageNew, globals(), loc)
    #     sorted_l = loc['sorted_l']

    #     endExec = timeit.default_timer()

    #     times.append((endExec - startExec) * 1000.0)
    #     if sorted_l == case[1]:
    #         correctCases += 1

    # caseResults = "Execution times\n" + '\n'.join(["Case {}: {:.5f}ms".format(i, times[i]) for i in range(len(times))])
    # accuracy = correctCases / len(cases)

    # results.addstr(0, 0, caseResults + "\n\nAccuracy: {:.2f}%".format(accuracy * 100.0) + "\n\nTime taken to type: {:.2f}s".format(endCode - startCode) + "\n\n\n\n\nPress any key to exit")
