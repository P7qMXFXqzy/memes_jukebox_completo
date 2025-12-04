from os import listdir, environ
import keyboard
from random import choice, uniform
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
from pygame import mixer, sndarray


class AudioPlayer:

    def __init__(self, max_volume, min_volume, randomize_volume, allow_repetitions):
        mixer.init()
        #files section
        self.chosen_file = ""
        self.loaded_audios = []
        self.load_all_audios()
        #volume section
        if (max_volume < min_volume): max_volume = min_volume
        self.max_volume = float(max_volume / 100)
        self.min_volume = float(min_volume / 100)
        self.randomize_volume = randomize_volume
        self.set_volume(self.max_volume)
        #others
        self.keep_on_array = allow_repetitions

    def load_all_audios(self):
        self.loaded_audios = listdir(".\\audios\\")

    def choose_random_file_to_play(self):
        self.chosen_file = choice(self.loaded_audios)

    def remove_played_file_from_array(self):
        file_index = self.loaded_audios.index(self.chosen_file)
        self.loaded_audios.pop(file_index)
        if (len(self.loaded_audios) <= 0): self.load_all_audios()

    def random_volume(self):
        chosen_volume = uniform(self.min_volume, self.max_volume)
        self.set_volume(chosen_volume)

    def play_audio(self):
        self.choose_random_file_to_play()
        if (self.randomize_volume == True): self.random_volume()
        chosen = (".\\audios\\" + self.chosen_file)
        mixer.music.load(chosen)
        mixer.music.play()
        while mixer.music.get_busy():
            pass
        mixer.music.unload()
        if (self.keep_on_array == False): self.remove_played_file_from_array()
    
    def set_volume(self, volume):
        mixer.music.set_volume(volume)

    def volume_test(self):
        self.set_volume(self.max_volume)
        mixer.music.load(".\\sys\\volume_test.mp3")
        mixer.music.play()
        while mixer.music.get_busy():
            pass
        mixer.music.unload()