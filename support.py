import pygame
import csv
import pandas as pd

class Objs(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

    def update(self, events):
        # Updating all sprites
        for sprite in self.sprites():
            sprite.update(events)

class DisplayText(pygame.sprite.Sprite):
    def __init__(self, text, font, pos, kb=False, kb_sprite=None):
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
        self.image = font.render(text, False, "#db4307") # Text surface
        self.rect = self.image.get_rect(topleft=pos) # Getting the rectangle for the text srf
        self.kb = kb
        self.kb_sprite = kb_sprite
        self.text = text

    def draw(self):
        if not self.kb: # If not a key button
            self.screen.blit(self.image, self.rect)
        else:
            start_y = 160
            end_y = 800
            total_length = end_y - start_y

            new_y_pos = self.rect.y - total_length * self.kb_sprite.button_magnitude

            # Only the key buttons will move when sliding the bar, the titles will stay in place
            if self.text in ["Key Binds", "Player 1", "Player 2"]:
                self.screen.blit(self.image, self.rect)
            else:
                if 145 <= new_y_pos < 560:
                    self.screen.blit(self.image, [self.rect.x, new_y_pos])

    def update(self, events):
        self.draw()

class TextButton(pygame.sprite.Sprite):
    def __init__(self, text, font, pos):
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
        self.text = text
        self.image = font.render(text, False, "#db4307")  # Text surface
        self.rect = self.image.get_rect(topleft=pos)  # Getting the rectangle for the text surface
        self.rect.inflate_ip(20, 10)  # Making the rectangle larger
        self.clicked = False

    def draw(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        click = False
        # If the button is clicked
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        # Draw the Rectangles
        self.screen.blit(self.image, self.rect.topleft + pygame.Vector2(10, 5))

        # Hovering will change colour to white
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, "white", self.rect, 4)

            # Check for clicks
            if click:
                self.clicked = True
        else:
            pygame.draw.rect(self.screen, [190, 25, 23], self.rect, 4)

    def update(self, events):
        self.draw(events)

class TextButtons(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

    def update(self, events):
        for sprite in self.sprites():
            sprite.update(events)

class FadeInButton(pygame.sprite.Sprite):
    def __init__(self, text, font, pos):
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
        self.text = text
        self.image = font.render(text, False, "#db4307")
        self.rect = self.image.get_rect(topleft=pos)
        self.fade_in = 0
        self.rect.inflate_ip(8, 2)
        self.delay = pygame.time.get_ticks()
        self.clicked = False

    def draw(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        click = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        # Used to change the alpha value
        if self.fade_in <= 135:
            self.fade_in += 0.3
        else:
            self.fade_in = 135
        self.image.set_alpha(self.fade_in)
        self.screen.blit(self.image, self.rect.topleft + pygame.Vector2(6, 2))
        if self.fade_in >= 10:
            # Checing if PvE or PvP is pressed
            if self.rect.collidepoint(mouse_pos):
                if click:
                    pygame.draw.rect(self.screen, "red", self.rect, 2, 10)
                    self.clicked = True
                else:
                    pygame.draw.rect(self.screen, "white", self.rect, 2, 10)
            else:
                pygame.draw.rect(self.screen, "#db4307", self.rect, 2, 10)

    def update(self, events):
        self.draw(events)

class KBScrollButton(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
        self.rect = rect
        self.button_magnitude = 0
        self.button_held = False

    def draw(self):
        adj_rect = self.rect.copy()
        adj_rect.y = self.rect.y + 470 * self.button_magnitude
        pygame.draw.rect(self.screen, "gray", adj_rect)

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        adj_rect = self.rect.copy()
        adj_rect.y = self.rect.y + 470 * self.button_magnitude

        if adj_rect.collidepoint(mouse_pos) or self.button_held:
            if mouse_press[0]:
                self.button_held = True

                # (Y-value - top line)/total length * 100 total length is either 470 or 640
                self.button_magnitude = (mouse_pos[1] - 160) / 470
                if self.button_magnitude < 0:
                    self.button_magnitude = 0
                if self.button_magnitude > 1:
                    self.button_magnitude = 1
            else:
                self.button_held = False

        self.draw()

class KBRect(pygame.sprite.Sprite):
    def __init__(self, rect, button, text, player, index):
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font("./Fonts/retro.ttf", 40)
        self.text = text
        self.text_srf = self.font.render(str(text), False, "black")
        self.rect = rect
        self.selected = False
        self.button = button
        self.confirm_choice = False
        self.id = index
        self.player = player - 1

    def draw(self, events):
        mouse_pos = pygame.mouse.get_pos()
        click = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        new_y_pos = self.rect.y - 640 * self.button.button_magnitude
        adj_rect = self.rect.copy()
        adj_rect.y = new_y_pos

        if 145 < new_y_pos < 560:
            if adj_rect.collidepoint(mouse_pos):
                if click:
                    pygame.draw.rect(self.screen, "red", adj_rect, 3)
                    self.selected = True
                else:
                    pygame.draw.rect(self.screen, "white", adj_rect, 3)
                    if not self.selected:
                        self.screen.blit(self.text_srf, adj_rect.topleft + pygame.Vector2(20, 4))
            else:
                if click:
                    self.selected = False
                pygame.draw.rect(self.screen, "gray", adj_rect, 3)
                if not self.selected:
                    self.screen.blit(self.text_srf, adj_rect.topleft + pygame.Vector2(20, 4))


    def update(self, events):
        self.draw(events)

        if self.selected:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.confirm_choice = True

                    else:
                        self.text = str(event.unicode).upper()
                        if event.key == pygame.K_UP:
                            self.text = "UP"
                        if event.key == pygame.K_DOWN:
                            self.text = "DOWN"
                        if event.key == pygame.K_LEFT:
                            self.text = "LEFT"
                        if event.key == pygame.K_RIGHT:
                            self.text = "RIGHT"
                        self.text_srf = self.font.render(self.text, False, "black")

        if self.confirm_choice:
            ls = ["up","down","left","right","jump","dash","normal attack","strong attack","special attack"]
            df = pd.read_csv('keyBinds.csv')
            df.loc[self.player, ls[self.id]] = self.text
            df.to_csv('keyBinds.csv', index=False)
            self.confirm_choice = False
            self.selected = False

class ImgButtons(pygame.sprite.Sprite):
    def __init__(self, img, pos, index, state=None):
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
        self.image = img
        self.rect = self.image.get_rect(topleft=pos)
        if state == "character selection":
            self.rect.width, self.rect.height = 160, 160
        self.selected = False
        self.selected_times = 0
        self.id = index
        self.state = state

    def draw(self, events, data=None):
        mouse_pos = pygame.mouse.get_pos()

        click = False
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if self.state == None:
            self.screen.blit(self.image, self.rect)
            if self.rect.collidepoint(mouse_pos):
                if click:
                    pygame.draw.rect(self.screen, "red", self.rect, 3)
                    self.selected = True
                    self.selected_times += 1
                else:
                    pygame.draw.rect(self.screen, "white", self.rect, 3)
            else:
                pygame.draw.rect(self.screen, "gray", self.rect, 3)
        else:
            if self.state == "character selection":
                if data == "stop":
                    click = False

            pygame.draw.rect(self.screen, "gray", self.rect)
            if self.rect.collidepoint(mouse_pos):
                if click:
                    pygame.draw.rect(self.screen, "red", self.rect, 3)
                    self.selected = True
                    self.selected_times += 1
                else:
                    pygame.draw.rect(self.screen, "white", self.rect, 3)
            else:
                pygame.draw.rect(self.screen, "black", self.rect, 3)
            self.screen.blit(self.image, self.rect.topleft + pygame.Vector2(-24, -30))

    def update(self, events, data=None):
        self.draw(events, data)

class Fighter1(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

class Fighter2(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
