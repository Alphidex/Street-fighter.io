import pygame
import sys
import os

from characters import *

pygame.init()

# GAME WINDOW
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Street-fighter.io")

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

# Define the cooldown before the game starts
start_cooldown = 0
update_timer = pygame.time.get_ticks()
intro_font = pygame.font.Font("freesansbold.ttf", 64)

# LOAD BACKGROUND IMAGES
game_bg = pygame.image.load(r"Images/Background Images/background_image.jpg").convert_alpha()
game_bg = pygame.transform.scale(game_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

character_choice_bg = pygame.image.load(r"Images/Background Images/character_choice_background.jpg").convert_alpha()
character_choice_bg = pygame.transform.scale(character_choice_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

start_menu_bg = pygame.image.load("Images/Background Images/pixel art game menu.jpg").convert_alpha()
start_menu_bg = pygame.transform.scale(start_menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

character_selection_spritesheet = pygame.image.load("Images/Background Images/character_selection_spritesheet.png")\
    .convert_alpha()
character_selection_list = []
for x in range(10):
    temp_img = character_selection_spritesheet.subsurface(x * 160, 0, 160, 160)
    scaled_img = pygame.transform.scale(temp_img, (320, 320))
    character_selection_list.append(scaled_img)

# Dealing with the GAME COUNTDOWN
game_countdown = 3
game_timer = pygame.time.get_ticks()
game_countdown_font = pygame.font.Font("freesansbold.ttf", 60)

################################## SpreadSheet Annotations ###############################

# This is where I will be working with SQL databases to load the info in, for now it's just going to be code
""" Asuka """
Asuka_SCALE = 2.5
Asuka_OFFSET = [47, 49]
Asuka_DATA = [160, 160, Asuka_SCALE, Asuka_OFFSET]
asuka = pygame.image.load(r"Images/Game Characters Organised/Asuka/Result.png").convert_alpha()
Asuka_ANIMATION_STEPS = [17, 13, 11, 8, 8, 8, 8, 7, 7, 6, 6, 5, 5, 4, 3, 2]

""" Daichi """
Daichi_SCALE = 2.5
Daichi_OFFSET = [60, 48]
Daichi_DATA = [160, 160, Daichi_SCALE, Daichi_OFFSET]
daichi = pygame.image.load(r"Images/Game Characters Organised/Daichi/Result.png").convert_alpha()
Daichi_ANIMATION_STEPS = [14, 14, 13, 9, 8, 8, 7, 6, 6, 6, 5, 4, 4, 3, 3, 2, 2]


""" Gyamon """
Gyamon_SCALE = 2.5
Gyamon_OFFSET = [60, 32]
Gyamon_DATA = [160, 160, Gyamon_SCALE, Gyamon_OFFSET]
gyamon = pygame.image.load(r"Images/Game Characters Organised/Gyamon/Result.png").convert_alpha()
Gyamon_ANIMATION_STEPS = [27, 24, 12, 10, 10, 8, 8, 8, 7, 6, 6, 6, 6, 6, 6, 2, 2]
# Note: First animation is 300x300 dimensions

""" Heihachi """
Heihachi_SCALE = 2.5
Heihachi_OFFSET = [53, 50]
Heihachi_DATA = [160, 160, Heihachi_SCALE, Heihachi_OFFSET]
heihachi = pygame.image.load(r"Images/Game Characters Organised/Heihachi/Result.png").convert_alpha()
Heihachi_ANIMATION_STEPS = [19, 7, 18, 16, 16, 15, 13, 12, 9, 8, 8, 8, 8, 6, 5, 4, 4, 3, 3, 2]

""" Ichigo """
Ichigo_SCALE = 2.5
Ichigo_OFFSET = [56, 50]
Ichigo_DATA = [160, 160, Ichigo_SCALE, Ichigo_OFFSET]
ichigo = pygame.image.load(r"Images/Game Characters Organised/Ichigo/Result.png").convert_alpha()
Ichigo_ANIMATION_STEPS = [15, 13, 13, 12, 12, 12, 11, 9, 9, 8, 7, 7, 7, 7, 5, 5, 5, 4, 4, 3, 2]

""" Renji """
Renji_SCALE = 2.5
Renji_OFFSET = [58, 50]
Renji_DATA = [160, 160, Renji_SCALE, Renji_OFFSET]
renji = pygame.image.load(r"Images/Game Characters Organised/Renji/Result.png").convert_alpha()
Renji_ANIMATION_STEPS = [12, 11, 18, 19, 10, 10, 12, 11, 11, 10, 10, 9, 8, 8, 7, 7, 6, 6, 5, 4, 4, 4, 3, 1]  # Len = 24

""" Sanji """
Sanji_SCALE = 2.5
Sanji_OFFSET = [51, 50]
Sanji_DATA = [160, 160, Sanji_SCALE, Sanji_OFFSET]
sanji = pygame.image.load(r"Images/Game Characters Organised/Sanji/Result.png").convert_alpha()
Sanji_ANIMATION_STEPS = [44, 26, 18, 17, 15, 14, 12, 12, 8, 8, 8, 7, 7, 7, 7, 6, 5, 4, 3, 3, 3, 2]

""" Toshiro """
Toshiro_SCALE = 2.5
Toshiro_OFFSET = [58, 50]
Toshiro_DATA = [160, 160, Toshiro_SCALE, Toshiro_OFFSET]
toshiro = pygame.image.load(r"Images/Game Characters Organised/Toshiro/Result.png").convert_alpha()
Toshiro_ANIMATION_STEPS = [21, 15, 11, 11, 10, 10, 10, 8, 8, 8, 8, 8, 7, 6, 6, 6, 6, 6, 5, 4, 4, 4, 4, 4, 4, 4, 3, 3, 1]

""" Uryu """
Uryu_SCALE = 2.5
Uryu_OFFSET = [52, 50]
Uryu_DATA = [160, 160, Uryu_SCALE, Uryu_OFFSET]
uryu = pygame.image.load(r"Images/Game Characters Organised/Uryu/Result.png").convert_alpha()
Uryu_ANIMATION_STEPS = [7, 10, 10, 8, 8, 8, 8, 8, 7, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 4, 4, 4, 4, 4, 4, 4, 3, 3]


""" Zoro """
Zoro_SCALE = 2.65
Zoro_OFFSET = [53, 38]
Zoro_DATA = [160, 160, Zoro_SCALE, Zoro_OFFSET]
special_attack_list = [14]
zoro = pygame.image.load(r"Images/Game Characters Organised/Zoro/Result.png").convert_alpha()
Zoro_ANIMATION_STEPS = [16, 15, 15, 15, 14, 14, 11, 10, 10, 9, 9, 8, 8, 8, 7, 6, 6, 6, 6, 5, 4, 3, 2]


class Deploy_Fighter:
    def __init__(self, data, character, player):
        self.data = data
        self.character = character
        self.player = player

    def _draw(self):
        if self.character == "Asuka":
            self.data.draw(screen)
        if self.character == "Daichi":
            self.data.draw(screen)
        if self.character == "Gyamon":
            self.data.draw(screen)
        if self.character == "Heihachi":
            self.data.draw(screen)
        if self.character == "Ichigo":
            self.data.draw(screen)
        if self.character == "Renji":
            self.data.draw(screen)
        if self.character == "Sanji":
            self.data.draw(screen)
        if self.character == "Toshiro":
            self.data.draw(screen)
        if self.character == "Uryu":
            self.data.draw(screen)
        if self.character == "Zoro":
            self.data.draw(screen)

    def _move(self):
        if self.player == 1:
            self.data.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, island_rect_bg_0, island_rect_bg_1,
                           clock_tick)
        else:
            self.data.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, island_rect_bg_0, island_rect_bg_1,
                           clock_tick)

    def _update(self):
        if self.player == 1:
            self.data.update(fighter_2, screen)
        else:
            self.data.update(fighter_1, screen)


############################################################################################
# Variables
playing = False
choosing_characters = False

# Functions
def draw_healthbar(health, x, y):
    ratio = health / 100
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    pygame.draw.rect(screen, RED, (x, y, 400, 40))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 40))


def draw_bg(image):
    screen.blit(image, (0, 0))


def draw_text(font, sentence, text_col, x, y):
    text = font.render(sentence, True, text_col)
    screen.blit(text, (x, y))


def draw_rectangles(x, y, width, height):
    rect = pygame.Rect(x, y, width, height)
    return rect


class Select_Characters:
    def __init__(self):
        self.playing = False
        self.mouse_holding = False
        self.characters_selected = 0
        self.character_database = ["Asuka", "Daichi", "Gyamon", "Heihachi", "Ichigo", "Renji", "Sanji", "Toshiro", "Uryu",
                                   "Zoro"]
        self.fighter_1 = None
        self.fighter_2 = None
        self.instance_1 = None
        self.instance_2 = None
        self.selected_rectangles = []
        self.starting_selections_time_delay = pygame.time.get_ticks()
        self.ending_selections_time_delay = None

    def draw_character_images(self, x, y, width, height, img_list):
        # Colours
        unselected_color = (175, 175, 175)
        player_1_selected_color = (0, 0, 255)
        player_2_selected_color = (255, 0, 0)
        rect_list = []
        for g in range(1, 3):
            for f in range(1, 6):
                rect = pygame.Rect(x * f, y * g, width, height)
                rect_list.append(rect)

        for h in range(10):
            if self.characters_selected == 0:
                pygame.draw.rect(screen, unselected_color, rect_list[h])
            elif self.characters_selected == 1:
                if rect_list[h] == self.selected_rectangles[0]:
                    pygame.draw.rect(screen, player_1_selected_color, rect_list[h])
                else:
                    pygame.draw.rect(screen, unselected_color, rect_list[h])
            else:
                if rect_list[h] == self.selected_rectangles[0]:
                    pygame.draw.rect(screen, player_1_selected_color, rect_list[h])
                elif rect_list[h] == self.selected_rectangles[1]:
                    pygame.draw.rect(screen, player_2_selected_color, rect_list[h])
                else:
                    pygame.draw.rect(screen, unselected_color, rect_list[h])

            pygame.draw.rect(screen, (0, 0, 0), rect_list[h], 4)

            # To offset Gyamon 65 pixels to the left and 80 pixels up
            if h != 2:
                screen.blit(img_list[h], (rect_list[h].x - 60, rect_list[h].y - 65))
            else:
                screen.blit(img_list[h], (rect_list[h].x - 80, rect_list[h].y - 65))

        # To allow a delay between pressing start and choosing a character - so that you don't
        # accidentally hold the button and selected a character
        if pygame.time.get_ticks() - self.starting_selections_time_delay > 500:
            if self.characters_selected < 2:
                self.check_if_characters_selected(rect_list)

    def check_if_characters_selected(self, rect_list):
        if not self.mouse_holding:
            if mouse_press[0]:
                for rect in rect_list:
                    if (rect.x <= mouse_pos[0] <= rect.x + 160) \
                            and (rect.y <= mouse_pos[1] <= rect.y + 160):
                        self.check_which_character_is_selected(rect_list, rect)
                        self.characters_selected += 1
                        self.mouse_holding = True
        elif not mouse_press[0]:
            self.mouse_holding = False

    def check_which_character_is_selected(self, rect_list, rect):
        index = rect_list.index(rect)
        if self.characters_selected == 0:
            if self.character_database[index] == "Asuka":
                self.fighter_1 = Asuka(1, 360, 240, False, Asuka_DATA, asuka, Asuka_ANIMATION_STEPS, "Asuka")
                self.instance_1 = Deploy_Fighter(self.fighter_1, "Asuka", 1)
            elif self.character_database[index] == "Daichi":
                self.fighter_1 = Daichi(1, 360, 240, False, Daichi_DATA, daichi, Daichi_ANIMATION_STEPS, "Daichi")
                self.instance_1 = Deploy_Fighter(self.fighter_1, "Daichi", 1)
            elif self.character_database[index] == "Gyamon":
                self.fighter_1 = Gyamon(1, 360, 240, False, Gyamon_DATA, gyamon, Gyamon_ANIMATION_STEPS, "Gyamon")
                self.instance_1 = Deploy_Fighter(self.fighter_1, "Gyamon", 1)
            elif self.character_database[index] == "Heihachi":
                self.fighter_1 = Heihachi(1, 360, 240, False, Heihachi_DATA, heihachi, Heihachi_ANIMATION_STEPS, "Heihachi")
                self.instance_1 = Deploy_Fighter(self.fighter_1, "Heihachi", 1)
            elif self.character_database[index] == "Ichigo":
                self.fighter_1 = Ichigo(1, 360, 240, False, Ichigo_DATA, ichigo, Ichigo_ANIMATION_STEPS, "Ichigo")
                self.instance_1 = Deploy_Fighter(self.fighter_1, "Ichigo", 1)
            elif self.character_database[index] == "Renji":
                self.fighter_1 = Renji(1, 360, 240, False, Renji_DATA, renji, Renji_ANIMATION_STEPS, "Renji")
                self.instance_1 = Deploy_Fighter(self.fighter_1, "Renji", 1)
            elif self.character_database[index] == "Sanji":
                self.fighter_1 = Sanji(1, 360, 240, False, Sanji_DATA, sanji, Sanji_ANIMATION_STEPS, "Sanji")
                self.instance_1 = Deploy_Fighter(self.fighter_1, "Sanji", 1)
            elif self.character_database[index] == "Toshiro":
                self.fighter_1 = Toshiro(1, 360, 240, False, Toshiro_DATA, toshiro, Toshiro_ANIMATION_STEPS, "Toshiro")
                self.instance_1 = Deploy_Fighter(self.fighter_1, "Toshiro", 1)
            elif self.character_database[index] == "Uryu":
                self.fighter_1 = Uryu(1, 360, 240, False, Uryu_DATA, uryu, Uryu_ANIMATION_STEPS, "Uryu")
                self.instance_1 = Deploy_Fighter(self.fighter_1, "Uryu", 1)
            else:
                self.fighter_1 = Zoro(1, 360, 240, False, Zoro_DATA, zoro, Zoro_ANIMATION_STEPS, "Zoro")
                self.instance_1 = Deploy_Fighter(self.fighter_1, "Zoro", 1)

        if self.characters_selected == 1:
            if self.character_database[index] == "Asuka":
                self.fighter_2 = Asuka(2, 920, 240, True, Asuka_DATA, asuka, Asuka_ANIMATION_STEPS, "Asuka")
                self.instance_2 = Deploy_Fighter(self.fighter_2, "Asuka", 2)
            elif self.character_database[index] == "Daichi":
                self.fighter_2 = Daichi(2, 920, 240, True, Daichi_DATA, daichi, Daichi_ANIMATION_STEPS, "Daichi")
                self.instance_2 = Deploy_Fighter(self.fighter_2, "Daichi", 2)
            elif self.character_database[index] == "Gyamon":
                self.fighter_2 = Gyamon(2, 920, 240, True, Gyamon_DATA, gyamon, Gyamon_ANIMATION_STEPS, "Gyamon")
                self.instance_2 = Deploy_Fighter(self.fighter_2, "Gyamon", 2)
            elif self.character_database[index] == "Heihachi":
                self.fighter_2 = Heihachi(2, 920, 240, True, Heihachi_DATA, heihachi, Heihachi_ANIMATION_STEPS, "Heihachi")
                self.instance_2 = Deploy_Fighter(self.fighter_2, "Heihachi", 2)
            elif self.character_database[index] == "Ichigo":
                self.fighter_2 = Ichigo(2, 920, 240, True, Ichigo_DATA, ichigo, Ichigo_ANIMATION_STEPS, "Ichigo")
                self.instance_2 = Deploy_Fighter(self.fighter_2, "Ichigo", 2)
            elif self.character_database[index] == "Renji":
                self.fighter_2 = Renji(2, 920, 240, True, Renji_DATA, renji, Renji_ANIMATION_STEPS, "Renji")
                self.instance_2 = Deploy_Fighter(self.fighter_2, "Renji", 2)
            elif self.character_database[index] == "Sanji":
                self.fighter_2 = Sanji(2, 920, 240, True, Sanji_DATA, sanji, Sanji_ANIMATION_STEPS, "Sanji")
                self.instance_2 = Deploy_Fighter(self.fighter_2, "Sanji", 2)
            elif self.character_database[index] == "Toshiro":
                self.fighter_2 = Toshiro(2, 920, 240, True, Toshiro_DATA, toshiro, Toshiro_ANIMATION_STEPS, "Toshiro")
                self.instance_2 = Deploy_Fighter(self.fighter_2, "Toshiro", 2)
            elif self.character_database[index] == "Uryu":
                self.fighter_2 = Uryu(2, 920, 240, True, Uryu_DATA, uryu, Uryu_ANIMATION_STEPS, "Uryu")
                self.instance_2 = Deploy_Fighter(self.fighter_2, "Uryu", 2)
            else:
                self.fighter_2 = Zoro(2, 920, 240, True, Zoro_DATA, zoro, Zoro_ANIMATION_STEPS, "Zoro")
                self.instance_2 = Deploy_Fighter(self.fighter_2, "Zoro", 2)

            self.ending_selections_time_delay = pygame.time.get_ticks()

        # Used later to change the color of a rectangle
        self.selected_rectangles.append(rect)

    def get_fighters_and_instances(self):
        # Check if the countdown is over
        self.selections_complete()
        # Return the data for further processes
        if self.playing and self.fighter_1 != None and self.fighter_2 != None and self.instance_1 != None and self.instance_2 != None:
            return self.playing, self.fighter_1, self.fighter_2, self.instance_1, self.instance_2

    def selections_complete(self):
        # Allows a delay after choosing both characters so that the second rectangle is also coloured;
        # (basically the game is not started immediately)
        if pygame.time.get_ticks() - self.ending_selections_time_delay > 1500:
            self.playing = True


############################################ RUNNING THE GAME ##################################################

running = True

while running:
    # Refresh at 60 FPS
    clock_tick = clock.tick(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # I know it's wrong, but I can't use the jump function in characters.py as it causes input lag and doesn't
        # record the events properly, I would try to find a way through pygame.key.get_pressed()

        if playing and event.type == pygame.KEYDOWN:
            # Jumping
            # Player 1
            if event.key == pygame.K_k:
                if fighter_1.jump[1] == False:
                    if fighter_1.jump[0] == False:
                        fighter_1.jump[0] = True
                    else:
                        fighter_1.jump[1] = True
                    fighter_1.vel_y = -30
            # Player 2
            if event.key == pygame.K_n:
                if fighter_2.jump[1] == False:
                    if fighter_2.jump[0] == False:
                        fighter_2.jump[0] = True
                    else:
                        fighter_2.jump[1] = True
                    fighter_2.vel_y = -30

    # Used for the game Menu and other stuff
    mouse_press = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    if playing:
        # GAME COUNTDOWN
        # Once the countdown has been reached the game freezes (NEED TO FIX) - Ending the ROUND
        if pygame.time.get_ticks() - game_timer < game_countdown * 1000 * 60:

            # Draw images
            draw_bg(game_bg)

            # Draw the rectangles for the islands
            island_rect_bg_0 = draw_rectangles(605, 372, 275, 30)
            pygame.draw.rect(screen, (195, 60, 59), island_rect_bg_0, 2)

            island_rect_bg_1 = draw_rectangles(933, 250, 275, 30)
            pygame.draw.rect(screen, (195, 60, 59), island_rect_bg_1, 2)

            # Draw health-bars
            draw_healthbar(fighter_1.health, 150, 20)
            draw_healthbar(fighter_2.health, 790, 20)

            # Draw fighters
            instance_1._draw()
            instance_2._draw()

            # Literally does nothing for now as im testing the game
            if start_cooldown <= 0:
                # Move fighters
                instance_1._move()
                instance_2._move()

            else:
                if (pygame.time.get_ticks() - update_timer) >= 1000:
                    update_timer = pygame.time.get_ticks()
                    start_cooldown -= 1
                draw_text(intro_font, f"{start_cooldown + 1}", (255, 0, 0), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3.5)

            # Update the character animation
            instance_1._update()
            instance_2._update()

            # Converts the time to seconds
            temp_countdown = (game_countdown * 1000 * 60 - (pygame.time.get_ticks() - game_timer)) / 1000
            # Converts the time to minutes : seconds format
            # The : .0f converts the decimals to whole numbers
            temp_countdown = f"0{temp_countdown // 60 : .0f} : {temp_countdown % 60 : .0f}"
            # Draw the countdown
            draw_text(game_countdown_font, temp_countdown, (255, 0, 0), 560, 12)


    elif choosing_characters:
        # Setup
        draw_bg(character_choice_bg)
        init_chr_selection_setup.draw_character_images(190, 250, 160, 160, character_selection_list)
        try:
            playing, fighter_1, fighter_2, instance_1, instance_2 = init_chr_selection_setup.get_fighters_and_instances()
            choosing_characters = False
        except:
            pass

    else:
        draw_bg(start_menu_bg)
        rect_0 = draw_rectangles(390, 200, 500, 80)
        rect_1 = draw_rectangles(525, 295, 210, 50)
        rect_2 = draw_rectangles(510, 345, 245, 55)
        rect_3 = draw_rectangles(580, 400, 120, 43)

        pygame.draw.rect(screen, (190, 90, 180), rect_0, 5)
        pygame.draw.rect(screen, (255, 0, 0), rect_1, 5)
        pygame.draw.rect(screen, (0, 74, 83), rect_2, 5)
        pygame.draw.rect(screen, (75, 15, 19), rect_3, 5)

        # If you press play
        if 390 <= mouse_pos[0] <= 890 and 200 <= mouse_pos[1] <= 280:
            if mouse_press[0] == True:
                choosing_characters = True
                init_chr_selection_setup = Select_Characters()
        # If you press
        if 580 <= mouse_pos[0] <= 700 and 400 <= mouse_pos[1] <= 443:
            if mouse_press[0] == True:
                running = False

        # Updates continuously until u press play
        game_timer = pygame.time.get_ticks()

    # Update the screen
    pygame.display.update()

# Get out of pygame
pygame.quit()
