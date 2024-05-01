import pygame
from random import choice
import pandas as pd

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(64)  # Allows to play multiple sounds at the same time

class Sounds:
    def __init__(self, state):
        self.sounds_dict = {
            "hit": {"list": None},
            "explosion": {"list": None},
            "slash": {"list": None},
            "ice": {"list": None},
            "click": {"list": None},
            "dash": {"list": None}
        }

        df = pd.read_csv("settings.csv")
        df_dic = df.to_dict("records")
        self.volume = int(df_dic[0]["volume"])

        hit_sounds = []
        for x in range(1, 4):
            hit_sound = pygame.mixer.Sound(f"./Sound Effects/hit{str(x)}.wav")
            hit_sounds.append(hit_sound)

        self.sounds_dict["hit"]["list"] = hit_sounds
        self.sounds_dict["explosion"]["list"] = [pygame.mixer.Sound("./Sound Effects/explosion.mp3")]
        self.sounds_dict["ice"]["list"] = [pygame.mixer.Sound("./Sound Effects/ice1.wav")]
        self.sounds_dict["slash"]["list"] = [pygame.mixer.Sound("./Sound Effects/slash1.mp3")]
        self.sounds_dict["click"]["list"] = [pygame.mixer.Sound("./Sound Effects/mouse_click.mp3")]
        self.sounds_dict["dash"]["list"] = [pygame.mixer.Sound("./Sound Effects/dash.wav")]
        if state == "background_music":
            self.play_music()
        self.delay = 0

    def play_music(self):
        # Background music
        pygame.mixer.music.load("./Sound Effects/crimsonSpire.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.volume)

    def change_volume(self):
        df = pd.read_csv("settings.csv")
        df_dic = df.to_dict("records")
        self.volume = df_dic[0]["volume"]/100
        pygame.mixer.music.set_volume(self.volume)

    def click_sounds(self, events):
        click = False
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if click:
            if pygame.time.get_ticks() - self.delay > 200:
                self.sounds_dict["click"]["list"][0].play().set_volume(0.3)
                self.delay = pygame.time.get_ticks()

    def update(self, events):
        self.click_sounds(events)
        self.change_volume()
