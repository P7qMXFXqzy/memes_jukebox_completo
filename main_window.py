from sys import argv, exit
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QComboBox, QLineEdit, QScrollArea, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QDoubleValidator, QIntValidator
from PyQt5.QtCore import Qt, QTimer
from pyautogui import size as screen_size
from classes.images import ImagesViewer
from classes.audio import AudioPlayer
from random import randrange
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #window data
        self.running = False
        self.max_resolution_x,  self.max_resolution_y = screen_size()
        self.resize((int(self.max_resolution_x / 4)), (int(self.max_resolution_y / 2)))
        self.move(0,0)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)

        #background image
        self.background_image = QPixmap("")
        self.image_label = QLabel(self)
        self.image_label.setPixmap(self.background_image)
        self.image_label.setGeometry(0,0, 200,200)
        
        #validators
        seconds_validator = QIntValidator(0, 60, self)
        volume_validator = QDoubleValidator(0.0, 100.0, 2, self)

        #Scroll area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(0, 0, self.width(), self.height())
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background: rgb(50,50,50); border: none;")
        self.content = QWidget()
        self.content.setStyleSheet("background: rgb(50,50,50);")
        self.content.setAttribute(Qt.WA_StyledBackground, True)
        self.scroll_area.setWidget(self.content)

        #fields -o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
        screen_width = self.width()

        #Volume
        initialPosY = 30
        self.max_volume_text = QLabel("Max volume", self.content)
        self.max_volume_text.move(10, (initialPosY - 20))
        self.max_volume_text.setStyleSheet("color: white; font: 14px")
        self.max_volume_field = QLineEdit(self.content)
        self.max_volume_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.max_volume_field.setValidator(volume_validator)
        self.max_volume_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")
        self.max_volume_field.setText("1")

        initialPosY += 70
        self.min_volume_text = QLabel("Min volume", self.content)
        self.min_volume_text.move(10, (initialPosY - 20))
        self.min_volume_text.setStyleSheet("color: white; font: 14px")
        self.min_volume_field = QLineEdit(self.content)
        self.min_volume_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.min_volume_field.setValidator(volume_validator)
        self.min_volume_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")
        self.min_volume_field.setText("1")

        initialPosY += 70
        self.randomize_volume_text = QLabel("Randomize volume", self.content)
        self.randomize_volume_text.move(10, (initialPosY - 20))
        self.randomize_volume_text.setStyleSheet("color: white; font: 14px")
        self.randomize_volume_field = QComboBox(self.content)
        self.randomize_volume_field.addItems(["No", "Yes"])
        self.randomize_volume_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.randomize_volume_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")
        
        #images
        initialPosY += 70
        self.use_images_text = QLabel("Use images", self.content)
        self.use_images_text.move(10, (initialPosY - 20))
        self.use_images_text.setStyleSheet("color: white; font: 14px")
        self.use_images_field = QComboBox(self.content)
        self.use_images_field.addItems(["No", "Yes", "Randomly"])
        self.use_images_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.use_images_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")
        
        initialPosY += 70
        self.random_img_pos_text = QLabel("Random image position", self.content)
        self.random_img_pos_text.move(10, (initialPosY - 20))
        self.random_img_pos_text.setStyleSheet("color: white; font: 14px")
        self.random_img_position_field = QComboBox(self.content)
        self.random_img_position_field.addItems(["No", "Yes"])
        self.random_img_position_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.random_img_position_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")
        
        initialPosY += 70
        self.hide_img_after_audio_text = QLabel("Hide image after playing audio", self.content)
        self.hide_img_after_audio_text.move(10, (initialPosY - 20))
        self.hide_img_after_audio_text.setStyleSheet("color: white; font: 14px")
        self.hide_img_after_audio_field = QComboBox(self.content)
        self.hide_img_after_audio_field.addItems(["No", "Yes"])
        self.hide_img_after_audio_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.hide_img_after_audio_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")
        
        #seconds per meme
        initialPosY += 70
        self.seconds_per_meme_text = QLabel("Wait time per meme", self.content)
        self.seconds_per_meme_text.move(10, (initialPosY - 20))
        self.seconds_per_meme_text.setStyleSheet("color: white; font: 14px")
        self.seconds_per_meme_field = QLineEdit(self.content)
        self.seconds_per_meme_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.seconds_per_meme_field.setValidator(seconds_validator)
        self.seconds_per_meme_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")
        self.seconds_per_meme_field.setText("0")

        initialPosY += 70
        self.randomize_seconds_text = QLabel("Randomize seconds", self.content)
        self.randomize_seconds_text.move(10, (initialPosY - 20))
        self.randomize_seconds_text.setStyleSheet("color: white; font: 14px")
        self.randomize_seconds_field = QComboBox(self.content)
        self.randomize_seconds_field.addItems(["No", "Yes"])
        self.randomize_seconds_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.randomize_seconds_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")

        #repetitions
        initialPosY += 70
        self.allow_repetitions_text = QLabel("Allow repetitions", self.content)
        self.allow_repetitions_text.move(10, (initialPosY - 20))
        self.allow_repetitions_text.setStyleSheet("color: white; font: 14px")
        self.allow_repetitions_field = QComboBox(self.content)
        self.allow_repetitions_field.addItems(["No", "Yes"])
        self.allow_repetitions_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.allow_repetitions_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")

        #buttons
        initialPosY += 70
        self.start_button = QPushButton("Start", self.content)
        self.start_button.setGeometry(20, initialPosY, (int(screen_width / 3)), (int((screen_width / 3) / 2)))
        self.start_button.setStyleSheet("QPushButton{background: rgb(250,0,0); color: white; font: 30px; border: 5px solid rgb(0,0,0)} QPushButton:pressed{background: rgb(250,250,250); color: red;}")
        self.start_button.clicked.connect(self.start_jukebox)

        self.quit_button = QPushButton("Quit", self.content)
        self.quit_button.setGeometry(((int(screen_width / 3)) + 60), initialPosY, (int(screen_width / 3)), (int((screen_width / 3) / 2)))
        self.quit_button.setStyleSheet("QPushButton{background: rgb(250,0,0); color: white; font: 30px; border: 5px solid rgb(0,0,0)} QPushButton:pressed{background: rgb(250,250,250); color: red;}")
        self.quit_button.clicked.connect(self.save_and_exit)

        initialPosY += 70
        self.minimize_button = QPushButton("Minimize", self.content)
        self.minimize_button.setGeometry(20, initialPosY, (int(screen_width / 3)), (int((screen_width / 3) / 2)))
        self.minimize_button.setStyleSheet("QPushButton{background: rgb(250,0,0); color: white; font: 25px; border: 5px solid rgb(0,0,0)} QPushButton:pressed{background: rgb(250,250,250); color: red;}")
        self.minimize_button.clicked.connect(self.showMinimized)

        self.volume_test_button = QPushButton("Volume\ntest", self.content)
        self.volume_test_button.setGeometry(((int(screen_width / 3)) + 60), initialPosY, (int(screen_width / 3)), (int((screen_width / 3) / 2)))
        self.volume_test_button.setStyleSheet("QPushButton{background: rgb(250,0,0); color: white; font: 20px; border: 5px solid rgb(0,0,0)} QPushButton:pressed{background: rgb(250,250,250); color: red;}")
        self.volume_test_button.clicked.connect(self.test_volume)

        initialPosY += 70
        self.randomize_configs_button = QPushButton("Randomize\nconfigurations", self.content)
        self.randomize_configs_button.setGeometry(20, initialPosY, (int(screen_width / 3)), (int((screen_width / 3) / 2)))
        self.randomize_configs_button.setStyleSheet("QPushButton{background: rgb(250,0,0); color: white; font: 15px; border: 5px solid rgb(0,0,0)} QPushButton:pressed{background: rgb(250,250,250); color: red;}")
        self.randomize_configs_button.clicked.connect(self.set_random_configs)

        # Set enough height for scrollable content
        self.content.setMinimumHeight(initialPosY + 100)

        self.load_on_open()
        #-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o 

    def hide_window(self):
        #Audio player object
        if (self.randomize_volume_field.currentIndex() == 0): randomize_volume = False
        else: randomize_volume = True
        if(self.allow_repetitions_field.currentIndex() == 0): allow_repetitions = False
        else:   allow_repetitions = True
        self.audio_player_obj = AudioPlayer((float(self.max_volume_field.text())), (float(self.min_volume_field.text())), randomize_volume, allow_repetitions)
        
        #Images viewer object
        if (self.use_images_field.currentIndex() == 0): use_images = 0
        elif (self.use_images_field.currentIndex() == 1): use_images = 1
        else: use_images = 2 #randomly use image per loop
        if (self.random_img_position_field.currentIndex() == 0): random_img_position = False
        else: random_img_position = True
        if (self.hide_img_after_audio_field.currentIndex() == 0): hide_img = False
        else: hide_img = True
        self.img_viewer_obj = ImagesViewer(self, use_images, self.max_resolution_x, self.max_resolution_y, self.background_image, self.image_label, random_img_position, allow_repetitions, hide_img)
        
        #wait seconds
        self.max_wait_seconds = int(self.seconds_per_meme_field.text())
        if (self.randomize_seconds_field.currentIndex() == 0): self.randomize_seconds = False
        else: self.randomize_seconds = True

        #Hide configurations menu's content, turn window transparent and extend to fullscreen, then begin application's loop.
        self.content.hide()
        self.scroll_area.hide()
        self.resize(200,200)
        if (hide_img == True): self.move((self.max_resolution_x + 100),0) #hide window

    def start_jukebox(self):
        self.running = True
        self.hide_window()
        self.wait_seconds = self.max_wait_seconds
        self.looper = QTimer(self)
        self.looper.timeout.connect(self.jukebox_step)
        self.looper.setInterval((self.wait_seconds * 1000))
        self.looper.start()

    def jukebox_step(self):
        #play audio
        self.img_viewer_obj.show_image()
        self.audio_player_obj.play_audio()
        self.img_viewer_obj.hide_after_audio()
        if (self.randomize_seconds == True and self.max_wait_seconds > 0): 
            self.looper.stop()
            self.wait_seconds = randrange(0, (self.max_wait_seconds + 1))
            self.looper.setInterval((self.wait_seconds * 1000))
            self.looper.start()

    def keyPressEvent(self, event):
        # close on ESC
        if (event.key() == Qt.Key_Escape and self.running == True):
            #background image
            self.content.show()
            self.scroll_area.show()
            self.resize((int(self.max_resolution_x / 4)), (int(self.max_resolution_y / 2)))
            self.move(0,0)
            self.running = False
            self.looper.stop()
        
    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton and self.running == True):
            self.looper.stop()
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if getattr(self, "dragging", False):
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if (event.button() == Qt.LeftButton and self.running == True):
            self.dragging = False
            event.accept()
            print(self.pos())
            self.looper.start()

    def test_volume(self):
        self.audio_player_obj = AudioPlayer((float(self.max_volume_field.text())), 0.0, "", "")
        self.audio_player_obj.volume_test()

    def save_and_exit(self):
        text_file = ".\\sys\\configs.txt"
        content = str(self.max_volume_field.text()) + "\n"
        content = content + str(self.min_volume_field.text()) + "\n" 
        content = content + str(self.randomize_volume_field.currentIndex()) + "\n"
        content = content + str(self.use_images_field.currentIndex()) + "\n"
        content = content + str(self.random_img_position_field.currentIndex()) + "\n"
        content = content + str(self.hide_img_after_audio_field.currentIndex()) + "\n"
        content = content + str(self.seconds_per_meme_field.text()) + "\n"
        content = content + str(self.randomize_seconds_field.currentIndex()) + "\n"
        content = content + str(self.allow_repetitions_field.currentIndex())
        if (not(os.path.exists(text_file))):#Create file if it doesn't exist and write
            with open(text_file, 'w') as file:
                file.write("")
        with open(text_file, 'w+') as file:
            file.write(content)
        QApplication.instance().quit()

    def load_on_open(self):
        content = ""
        text_file = ".\\sys\\configs.txt"
        if (os.path.exists(text_file)):
            with open(text_file) as file:
                content = [line.rstrip() for line in file]
            self.max_volume_field.setText(content[0])
            self.min_volume_field.setText(content[1])
            self.randomize_volume_field.setCurrentIndex(int(content[2]))
            self.use_images_field.setCurrentIndex(int(content[3]))
            self.random_img_position_field.setCurrentIndex(int(content[4]))
            self.hide_img_after_audio_field.setCurrentIndex(int(content[5]))
            self.seconds_per_meme_field.setText(content[6])
            self.randomize_seconds_field.setCurrentIndex(int(content[7]))
            self.allow_repetitions_field.setCurrentIndex(int(content[8]))
    
    def set_random_configs(self):
        max_volume = int(self.max_volume_field.text())
        self.min_volume_field.setText(str(randrange(10, max_volume)))
        self.randomize_volume_field.setCurrentIndex(randrange(0,2))
        self.use_images_field.setCurrentIndex(randrange(0,3))
        self.random_img_position_field.setCurrentIndex(randrange(0,2))
        self.hide_img_after_audio_field.setCurrentIndex(randrange(0,2))
        self.seconds_per_meme_field.setText(str(randrange(0,11)))
        self.randomize_seconds_field.setCurrentIndex(randrange(0,2))
        self.allow_repetitions_field.setCurrentIndex(randrange(0,2))

app = QApplication(argv)
window = MainWindow()
window.setWindowTitle("Meme Jukebox")
window.show()
exit(app.exec_())