import pygame
from character_data import *
from characters import Fighter
from GUI import *
from character_selection import *
from debug import debug

class Game:
    def __init__(self):
        # Key Game Variables
        self.exit_game = False

        # Display
        self.screen = pygame.display.get_surface()
        self.SCREEN_WIDTH = self.screen.get_width()
        self.SCREEN_HEIGHT = self.screen.get_height()

        # Backgrounds + Icons
        self.game_bg = load_image("Images/Background Images/background_image.jpg")
        self.game_bg = pygame.transform.scale(self.game_bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.start_menu_bg = load_image("Images/Background Images/pixel art game menu.jpg")
        self.start_menu_bg = pygame.transform.scale(self.start_menu_bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Game States
        # Menu
        self.start_selected = False

        # Options
        self.options_entered = False
        self.resolution_entered = False
        self.volume_entered = False
        self.key_binds_entered = False

        # Arena
        self.game_state = Game_States()
        self.fight_countdown_complete = False
        self.round_countdown_complete = False

        # Characters
        self.CHARACTER_DATA = self.get_CHARACTER_DATA()

        # Character Selection
        self.fighters_selection = Select_Characters(self.CHARACTER_DATA)
        self.fighters_selection_complete = False
        self.fighter_1 = None
        self.fighter_2 = None

    def get_CHARACTER_DATA(self):
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

    def run(self):
        # Game Options
        if self.fighters_selection_complete:
            self.arena()
            
        elif not self.start_selected:
            if self.options_entered:
                self.options()
            else:
                self.start_menu()
        else:
            if not self.fighters_selection_complete:
                self.fighters_selection.run()
                self.fighters_selection_complete, self.fighter_1, self.fighter_2 = self.fighters_selection.selection_complete()

    def start_menu(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        text_list = ["Start", "Options", "Exit", "Game Menu"]
        font = pygame.font.Font("./Fonts/retro.ttf", 80)
        text_surface_list = []
        rect_list = []
        pos_list = [(120, 200), (120, 300), (120, 400), (500, 20)]

        for text in text_list:
            text_surface = font.render(text, False, "#db4307")
            text_surface_list.append(text_surface)
            rect = text_surface.get_rect(topleft=pos_list[len(text_surface_list)-1])
            rect = rect.inflate(16, 3)
            rect_list.append(rect)

        draw_bg(self.screen, self.start_menu_bg)

        # Draw the Rectangles
        for index, rect in enumerate(rect_list):
            if index != 3:
                pygame.draw.rect(self.screen, (190, 25, 23), rect, 4)
            self.screen.blit(text_surface_list[index], rect.topleft + pygame.math.Vector2(8, 0))

            if rect.collidepoint(mouse_pos):
                # Change Rectangle Color
                pygame.draw.rect(self.screen, "white", rect, 4)

                # Make Noise

                # Check for clicks
                if mouse_press[0]:
                    if index == 0:
                        self.start_selected = True
                    if index == 1:
                        self.options_entered = True
                    if index == 2:
                        self.exit_game = True

    def options(self):
        self.game_state.options()
                
    def arena(self):
        draw_bg(self.screen, self.game_bg)

        if self.fight_countdown_complete:
            # Character Methods
            self.fighter_1.run(self.fighter_2)
            self.fighter_2.run(self.fighter_1)
            self.round_countdown_complete = self.game_state.round_countdown()

        else:
            self.fight_countdown_complete = self.game_state.fight_countdown()
