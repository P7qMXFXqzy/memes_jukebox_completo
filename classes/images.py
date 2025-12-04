from os import listdir
from random import randrange, choice
from PyQt5.QtGui import QPixmap

class ImagesViewer:

    def __init__(self, main_window, use_images, max_resolution_x, max_resolution_y, pixmap_obj, label_obj, random_pos, repetition_allowed, hide_img):
        #pass parameters to variables
        self.main_window_obj = main_window
        self.use_images = use_images
        self.max_resolution_x = max_resolution_x
        self.max_resolution_y = max_resolution_y
        self.current_location_x = 0
        self.current_location_y = 0
        self.pixmap_obj = pixmap_obj
        self.label_obj = label_obj
        self.random_pos = random_pos
        self.keep_played_in_array = repetition_allowed
        self.hide_img = hide_img
        self.chosen_image = ""
        self.show_current_image = ""
        #load files
        self.loaded_images = []
        self.load_all_images()

    def load_all_images(self):
        self.loaded_images = listdir(".\\images\\")

    def show_image(self):
        #first define if images will be used
        if (self.use_images == 0): self.show_current_image = False
        elif (self.use_images == 1): self.show_current_image = True
        else: self.show_current_image = choice([False, True])
        #if yes, pick a random image, random location (if needed) and show the image.
        if (self.show_current_image == True):
            self.chosen_image = (choice(self.loaded_images))
            self.pixmap_obj.swap(QPixmap(".\\images\\" + self.chosen_image))
            self.label_obj.setPixmap(self.pixmap_obj)
            self.label_obj.repaint()
            if (self.random_pos == True): 
                self.current_location_x = randrange(0, self.max_resolution_x)
                self.current_location_y = randrange(0, self.max_resolution_y)
            if (self.hide_img == True): self.main_window_obj.move(self.current_location_x, self.current_location_y)

    def remove_played_file_from_array(self):
        file_index = self.loaded_images.index(self.chosen_image)
        self.loaded_images.pop(file_index)
        if (len(self.loaded_images) <= 0): self.load_all_images()
        
    def hide_after_audio(self):
        if (self.hide_img == True and self.show_current_image == True): self.main_window_obj.move(self.max_resolution_x + 100, 0)
        if (self.keep_played_in_array == False and self.show_current_image): self.remove_played_file_from_array()
        