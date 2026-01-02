from sys import argv, exit
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QComboBox, QLineEdit, QScrollArea, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtCore import Qt, QTimer
from pyautogui import size as screen_size
from classes.images import ImagesViewerWindow
from classes.audio import AudioPlayer
from classes.keys_press import KeysPresser
from random import randrange, choice
import os
from time import sleep

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.running = False
        self.running_fullscreen_effect = False
        self.current_play = 0
        self.queries_combinations = []
        self.max_resolution_x,  self.max_resolution_y = screen_size()
        self.resize((int(self.max_resolution_x / 4)), (int(self.max_resolution_y / 2)))
        self.move(0,0)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)

        #background image
        self.background_pixmap = QPixmap("")
        self.image_label = QLabel(self)
        self.image_label.setPixmap(self.background_pixmap)
        self.image_label.setGeometry(0,0, 200,200)
        
        ints_validator = QIntValidator(1, 1000, self)

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

        #audios
        initialPosY = 30
        self.use_audios_text = QLabel("Use audios", self.content)
        self.use_audios_text.move(10, (initialPosY - 20))
        self.use_audios_text.setStyleSheet("color: white; font: 14px")
        self.use_audios_field = QComboBox(self.content)
        self.use_audios_field.addItems(["No", "Yes", "Randomly"])
        self.use_audios_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.use_audios_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")
        
        initialPosY += 70
        self.max_volume_text = QLabel("Max volume", self.content)
        self.max_volume_text.move(10, (initialPosY - 20))
        self.max_volume_text.setStyleSheet("color: white; font: 14px")
        self.max_volume_field = QLineEdit(self.content)
        self.max_volume_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.max_volume_field.setValidator(ints_validator)
        self.max_volume_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")
        self.max_volume_field.setText("1")

        initialPosY += 70
        self.min_volume_text = QLabel("Min volume", self.content)
        self.min_volume_text.move(10, (initialPosY - 20))
        self.min_volume_text.setStyleSheet("color: white; font: 14px")
        self.min_volume_field = QLineEdit(self.content)
        self.min_volume_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.min_volume_field.setValidator(ints_validator)
        self.min_volume_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")
        self.min_volume_field.setText("1")

        initialPosY += 70
        self.volume_test_button = QPushButton("Volume\ntest", self.content)
        self.volume_test_button.setGeometry(10, (initialPosY - 20), (int(screen_width / 3)), (int((screen_width / 3) / 2)))
        self.volume_test_button.setStyleSheet("QPushButton{background: rgb(250,0,0); color: white; font: 20px; border: 5px solid rgb(0,0,0)} QPushButton:pressed{background: rgb(250,250,250); color: red;}")
        self.volume_test_button.clicked.connect(self.test_volume)
       
        #images
        initialPosY += 70
        self.use_images_text = QLabel("Use images", self.content)
        self.use_images_text.move(10, (initialPosY - 20))
        self.use_images_text.setStyleSheet("color: white; font: 14px")
        self.use_images_field = QComboBox(self.content)
        self.use_images_field.addItems(["No", "Yes", "Randomly"])
        self.use_images_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.use_images_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")

        #random inputs
        initialPosY += 70
        self.random_inputs_text = QLabel("Random inputs", self.content)
        self.random_inputs_text.move(10, (initialPosY - 20))
        self.random_inputs_text.setStyleSheet("color: white; font: 14px")
        self.random_inputs_field = QComboBox(self.content)
        self.random_inputs_field.addItems(["No", "Yes", "Randomly"])
        self.random_inputs_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.random_inputs_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")

        initialPosY += 70
        self.allowed_keys_text = QLabel("Allowed keys (separate by comma)", self.content)
        self.allowed_keys_text.move(10, (initialPosY - 20))
        self.allowed_keys_text.setStyleSheet("color: white; font: 14px")
        self.allowed_keys_field = QLineEdit(self.content)
        self.allowed_keys_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.allowed_keys_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")
        self.allowed_keys_field.setText("")

        #seconds per meme
        initialPosY += 70
        self.seconds_per_meme_text = QLabel("Wait time per meme", self.content)
        self.seconds_per_meme_text.move(10, (initialPosY - 20))
        self.seconds_per_meme_text.setStyleSheet("color: white; font: 14px")
        self.seconds_per_meme_field = QLineEdit(self.content)
        self.seconds_per_meme_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.seconds_per_meme_field.setValidator(ints_validator)
        self.seconds_per_meme_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")
        self.seconds_per_meme_field.setText("0")

        initialPosY += 70
        self.randomize_seconds_text = QLabel("Randomize seconds", self.content)
        self.randomize_seconds_text.move(10, (initialPosY - 20))
        self.randomize_seconds_text.setStyleSheet("color: white; font: 14px")
        self.randomize_seconds_field = QComboBox(self.content)
        self.randomize_seconds_field.addItems(["No", "Yes", "Randomly"])
        self.randomize_seconds_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.randomize_seconds_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")

        #sequential mode
        initialPosY += 70
        self.sequential_mode_text = QLabel("Sequential mode", self.content)
        self.sequential_mode_text.move(10, (initialPosY - 20))
        self.sequential_mode_text.setStyleSheet("color: white; font: 14px")
        self.sequential_mode_field = QComboBox(self.content)
        self.sequential_mode_field.addItems(["No", "Yes"])
        self.sequential_mode_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.sequential_mode_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")

        initialPosY += 70
        self.plays_before_wait_text = QLabel("Quantity of sequences before wait", self.content)
        self.plays_before_wait_text.move(10, (initialPosY - 20))
        self.plays_before_wait_text.setStyleSheet("color: white; font: 14px")
        self.plays_before_wait_field = QLineEdit(self.content)
        self.plays_before_wait_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.plays_before_wait_field.setValidator(ints_validator)
        self.plays_before_wait_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")
        self.plays_before_wait_field.setText("1")

        #repetitions
        initialPosY += 70
        self.allow_repetitions_text = QLabel("Allow repetitions", self.content)
        self.allow_repetitions_text.move(10, (initialPosY - 20))
        self.allow_repetitions_text.setStyleSheet("color: white; font: 14px")
        self.allow_repetitions_field = QComboBox(self.content)
        self.allow_repetitions_field.addItems(["No", "Yes"])
        self.allow_repetitions_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.allow_repetitions_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")
        
        #quantity of queries
        initialPosY += 70
        self.queries_quantity_text = QLabel("Quantity of queries", self.content)
        self.queries_quantity_text.move(10, (initialPosY - 20))
        self.queries_quantity_text.setStyleSheet("color: white; font: 14px")
        self.queries_quantity_field = QLineEdit(self.content)
        self.queries_quantity_field.setGeometry(10, initialPosY, (screen_width - 30), 30)
        self.queries_quantity_field.setValidator(ints_validator)
        self.queries_quantity_field.setStyleSheet("background: rgb(250,0,0); color: white; font: 14px")
        self.queries_quantity_field.setText("1")

        #buttons
        initialPosY += 70
        self.start_button = QPushButton("Start", self.content)
        self.start_button.setGeometry(20, initialPosY, (int(screen_width / 3)), (int((screen_width / 3) / 2)))
        self.start_button.setStyleSheet("QPushButton{background: rgb(250,0,0); color: white; font: 30px; border: 5px solid rgb(0,0,0)} QPushButton:pressed{background: rgb(250,250,250); color: red;}")
        self.start_button.clicked.connect(lambda: (self.save_configurations(), self.start_jukebox()))

        self.quit_button = QPushButton("Quit", self.content)
        self.quit_button.setGeometry(((int(screen_width / 3)) + 60), initialPosY, (int(screen_width / 3)), (int((screen_width / 3) / 2)))
        self.quit_button.setStyleSheet("QPushButton{background: rgb(250,0,0); color: white; font: 30px; border: 5px solid rgb(0,0,0)} QPushButton:pressed{background: rgb(250,250,250); color: red;}")
        self.quit_button.clicked.connect(lambda: (self.save_configurations(), QApplication.instance().quit()))

        initialPosY += 70
        self.minimize_button = QPushButton("Minimize", self.content)
        self.minimize_button.setGeometry((int(screen_width / 3.5)), initialPosY, (int(screen_width / 3)), (int((screen_width / 3) / 2)))
        self.minimize_button.setStyleSheet("QPushButton{background: rgb(250,0,0); color: white; font: 25px; border: 5px solid rgb(0,0,0)} QPushButton:pressed{background: rgb(250,250,250); color: red;}")
        self.minimize_button.clicked.connect(self.showMinimized)

        initialPosY += 70
        self.randomize_configs_button = QPushButton("Randomize\nconfigurations", self.content)
        self.randomize_configs_button.setGeometry(20, initialPosY, (int(screen_width / 3)), (int((screen_width / 3) / 2)))
        self.randomize_configs_button.setStyleSheet("QPushButton{background: rgb(250,0,0); color: white; font: 15px; border: 5px solid rgb(0,0,0)} QPushButton:pressed{background: rgb(250,250,250); color: red;}")
        self.randomize_configs_button.clicked.connect(self.set_random_configs)

        self.chaos_configs_button = QPushButton("Chaos\nconfigurations", self.content)
        self.chaos_configs_button.setGeometry(((int(screen_width / 3)) + 60), initialPosY, (int(screen_width / 3)), (int((screen_width / 3) / 2)))
        self.chaos_configs_button.setStyleSheet("QPushButton{background: rgb(250,0,0); color: white; font: 15px; border: 5px solid rgb(0,0,0)} QPushButton:pressed{background: rgb(250,250,250); color: red;}")
        self.chaos_configs_button.clicked.connect(self.set_chaos_configs)

        # Set enough height for scrollable content
        self.content.setMinimumHeight(initialPosY + 100)

        self.load_on_open()
        #-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o 

    def hide_window(self):
        #Hide configurations menu's content, turn window transparent and extend to fullscreen, then begin application's loop.
        self.content.hide()
        self.scroll_area.hide()
        self.move((self.max_resolution_x + 100),0) #hide window
    
    def prepare_objects(self):
        self.queries_quantity_number = (int(self.queries_quantity_field.text()))
        self.use_audios = self.use_audios_field.currentIndex()
        self.use_images = self.use_images_field.currentIndex()
        self.use_key_presses = self.random_inputs_field.currentIndex()
        #Objects
        if(self.allow_repetitions_field.currentIndex() == 0): allow_repetitions = False
        else:   allow_repetitions = True
        self.audio_player_obj = AudioPlayer((float(self.max_volume_field.text())), (float(self.min_volume_field.text())), allow_repetitions, self.queries_quantity_number)
        self.img_viewer_obj = ImagesViewerWindow(allow_repetitions, self.queries_quantity_number)
        self.keys_presses_obj = KeysPresser(self.allowed_keys_field.text(), self.queries_quantity_number)
        #wait seconds
        self.max_wait_seconds = (int(self.seconds_per_meme_field.text()))
        self.randomize_seconds = (int(self.randomize_seconds_field.currentIndex()))
        #sequential mode
        self.current_play = 0
        if(self.sequential_mode_field.currentIndex() == 1): 
            self.sequences_before_wait = (int(self.plays_before_wait_field.text()))
        else: 
            self.sequences_before_wait = 0

    def start_jukebox(self):
        self.running = True
        self.prepare_objects()
        self.hide_window()
        self.set_queries()
        self.looper = QTimer(self)
        self.looper.timeout.connect(self.jukebox_step)
        self.looper.setInterval(self.set_seconds_for_next_step())
        self.looper.start()

    def jukebox_step(self):
        #Execute effects only after defining the queries array's value
        if (len(self.queries_combinations) == 0): self.set_queries()
        #reload each class's query if present on current query (index 0)
        if ("1" in self.queries_combinations[0]): self.audio_player_obj.prepare_query()
        if ("2" in self.queries_combinations[0]): self.img_viewer_obj.prepare_query()
        if ("3" in self.queries_combinations[0]): self.keys_presses_obj.prepare_query()
        self.play_current_query(self.queries_combinations[0])
        #check again to remove the already-played query
        if ("1" in self.queries_combinations[0]): self.audio_player_obj.remove_played_query()
        if ("2" in self.queries_combinations[0]): self.img_viewer_obj.remove_played_query()
        if ("3" in self.queries_combinations[0]): self.keys_presses_obj.remove_played_query()
        self.queries_combinations.pop(0)
        self.looper.stop()
        self.looper.setInterval(self.set_seconds_for_next_step())
        self.looper.start()

    def play_current_query(self, current_query):
        if ("3" in current_query): press_type = choice(["press", "hold"])
        #will always play audio, image and key press are variables
        if (current_query[0] == "1"):
            self.audio_player_obj.random_volume()

            if (current_query[1] == "2"):
                #current query = "123"
                if (current_query[2] == "3"):
                    #press key, show image, play audio, hide image
                    if (press_type == "press"):
                        self.keys_presses_obj.quick_press()
                        self.img_viewer_obj.show_image()
                        self.audio_player_obj.play_audio()
                        self.img_viewer_obj.hide_window()
                    else:
                        #hold key, show image, play audio, hide image, release key
                        self.keys_presses_obj.press_release("hold")
                        self.img_viewer_obj.show_image()
                        self.audio_player_obj.play_audio()
                        self.img_viewer_obj.hide_window()
                        self.keys_presses_obj.press_release("release")

                #current query = "12"
                else:
                    self.img_viewer_obj.show_image()
                    self.audio_player_obj.play_audio()
                    self.img_viewer_obj.hide_window()
            #current query = "13"
            elif (current_query[1] == "3"):
                #press key, play audio
                if (press_type == "press"):
                    self.keys_presses_obj.quick_press()
                    self.audio_player_obj.play_audio()
                #hold key, play audio, release key
                else:
                    self.keys_presses_obj.press_release("hold")
                    self.audio_player_obj.play_audio()
                    self.keys_presses_obj.press_release("release")
            #current query = "1"
            else:
                self.audio_player_obj.play_audio()

        #will always show image
        elif (current_query[0] == "2"):
            #current query = "23", press key and show image
            if (current_query[1] == "3"):
                if (press_type == "press"):
                    self.img_viewer_obj.show_image()
                    self.keys_presses_obj.quick_press()
                    sleep(1)
                    self.img_viewer_obj.hide_window()
                else:
                    self.keys_presses_obj.press_release("hold")
                    self.img_viewer_obj.show_image()
                    sleep(1)
                    self.keys_presses_obj.press_release("release")
                    self.img_viewer_obj.hide_window()

            #just show image for 1 second
            else:
                self.img_viewer_obj.show_image()
                sleep(1)
                self.img_viewer_obj.hide_window()

        #just key press alone
        elif (current_query[0] == "3"):
            if (press_type == "press"):
                self.keys_presses_obj.quick_press()
            else:
                self.keys_presses_obj.press_release("hold")
                sleep(1)
                self.keys_presses_obj.press_release("release")

    def set_queries(self):
        #1 = audio; 2 = images; 3 = keys presses
        for x in range(0, self.queries_quantity_number):
            new_query = ""
            #add audio to query
            if ((self.use_audios == 1) or (self.use_audios == 2 and (choice([False, True]) == True))):
                new_query = new_query + "1"
            if ((self.use_images == 1) or (self.use_images == 2 and (choice([False, True]) == True))):
                new_query = new_query + "2"
            if ((self.use_key_presses == 1) or (self.use_key_presses == 2 and (choice([False, True]) == True))):
                new_query = new_query + "3"
            if (new_query != ""): 
                new_query = new_query + " "
                self.queries_combinations.append(new_query)

    def set_seconds_for_next_step(self):
        next_second = 0
        #normal mode
        if (self.sequences_before_wait == 0):
            if (self.randomize_seconds == 1): #randomize
                next_second = randrange(0, (self.max_wait_seconds + 1))
            else: next_second = self.max_wait_seconds
            next_second = next_second * 1000
        #sequential mode
        else: 
            self.current_play += 1
            if (self.current_play == self.sequences_before_wait):
                if (self.randomize_seconds == 1): #randomize
                    next_second = randrange(0, (self.max_wait_seconds + 1))
                else: next_second = self.max_wait_seconds
                next_second = next_second * 1000
                self.current_play = 0
            else: next_second = 0

        return next_second

    def keyPressEvent(self, event):
        #Reopen menu on ESC
        if (event.key() == Qt.Key_Escape and self.running == True):
            self.queries_combinations = []
            self.running = False
            self.looper.stop()
            self.img_viewer_obj.hide()
            self.resize((int(self.max_resolution_x / 4)), (int(self.max_resolution_y / 2)))
            self.content.show()
            self.scroll_area.show()
            self.move(0,0)
        elif (event.key() == Qt.Key_Semicolon and self.running == True):
            sleep(0.1)
            self.looper.stop()
            self.looper.setInterval(0)
            self.looper.start()

    def test_volume(self):
        self.audio_player_obj = AudioPlayer((float(self.max_volume_field.text())), 0.0, "", "")
        self.audio_player_obj.volume_test()
        self.audio_player_obj = None

    def save_configurations(self):
        text_file = ".\\sys\\configs.txt"
        content = str(self.use_audios_field.currentIndex())         + "\n"
        content += self.max_volume_field.text()                     + "\n"
        content += self.min_volume_field.text()                     + "\n" 
        content += str(self.use_images_field.currentIndex())        + "\n"
        content += str(self.random_inputs_field.currentIndex())     + "\n"
        content += self.allowed_keys_field.text()                   + "\n"
        content += self.seconds_per_meme_field.text()               + "\n"
        content += str(self.allow_repetitions_field.currentIndex()) + "\n"
        content += self.queries_quantity_field.text()               + "\n"
        content += str(self.randomize_seconds_field.currentIndex()) + "\n"
        content += str(self.sequential_mode_field.currentIndex())      + "\n"
        content += self.plays_before_wait_field.text()              + "\n"

        if (not(os.path.exists(text_file))):#Create file if it doesn't exist and write
            with open(text_file, 'w') as file:
                file.write("")
        with open(text_file, 'w+') as file:
            file.write(content)

    def load_on_open(self):
        content = ""
        text_file = ".\\sys\\configs.txt"
        if (os.path.exists(text_file)):
            with open(text_file) as file:
                content = [line.rstrip() for line in file]
            try:
                self.use_audios_field.setCurrentIndex(int(content[0]))
                self.max_volume_field.setText(content[1])
                self.min_volume_field.setText(content[2])
                self.use_images_field.setCurrentIndex(int(content[3]))
                self.random_inputs_field.setCurrentIndex(int(content[4]))
                self.allowed_keys_field.setText(content[5])
                self.seconds_per_meme_field.setText(content[6])
                self.allow_repetitions_field.setCurrentIndex(int(content[7]))
                self.queries_quantity_field.setText(content[8])
                self.randomize_seconds_field.setCurrentIndex(int(content[9]))
                self.sequential_mode_field.setCurrentIndex(int(content[10]))
                self.plays_before_wait_field.setText(content[11])
            except: pass
    
    def set_random_configs(self):
        self.use_audios_field.setCurrentIndex(randrange(0,3))
        self.max_volume_field.setText(str(randrange(1, 1000)))
        self.min_volume_field.setText(str(randrange(1, ((int(self.max_volume_field.text()))) + 1)))
        self.use_images_field.setCurrentIndex(randrange(0,3))
        self.random_inputs_field.setCurrentIndex(randrange(0,3))
        self.seconds_per_meme_field.setText(str(randrange(0,1000)))
        self.allow_repetitions_field.setCurrentIndex(randrange(0,2))
        self.queries_quantity_field.setText(str(randrange(1,1000)))
        self.randomize_seconds_field.setCurrentIndex(randrange(0,2))
        self.sequential_mode_field.setCurrentIndex(randrange(0,2))
        self.plays_before_wait_field.setText(str(randrange(1,1000)))

    def set_chaos_configs(self):
        self.use_audios_field.setCurrentIndex(2)
        max_volume = int(self.max_volume_field.text())
        self.min_volume_field.setText(str(int(max_volume / 2)))
        self.use_images_field.setCurrentIndex(2)
        self.random_inputs_field.setCurrentIndex(2)
        self.seconds_per_meme_field.setText("1")
        self.allow_repetitions_field.setCurrentIndex(1)
        self.queries_quantity_field.setText("10")
        self.randomize_seconds_field.setCurrentIndex(1)
        self.sequential_mode_field.setCurrentIndex(0)
        self.plays_before_wait_field.setText("10")

app = QApplication(argv)
window = MainWindow()
window.setWindowTitle("Meme Jukebox")
window.show()
exit(app.exec_())
