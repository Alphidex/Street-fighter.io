import pygame
from debug import debug, Select_Rect

""" 
To Fix:
Check lines 117 (previously on self.attacking) and another one in update method to make sure i revert it back to normal
after testing...
Line 145 ; attacking should be True
Line 97 ; removed attacking = False whenever move() method runs

/!\ Continue with special attack hit-boxes (Zoro Done)
/!\ Remove attack forward (done) and swap it with 
Combo logic:
1. Attack one 
2. Wait (1-2 seconds)
3. If attacked again produces the second attack
4. ... same till 3rd attack
5. Where to place the code?
"""

# Fighter has to be generalised
class Fighter(pygame.sprite.Sprite):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, character_name):
        super().__init__()
        # Fighter Data
        self.player = player
        self.opponent = None
        self.name = character_name
        self.health = 100
        self.flip = flip
        self.control_keys = {
            "player_1": {"right": pygame.K_d, "left": pygame.K_a, "up": pygame.K_w, "down": pygame.K_s,
                         "normal_attack": pygame.K_j, "jump": pygame.K_k, "dash": pygame.K_l, "block": pygame.K_s,
                         "strong_attack": pygame.K_u, "special_attack": pygame.K_i, "assist": pygame.K_o},
            "player_2": {"right": pygame.K_RIGHT, "left": pygame.K_LEFT, "up": pygame.K_UP, "down": pygame.K_DOWN,
                         "normal_attack": pygame.K_f, "jump": pygame.K_g, "dash": pygame.K_h, "block": pygame.K_DOWN,
                         "strong_attack": pygame.K_r, "special_attack": pygame.K_t, "assist": pygame.K_y}}

        # Fighter Status
        self.hit = False
        self.knockback = False
        self.dead = False
        self.block = False

        # Display
        self.screen = pygame.display.get_surface()

        # Fighter Image Data
        self.image_scale = data[2]
        self.size = data[:2]  # Create a list for the first 2 items
        self.offset = data[3]
        self.frame_index = 0
        self.action = 3
        self.animation_list = self.load_images(sprite_sheet, animation_steps, "animations")
        self.image = self.get_current_image()

        # Fighter Rect
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.width, self.rect.height = 100, 143

        # Gravity
        self.vel_y = 0  # Keeps track of speed when the character is accelerating down due to gravity

        # Movement
        self.running = False
        self.dash = False
        self.jump = [False, False]
        self.jumping = False

        # Attacks
        self.attacking = False
        self.attack_list_trigger = [False]
        self.attacking_rectangle = None
        # Ranged Attacks
        self.ranged_attack_instance_list = []
        self.range_attack = False
        # Normal Attack Combo
        self.normal_combo_timer = pygame.time.get_ticks()
        self.normal_combo_count = 0
        self.attack_triggers = {
            "normal_attack": {"trigger": False},
            "normal_attack_up": {"trigger": False},
            "normal_attack_down": {"trigger": False},
            "normal_jump_attack": {"trigger": False},
            "strong_attack": {"trigger": False},
            "strong_attack_up": {"trigger": False},
            "strong_attack_down": {"trigger": False},
            "strong_jump_attack": {"trigger": False},
            "special_attack": {"trigger": False},
            "special_attack_up": {"trigger": False},
            "special_attack_down": {"trigger": False}
        }

        # Clock
        self.update_time = pygame.time.get_ticks()

        # Debugging
        self.game_paused = False
        self.paused_time = 0
        self.debug_rect = Select_Rect(pygame.display.get_surface())

    def set_opponent(self, opponent):
        self.opponent = opponent

    def run(self, target):
        self.draw(self.screen)
        keys = pygame.key.get_pressed()

        if pygame.time.get_ticks() - self.paused_time > 300:
            if keys[pygame.K_p]:
                self.paused_time = pygame.time.get_ticks()
                self.game_paused = not self.game_paused

        if self.game_paused:
            self.debug_rect.select_rect()
        else:
            self.move(target)
            self.update(target, self.screen)

    def draw(self, screen):
        pass

    def update(self, target, screen):
        pass

    def draw_character_rect(self):
        pygame.draw.rect(self.screen, "green", self.rect, 3)

    def get_current_image(self):
        return self.animation_list[self.action][self.frame_index]

    def load_images(self, x, y, z):
        pass

    def borders(self, SCREEN_WIDTH, SCREEN_HEIGHT, dx, dy):
        # For x Variable
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        # For Y Variable
        if self.rect.bottom + dy > 550:
            self.vel_y = 0
            dy = 550 - self.rect.bottom
            self.jump[0], self.jump[1] = False, False

        return dx, dy

    def time_passed(self):
        return pygame.time.get_ticks() - self.update_time

    def check_key_presses(self, key, dx, SPEED):
        # Checking if character is in air
        if self.rect.bottom < 550:
            chr_in_air = True
        else:
            chr_in_air = False

        if not self.dead:
            for dic_key in self.control_keys.keys():
                player = "player_" + str(self.player)
                if player == dic_key:
                    # If you attack then you can't perform another action - gonna change
                    if not self.attacking:
                        # MOVEMENT
                        if key[self.control_keys[player]["left"]]:
                            dx -= SPEED
                            self.running = True
                        if key[self.control_keys[player]["right"]]:
                            dx += SPEED
                            self.running = True

                        # Dodging
                        if key[self.control_keys[player]["dash"]]:
                            self.dash = True

                        # Jumping
                        if key[self.control_keys[player]["jump"]]:
                            if self.jump[1] == False:
                                if self.jump[0] == False:
                                    self.jump[0] = True
                                else:
                                    self.jump[1] = True
                                self.vel_y = -30
                                self.jumping = True

                        # Blocking
                        if key[self.control_keys[player]["block"]] and (not chr_in_air):
                            self.block = True
                        else:
                            self.block = False

                        # ATTACKS
                        if key[self.control_keys[player]["normal_attack"]] \
                                or key[self.control_keys[player]["strong_attack"]] \
                                or key[self.control_keys[player]["special_attack"]]:

                            self.attacking = True

                            # Normal Attack Attacks
                            if key[self.control_keys[player]["normal_attack"]]:
                                if chr_in_air:
                                    self.attack_triggers["normal_jump_attack"]["trigger"] = True
                                elif key[self.control_keys[player]["down"]]:
                                    self.attack_triggers["normal_attack_down"]["trigger"] = True
                                elif key[self.control_keys[player]["up"]]:
                                    self.attack_triggers["normal_attack_up"]["trigger"] = True
                                else:
                                    self.combo_attack_logic()

                            # Strong Attack Attacks
                            if key[self.control_keys[player]["strong_attack"]]:
                                if chr_in_air:
                                    self.attack_triggers["strong_jump_attack"]["trigger"] = True
                                elif key[self.control_keys[player]["down"]]:
                                    self.attack_triggers["strong_attack_down"]["trigger"] = True
                                elif key[self.control_keys[player]["up"]]:
                                    self.attack_triggers["strong_attack_up"]["trigger"] = True
                                else:
                                    self.attack_triggers["strong_attack"]["trigger"] = True

                            # Special Attack Attacks
                            if key[self.control_keys[player]["special_attack"]]:
                                if key[self.control_keys[player]["down"]]:
                                    self.attack_triggers["special_attack_down"]["trigger"] = True
                                elif key[self.control_keys[player]["up"]]:
                                    self.attack_triggers["special_attack_up"]["trigger"] = True
                                else:
                                    self.attack_triggers["special_attack"]["trigger"] = True

                            # Update the attack_list_trigger
                            self.attack_list_trigger *= 50
        return dx

    def direction_system(self, key, target):
        # Ensure players face each other but not when moving
        if not self.dead:
            # Dash and Movement are separate
            if not self.dash and not self.attacking:
                # Flipping the character when moving
                if self.rect.centerx <= target.rect.centerx:
                    if self.player == 1:
                        if not (key[pygame.K_a] or key[pygame.K_d]):
                            self.flip = False
                        elif key[pygame.K_a]:
                            self.flip = True
                        elif key[pygame.K_d]:
                            self.flip = False
                    if self.player == 2:
                        if not (key[pygame.K_LEFT] or key[pygame.K_RIGHT]):
                            self.flip = False
                        elif key[pygame.K_LEFT]:
                            self.flip = True
                        elif key[pygame.K_RIGHT]:
                            self.flip = False

                elif self.rect.centerx > target.rect.centerx:
                    if self.player == 1:
                        if not (key[pygame.K_a] or key[pygame.K_d]):
                            self.flip = True
                        elif key[pygame.K_a]:
                            self.flip = True
                        elif key[pygame.K_d]:
                            self.flip = False
                    if self.player == 2:
                        if not (key[pygame.K_LEFT] or key[pygame.K_RIGHT]):
                            self.flip = True
                        elif key[pygame.K_LEFT]:
                            self.flip = True
                        elif key[pygame.K_RIGHT]:
                            self.flip = False

            if self.dash:
                self.rect.x += 30 + (-60 * self.flip)

    def combo_attack_logic(self):
        # Combo attacks
        # Update module (preparation)
        if pygame.time.get_ticks() - self.normal_combo_timer >= 1200 or \
                self.normal_combo_count >= 3:
            self.normal_combo_count = 0
            self.normal_combo_timer = pygame.time.get_ticks()

        # Logic
        if self.normal_combo_count == 0:
            self.attack_triggers["normal_attack"]["trigger"] = True
        if pygame.time.get_ticks() - self.normal_combo_timer < 1200:
            if self.normal_combo_count == 1:
                self.attack_triggers["normal_attack_down"]["trigger"] = True
            elif self.normal_combo_count == 2:
                self.attack_triggers["normal_attack_up"]["trigger"] = True
        self.normal_combo_count += 1
        self.normal_combo_timer = pygame.time.get_ticks()

    def move(self, target):
        # Variables
        SPEED = 7
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        key = pygame.key.get_pressed()

        self.draw_character_rect()
        dx = self.check_key_presses(key, dx, SPEED)

        # Define Gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Attacking in air, holds you in air
        if self.attack_triggers["normal_jump_attack"]["trigger"] or self.attack_triggers["strong_jump_attack"]["trigger"]:
            dy = 0
            self.vel_y = 0

        # dx and dy are returned once calculations are done
        dx, dy = self.borders(self.screen.get_width(), self.screen.get_height(), dx, dy)

        self.direction_system(key, target)

        # UPDATE POSITION OF RECTANGLE
        self.rect.x += dx
        self.rect.y += dy


class Ranged_Attack:
    def __init__(self, flip, attack_animation_list, action, character_rect, character):
        # Data
        self.character = character
        self.flip = flip
        self.attacking = True

        # Ranged Attacks
        self.attack_rect_list = []
        self.attacking_rectangle = None
        self.attack_list_trigger = [False]
        self.collision = False

        # Animations
        self.action = action  # 0 - Attack #1 - Death #2 - Idle #3 - Attack #4
        self.frame_index = 0
        self.image = attack_animation_list[self.action][self.frame_index]
        self.attack_animation_list = attack_animation_list

        # Clock
        self.update_time = pygame.time.get_ticks()

    def main(self, surface, offset, image_scale, target):
        self.draw_ranged_attack(surface, offset, image_scale)
        self.update_ranged_attack(surface)
        self.attack_collisions(target)

    def draw_ranged_attack(self, surface, offset, image_scale):
        pass

    def update_ranged_attack(self, surface):
        pass

    def attack_collisions(self, target):
        pass