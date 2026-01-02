from os import listdir, environ
import keyboard
from random import choice, uniform
from pygame import mixer
from time import sleep
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"


class AudioPlayer:

    def __init__(self, max_volume, min_volume, allow_repetitions, qnt_queries):
        mixer.init()
        #files section
        self.chosen_file = ""
        self.all_audios = []
        #volume section
        if (max_volume < min_volume): max_volume = min_volume
        self.max_volume = float(max_volume / 100)
        self.min_volume = float(min_volume / 100)
        #others
        self.keep_on_array = allow_repetitions
        self.queries_number = qnt_queries
        self.queried = []
    
    def prepare_query(self):
        #load all audios
        if (len(self.all_audios) == 0): self.all_audios = listdir(".\\audios\\")
        if (len(self.queried) == 0):
            for x in range(0, self.queries_number):
                chosen_file = choice(self.all_audios)
                self.queried.append(chosen_file)
                #remove from all audios array if repetition is not allowed
                if (self.keep_on_array == False):
                    file_index = self.all_audios.index(chosen_file)
                    self.all_audios.pop(file_index)
                    #quit loop if array is zeroed
                    if (len(self.all_audios) == 0): break

    def play_audio(self):
        mixer.music.load(".\\audios\\" + self.queried[0])
        mixer.music.play()
        while mixer.music.get_busy():
            if (keyboard.is_pressed(";")):
                sleep(0.1)
                break
            pass
        mixer.music.unload()

    #set a random volume between the minimum and maximum set volumes 
    def random_volume(self):
        chosen_volume = uniform(self.min_volume, self.max_volume)
        mixer.music.set_volume(chosen_volume)
        
    def volume_test(self):
        mixer.music.set_volume(self.max_volume)
        mixer.music.load(".\\sys\\volume_test.mp3")
        mixer.music.play()
        while mixer.music.get_busy():
            pass
        mixer.music.unload()

    def remove_played_query(self):
        self.queried.pop(0)
