import pygame

################################## SpreadSheet Annotations ###############################

def load_character_image(path):
    return pygame.image.load(path).convert_alpha()

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
Ichigo_ANIMATION_STEPS = [15, 13, 13, 12, 12, 12, 11, 9, 9, 8, 7, 7, 7, 7, 5, 5, 5, 4, 4, 3, 2]

""" Renji """
Renji_SCALE = 2.5
Renji_OFFSET = [58, 50]
Renji_DATA = [160, 160, Renji_SCALE, Renji_OFFSET]
Renji_ANIMATION_STEPS = [12, 11, 18, 19, 10, 10, 12, 11, 11, 10, 10, 9, 8, 8, 7, 7, 6, 6, 5, 4, 4, 4, 3, 1]  # Len = 24

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
