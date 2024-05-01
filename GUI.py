import pygame
from os import walk
from random import choice
from support import *

def load_image(path):
    return pygame.image.load(f"{path}").convert_alpha()


def draw_bg(screen, image):
    screen.blit(image, (0, 0))


def draw_text(screen, font, sentence, text_col, x, y):
    text = font.render(sentence, True, text_col)
    screen.blit(text, (x, y))


def create_rectangle(x, y, width, height):
    rect = pygame.Rect(x, y, width, height)
    return rect


class Map_Management:
    def __init__(self, groups):
        # Display
        self.screen = pygame.display.get_surface()
        self.background_image = pygame.image.load(
            r"Images/Background Images/character_choice_background.jpg").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, self.screen.get_size())

        # Map Data
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

        # Groups
        self.map_group = pygame.sprite.Group()

        # Players
        self.p1 = None
        self.p2 = None

        # Camera System
        self.camera = Camera_Management(self.game_maps)

    def import_maps(self):
        game_maps = []
        map_sizes = [(1580, 900), (1580, 900), (1580, 900), (1580, 900)]
        for _, __, img_files in walk("Images/Background Images/Game Maps"): # Only interested in the file names, so
            # use _, __ as i don't need the directory name
            for count, image in enumerate(img_files):
                full_path = "Images/Background Images/Game Maps" + "/" + image
                surface = pygame.image.load(full_path).convert_alpha()
                surface = pygame.transform.scale(surface, map_sizes[count])
                game_maps.append(surface)
        return game_maps

    def run(self, events):
        self.draw_maps(events)

        # Check if any map is selected
        for map in self.map_group.sprites():
            if map.selected:
                self.map_selected = self.game_maps[map.id]
                self.fighter_positions = self.fighter_pos_per_map[map.id]
                self.previously_selected_maps.append(self.map_selected)
                self.map_selection_complete = True
                for sprite in self.map_group.sprites():
                    sprite.kill()
                break

        return self.fighter_positions

    def draw_maps(self, events):
        draw_bg(self.screen, self.background_image)  # Drawing the background image
        # Text data
        text = self.font.render("Map Selection", False, "#ad4809")
        self.screen.blit(text, (520, 60))
        # Create sprites
        if len(self.map_group.sprites()) == 0:
            for x, image in enumerate(self.game_maps):
                image = pygame.transform.scale(image, (270, 220))
                self.map_group.add(ImgButtons(image, (50 + x * 290, 300), x))
        # Updating the sprites
        else:
            self.map_group.update(events)

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

        # Change the player position back to the original position
        p1.rect.topleft = self.fighter_positions[0]
        p2.rect.topleft = self.fighter_positions[1]

    def camera_movement(self, p1, p2):
        self.camera.camera_movement(p1, p2, self.map_selected)

class Camera_Management(pygame.sprite.Group):
    def __init__(self, game_maps):
        pygame.sprite.Group.__init__(self)
        self.screen = pygame.display.get_surface()
        self.game_maps = game_maps
        self.map_selected = None
        self.mapTopLeft = [[-110, -145], [-110, -140], [-110, -150], [-110, -180]]
        self.boundaries = [[[[0, 550]], [[66, 293], [450, 293]], [[934, 293], [1318, 293]], [[202, 105], [1160, 105]]],
                           [[[240, 540], [1062, 540]], [[534, 130], [620, 130]], [[-5, 318], [154, 318]],
                            [[1213, 272], [1372, 272]]],
                           [[[0, 550]], [[216, 290], [588, 290]], [[791, 290], [1163, 290]], [[310, 44], [974, 54]]],
                           [[[0, 600]]]]

    def camera_movement(self, p1, p2, map_selected):
        self.index = self.game_maps.index(map_selected)
        self.p1 = p1
        self.p2 = p2
        self.map_selected = map_selected
        self.map_rect = self.map_selected.get_rect(topleft=pygame.Vector2(self.mapTopLeft[self.index]))
        self.screen.fill("blue")
        self.screen.blit(self.map_selected, self.map_rect)
