from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from pyautogui import size as screen_size
from random import randrange, choice
from os import listdir

class ImagesViewerWindow(QMainWindow):

    def __init__(self, repetition_allowed, qnt_queries):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.keep_played_in_array = repetition_allowed
        self.queries_qnt = qnt_queries
        self.queried = []
        self.loaded_images = []
        self.max_resolutions = [0, 0]
        self.max_resolutions[0],  self.max_resolutions[1] = screen_size()
        self.resize(200,200)
        self.background_pixmap = QPixmap("")
        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)
        self.image_label.resize(200,200)
        self.show()
        
    def prepare_query(self):
        if (len(self.loaded_images) == 0): self.loaded_images = listdir(".\\images\\")
        if (len(self.queried) == 0):
            for x in range(0, self.queries_qnt):
                chosen_file = choice(self.loaded_images)
                self.queried.append(chosen_file)
                #remove from all files array if set to not repeat
                if (self.keep_played_in_array == False):
                    file_index = self.loaded_images.index(chosen_file)
                    self.loaded_images.pop(file_index)
                    if (len(self.loaded_images) == 0): break

    def show_image(self):
        self.background_pixmap = QPixmap(".\\images\\" + self.queried[0])
        #move pixmap to label
        self.image_label.setPixmap(self.background_pixmap)
        self.image_label.repaint()
        #show window with image to a random location
        self.move((randrange(0, self.max_resolutions[0])), (randrange(0, self.max_resolutions[1])))

    def hide_window(self):
        self.move((self.max_resolutions[0] + 100), 0)

    def remove_played_query(self):
        self.queried.pop(0)
