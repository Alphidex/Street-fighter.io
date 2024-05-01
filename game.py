import pygame
from character_data import *
from character_selection import *
from level_design import Level_Design
from Sounds import Sounds
from support import *
from options import Options
import random
from debug import debug

class Game:
    def __init__(self):
        # Display
        self.screen = pygame.display.get_surface()  # Screen Surface

        # Menu
        self.start_selected = False  # Check if the start button is pressed
        self.gameMode = [False, None]  # PVE and PVP fade in once Start button is pressed, and this variable
        # is responsible for checking which one is pressed

        # Key Game Variables
        self.exit_game = False  # If the Exit button is pressed in the Main menu
        self.reset = False  # Reset the game once all levels are complete

        # Groups
        # Instantiated a few groups (code is in the support file), I am using a dictionary as it provides O(1)
        # time complexity, and I'm accessing the groups constantly throughout the game.
        self.groups = {
            "Objs": Objs(),
            "TextButtons": TextButtons(),
            "FadeInBts": pygame.sprite.Group()
        }

        # Start Menu BG
        self.start_menu_bg = pygame.transform.scale(load_image("Images/Background Images/pixel art game menu.jpg"),
                                          list(self.screen.get_size()))

        # Options
        self.options_entered = False
        self.resolution_entered = False
        self.volume_entered = False
        self.key_binds_entered = False
        self.pause = False

        # Map Selection
        self.map_management = Map_Management(self.groups)  # Initialize the Map_Management class
        self.fighters_pos = None  # The positions will be returned from the Map_management class as each map has
        # different player positions
        self.options = Options(self.groups)  # Initializing the Options class

        # Level
        self.level = None

        # Characters
        self.CHARACTER_DATA = get_character_data()

        # Character Selection
        self.fighters_selection = None  # I will initialize the fighter selection Class later on in the program as
        # currently I don't have the necessary parameters
        self.fighters_selection_complete = False  # Check if the selection for fighters is complete
        self.fighter_1 = None
        self.fighter_2 = None

        # Sounds
        self.sound = Sounds("background_music")

        # Events
        self.events = None

        # Camera Class
        self.camera = None

    def run(self, events):
        # Play Sounds
        self.sound.update(events)
        self.events = events

        # Selection Statements
        if not self.gameMode[0]:
            # Options
            if self.options_entered:
                self.options_entered = self.options.options(events, self.options_entered)

                # Destroy all the sprites once you quit options
                if not self.options_entered:
                    for sprite in self.groups["Objs"].sprites():
                        sprite.kill()
            # Main Menu
            else:
                self.displayTitleScreen(events)

        # Map Selection
        elif not self.map_management.map_selection_complete:
            self.fighters_pos = self.map_management.run(events)
            if self.map_management.map_selection_complete:
                # Initialize the fighter_selection class
                self.fighters_selection = Select_Characters(self.CHARACTER_DATA, self.fighters_pos, self.groups)

        # Fighter Selection
        elif not self.fighters_selection_complete:
            self.fighters_selection.run(events, self.gameMode[1])
            self.fighters_selection_complete, self.fighter_1, self.fighter_2 = self.fighters_selection.selection_complete()
            if self.fighters_selection_complete:
                # Initialize the level design and the camera classes
                self.level = Level_Design(self.fighter_1, self.fighter_2, self.fighters_pos, self.map_management, self.gameMode[1])
                self.camera = Camera_Management(self.map_management.game_maps)

        # Arena
        else:
            if self.fighters_selection_complete:
                self.arena()
                self.pause_menu(events)

    def displayTitleScreen(self, events):
        # Check before all sprites are created (to prevent the declaration of new sprites repeatedly)
        if len(self.groups["Objs"].sprites()) == 0:
            draw_bg(self.screen, self.start_menu_bg) # Start menu BG

            # Text data
            text_list = ["Start", "Options", "Exit", "PVP", "PVE", "Game Menu"]
            font = pygame.font.Font("./Fonts/retro.ttf", 80)
            pos_list = [(120, 200), (120, 350), (120, 500), (300, 160), (300, 240), (500, 20)]
            obj_group = self.groups["TextButtons"]  # Initialise the TextButton Class

            for x in range(5):
                # Selection statement as PVP and PVE will have the FadeInEffect
                if x < 3:
                    sprite = TextButton(text_list[x], font, pos_list[x])
                    obj_group.add(sprite)
                else:
                    sprite = FadeInButton(text_list[x], font, pos_list[x])
                    self.groups["FadeInBts"].add(sprite)
            # Adding the "Game Menu" text
            self.groups["Objs"].add(DisplayText(text_list[5], font, pos_list[5]))
            self.groups["Objs"].add(obj_group.sprites())

        else:
            # Check which button is clicked
            for sprite in self.groups["TextButtons"]:
                if sprite.clicked:
                    id = sprite.text
                    if id == "Start":
                        self.start_selected = True
                    elif id == "Options":
                        self.options_entered = True
                    else:
                        self.exit_game = True
                    # Empty the Objs group once one of the buttons is clicked
                    for x in self.groups["Objs"]:
                        x.kill()
                    break

            # PvE and PvP fade in when start is selected
            if self.start_selected:
                self.groups["Objs"].add(self.groups["FadeInBts"].sprites())
            # Check whether PvE or PvP is selected
            for sprite in self.groups["FadeInBts"].sprites():
                if sprite.clicked:
                    self.gameMode = [True, sprite.text]
                    for button in self.groups["FadeInBts"].sprites():
                        button.kill()
                    break

        # Update the Objs group
        self.groups["Objs"].update(events)

    def pause_menu(self, events):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.pause = True

        if self.pause:
            if len(self.groups["Objs"].sprites()) == 0:
                # Pause Rectangle
                pause_rect = self.screen.get_rect().copy()
                pygame.draw.rect(self.screen, "gray", pause_rect)

                # Text data
                text_list = ["Paused", "Continue", "Exit"]
                font = pygame.font.Font("./Fonts/retro.ttf", 80)
                pos_list = [(550, 100), (120, 300), (120, 450)]
                obj_group = self.groups["TextButtons"]  # Initialise the TextButton Class

                for x in range(3):
                    if x >= 1:
                        sprite = TextButton(text_list[x], font, pos_list[x])
                        obj_group.add(sprite)

                self.groups["Objs"].add(DisplayText(text_list[0], font, pos_list[0]))
                self.groups["Objs"].add(obj_group.sprites())

            else:
                # Check which button is clicked
                for sprite in self.groups["TextButtons"]:
                    if sprite.clicked:
                        id = sprite.text
                        if id == "Continue":
                            self.pause = False
                        elif id == "Exit":
                            self.reset = True
                        # Empty the Objs group once one of the buttons is clicked
                        for x in self.groups["Objs"]:
                            x.kill()
                        break

            # Update the Objs group
            self.groups["Objs"].update(events)

    def arena(self):
        if not self.pause:
            # Update the camera class with fighter's new positions
            self.camera.camera_movement(self.fighter_1, self.fighter_2, self.map_management.map_selected)
            # Update the fighter classes
            if self.level.fight_countdown_complete:
                # Character Methods
                self.fighter_1.run(self.fighter_2, self.events, self.camera, self.level.current_match)
                self.fighter_2.run(self.fighter_1, self.events, self.camera, self.level.current_match)
            # Update the level class
            self.level.run(self.fighter_1.health, self.fighter_2.health)

            # Reset the camera back to initial position after a round ends
            if self.level.round_over:
                self.camera.mapTopLeft = [[-110, -145], [-110, -140], [-110, -150], [-110, -180]]
                self.camera.boundaries = [[[[0, 550]], [[66, 293], [450, 293]], [[934, 293], [1318, 293]], [[202, 105], [1160, 105]]],
                           [[[240, 540], [1062, 540]], [[534, 130], [620, 130]], [[-5, 318], [154, 318]],
                            [[1213, 272], [1372, 272]]],
                           [[[0, 550]], [[216, 290], [588, 290]], [[791, 290], [1163, 290]], [[310, 44], [974, 54]]],
                           [[[0, 600]]]]

            # Screen Shake
            screen_shake_offset = [0, 0]
            if self.fighter_1.shake == True or self.fighter_2.shake == True:
                screen_shake_offset = [random.randint(-4, 4), random.randint(-4, 4)]
            self.screen.blit(self.screen, screen_shake_offset)

        # If game is finished
        if self.level.quit:
            self.reset = True
