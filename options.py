import pygame
import csv
import pandas as pd
from GUI import load_image, draw_bg
from support import *

class Options:
    def __init__(self, groups):
        # Retrieving data from csv file
        with open("settings.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.volume_magnitude = float(row["volume"])

        data = pd.read_csv('keyBinds.csv')
        self.player_key_binds = data.to_dict('records')

        # Screen
        self.screen = pygame.display.get_surface()

        # Groups
        self.groups = groups

        # Options
        self.quit = False
        self.resolution_entered = False
        self.volume_entered = False
        self.key_binds_entered = False

        # Options Bg
        self.bg = load_image("Images/Background Images/options_bg.png")
        self.bg = pygame.transform.scale(self.bg, self.screen.get_size())

        self.go_back = load_image("Images/Background Images/Options Icons/go_back.png")
        self.go_back = pygame.transform.scale(self.go_back, (100, 100))

        # Volume
        self.button_held = False

        # Scroll Bar
        self.scroll_bar = None

        # Font
        self.intro_font = pygame.font.Font("./Fonts/retro.ttf", 80)

        # Key Bind Rectangles
        self.p1_key_rects = [pygame.Rect(680, 160 + 80 * i, 100, 40) for i in range(9)]

        self.p2_key_rects = [pygame.Rect(900, 160 + 80 * i, 100, 40) for i in range(9)]

        self.rect_clicked = [False, None]
        self.txt_input = None
        
        self.events = None

    def options(self, events, value):
        # Setting Up
        draw_bg(self.screen, self.bg)
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        font = pygame.font.Font("./Fonts/retro.ttf", 80)
        font2 = pygame.font.Font("./Fonts/retro.ttf", 40)
        self.events = events
        self.quit = not(value)

        # Go back icon
        self.screen.blit(self.go_back, (50, 50))
        go_back_rect = self.go_back.get_rect()

        click = False
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if go_back_rect.collidepoint(mouse_pos):
            if click:
                if not (self.resolution_entered or self.volume_entered or self.key_binds_entered):
                    self.quit = True
                else:
                    if self.resolution_entered: self.resolution_entered = False
                    if self.volume_entered: self.volume_entered = False
                    if self.key_binds_entered: self.key_binds_entered = False
                for sprite in self.groups["Objs"].sprites():
                    sprite.kill()

        # Check if any options are clicked
        if not (self.resolution_entered or self.volume_entered or self.key_binds_entered):
            if len(self.groups["Objs"].sprites()) == 0:
                text_list = ["Resolution", "Volume", "Key Binds", "Options"]
                pos_list = [(100, 200), (100, 300), (100, 400), (540, 20)]

                obj_group = self.groups["TextButtons"]

                for x in range(3):
                    sprite = TextButton(text_list[x], font, pos_list[x])
                    obj_group.add(sprite)

                self.groups["Objs"].add(DisplayText(text_list[3], font, pos_list[3]))
                self.groups["Objs"].add(obj_group.sprites())

            else:
                for sprite in self.groups["TextButtons"]:
                    if sprite.clicked:
                        id = sprite.text
                        if id == "Resolution":
                            self.resolution_entered = True
                        elif id == "Volume":
                            self.volume_entered= True
                        else:
                            self.key_binds_entered = True
                        for x in self.groups["Objs"]:
                            x.kill()
                        break

            self.groups["Objs"].update(self.events)

        self.options_volume_entered(font, mouse_pos, mouse_press, click)

        self.options_resolution_entered(font, mouse_pos, mouse_press, click)

        self.options_key_binds_entered(font2, mouse_pos, mouse_press, click)

        return not self.quit

    def options_volume_entered(self, font, mouse_pos, mouse_press, click):
        if self.volume_entered:
            # Setting Things Up
            text_list = ["Volume:", "0%", f"{float(self.volume_magnitude):.0f}%", "100%", "Volume"]
            pos_list = [(100, 200), (350, 300), (350 + (int(self.volume_magnitude) / 100 * 600), 300), (950, 300), (540, 20)]
            volume_line_pos = []
            sprites = []

            for i in range(len(text_list)):
                text_surface = font.render(text_list[i], False, "#db4307")
                rect = text_surface.get_rect(topleft=pos_list[i])
                rect = rect.inflate(16, 3)
                sprite = pygame.sprite.Sprite()
                sprite.image, sprite.rect = text_surface, rect
                sprites.append(sprite)

            def create_volume_scroll_bar():
                volume_line_pos.append(sprites[0].rect.midright + pygame.math.Vector2(60, 0))
                volume_line_pos.append(sprites[0].rect.midright + pygame.math.Vector2(660, 0))

                # Line
                pygame.draw.line(self.screen, "white", volume_line_pos[0], volume_line_pos[1], 3)

                # Little Rectangle on the left
                pygame.draw.rect(self.screen, "white",
                                 pygame.Rect(volume_line_pos[0][0] - 5, volume_line_pos[0][1] - 20, 10, 40))

                # Little Rectangle on the right
                pygame.draw.rect(self.screen, "white",
                                 pygame.Rect(volume_line_pos[1][0] - 5, volume_line_pos[1][1] - 20, 10, 40))

                # Scroll Bar
                total_length = volume_line_pos[1][0] - volume_line_pos[0][0]
                scroll_bar = pygame.Rect(volume_line_pos[0][0] + total_length * (int(self.volume_magnitude) / 100) - 5,
                                         volume_line_pos[0][1] - 20, 10, 40)

                pygame.draw.rect(self.screen, "blue", scroll_bar)

                # Updating the database
                return scroll_bar, volume_line_pos

            scroll_bar, volume_line_pos = create_volume_scroll_bar()

            # # Draw the Rectangles
            for index, sprite in enumerate(sprites):
                if not sprites[2].rect.colliderect(sprite):
                    pygame.draw.rect(self.screen, (190, 25, 23), sprite.rect, 4)
                    self.screen.blit(sprite.image, sprite.rect.topleft + pygame.math.Vector2(8, 0))
                else:
                    if sprites[2].rect.colliderect(sprites[2].rect):
                        pygame.draw.rect(self.screen, (190, 25, 23), sprites[2].rect, 4)
                        self.screen.blit(sprites[2].image, sprites[2].rect.topleft + pygame.math.Vector2(8, 0))

            # Bar Sliding Mechanic
            def mouse_scrolling():
                if mouse_press[0]:
                    self.button_held = True

                    self.volume_magnitude = (mouse_pos[0] - volume_line_pos[0][0]) / (
                            volume_line_pos[1][0] - volume_line_pos[0][0]) * 100

                    if self.volume_magnitude < 0:
                        self.volume_magnitude = 0
                    if self.volume_magnitude > 100:
                        self.volume_magnitude = 100

                    df = pd.read_csv('settings.csv')
                    df.loc[0, 'volume'] = int(self.volume_magnitude)
                    df.to_csv('settings.csv', index=False)

                else:
                    self.button_held = False

            if scroll_bar.collidepoint(mouse_pos):
                mouse_scrolling()
            else:
                if self.button_held:
                    mouse_scrolling()

    def options_resolution_entered(self, font, mouse_pos, mouse_press, click):
        if self.resolution_entered:
            text_list = ["Full-Screen:", "Resolution:", "Video", "Off", "1280x720"]
            text_surface_list = []
            rect_list = []
            pos_list = [(100, 200), (100, 300), (540, 20), (600, 200), (600, 300)]

            for text in text_list:
                text_surface = font.render(text, False, "#db4307")
                text_surface_list.append(text_surface)
                rect = text_surface.get_rect(topleft=pos_list[len(text_surface_list) - 1])
                rect = rect.inflate(16, 3)
                rect_list.append(rect)

            # Draw the Rectangles
            for index, rect in enumerate(rect_list):
                pygame.draw.rect(self.screen, [190, 25, 23], rect, 4)
                self.screen.blit(text_surface_list[index], rect.topleft + pygame.math.Vector2(8, 0))

                if rect.collidepoint(mouse_pos):
                    if index >= 3:
                        pygame.draw.rect(self.screen, "white", rect, 4)

    def options_key_binds_entered(self, font2, mouse_pos, mouse_press, click):
        if self.key_binds_entered:
            scroll_bar_boundaries = [(1065, 160), (1065, 630)]
            scroll_length = (scroll_bar_boundaries[1][1] - scroll_bar_boundaries[0][1])

            # Create Menu Rectangle
            package_rect = pygame.Rect(200, 80, 880, 560)
            pygame.draw.rect(self.screen, "#524e44", package_rect)
            pygame.draw.rect(self.screen, "#2f3540", package_rect, 4)

            # Lines Drawn
            pygame.draw.line(self.screen, "#2f3540",
                             [package_rect.x, package_rect.y + 65],
                             [package_rect.right, package_rect.y + 65], 4)
            pygame.draw.line(self.screen, "#2f3540",
                             [package_rect.x + 600, package_rect.y],
                             [package_rect.x + 600, package_rect.bottom], 4)

            # Scroll Line
            pygame.draw.line(self.screen, "#2f3540",
                             [package_rect.right - 30, package_rect.y + 65],
                             [package_rect.right - 30, package_rect.bottom], 4)

            if len(self.groups["Objs"].sprites()) == 0:
                text_list = ["Key Binds", "Player 1", "Player 2", "Movement", "UP", "DOWN", "LEFT", "RIGHT", "Jump", "Dash",
                             "Attacks", "Normal Attack", "Strong Attack", "Special Attack"]
                pos_list = [(540, 20), (600, 100), (880, 100), (250, 160), *[(440, 80 + 80 * x) for x in range(1, 7)],
                            (250, 640), *[(440, 560 + 80 * x) for x in range(1, 4)]]
                scroll_bar = pygame.Rect(package_rect.right - 26,
                                         package_rect.y + 68, 20, 20)
                self.scroll_bar = KBScrollButton(scroll_bar)
                for i in range(len(text_list)):
                    self.groups["Objs"].add(DisplayText(text_list[i], font2, pos_list[i], True, self.scroll_bar))

                p1_values = list(self.player_key_binds[0].values())
                p2_values = list(self.player_key_binds[1].values())
                for i in range(len(self.p1_key_rects)):
                    self.groups["Objs"].add(KBRect(self.p1_key_rects[i], self.scroll_bar, p1_values[i], 1, i))
                    self.groups["Objs"].add(KBRect(self.p2_key_rects[i], self.scroll_bar, p2_values[i], 2, i))

                self.groups["Objs"].add(self.scroll_bar)

            else:
                self.groups["Objs"].update(self.events)

