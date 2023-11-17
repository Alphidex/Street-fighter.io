import pygame

pygame.init()
font = pygame.font.Font(None, 30)


class Select_Rect:
    def __init__(self, screen):
        self.click_released = False
        self.topleft = None
        self.bottomright = None
        self.screen = screen

    def select_rect(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()

        if mouse_press[0]:
            if self.topleft is None:
                self.topleft = mouse_pos
            pos_1 = self.topleft
            pos_2 = (mouse_pos[0], self.topleft[1])
            pos_3 = mouse_pos
            pos_4 = (self.topleft[0], mouse_pos[1])
            self.bottomright = pos_3
            pygame.draw.lines(self.screen, (122, 213, 50), True, (pos_1, pos_2, pos_3, pos_4), 2)
            debug(f"Topleft: {self.topleft}")
            debug(f"Bottomright: {self.bottomright}", 50)
            print(f"Topleft: {self.topleft}")
            print(f"Bottomright: {self.bottomright}\n")
        else:
            self.topleft = None


def debug(info, y=10, x=10):
    screen = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(screen, 'Black', debug_rect)
    screen.blit(debug_surf, debug_rect)
