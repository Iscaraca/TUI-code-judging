import curses
from curses.textpad import Textbox, rectangle
import timeit

def draw_menu(stdscr):

    stdscr.clear()
    stdscr.refresh()

    # Instructions box
    helpOutlineULY = (int(stdscr.getbegyx()[0]))
    helpOutlineULX = (int(stdscr.getbegyx()[1]))
    helpOutlineLRY = (int(stdscr.getbegyx()[0]) + 2)
    helpOutlineLRX = (int(stdscr.getmaxyx()[1] - 1))

    rectangle(stdscr, helpOutlineULY, helpOutlineULX, helpOutlineLRY, helpOutlineLRX)

    # Editor box
    writeboxOutlineULY = (int(stdscr.getbegyx()[0]) + 3)
    writeboxOutlineULX = (int(stdscr.getbegyx()[1]))
    writeboxOutlineLRY = (int(stdscr.getmaxyx()[0] * 0.7) + 7)
    writeboxOutlineLRX = (int(stdscr.getmaxyx()[1] - 1) - 49)

    rectangle(stdscr, writeboxOutlineULY, writeboxOutlineULX, writeboxOutlineLRY, writeboxOutlineLRX)

    stdscr.refresh()

    writeboxH = (int(stdscr.getmaxyx()[0] * 0.7) - int(stdscr.getbegyx()[0]) + 3)
    writeboxW = (int(stdscr.getmaxyx()[1] - 1) - int(stdscr.getbegyx()[1]) - 51)
    writeboxURY = (int(stdscr.getbegyx()[0]) + 4)
    writeboxURX = (int(stdscr.getbegyx()[1]) + 1)

    writebox = curses.newwin(writeboxH, writeboxW, writeboxURY, writeboxURX)

    # Results box
    resultsOutlineULY = (int(stdscr.getbegyx()[0]) + 3)
    resultsOutlineULX = (int(stdscr.getmaxyx()[1] - 1) - 47)
    resultsOutlineLRY = (int(stdscr.getmaxyx()[0] * 0.7) + 7)
    resultsOutlineLRX = (int(stdscr.getmaxyx()[1] - 1))

    rectangle(stdscr, resultsOutlineULY, resultsOutlineULX, resultsOutlineLRY, resultsOutlineLRX)

    resultsH = (int(stdscr.getmaxyx()[0] * 0.7) - int(stdscr.getbegyx()[0]) + 2)
    resultsW = (int(stdscr.getmaxyx()[1] - 1) - int(stdscr.getmaxyx()[1] - 1) + 45)
    resultsURY = (int(stdscr.getbegyx()[0]) + 4)
    resultsURX = (int(stdscr.getmaxyx()[1] - 1) - 46)

    results = curses.newwin(resultsH, resultsW, resultsURY, resultsURX)

    stdscr.refresh()


    # Update instructions
    helpH = (1)
    helpW = (int(stdscr.getmaxyx()[1] - 2))
    helpURY = (1)
    helpURX = (1)

    helpbox = curses.newwin(helpH, helpW, helpURY, helpURX)

    helpbox.addstr(0, 0, "Sort a list <l> using bubble sort and reassign the sorted array to the variable <sorted_l>. (CTRL-G to submit)")
    helpbox.refresh()

    startCode = timeit.default_timer()

    # Allow for text input
    box = Textbox(writebox)
    box.edit()

    # Test code
    sorted_l = []
    message = box.gather()
    message = "sorted_l = []\nl = [5, 4, 3, 2, 1, 0]\n" + message

    startExec = timeit.default_timer()

    loc = {}
    exec(message, globals(), loc)
    sorted_l = loc['sorted_l']

    end = timeit.default_timer()

    results.addstr(0, 0, "Input:\n[5, 4, 3, 2, 1, 0]\nOutput:\n" + str(sorted_l) + "\n\nExecution time: {:.5f}ms".format((end - startExec) * 1000.0) + "\n\nTime taken to type: {:.2f}s".format(end - startCode) + "\n\n\n\n\nPress any key to exit")

    results.refresh()
    k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()