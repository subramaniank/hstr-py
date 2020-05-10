import sys,os,re,termios,fcntl
import curses
import string

from parser.history_parser import HistoryParser
from processor.input_processor import InputProcessor

CONFIG = {
        'EXTENDED_HISTORY': True,
}

def format_curr_search_string(new_char, curr_search_string):
    new_search_string = curr_search_string
    if (chr(new_char) in string.printable):
        new_search_string += chr(new_char)
    elif new_char == 263 or new_char == 127:
        # backspace
        new_search_string = new_search_string[:-1]
    return new_search_string

def get_cursor_pos(curr_search_stringstr):
    return len(curr_search_stringstr), 0 

def print_formatted_output(output_lines, stdscr, curr_selection, print_offset_from_top):
    _, width = stdscr.getmaxyx()

    curr_print_index = print_offset_from_top
    index_to_highlight = curr_selection + print_offset_from_top

    for line in output_lines:
        if curr_print_index == index_to_highlight:
           stdscr.attron(curses.color_pair(2))
        output_str = line[:width-1].strip() + "\n"
        stdscr.addstr(curr_print_index, 0, output_str)
        if curr_print_index == index_to_highlight:
           stdscr.attroff(curses.color_pair(2))
        curr_print_index += 1



def draw_menu(stdscr, history_parser, input_processor):
    curr_selection = 0
    current_selected_cmd = None
    curr_search_string = ""
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while (True):

        # Reset and break on Ctrl-g
        if (k == 7):
            current_selected_cmd = None
            break

        if (k == 10):
            break

        curr_search_string = format_curr_search_string(k, curr_search_string)
        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Declaration of strings
        title = "Curses example"[:width-1]
        subtitle = "Credit to Clay McLeod"[:width-1]
        keystr = "Last key pressed: {}".format(k)[:width-1]
        curr_search_stringstr = "Current search string: {}".format(curr_search_string)
        cursor_x, cursor_y = get_cursor_pos(curr_search_stringstr)

        # Parse history and get output
        output_lines = history_parser.get_output(curr_search_string, height)

        # Get current selected command and index
        curr_selection, current_selected_cmd = input_processor.get_current_selected_cmd(k, curr_selection, output_lines)

        # Rendering current search at the top
        stdscr.addstr(0, 0, curr_search_stringstr, curses.color_pair(1))

        # Rendering status bar below current search string
        statusbarstr = "Press 'Ctrl-g' to exit | STATUS BAR | Pos: {}, {} | Current Selection {} | {} | Current selected cmd {}".format(cursor_x, cursor_y, curr_selection, keystr, current_selected_cmd)
        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(1, 0, statusbarstr)
        stdscr.attroff(curses.color_pair(3))

        print_formatted_output(output_lines, stdscr, curr_selection, 2)
        # Wait for next input
        k = stdscr.getch()

    return current_selected_cmd

def main():
    history_parser = HistoryParser(os.environ["HISTFILE"], CONFIG['EXTENDED_HISTORY'])
    input_processor = InputProcessor()
    current_selected_cmd = curses.wrapper(draw_menu, history_parser, input_processor)
    if (current_selected_cmd):
        for curr_char in current_selected_cmd:
            fcntl.ioctl(0, termios.TIOCSTI, curr_char)

if __name__ == "__main__":
    main()
