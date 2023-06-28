import pygame
from os import walk
from random import choice

def load_image(path):
    return pygame.image.load(r"{}".format(path)).convert_alpha()
    
def draw_bg(screen, image):
    screen.blit(image, (0, 0))

def draw_text(screen, font, sentence, text_col, x, y):
    text = font.render(sentence, True, text_col)
    screen.blit(text, (x, y))

def create_rectangle(x, y, width, height):
    rect = pygame.Rect(x, y, width, height)
    return rect

class Display_Character_Stats:
    def __init__(self, player, health, rect, stamina):
        self.screen = pygame.display.get_surface()
        self.health = health
        self.stamina = stamina
        self.sp_count = 0
        self.player = player
        self.player_rect = rect
        self.player_image = load_image(rf"Images/Background Images/Player Stats/player_{self.player}.png")
        self.player_image = pygame.transform.scale_by(self.player_image, 0.2)

    def draw_everything(self, health, stamina, character_rect):
        self.draw_player_label(character_rect)
        self.draw_health_bar(health)
        self.draw_health_label()
        self.draw_stamina_bar(stamina)
        self.draw_sp_bar()

    def draw_player_label(self, rect):
        self.player_rect = rect
        self.screen.blit(self.player_image, self.player_rect.midbottom + pygame.math.Vector2(-60, 0))

    def draw_health_bar(self, health):
        self.health = health
        ratio = self.health / 100
        RED = (255, 0, 0)
        YELLOW = (255, 255, 0)

        if self.player == 1:
            rect = pygame.Rect(150, 20, 400, 40)
        else:
            rect = pygame.Rect(790, 20, 400, 40)

        pygame.draw.rect(self.screen, YELLOW, (rect.x, rect.y, 400 * ratio, 40))
        pygame.draw.rect(self.screen, RED, rect, 2)

    def draw_health_label(self):
        font = pygame.font.Font("./Fonts/retro.ttf", 40)
        text_surface = font.render(f"Health: {self.health}%", False, "white")
        if self.player == 1:
            pos = (270, 25)
        else:
            pos = (920, 25)
        self.screen.blit(text_surface, pos)

    def draw_stamina_bar(self, stamina):
        self.stamina = stamina
        ratio = self.stamina/100

        if self.player == 1:
            rect = pygame.Rect(230, 80, 300, 30)
        else:
            rect = pygame.Rect(800, 80, 300, 30)

        pygame.draw.rect(self.screen, "blue", (rect.x, rect.y, ratio * rect.width, rect.height))
        pygame.draw.rect(self.screen, "white", rect, 2)

    def draw_sp_bar(self):
        font = pygame.font.Font("./Fonts/retro.ttf", 40)
        text_surface = font.render(f"{self.sp_count}%", False, "red")

        if self.player == 1:
            rect = pygame.Rect(150, 670, 300, 30)
        else:
            rect = pygame.Rect(900, 670, 300, 30)

        pygame.draw.rect(self.screen, "orange", rect)
        self.screen.blit(text_surface, (rect.right + 10, rect.y - 5))

class Create_Shield:
    def __init__(self, shield_amount):
        # Change Shield Color based on health
        self.shield_amount = shield_amount
        self.current_color = pygame.Color(0, 0, 255)

    def change_shield_color(self, current_shield, pos):
        self.shield_amount = current_shield

        # Define the initial color values
        start_color = pygame.Color(0, 0, 255)  # Blue
        end_color = pygame.Color(255, 0, 0)  # Red

        if self.shield_amount < 100:
            # Calculate the interpolation factor based on elapsed time and transition duration
            interpolation_factor = self.shield_amount/100

            # Interpolate the RGB values between red and blue
            self.current_color.r = int(min((start_color.r + 255 * (1 - interpolation_factor)), 255))
            self.current_color.b = int(max((start_color.b * interpolation_factor), 0))

        # Draw Shield Circle
        pygame.draw.circle(pygame.display.get_surface(), self.current_color, pos, 70, 5)

class Game_States:
    def __init__(self):
        # Screen
        self.screen = pygame.display.get_surface()
        
        # Options
        self.options_entered = True
        self.resolution_entered = False
        self.volume_entered = False
        self.key_binds_entered = False

        # Delay
        self.check_once = False
        self.delay_timer = 0
        
        # Options Bg
        self.options_bg = load_image("Images/Background Images/options_bg.png")
        self.options_bg = pygame.transform.scale(self.options_bg, (self.screen.get_width(), self.screen.get_height()))

        self.option_go_back = load_image("Images/Background Images/Options Icons/go_back.png")
        self.option_go_back = pygame.transform.scale(self.option_go_back, (80, 80))
        self.option_go_back = pygame.transform.scale(self.option_go_back, (100, 100))

        self.option_exit = load_image("Images/Background Images/Options Icons/exit_menu.png")
        self.option_exit = pygame.transform.scale(self.option_exit, (100, 100))

        # Volume
        self.volume_magnitude = 30
        self.button_held = False

        # Options
        self.button_magnitude = 0

        # Font
        self.intro_font = pygame.font.Font("./Fonts/retro.ttf", 80)
        
    def options(self):
        # Setting Up
        draw_bg(self.screen, self.options_bg)
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        font = pygame.font.Font("./Fonts/retro.ttf", 80)
        font2 = pygame.font.Font("./Fonts/retro.ttf", 40)
        self.options_entered = True

        # Go back icon
        self.screen.blit(self.option_go_back, (50, 50))
        go_back_rect = self.option_go_back.get_rect()

        if go_back_rect.collidepoint(mouse_pos):
            if mouse_press[0]:
                if not (self.resolution_entered or self.volume_entered or self.key_binds_entered) \
                        and pygame.time.get_ticks() - self.delay_timer > 300:
                    self.options_entered = False
                    self.check_once = False
                else:
                    self.delay_timer = pygame.time.get_ticks()

                if self.resolution_entered: self.resolution_entered = False
                if self.volume_entered: self.volume_entered = False
                if self.key_binds_entered: self.key_binds_entered = False

        # Delay
        if not self.check_once and self.options_entered:
            self.check_once = True
            self.delay_timer = pygame.time.get_ticks()

        if not (self.resolution_entered or self.volume_entered or self.key_binds_entered):
            text_list = ["Resolution", "Volume", "Key Binds", "Options"]
            text_surface_list = []
            rect_list = []
            pos_list = [(100, 200), (100, 300), (100, 400), (540, 20)]

            for text in text_list:
                text_surface = font.render(text, False, "#db4307")
                text_surface_list.append(text_surface)
                rect = text_surface.get_rect(topleft=pos_list[len(text_surface_list) - 1])
                rect = rect.inflate(16, 3)
                rect_list.append(rect)

            # Draw the Rectangles
            for index, rect in enumerate(rect_list):
                if index != 3:
                    pygame.draw.rect(self.screen, (190, 25, 23), rect, 4)
                self.screen.blit(text_surface_list[index], rect.topleft + pygame.math.Vector2(8, 0))

                if rect.collidepoint(mouse_pos):
                    # Change Rect Color
                    pygame.draw.rect(self.screen, "white", rect, 4)

                    # Make Noise

                    if pygame.time.get_ticks() - self.delay_timer > 300:
                        # Check for clicks
                        if mouse_press[0]:
                            if index == 0:
                                self.resolution_entered = True
                            if index == 1:
                                self.volume_entered = True
                            if index == 2:
                                self.key_binds_entered = True

        self.options_volume_entered(font, mouse_pos, mouse_press)

        self.options_resolution_entered(font, mouse_pos, mouse_press)

        self.options_key_binds_entered(font2, mouse_pos, mouse_press)

        return self.options_entered

    def options_volume_entered(self, font, mouse_pos, mouse_press):
        if self.volume_entered:
            # Setting Things Up
            text_list = ["Volume:", "Volume", "0%", f"{self.volume_magnitude:.0f}%", "100%"]
            text_surface_list = []
            rect_list = []
            pos_list = [(100, 200), (540, 20), (350, 300), (350 + (self.volume_magnitude / 100 * 600), 300), (950, 300)]
            volume_line_pos = []

            for text in text_list:
                text_surface = font.render(text, False, "#db4307")
                text_surface_list.append(text_surface)
                rect = text_surface.get_rect(topleft=pos_list[len(text_surface_list) - 1])
                rect = rect.inflate(16, 3)
                rect_list.append(rect)

            # Draw the Rectangles
            for index, rect in enumerate(rect_list):
                pygame.draw.rect(self.screen, (190, 25, 23), rect, 4)
                self.screen.blit(text_surface_list[index], rect.topleft + pygame.math.Vector2(8, 0))

            def create_volume_scroll_bar():
                volume_line_pos.append(rect_list[0].midright + pygame.math.Vector2(60, 0))
                volume_line_pos.append(rect_list[0].midright + pygame.math.Vector2(660, 0))

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
                scroll_bar = pygame.Rect(volume_line_pos[0][0] + total_length * (self.volume_magnitude / 100) - 5,
                                         volume_line_pos[0][1] - 20, 10, 40)

                pygame.draw.rect(self.screen, "blue", scroll_bar)

                return scroll_bar, volume_line_pos

            scroll_bar, volume_line_pos = create_volume_scroll_bar()

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
                else:
                    self.button_held = False

            if scroll_bar.collidepoint(mouse_pos):
                mouse_scrolling()
            else:
                if self.button_held:
                    mouse_scrolling()

    def options_resolution_entered(self, font, mouse_pos, mouse_press):
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
                pygame.draw.rect(self.screen, (190, 25, 23), rect, 4)
                self.screen.blit(text_surface_list[index], rect.topleft + pygame.math.Vector2(8, 0))

                if rect.collidepoint(mouse_pos):
                    if index >= 3:
                        pygame.draw.rect(self.screen, "white", rect, 4)

    def options_key_binds_entered(self, font2, mouse_pos, mouse_press):
        if self.key_binds_entered:
            # General
            text_list_general = ["Key Binds", "Player 1", "Player 2"]
            pos_list_general = [(540, 20), (600, 100), (880, 100)]
            # Movement
            text_list_movement = ["Movement", "UP", "DOWN", "LEFT", "RIGHT", "Jump", "Dash"]
            text_list_movement_player1 = ["W", "S", "A", "D", "K", "L"]
            text_list_movement_player2 = ["Up", "Down", "Left", "Right", "G", "H"]
            pos_list_movement = [(250, 160)]
            for x in range(1, len(text_list_movement)):
                pos_list_movement.append((440, 80 + 80 * x))

            # Attacks
            text_list_attacks = ["Attacks", "Normal Attack", "Strong Attack", "Special Attack"]
            text_list_attacks_player1 = ["J", "U", "I"]
            text_list_attacks_player1 = ["F", "R", "T"]
            pos_list_attacks = [(250, 640)]
            for x in range(1, len(text_list_attacks)):
                pos_list_attacks.append((440, 560 + 80 * x))

            # Dictionary that houses every text element
            text_elements_dict = {}  # element : {"position":x, "surface": y, "rect:z}

            for index, text in enumerate(text_list_movement):
                text_elements_dict[text] = {"pos": pos_list_movement[index]}

            for index, text in enumerate(text_list_general):
                text_elements_dict[text] = {"pos": pos_list_general[index]}

            for index, text in enumerate(text_list_attacks):
                text_elements_dict[text] = {"pos": pos_list_attacks[index]}


            # Scroll Bar
            scroll_bar_boundaries = [(1065, 160), (1065, 630)]
            scroll_length = (scroll_bar_boundaries[1][1] - scroll_bar_boundaries[0][1])

            # Create Key Binding Rectangle
            package_rect = pygame.Rect(200, 80, 880, 560)
            pygame.draw.rect(self.screen, "#2f3540", package_rect, 4)

            # Horizontal Line
            pygame.draw.line(self.screen, "#2f3540",
                             (package_rect.x, package_rect.y + 65),
                             (package_rect.right, package_rect.y + 65), 4)
            # Vertical Line
            pygame.draw.line(self.screen, "#2f3540",
                             (package_rect.x + 600, package_rect.y),
                             (package_rect.x + 600, package_rect.bottom), 4)

            # Scroll Bar Line and Rectangle
            pygame.draw.line(self.screen, "#2f3540",
                             (package_rect.right - 30, package_rect.y + 65),
                             (package_rect.right - 30, package_rect.bottom), 4)
            scroll_bar = pygame.Rect(package_rect.right - 26,
                                     package_rect.y + 68 + (scroll_length * self.button_magnitude//100),
                                     20, 20)
            pygame.draw.rect(self.screen, "gray", scroll_bar, 0, 2)

            # Getting the Text Surfaces and Rectangles
            for text, values in text_elements_dict.items():
                # Change the elements position based on the button location
                length_screen_constrained = package_rect.y + 65 - (package_rect.bottom - 80)
                start_y = 160
                end_y = text_elements_dict["Special Attack"]["pos"][1]
                total_length = end_y - start_y

                text_surface = font2.render(text, False, "#b03d10")
                text_elements_dict[text]["surface"] = text_surface
                if text in ["Key Binds", "Player 1", "Player 2"]:
                    rect = text_surface.get_rect(topleft=values["pos"])
                else:
                    new_pos = (values["pos"][0], values["pos"][1] - total_length * self.button_magnitude//100)
                    rect = text_surface.get_rect(topleft=new_pos)
                text_elements_dict[text]["rect"] = rect

                if text in ["Key Binds", "Player 1", "Player 2"]:
                    self.screen.blit(text_surface, rect)
                else:
                    if package_rect.y + 65 <= new_pos[1] < package_rect.bottom - 80:
                        self.screen.blit(text_surface, rect)

            # Scrolling Button Mechanic
            def mouse_scrolling():
                if mouse_press[0]:
                    self.button_held = True

                    self.button_magnitude = ((mouse_pos[1] - scroll_bar_boundaries[0][1]) / scroll_length) * 100
                    if self.button_magnitude < 0:
                        self.button_magnitude = 0
                    if self.button_magnitude > 100:
                        self.button_magnitude = 100
                else:
                    self.button_held = False

            if scroll_bar.collidepoint(mouse_pos):
                mouse_scrolling()
            else:
                if self.button_held:
                    mouse_scrolling()

class Map_Management:
    def __init__(self):
        # Display
        self.screen = pygame.display.get_surface()
        self.background_image = pygame.image.load(
            r"Images/Background Images/character_choice_background.jpg").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (self.screen.get_width(), self.screen.get_height()))

        # Maps
        self.game_maps = self.import_maps()
        self.map_rects = []
        self.map_selection_complete = False
        self.map_selected = None
        self.fighter_pos_per_map = [[(360, 240), (920, 240)], [(360, 240), (920, 240)],
                                    [(360, 240), (920, 240)], [(360, 240), (920, 240)]]
        self.fighter_positions = None
        self.previously_selected_maps = []
        
        # Font
        self.font = pygame.font.Font("./Fonts/retro.ttf", 70)

    def import_maps(self):
        game_maps = []
        for _,__,img_files in walk("Images/Background Images/Game Maps"):
            for image in img_files:
                full_path = "Images/Background Images/Game Maps" + "/" + image
                surface = pygame.image.load(full_path).convert_alpha()
                surface = pygame.transform.scale(surface, (1280, 720))
                game_maps.append(surface)
        return game_maps

    def run(self):
        self.draw_maps()
        self.map_selection()

        return self.fighter_positions
    
    def draw_map_in_arena(self):
        draw_bg(self.screen, self.map_selected)
    
    def map_selection(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()

        for index, rect in enumerate(self.map_rects):
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, "white", rect, 2)
                if mouse_press[0]:
                    self.map_selected = self.game_maps[index]
                    self.fighter_positions = self.fighter_pos_per_map[index]
                    self.previously_selected_maps.append(self.map_selected)
                    self.map_selection_complete = True

    def draw_maps(self):
        draw_bg(self.screen, self.background_image)
        # Font
        text = self.font.render("Map Selection", False, "#ad4809")
        self.screen.blit(text, (550, 60))
        # Defining initial position
        pos = (50, 400)

        # Resizing the images
        resized_maps = []
        self.map_rects = []
        for x, image in enumerate(self.game_maps):
            image = pygame.transform.scale(image, (270, 220))
            resized_maps.append(image)
            self.screen.blit(image, (pos[0] + x * 290, pos[1]))
            rect = pygame.Rect(pos[0] + x * 290, pos[1], 270, 220)
            self.map_rects.append(rect)

    def randomize_map(self, p1, p2):
        # Get a random map
        map_options = []
        for map in self.game_maps:
            if map not in self.previously_selected_maps:
                map_options.append(map)
        random_map = choice(map_options)
        
        # Reconfigure the player position and current map
        self.previously_selected_maps.append(random_map)
        index = self.game_maps.index(random_map)
        self.map_selected = random_map
        self.fighter_positions = self.fighter_pos_per_map[index]

        p1.rect.topleft = self.fighter_positions[0]
        p2.rect.topleft = self.fighter_positions[1]
