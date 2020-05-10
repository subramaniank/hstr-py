import re

class HistoryParser:

    def __init__(self, history_file_name, use_extended_history):
        self.history_file_name = history_file_name
        self.extended_history = use_extended_history

    def get_formatted_cmd(self, line):
        if self.extended_history and line and line.startswith(":"):
            return ''.join(line.split(';')[1:])
        return line

    def get_output(self, curr_search_string, max_matches):
        f_shell_history = open(self.history_file_name)
        output_lines = set()
        output_str = ""
        current_match = 0
        for line in f_shell_history:
            formatted_cmd = self.get_formatted_cmd(line)
            if formatted_cmd and re.search(curr_search_string, formatted_cmd):
                current_match += 1
                output_lines.add(formatted_cmd)
                if current_match >= max_matches:
                    break
        return list(output_lines)

