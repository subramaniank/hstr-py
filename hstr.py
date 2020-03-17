import sys,os,re
import curses
import string
import logging
current_selected_cmd = ""

CONFIG = {
        'EXTENDED_HISTORY': True,
        'MAX_MATCHES': 30
}

logging.basicConfig(filename='/tmp/hstr_subkale.log', level=logging.DEBUG)

def format_curr_search_string(new_char, curr_search_string):
    new_search_string = curr_search_string
    if (chr(new_char) in string.printable):
        new_search_string += chr(new_char)
    elif new_char == 263:
        # backspace
        new_search_string = new_search_string[:-1]
    return new_search_string

def get_cursor_pos(curr_search_stringstr):
    return len(curr_search_stringstr), 0 

def print_formatted_output(output_lines, stdscr, curr_selection):
    height, width = stdscr.getmaxyx()
    curr_print_index = 1
    for line in output_lines:
        if curr_selection != None and curr_print_index == curr_selection+1:
           stdscr.attron(curses.color_pair(2))
        output_str = line[:width-1].strip() + "\n"
        stdscr.addstr(curr_print_index, 0, output_str)
        if curr_selection != None and curr_print_index == curr_selection+1:
           stdscr.attroff(curses.color_pair(2))
        curr_print_index += 1

def get_formatted_cmd(line):
    if CONFIG['EXTENDED_HISTORY']:
        return ''.join(line.split(';')[1:])
    return line

def get_output(curr_search_string, stdscr):
    f_shell_history = open(os.environ["HISTFILE"])
    output_lines = set()
    output_str = ""
    max_matches = CONFIG['MAX_MATCHES'] 
    current_match = 0
    for line in f_shell_history:
        formatted_cmd = get_formatted_cmd(line)
        if re.search(curr_search_string, formatted_cmd):
            current_match += 1
            output_lines.add(formatted_cmd)
            if current_match >= max_matches:
                break
    return list(output_lines)

def get_current_selected_cmd(k, curr_selection, output_lines):
    if k == curses.KEY_DOWN:
        if curr_selection == None:
            curr_selection = -1
        curr_selection = min(len(output_lines)-1, curr_selection+1)
        curr_selected_cmd = output_lines[curr_selection]
    elif k == curses.KEY_UP:
        if curr_selection == None:
            curr_selection = 0
        curr_selection = max(0, curr_selection-1)
    if curr_selection == None or curr_selection > (len(output_lines) - 1):
        curr_selected_cmd = None
    else:
        curr_selected_cmd = output_lines[curr_selection]
    return curr_selection, curr_selected_cmd

def draw_menu(stdscr):
    curr_selection = None
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
    while (k != 7):

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

        # Centering calculations
        #start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        #start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        #start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        #start_y = int((height // 2) - 2)

        # Rendering some text
        stdscr.addstr(0, 0, curr_search_stringstr, curses.color_pair(1))


        # Turning on attributes for title
        #stdscr.attron(curses.color_pair(2))
        #stdscr.attron(curses.A_BOLD)

        # Rendering title
        #stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        #stdscr.attroff(curses.color_pair(2))
        #stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        #stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        #stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        #stdscr.addstr(start_y + 5, start_x_keystr, keystr)

        output_lines = get_output(curr_search_string, stdscr)

        # Refresh the screen
        global current_selected_cmd
        curr_selection, current_selected_cmd = get_current_selected_cmd(k, curr_selection, output_lines)
        logging.debug(current_selected_cmd)
        stdscr.move(cursor_y, cursor_x)
        
        statusbarstr = "Press 'Ctrl-g' to exit | STATUS BAR | Pos: {}, {} | Current Selection {} | {} | Current selected cmd {}".format(cursor_x, cursor_y, curr_selection, keystr, current_selected_cmd)
        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-20, 0, statusbarstr)
        #stdscr.addstr(height-30, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))
        stdscr.refresh()

        print_formatted_output(output_lines, stdscr, curr_selection)
        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)
    print(current_selected_cmd)

if __name__ == "__main__":
    main()
