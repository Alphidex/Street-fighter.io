import pygame
from Characters_Code.Asuka import *
from Characters_Code.Daichi import *
from Characters_Code.Gyamon import *
from Characters_Code.Heihachi import *
from Characters_Code.Ichigo import *
from Characters_Code.Renji import *
from Characters_Code.Sanji import *
from Characters_Code.Toshiro import *
from Characters_Code.Uryu import *
from Characters_Code.Zoro import *

#--------------------------- SpreadSheet Annotations ------------------------------>

""" Asuka """
Asuka_SCALE = 2.5
Asuka_OFFSET = [47, 49]
Asuka_DATA = [160, 160, Asuka_SCALE, Asuka_OFFSET]
Asuka_ANIMATION_STEPS = [17, 13, 11, 8, 8, 8, 8, 7, 7, 6, 6, 5, 5, 4, 3, 2]

""" Daichi """
Daichi_SCALE = 2.5
Daichi_OFFSET = [60, 48]
Daichi_DATA = [160, 160, Daichi_SCALE, Daichi_OFFSET]
Daichi_ANIMATION_STEPS = [14, 14, 13, 9, 8, 8, 7, 6, 6, 6, 5, 4, 4, 3, 3, 2, 2]


""" Gyamon """
Gyamon_SCALE = 2.5
Gyamon_OFFSET = [60, 32]
Gyamon_DATA = [160, 160, Gyamon_SCALE, Gyamon_OFFSET]
Gyamon_ANIMATION_STEPS = [27, 24, 12, 10, 10, 8, 8, 8, 7, 6, 6, 6, 6, 6, 6, 2, 2]
# Note: First animation is 300x300 dimensions

""" Heihachi """
Heihachi_SCALE = 2.5
Heihachi_OFFSET = [53, 50]
Heihachi_DATA = [160, 160, Heihachi_SCALE, Heihachi_OFFSET]
Heihachi_ANIMATION_STEPS = [19, 7, 18, 16, 16, 15, 13, 12, 9, 8, 8, 8, 8, 6, 5, 4, 4, 3, 3, 2]

""" Ichigo """
Ichigo_SCALE = 2.5
Ichigo_OFFSET = [56, 50]
Ichigo_DATA = [160, 160, Ichigo_SCALE, Ichigo_OFFSET]
Ichigo_ANIMATION_STEPS = [15, 13, 13, 12, 12, 12, 11, 9, 9, 8, 7, 7, 7, 7, 5, 5, 5, 4, 4, 2, 2]

""" Renji """
Renji_SCALE = 2.5
Renji_OFFSET = [58, 50]
Renji_DATA = [160, 160, Renji_SCALE, Renji_OFFSET]
Renji_ANIMATION_STEPS = [12, 11, 18, 19, 10, 10, 12, 11, 11, 10, 10, 9, 8, 8, 7, 7, 6, 6, 5, 4, 4, 4, 2, 1]  # Len = 24

""" Sanji """
Sanji_SCALE = 2.5
Sanji_OFFSET = [51, 50]
Sanji_DATA = [160, 160, Sanji_SCALE, Sanji_OFFSET]
Sanji_ANIMATION_STEPS = [44, 26, 18, 17, 15, 14, 12, 12, 8, 8, 8, 7, 7, 7, 7, 6, 5, 4, 3, 3, 3, 2]

""" Toshiro """
Toshiro_SCALE = 2.5
Toshiro_OFFSET = [58, 50]
Toshiro_DATA = [160, 160, Toshiro_SCALE, Toshiro_OFFSET]
Toshiro_ANIMATION_STEPS = [21, 15, 11, 11, 10, 10, 10, 8, 8, 8, 8, 8, 7, 6, 6, 6, 6, 6, 5, 4, 4, 4, 4, 4, 4, 4, 3, 3, 1]

""" Uryu """
Uryu_SCALE = 2.5
Uryu_OFFSET = [52, 50]
Uryu_DATA = [160, 160, Uryu_SCALE, Uryu_OFFSET]
Uryu_ANIMATION_STEPS = [7, 10, 10, 8, 8, 8, 8, 8, 7, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 4, 4, 4, 4, 4, 4, 4, 3, 3]


""" Zoro """
Zoro_SCALE = 2.65
Zoro_OFFSET = [53, 38]
Zoro_DATA = [160, 160, Zoro_SCALE, Zoro_OFFSET]
special_attack_list = [14]
Zoro_ANIMATION_STEPS = [16, 15, 15, 15, 14, 14, 11, 10, 10, 9, 9, 8, 8, 8, 7, 6, 6, 6, 6, 5, 4, 3, 2]

# [attack, range (0 - close, 1 - mid, 2 - long), effects? projectile]
attack_patterns = {
        "Asuka": [["normal_attack", 0, None, False], ["normal_attack_up", 0, ["knockback"], False], ["normal_jump_attack", 0, None, False],
                             ["strong_attack", 2, None, True], ["strong_attack_down", 0, ["guard-break"], False], ["strong_attack_up", 2, ["teleport"], False],
                             ["strong_jump_attack", 2, None, True], ["special_attack", 2, None, True]],
        "Daichi": [["normal_attack",  ], ["normal_attack_up"], ["normal_attack_down"], ["normal_jump_attack"],
                             ["strong_attack"], ["strong_attack_down"], ["strong_attack_up"], ["strong_jump_attack"],
                             ["special_attack"]],
        "Gyamon": [["normal_attack", ], ["normal_attack_up"], ["normal_attack_down"], ["normal_jump_attack"],
                             ["strong_attack"], ["strong_attack_down"], ["strong_attack_up"], ["strong_jump_attack"],
                             ["special_attack"]],
        "Heihachi": [["normal_attack", ], ["normal_attack_up"], ["normal_attack_down"], ["normal_jump_attack"],
                             ["strong_attack"], ["strong_attack_down"], ["strong_attack_up"], ["strong_jump_attack"],
                             ["special_attack"]],
        "Ichigo": [["normal_attack", ], ["normal_attack_up"], ["normal_attack_down"], ["normal_jump_attack"],
                             ["strong_attack"], ["strong_attack_down"], ["strong_attack_up"], ["strong_jump_attack"],
                             ["special_attack"]],
        "Renji": [["normal_attack", ], ["normal_attack_up"], ["normal_attack_down"], ["normal_jump_attack"],
                             ["strong_attack"], ["strong_attack_down"], ["strong_attack_up"], ["strong_jump_attack"],
                             ["special_attack"]],
        "Sanji": [["normal_attack", ], ["normal_attack_up"], ["normal_attack_down"], ["normal_jump_attack"],
                             ["strong_attack"], ["strong_attack_down"], ["strong_attack_up"], ["strong_jump_attack"],
                             ["special_attack"]],
        "Toshiro": [["normal_attack", ], ["normal_attack_up"], ["normal_attack_down"], ["normal_jump_attack"],
                             ["strong_attack"], ["strong_attack_down"], ["strong_attack_up"], ["strong_jump_attack"],
                             ["special_attack"]],
        "Uryu": [["normal_attack", ], ["normal_attack_up"], ["normal_attack_down"], ["normal_jump_attack"],
                             ["strong_attack"], ["strong_attack_down"], ["strong_attack_up"], ["strong_jump_attack"],
                             ["special_attack"]],
        "Zoro": [["normal_attack", ], ["normal_attack_up"], ["normal_attack_down"], ["normal_jump_attack"],
                             ["strong_attack"], ["strong_attack_down"], ["strong_attack_up"], ["strong_jump_attack"],
                             ["special_attack"]]}

def load_character_image(path):
    return pygame.image.load(path).convert_alpha()


def get_character_data():
    # Load Images in Main since I can't do it from other modules without initializing a surface
    Asuka_Surface = load_character_image(r"Images/Game Characters Organised/Asuka/Result.png")
    Daichi_Surface = load_character_image(r"Images/Game Characters Organised/Daichi/Result.png")
    Gyamon_Surface = load_character_image(r"Images/Game Characters Organised/Gyamon/Result.png")
    Heihachi_Surface = load_character_image(r"Images/Game Characters Organised/Heihachi/Result.png")
    Ichigo_Surface = load_character_image(r"Images/Game Characters Organised/Ichigo/Result.png")
    Renji_Surface = load_character_image(r"Images/Game Characters Organised/Renji/Result.png")
    Sanji_Surface = load_character_image(r"Images/Game Characters Organised/Sanji/Result.png")
    Toshiro_Surface = load_character_image(r"Images/Game Characters Organised/Toshiro/Result.png")
    Uryu_Surface = load_character_image(r"Images/Game Characters Organised/Uryu/Result.png")
    Zoro_Surface = load_character_image(r"Images/Game Characters Organised/Zoro/Result.png")

    # Dictionary for Class Parameters
    CHARACTER_DATA = {
        "Asuka": [Asuka_DATA, Asuka_Surface, Asuka_ANIMATION_STEPS, "Asuka", Asuka],
        "Daichi": [Daichi_DATA, Daichi_Surface, Daichi_ANIMATION_STEPS, "Daichi", Daichi],
        "Gyamon": [Gyamon_DATA, Gyamon_Surface, Gyamon_ANIMATION_STEPS, "Gyamon", Gyamon],
        "Heihachi": [Heihachi_DATA, Heihachi_Surface, Heihachi_ANIMATION_STEPS, "Heihachi", Heihachi],
        "Ichigo": [Ichigo_DATA, Ichigo_Surface, Ichigo_ANIMATION_STEPS, "Ichigo", Ichigo],
        "Renji": [Renji_DATA, Renji_Surface, Renji_ANIMATION_STEPS, "Renji", Renji],
        "Sanji": [Sanji_DATA, Sanji_Surface, Sanji_ANIMATION_STEPS, "Sanji", Sanji],
        "Toshiro": [Toshiro_DATA, Toshiro_Surface, Toshiro_ANIMATION_STEPS, "Toshiro", Toshiro],
        "Uryu": [Uryu_DATA, Uryu_Surface, Uryu_ANIMATION_STEPS, "Uryu", Uryu],
        "Zoro": [Zoro_DATA, Zoro_Surface, Zoro_ANIMATION_STEPS, "Zoro", Zoro]}

    return CHARACTER_DATA