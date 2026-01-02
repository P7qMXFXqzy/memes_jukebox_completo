import keyboard
from random import choice
from time import sleep

class KeysPresser:
    def __init__(self, allowed_keys, qnt_queries):
        self.enabled_keys = self.separate_by_comma(allowed_keys)
        self.queried = []
        self.queries_qnt = qnt_queries

    def separate_by_comma(self, received):
        #separate by each commas into an array, remove the spaces and return.
        separated = received.split(",")
        for x in range(0, len(separated)):
            spaces_removed = separated[x].strip()
            separated[x] = spaces_removed
        return separated

    def prepare_query(self):
        if (len(self.queried) == 0):
            for x in range(0, self.queries_qnt):
                self.queried.append(choice(self.enabled_keys))

    def quick_press(self):
        keyboard.press(self.queried[0])
        sleep(0.01)
        keyboard.release(self.queried[0])

    def press_release(self, hold_release):
        if (hold_release == "hold"):
            keyboard.press(self.queried[0])
        else: 
            keyboard.release(self.queried[0])

    def remove_played_query(self):
        self.queried.pop(0)