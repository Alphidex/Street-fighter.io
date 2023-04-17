import pygame

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
class Fighter:
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, character_name):
        # Data
        self.player = player
        self.name = character_name
        self.health = 100
        self.flip = flip
        self.hit = False
        self.knockback = False
        self.dead = False
        self.block = False

        # Image size and rendering onto the screen
        self.image_scale = data[2]
        self.size = data[:2]  # Create a list for the first 2 items
        self.offset = data[3]

        # Drawing rect and gravity
        self.rect = pygame.Rect((x, y, 100, 143))
        self.vel_y = 0  # Keeps track of speed when the character is accelerating down due to gravity

        # Movement
        self.running = False
        self.dash = False
        self.jump = [False, False]  # First Jump, Second Jump

        # Attacks ---
        self.attacking = False
        self.attack_list_trigger = [False]
        self.attacking_rectangle = None

        # Ranged Attacks
        self.ranged_attack_instance_list = []
        self.range_attack = False

        # Normal Attack Attacks
        self.normal_attack = False
        self.normal_attack_forward = False
        self.normal_attack_up = False
        self.normal_attack_down = False
        self.normal_jump_attack = False
        # Normal Attack Combo
        self.normal_combo_timer = pygame.time.get_ticks()
        self.normal_combo_count = 0
        # Strong Attack Attacks
        self.strong_attack = False
        self.strong_attack_up = False
        self.strong_attack_down = False
        self.strong_jump_attack = False
        # Special Attack Attacks
        self.special_attack = False
        self.special_attack_up = False
        self.special_attack_down = False
        # Clock
        self.update_time = pygame.time.get_ticks()
        self.attack_cooldown = 0

    def borders(self, SCREEN_WIDTH, SCREEN_HEIGHT, dx, dy, rect_bg_0, rect_bg_1):
        # Setting up borders
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

        # *** Need to fix the thing with teleporting on the platforms ***
        # First Platform
        if (self.rect.bottom + dy > rect_bg_0.top - 10) and (rect_bg_0.top - 10 < self.rect.bottom < rect_bg_0.bottom):
            if (self.rect.midbottom[0] > rect_bg_0.topleft[0]) and (self.rect.midbottom[0] < rect_bg_0.topright[0]):
                self.vel_y = 0
                dy = rect_bg_0.top - self.rect.bottom + 2
                self.jump[0], self.jump[1] = False, False

        # Second Platform
        if (self.rect.bottom + dy > rect_bg_1.top - 10) and (rect_bg_1.top - 10 < self.rect.bottom < rect_bg_1.bottom):
            if (self.rect.midbottom[0] > rect_bg_1.topleft[0]) and (self.rect.midbottom[0] < rect_bg_1.topright[0]):
                self.vel_y = 0
                dy = rect_bg_1.top - self.rect.bottom + 2
                self.jump[0], self.jump[1] = False, False

        return dx, dy

    def time_passed(self):
        return pygame.time.get_ticks() - self.update_time

    def move(self, SCREEN_WIDTH, SCREEN_HEIGHT, surface, target, rect_bg_0, rect_bg_1, FPS):
        SPEED = 7
        GRAVITY = 2  # Acceleration downward
        dx = 0
        dy = 0

        # Checking if character is in air
        if self.rect.bottom < 550:
            chr_in_air = True
        else:
            chr_in_air = False

        self.running = False
        # --------------  Here i removed attacking = False ------------

        # Get key presses
        key = pygame.key.get_pressed()

        if not self.dead:
            # Controls for the first player
            if self.player == 1:
                # If you attack then you can't perform another action - gonna change
                if not self.attacking:
                    # MOVEMENT
                    if key[pygame.K_a]:
                        dx -= SPEED
                        self.running = True
                    if key[pygame.K_d]:
                        dx += SPEED
                        self.running = True

                    # Dodging
                    if key[pygame.K_l]:
                        self.dash = True

                    # JUMPING
                    # Make sure to try it using pygame.key.get_pressed() and delay the continous presses

                    # Blocking
                    if key[pygame.K_s] and (not chr_in_air):
                        self.block = True
                    else:
                        self.block = False

                    # ATTACKS
                    if key[pygame.K_j] or key[pygame.K_u] or key[pygame.K_i]:
                        self.attacking = True

                        # Normal Attack Attacks
                        if key[pygame.K_j]:
                            if chr_in_air:
                                self.normal_jump_attack = True
                            elif key[pygame.K_s]:
                                self.normal_attack_down = True
                            elif key[pygame.K_w]:
                                self.normal_attack_up = True
                            else:
                                #Combo attacks

                                # Update module (preparation)
                                if pygame.time.get_ticks() - self.normal_combo_timer >= 1200 or\
                                        self.normal_combo_count >= 3:
                                    self.normal_combo_count = 0
                                    self.normal_combo_timer = pygame.time.get_ticks()

                                # Logic
                                if self.normal_combo_count == 0:
                                    self.normal_attack = True
                                if pygame.time.get_ticks() - self.normal_combo_timer < 1200:
                                    if self.normal_combo_count == 1:
                                        self.normal_attack_down = True
                                    elif self.normal_combo_count == 2:
                                        self.normal_attack_up = True
                                self.normal_combo_count += 1
                                self.normal_combo_timer = pygame.time.get_ticks()

                        # Strong Attack Attacks
                        if key[pygame.K_u]:
                            if chr_in_air:
                                self.strong_jump_attack = True
                            elif key[pygame.K_s]:
                                self.strong_attack_down = True
                            elif key[pygame.K_w]:
                                self.strong_attack_up = True
                            else:
                                self.strong_attack = True

                        # Special Attack Attacks
                        if key[pygame.K_i]:
                            if key[pygame.K_s]:
                                self.special_attack_down = True
                            elif key[pygame.K_w]:
                                self.special_attack_up = True
                            else:
                                self.special_attack = True

                        # Update the attack_list_trigger
                        self.attack_list_trigger *= 50

            # Controls for player 2
            if self.player == 2:
                # If you attack then you can't perform another action - gonna change
                if not self.attacking:
                    # MOVEMENT
                    if key[pygame.K_LEFT]:
                        dx -= SPEED
                        self.running = True
                    if key[pygame.K_RIGHT]:
                        dx += SPEED
                        self.running = True

                    # Dodging
                    if key[pygame.K_m]:
                        self.dash = True

                    # JUMPING
                    # Make sure to try it using pygame.key.get_pressed() and delay the continous presses

                    # Blocking
                    if key[pygame.K_DOWN] and (not chr_in_air):
                        self.block = True
                    else:
                        self.block = False

                    # ATTACKS
                    if key[pygame.K_b] or key[pygame.K_g] or key[pygame.K_h]:
                        self.attacking = True

                        # Normal Attack Attacks
                        if key[pygame.K_b]:
                            if chr_in_air:
                                self.normal_jump_attack = True
                            elif key[pygame.K_DOWN]:
                                self.normal_attack_down = True
                            elif key[pygame.K_UP]:
                                self.normal_attack_up = True
                            else:
                                #Combo attacks

                                # Update module (preparation)
                                if pygame.time.get_ticks() - self.normal_combo_timer >= 1200 or\
                                        self.normal_combo_count >= 3:
                                    self.normal_combo_count = 0
                                    self.normal_combo_timer = pygame.time.get_ticks()

                                # Logic
                                if self.normal_combo_count == 0:
                                    self.normal_attack = True
                                if pygame.time.get_ticks() - self.normal_combo_timer < 1200:
                                    if self.normal_combo_count == 1:
                                        self.normal_attack_down = True
                                    elif self.normal_combo_count == 2:
                                        self.normal_attack_up = True
                                self.normal_combo_count += 1
                                self.normal_combo_timer = pygame.time.get_ticks()


                        # Strong Attack Attacks
                        if key[pygame.K_g]:
                            if chr_in_air:
                                self.strong_jump_attack = True
                            elif key[pygame.K_DOWN]:
                                self.strong_attack_down = True
                            elif key[pygame.K_UP]:
                                self.strong_attack_up = True
                            else:
                                self.strong_attack = True

                        # Special Attack Attacks
                        if key[pygame.K_h]:
                            if key[pygame.K_DOWN]:
                                self.special_attack_down = True
                            elif key[pygame.K_UP]:
                                self.special_attack_up = True
                            else:
                                self.special_attack = True

                        # Update the attack_list_trigger
                        self.attack_list_trigger *= 50

        # Apply PHYSICS - NOTE: DON'T FORGET TO EXPERIMENT

        # Basically the target's gravity would be 0 for as long as he's attacked
        if self.name == "Zoro":
            if target.hit:
                if self.strong_attack_up:
                    target.vel_y = 0

        # Vel_y is a constant that keeps increasing by 2 through each iteration and resets to 0 when player touches
        # ground (something like acceleration where each second speed increases by 2 pixels)
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Attacking in air, holds you in air
        if self.normal_jump_attack or self.strong_jump_attack:
            dy = 0
            self.vel_y = 0

        # dx and dy are returned once calculations are done
        dx, dy = self.borders(SCREEN_WIDTH, SCREEN_HEIGHT, dx, dy, rect_bg_0, rect_bg_1)


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


        # UPDATE POSITION OF RECTANGLE
        self.rect.x += dx
        self.rect.y += dy


class Ranged_Attack:
    def __init__(self, flip, range_attack_animation_list, action, character_rect, character):
        # Data
        self.character = character
        self.range_flip = flip
        self.attacking = True

        # Ranged Attacks
        self.range_attack_rect_list = []
        self.ranged_attacking_rectangle = None
        self.ranged_attack_list_trigger = [False]
        self.collision = False

        # Animations
        self.range_action = action  # 0 - Attack #1 - Death #2 - Idle #3 - Attack #4
        self.range_frame_index = 0
        self.range_image = range_attack_animation_list[self.range_action][self.range_frame_index]
        self.range_attack_animation_list = range_attack_animation_list

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


""" Importing the modules """

# from Characters_Code import *
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
