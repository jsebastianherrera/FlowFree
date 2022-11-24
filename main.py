import curses
import random
import signal
from Grid import Grid
from Auto import Graph
TEXT = "Flow Free"
menu = ['Play', 'Auto',  'Exit']
interrupted = False


def handler(signum, frame):
    global interrupted
    interrupted = True


def print_menu(stdscr, selected_row_id):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w//2 - len(TEXT)//2
        y = h//2 - len(menu)//2 + idx
        if selected_row_id == idx:
            stdscr.addstr(y, x, row, curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()


def control_menu(stdscr):
    current_row_id = 0
    print_menu(stdscr, current_row_id)
    global interrupted
    while True:
        interrupted = False
        key = stdscr.getch()
        stdscr.clear()
        if key == curses.KEY_UP and current_row_id > 0:
            current_row_id -= 1
        elif key == curses.KEY_DOWN and current_row_id < len(menu)-1:
            current_row_id += 1
        elif key == 10:
            if menu[current_row_id] == 'Exit':
                exit(0)
            elif menu[current_row_id] == 'Play':
                i = 0
                j = 0
                grid = Grid()
                while not grid.finished() and not interrupted:
                    grid.print_grid(stdscr, i, j)
                    key = stdscr.getch()
                    i, j = grid.grid_control(key, i, j)
            elif menu[current_row_id] == 'Auto':
                r = random.choice([i for i in range(1, 14)])
                stdscr.addstr(0, 0, str(r), curses.color_pair(3))
                g = Graph(r, stdscr)
                g.printGrid(stdscr)
                key = stdscr.getch()
                if key > 0:
                    g.solver(0, 0)
                    g.printGrid(stdscr)
                stdscr.getch()
        print_menu(stdscr, current_row_id)


def main(stdscr):
    signal.signal(signal.SIGINT, handler)
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    for i in range(3, curses.COLORS):
        curses.init_pair(i + 1, i, i)
    control_menu(stdscr)


# ***************************************
if __name__ == '__main__':
    curses.wrapper(main)
