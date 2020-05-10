import curses

class InputProcessor:

    def get_current_selected_cmd(self, input_key, curr_selection_index, output_lines):
        if input_key == curses.KEY_DOWN:
            curr_selection_index += 1
        elif input_key == curses.KEY_UP:
            curr_selection_index -= 1

        # make sure selection is within bounds
        curr_selection_index = max(0, curr_selection_index)
        curr_selection_index = min(len(output_lines)-1, curr_selection_index)
        
        curr_selected_cmd = output_lines[curr_selection_index] if output_lines else None
        return curr_selection_index, curr_selected_cmd
                    
