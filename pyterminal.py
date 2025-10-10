"""
PyTerminal -
because why use a real game engine?

Made by lammmab for cs50p final project

- basically a game engine for the terminal
- uses mostly ASCII magic for flushing frames
- runs at target frame-rate
- no flickering
- cross-platform

"""

import os
from colorama import Fore, Style, init
import time
import event_emitter as events
from readchar import readkey, key
from threading import Thread


def get_color(color):
    return getattr(Fore, color.upper(), '') if color else ''


class PyTerminal:
    """
       PyTerminal entry point:
        - Builds input frame
        - Runs at specified fps (terminal.run_loop(update,draw,fps=fps)) (i went with 30 bc it works at 30 and why not)
        - Built in event emitter (mainly for connecting to the keyboard event, but can be used for custom events depending on use-case)
        - Captures input with readchar, input buffer, and prompt
        - Handles ctrl + c to end session
    """

    def __init__(self, init_func=None, end_func=None):
        init()

        self.last_lines = []
        self.full_frame = []

        self.current_warning = ""
        self.warning_time_left = 0

        self.events = events.EventEmitter()
        self.running = False
        self.last_time = time.time()
        self.capturing_input = False
        self.input_prompt = ""
        self.input_buffer = []

        self.end_func = end_func if end_func else None

        self.last_input = ""
        self.harsh_flush()
        if init_func:
            init_func(self)

    def flush_frame(self):
        max_lines = max(len(self.full_frame), len(self.last_lines))
        for i in range(max_lines):
            new = self.full_frame[i] if i < len(self.full_frame) else ''
            old = self.last_lines[i] if i < len(self.last_lines) else 'no diff'
            if new != old:
                # how this ascii stuff works:
                # \033[] starts the control sequence
                # {i+1};0H positions the cursor at the row/column start (i is row, 0H is the column)
                # {new} is the diffed text (from new, old)
                # \033[K erases everything after the cursor to the end of the line
                # end='\n' goes to the next line
                end = ''
                if not i == max_lines - 1:
                    end = '\n'
                else:
                    end = ''

                print(f"\033[{i + 1};0H{new}\033[K", end=end)

        # move to end of last line
        last_line = len(self.last_lines)
        input_length = len(self.input_prompt + ''.join(self.input_buffer))
        print(f"\033[{last_line};{input_length + 1}H", end='', flush=True)

        self.last_lines = self.full_frame.copy()
        self.full_frame = []

    def harsh_flush(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw(self, text, color=None):
        color_code = get_color(color)
        lines = text.split('\n')

        for line in lines:
            self.full_frame.append(f"{color_code}{line}{Style.RESET_ALL}")

    def get_input(self, prompt, color=None):
        color_code = get_color(color)
        return input(f"{color_code}{prompt}{Style.RESET_ALL}")

    def non_blocking_input(self, prompt):
        if not self.capturing_input:
            self.input_buffer = []
            self.capturing_input = True
            self.input_prompt = prompt

    def cut_input(self):
        if self.capturing_input:
            self.capturing_input = False
            self.input_prompt = ""

    # on backspace: clear the last buffer
    # on space: append a space
    # on enter: finish the text
    # pretty intuitive stuff
    def get_inputs(self):
        while self.running:
            try:
                if not self.capturing_input:
                    time.sleep(0.01)
                    continue
                k = readkey()

                self.last_input = None
                if k == key.BACKSPACE:
                    if self.input_buffer:
                        self.input_buffer.pop()
                elif k == key.SPACE:
                    self.input_buffer.append(' ')
                elif k == key.ENTER:
                    self.capturing_input = False
                    self.last_input = ''.join(self.input_buffer)

                    self.input_prompt = ""

                    self.input_buffer = []
                    self.events.emit(
                        'keyboardEvent', card_input=self.last_input)
                elif len(k) == 1:
                    self.input_buffer.append(k)

            except KeyboardInterrupt:
                self.harsh_quit()

            except Exception:
                self.quit()

    def warn(self, message, time=1):
        self.current_warning = message
        self.warning_time_left = time

    def run_loop(self, update_func, draw_func, fps=30):
        self.harsh_flush()
        self.running = True
        frame_duration = 1 / fps
        self.last_time = time.time()

        self.input_loop = Thread(target=self.get_inputs)
        self.input_loop.start()
        while self.running:
            try:
                current_time = time.time()
                delta = current_time - self.last_time
                time.sleep(max(0, frame_duration - delta))
                update_func(delta)
                draw_func(delta)
                if self.warning_time_left > 0:
                    self.draw(self.current_warning, color="RED")
                    self.warning_time_left -= delta

                self.draw(self.input_prompt + ''.join(self.input_buffer))

                if self.running:
                    self.flush_frame()
                self.last_time = current_time
            except KeyboardInterrupt:
                self.harsh_quit()

    def harsh_quit(self):
        self.harsh_flush()
        print("Terminated", end="\n")
        self.quit()

    def quit(self):
        self.running = False

        if self.end_func:
            self.end_func()

        self.harsh_flush()

        for frame in self.full_frame:
            print(frame)
