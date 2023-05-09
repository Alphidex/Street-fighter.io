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

        # Backgrounds
        self.game_bg = self.load_image("Images/Background Images/background_image.jpg")
        self.game_bg = pygame.transform.scale(self.game_bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.start_menu_bg = self.load_image("Images/Background Images/pixel art game menu.jpg")
        self.start_menu_bg = pygame.transform.scale(self.start_menu_bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Game Menu
        self.start_selected = False

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

    def load_image(self, path):
        return pygame.image.load(r"{}".format(path)).convert_alpha()

    def run(self):
        # Game Options
        if self.fighters_selection_complete:
            self.arena()
        elif not self.start_selected:
            self.start_menu()
        else:
            if not self.fighters_selection_complete:
                self.fighters_selection.run()
                self.fighters_selection_complete, self.fighter_1, self.fighter_2 = self.fighters_selection.selection_complete()

    def start_menu(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()

        draw_bg(self.screen, self.start_menu_bg)

        rect_0 = create_rectangle(390, 200, 500, 80)
        rect_1 = create_rectangle(525, 295, 210, 50)
        rect_2 = create_rectangle(510, 345, 245, 55)
        rect_3 = create_rectangle(580, 400, 120, 43)

        pygame.draw.rect(self.screen, (190, 90, 180), rect_0, 5)
        pygame.draw.rect(self.screen, (255, 0, 0), rect_1, 5)
        pygame.draw.rect(self.screen, (0, 74, 83), rect_2, 5)
        pygame.draw.rect(self.screen, (75, 15, 19), rect_3, 5)

        # If you press play
        if 390 <= mouse_pos[0] <= 890 and 200 <= mouse_pos[1] <= 280:
            if mouse_press[0] == True:
                self.start_selected = True

        # If you press exit
        if 580 <= mouse_pos[0] <= 700 and 400 <= mouse_pos[1] <= 443:
            if mouse_press[0] == True:
                self.exit_game = True

        # Updates continuously until u press play
        game_timer = pygame.time.get_ticks()

    def arena(self):
        draw_bg(self.screen, self.game_bg)
        # Draw health-bars
        draw_healthbar(self.screen, self.fighter_1.health, 150, 20)
        draw_healthbar(self.screen, self.fighter_2.health, 790, 20)
        # Character Methods
        self.fighter_1.run(self.fighter_2)
        self.fighter_2.run(self.fighter_1)

        # Game Countdown
        start_countdown = 0
        update_timer = pygame.time.get_ticks()
        intro_font = pygame.font.Font("freesansbold.ttf", 64)

        # Dealing with the GAME COUNTDOWN
        round_duration_mins = 3
        game_timer = pygame.time.get_ticks()
        game_countdown_font = pygame.font.Font("freesansbold.ttf", 60)
