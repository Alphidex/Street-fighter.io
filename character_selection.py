import pygame
import random
from GUI import *
from characters import *
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

class Select_Characters:
    def __init__(self, character_data, fighter_positions, groups):
        # Display
        self.screen = pygame.display.get_surface()
        self.background_image = pygame.image.load(r"Images/Background Images/character_choice_background.jpg").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, self.screen.get_size())
        self.start_selected = False

        # Character Data
        self.character_data = character_data
        self.selected_rect = []
        self.class_dictionary = self.get_character_class_by_index()
        self.character_images = self.get_img_list()
        self.characters_selected = [0, []]
        self.click_held = False
        self.fighter_1 = None
        self.fighter_2 = None
        self.fighters_positions = fighter_positions

        # Game Mode
        self.game_mode = None

        # Group
        self.groups = groups
        self.img_group = pygame.sprite.Group()

    def run(self, events, game_mode):
        self.game_mode = game_mode
        self.draw_chr_imgs(events)
        self.get_fighter_objects()

        # If "Start" is clicked, move on to the next stage
        if self.fighter_1 is not None:
            for sprite in self.groups["Objs"].sprites():
                if sprite.clicked:
                    self.start_selected = True

    def get_img_list(self):
        characters_spritesheet = pygame.image.load(r"Images/Background Images/character_selection_spritesheet.png").\
            convert_alpha()
        characters_image_list = []
        # Looping through the spritesheet, while cropping and resizing the images
        for x in range(10):
            temp_img = characters_spritesheet.subsurface(x * 160, 0, 160, 160)
            scaled_img = pygame.transform.scale(temp_img, (240, 240))
            characters_image_list.append(scaled_img)
        return characters_image_list

    def get_character_class_by_index(self):
        dic = {
            0: [Asuka, "Asuka"],
            1: [Daichi, "Daichi"],
            2: [Gyamon, "Gyamon"],
            3: [Heihachi, "Heihachi"],
            4: [Ichigo, "Ichigo"],
            5: [Renji, "Renji"],
            6: [Sanji, "Sanji"],
            7: [Toshiro, "Toshiro"],
            8: [Uryu, "Uryu"],
            9: [Zoro, "Zoro"]
        }
        return dic

    def draw_chr_imgs(self, events):
        draw_bg(self.screen, self.background_image)

        # Checkingi f the Objs group is empty, otherwise initialise all the sprites and add them to ImgButtons
        if len(self.groups["Objs"].sprites()) == 0:
            font = pygame.font.Font(None, 40)
            self.groups["Objs"].add(TextButton("Start", font, (600, 100)))
            chr_imgs_pos = [(190 * x + 165, 250 * y + 250) for y in range(2) for x in range(5)]
            for x in range(len(chr_imgs_pos)):
                self.img_group.add(ImgButtons(self.character_images[x], chr_imgs_pos[x], x, "character selection"))
        else:
            trigger = None
            if self.characters_selected[0] >= 2:
                trigger = "stop"

            # Updating the groups
            self.img_group.update(events, trigger)
            self.groups["Objs"].update(events)

            x = []
            i = []
            # Checking is the images are clicked
            for sprite in self.img_group.sprites():
                if sprite.selected:
                    x.append(sprite.rect)
                    i.append(sprite.id)

                    # Character is selected twice
                    if sprite.selected_times == 2:
                        x.append(sprite.rect)
                        i.append(sprite.id)

            # Bug fix - this makes sure than the characters are not reversed
            if len(i) >= 2 and len(self.characters_selected[1]) != 0:
                if i[1] == self.characters_selected[1][0]:
                    i.reverse() # I is the id list
                    x.reverse() # X is the rectangle list

            self.characters_selected = [len(x), i]

            player1_color = "#1788CA"
            player2_color = "#ED1C5E"

            if self.game_mode == "PVP":  # Selection statement, as there are different effects for PvE and PvP
                # Make the first player's choice blue
                if len(x) >= 1:
                    temp_rect = x[0]
                    pygame.draw.lines(self.screen, player1_color, True,
                                      [temp_rect.bottomleft, temp_rect.topleft, temp_rect.topright], 5)
                # Draw the second player's fighter rectangle as red
                if len(x) > 1:
                    temp_rect = x[1]
                    pygame.draw.lines(self.screen, player2_color, True,
                                      [temp_rect.bottomleft, temp_rect.topright, temp_rect.bottomright], 5)
            else:
                if len(x) == 1:
                    temp_rect = x[0]
                    pygame.draw.rect(self.screen, player1_color, temp_rect, 5)

    def get_fighter_objects(self):
        if self.game_mode == "PVP":
            if self.characters_selected[0] == 2 and self.fighter_2 == None: # Checking if both characters are selected
                # the reason i'm checking if fighter_2 is None is so the code afterwards doesn't execute multiple times
                f1Class = self.class_dictionary[self.characters_selected[1][0]][0]  # Fetching the first character class
                f2Class = self.class_dictionary[self.characters_selected[1][1]][0]  # Fetching the second character class
                data1 = self.character_data[self.class_dictionary[self.characters_selected[1][0]][1]]  # Fetching the data for the first class (e.g. spritesheet, nr of moves)
                data2 = self.character_data[self.class_dictionary[self.characters_selected[1][1]][1]]  # Fetching the data for the second class

                # Instantiating both classes
                self.fighter_1 = f1Class(1, *self.fighters_positions[0],
                                                False, data1[0], data1[1], data1[2], data1[3], False)
                self.fighter_2 = f2Class(2, *self.fighters_positions[1],
                                                True, data2[0], data2[1], data2[2], data2[3], False)
        else:
            if self.characters_selected[0] == 1 and self.fighter_2 == None: # Checking if the character is selected
                random_id = random.randint(0, 9) # Getting a random id for the opponent
                # Fetching the classes for both fighters
                f1Class = self.class_dictionary[self.characters_selected[1][0]][0]
                f2Class = self.class_dictionary[random_id][0]
                # Fetching the data for both fighters
                data1 = self.character_data[self.class_dictionary[self.characters_selected[1][0]][1]]
                data2 = self.character_data[self.class_dictionary[random_id][1]]
                # Instantiating both fighter classes
                self.fighter_1 = f1Class(1, *self.fighters_positions[0],
                                                False, data1[0], data1[1], data1[2], data1[3], False)

                self.fighter_2 = f2Class(2, *self.fighters_positions[1],
                                                True, data2[0], data2[1], data2[2], data2[3], True)

    def selection_complete(self):
        # Once the selection is complete, the sprites are removed from all groups
        if self.fighter_1 is not None and self.start_selected:
            self.fighter_1.set_opponent(self.fighter_2)
            self.fighter_2.set_opponent(self.fighter_1)

            for sprite in self.groups["Objs"].sprites():
                sprite.kill()
            for sprite in self.img_group.sprites():
                sprite.kill()
            return True, self.fighter_1, self.fighter_2
        else:
            return False, None, None
