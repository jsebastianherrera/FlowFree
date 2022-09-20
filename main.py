import curses
from Grid import Grid
TEXT = "Flow Free"
menu = ['Play',  'Exit']


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
    while True:
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
                while(grid.cont < grid.flows):
                    grid.print_grid(stdscr, i, j)
                    key = stdscr.getch()
                    i, j = grid.grid_control(key, i, j)
        print_menu(stdscr, current_row_id)


def main(stdscr):
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
