import pygame
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
"""
1. Draw a Start box
2. Overhaul the colors
"""

class Select_Characters:
    def __init__(self, character_data, fighter_positions):
        # Display
        self.screen = pygame.display.get_surface()
        self.background_image = pygame.image.load(
            r"Images/Background Images/character_choice_background.jpg").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image,
                                                      (self.screen.get_width(), self.screen.get_height()))
        self.start_selected = False

        # Characters
        self.character_data = character_data
        self.selected_rect = []
        self.class_dictionary = self.get_character_class_by_index()
        self.character_images = self.get_img_list()
        self.character_rectangles = self.get_img_rects()
        self.characters_selected = 0
        self.click_held = False
        self.fighter_1 = None
        self.fighter_2 = None
        self.fighters_positions = fighter_positions

    def run(self):
        self.draw_character_images_background()
        self.check_if_character_selected()

    def get_img_rects(self):
        rect_list = []
        for character in self.character_images:
            rect = character.get_rect()
            rect_list.append(rect)
        return rect_list

    def get_img_list(self):
        characters_spritesheet = pygame.image.load(r"Images/Background Images/character_selection_spritesheet.png").\
            convert_alpha()
        characters_image_list = []
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

    def generate_start_rectangle(self):
        font = pygame.font.Font(None, 50)
        surf = font.render("Start", True, "orange")
        rect = surf.get_rect(topleft=(600, 100))
        rect.width, rect.height = rect.width + 20, rect.height + 14
        pos = pygame.math.Vector2(rect.topleft)
        offset = pygame.math.Vector2(10, 7)
        offset_pos = pos + offset
        pygame.draw.rect(self.screen, 'gray', rect)
        self.screen.blit(surf, offset_pos)

        return rect

    def chr_rect_effects(self):
        player1_color = "#1788CA"
        player2_color = "#ED1C5E"
        hover_color = "#CFCBD3"
        normal_color = "#4A4F5B"
        edge_color = "gray"

        mouse_pos = pygame.mouse.get_pos()

        # Hover Color
        for rect in self.character_rectangles:
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, hover_color, rect)
            else:
                pygame.draw.rect(self.screen, normal_color, rect)
            pygame.draw.rect(self.screen, edge_color, rect, 3)

        # Selected Color
        if len(self.selected_rect) >= 1:
            temp_rect = self.selected_rect[0]
            pygame.draw.lines(self.screen, player1_color, True,
                              [temp_rect.bottomleft, temp_rect.topleft, temp_rect.topright], 5)
        if len(self.selected_rect) > 1:
            temp_rect = self.selected_rect[1]
            pygame.draw.lines(self.screen, player2_color, True,
                              [temp_rect.bottomleft, temp_rect.topright, temp_rect.bottomright], 5)

    def draw_character_images_background(self):

        draw_bg(self.screen, self.background_image)
        start_rect = self.generate_start_rectangle()

        character_position = []
        for y in range(2):
            for x in range(5):
                x_pos = 190 * x
                y_pos = 250 * y
                pos = (x_pos + 165, y_pos + 250)
                character_position.append(pos)

        # Draw Rectangles + Effects
        self.chr_rect_effects()

        for index in range(10):
            # Get Image Rect
            rect = self.character_images[index].get_rect(topleft = character_position[index])
            rect.width, rect.height = 160, 160
            # Draw Images
            offset = pygame.math.Vector2(rect.width//2 - 55, rect.height//2 - 50)
            pos = pygame.math.Vector2(character_position[index])
            offset_pos = pos - offset
            self.screen.blit(self.character_images[index], offset_pos)
            self.character_rectangles[index] = rect

        # Check if start_selected
        self.start_selected = self.check_if_start_rect_is_pressed(start_rect)

    def check_if_start_rect_is_pressed(self, rect):
        status = False
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        if rect.collidepoint(mouse_pos):
            if mouse_press[0]:
                status = True
        return status

    def check_if_character_selected(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()

        for rect in self.character_rectangles:
            if rect.collidepoint(mouse_pos):
                if mouse_press[0] and not self.click_held:
                    index = self.character_rectangles.index(rect)
                    if self.characters_selected == 0:
                        self.characters_selected = 1
                        self.click_held = True
                        self.fighter_1 = self.class_dictionary[index][0]
                        for character in self.character_data.keys():
                            if character == self.class_dictionary[index][1]:
                                self.selected_rect.append(rect)
                                self.fighter_1 = self.fighter_1(1, self.fighters_positions[0][0],
                                                                self.fighters_positions[0][1],
                                                                False, self.character_data[character][0],
                                                                self.character_data[character][1],
                                                                self.character_data[character][2],
                                                                self.character_data[character][3])
                    else:
                        self.characters_selected = 2
                        self.click_held = True
                        self.fighter_2 = self.class_dictionary[index][0]
                        for character in self.character_data.keys():
                            if character == self.class_dictionary[index][1]:
                                self.selected_rect.append(rect)
                                self.fighter_2 = self.fighter_2(2, self.fighters_positions[1][0],
                                                                self.fighters_positions[1][1],
                                                                True, self.character_data[character][0],
                                                                self.character_data[character][1],
                                                                self.character_data[character][2],
                                                                self.character_data[character][3])

        if not mouse_press[0]:
            self.click_held = False

    def selection_complete(self):
        if self.characters_selected == 2 and self.start_selected:
            self.fighter_1.set_opponent(self.fighter_2)
            self.fighter_2.set_opponent(self.fighter_1)
            return True, self.fighter_1, self.fighter_2
        else:
            return False, None, None
