import pygame
from Sounds import Sounds
from GUI import load_image
import pandas as pd
import random

class Fighter(pygame.sprite.Sprite):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, character_name, ai):
        pygame.sprite.Sprite.__init__(self)
        # Fighter Data
        self.player = player
        self.opponent = None
        self.name = character_name
        self.flip = flip
        self.aiDelay = 0
        self.aiDifficulty = 0

        # Key Binds
        df = pd.read_csv("keyBinds.csv")
        self.control_keys = df.to_dict('records')

        # Fighter Status
        self.health = 100
        self.hit = False
        self.hit_do_once = True
        self.knockback = False
        self.stun = False
        self.stun_duration = 50
        self.stun_timer = pygame.time.get_ticks()
        self.stun_frame_index = 0
        self.dead = False
        self.block = False
        self.shield_health = 100
        self.stamina = 100
        self.stamina_cost = 14
        self.create_shield = Create_Shield(self.shield_health)
        self.shield_broken = False
        self.shield_cooldown_timer = None
        self.in_air = False
        self.running = False
        self.dash = False
        self.jump = [False, False]
        self.jumping = False
        self.extend_attack = None
        self.position_checkpoint = 0
        self.knockback_duration = pygame.time.get_ticks()
        self.sp_level = 0

        # Display
        self.screen = pygame.display.get_surface()

        # Fighter Image Data
        self.image_scale = data[2]
        self.size = data[:2]  # Create a list for the first 2 items
        self.offset = data[3]
        self.frame_index = 0
        self.action = 3
        self.animation_list = self.load_images(sprite_sheet, animation_steps, "animations")
        self.image = self.animation_list[self.action][self.frame_index]
        self.mask = pygame.mask.from_surface(self.image)

        # Fighter Rect
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.width, self.rect.height = 100, 143

        # Fighter GUI
        self.fighter_gui = Display_Character_Stats(self.player, self.health, self.rect, self.stamina, self.sp_level)

        # Gravity
        self.vel_y = 0  # Keeps track of speed when the character is accelerating down due to gravity
        self.check_once_knockback = pygame.time.get_ticks()
        # Attacks
        self.attacking = False
        self.frame_index_counter = [-1, 0]
        # and when the rectangle triggers.
        self.attack_effect_executions = 0
        self.exclude_attacks = []
        self.attacking_rectangle = None
        # Ranged Attacks
        self.range_attack = False
        self.ranged_group = pygame.sprite.Group()

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
        self.attack_delay_list = {}

        # Clock
        self.update_time = pygame.time.get_ticks()

        # Sounds
        self.sounds = Sounds("fighters")

        # AI
        self.ai = ai
        self.ai_state = "idle"
        self.jump_ai_delay = [False, pygame.time.get_ticks()]

        # Events
        self.events = None

        # Camera
        self.camera = None

        # Dust
        self.dust = Dust(self.rect.midbottom)

        # Shake
        self.shake = False
        self.shake_duration = 0

        # Drop Down
        self.down_count = 0
        self.drop_down_timer = pygame.time.get_ticks()

    def run(self, target, events, camera, current_match):
        self.aiDifficulty = 1/current_match * 20
        self.mask = pygame.mask.from_surface(self.image)

        self.events = events
        self.camera = camera
        self.draw(self.screen)
        self.fighter_gui.draw_everything(self.health, self.stamina, self.rect, self.sp_level)

        if self.ai:
            self.AI_Mechanics(target)
        else:
            self.move(target)

        self.update(target, self.screen)

    def set_opponent(self, opponent):
        self.opponent = opponent

    def draw(self, screen):
        pass

    def load_images(self, x, y, z):
        pass

    # Update game state
    def update(self, target, screen):
        pass

    def update_animation(self, target):
        animation_cooldown = 60
        if self.stun:
            if self.stun_duration > 0:
                self.stun_duration-=1
                img = pygame.image.load("./Images/Effects/stun_effect.png").convert_alpha()
                img_ls = []
                for x in range(4):
                    temp_img = img.subsurface(x * 500, 0, 500, 500)
                    temp_img = pygame.transform.scale_by(temp_img, 0.15)
                    img_ls.append(temp_img)
                self.screen.blit(img_ls[self.stun_frame_index], self.rect.topleft + pygame.Vector2(-12, -20))

                if pygame.time.get_ticks() - self.stun_timer > 10:
                    self.stun_frame_index += 1
                if self.stun_frame_index >= 4:
                    self.stun_frame_index = 0
            else:
                self.stun = False
                self.stun_duration = 50
                self.stun_frame_index = 0
                self.stun_timer = pygame.time.get_ticks()

        if self.hit:
            self.attacking = False
            # Updating attack list
            self.frame_index_counter = [-1, 0]
            for attack in self.attack_data.values():
                attack["trigger"] = False
            for attack in self.attack_triggers.values():
                attack["trigger"] = False

            if self.hit_do_once:
                self.hit_do_once = False
                self.frame_index = 0

            if self.time_passed() > 130:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

            if self.frame_index >= 2:
                self.hit = False
                self.frame_index = 0
                self.hit_do_once = True

        elif self.attacking:
            for attack in self.attack_data.values():
                if attack["trigger"]:
                    if self.time_passed() > attack["cooldown"]:
                        self.frame_index += 1
                        self.update_time = pygame.time.get_ticks()
        else:
            if self.time_passed() > animation_cooldown:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

    def reset_character_state(self, pos):
        # Fighter Status
        self.rect.topleft = pos
        self.health = 100
        self.hit = False
        self.knockback = False
        self.stun = False
        self.dead = False
        self.block = False
        self.shield_health = 100
        self.stamina = 100
        self.stamina_cost = 14
        self.shield_broken = False
        self.shield_cooldown_timer = None
        self.in_air = False

    # Key Presses + Movement
    def check_key_presses(self, key, dx, SPEED):
        if not self.dead:
            # If you attack then you can't perform another action - gonna change
            if not self.attacking:
                # MOVEMENT
                if key[pygame.key.key_code(self.control_keys[self.player-1]["left"])]:
                    dx -= SPEED
                    self.running = True
                if key[pygame.key.key_code(self.control_keys[self.player-1]["right"])]:
                    dx += SPEED
                    self.running = True

                # Dodging
                if key[pygame.key.key_code(self.control_keys[self.player-1]["dash"])] and self.stamina - self.stamina_cost >= 0:
                    if not self.dash:
                        self.stamina -= self.stamina_cost
                        self.sounds.sounds_dict["dash"]["list"][0].play().set_volume(0.3)
                        if self.stamina < 0:
                            self.stamina = 0

                    self.dash = True

                # Jumping
                for event in self.events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.key.key_code(self.control_keys[self.player - 1]["jump"]):
                            if self.jump.count(False):
                                self.jump[self.jump.index(False)] = True  # specifies the jump count
                                self.vel_y = -30  # How far the image moves
                                self.jumping = True
                                self.dust = Dust(
                                    self.rect.midbottom)  # Creates dust particles whenever the character jumps
                                self.shake_duration = 20  # Makes the screen shake when you jump

                # Dust
                self.dust.update()

                # Blocking
                self.shield_cooldown()
                if key[pygame.key.key_code(self.control_keys[self.player-1]["down"])]:
                    if not self.in_air and not self.running and not self.shield_broken:
                        self.block = True
                        self.create_shield.change_shield_color(self.shield_health, self.rect.center)
                else:
                    self.block = False

                # Drop Down from a Platform
                for event in self.events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.key.key_code(self.control_keys[self.player-1]["down"]):
                            if self.down_count == 0:
                                self.drop_down_timer = pygame.time.get_ticks()
                            self.down_count += 1
                            if pygame.time.get_ticks() - self.drop_down_timer < 600:
                                if self.down_count >= 2:
                                    if self.rect.bottom != self.camera.boundaries[self.camera.index][0][0][1] and not self.in_air:
                                        self.rect.y += 10
                            else:
                                self.down_count = 0

                # ATTACKS
                if key[pygame.key.key_code(self.control_keys[self.player-1]["normal attack"])] \
                        or key[pygame.key.key_code(self.control_keys[self.player-1]["strong attack"])] \
                        or key[pygame.key.key_code(self.control_keys[self.player-1]["special attack"])]:

                    # Cancel the block
                    self.block = False

                    # Normal Attacks
                    if key[pygame.key.key_code(self.control_keys[self.player-1]["normal attack"])]:
                        if self.in_air and self.attack_cooldown("normal_jump_attack"):
                            self.attack_triggers["normal_jump_attack"]["trigger"] = True
                        elif key[pygame.key.key_code(self.control_keys[self.player-1]["down"])]:
                            if self.attack_cooldown("normal_attack_down"):
                                self.attack_triggers["normal_attack_down"]["trigger"] = True
                        elif key[pygame.key.key_code(self.control_keys[self.player-1]["up"])]:
                            if self.attack_cooldown("normal_attack_up"):
                                self.attack_triggers["normal_attack_up"]["trigger"] = True
                        else:
                            self.combo_attack_logic()

                    # Strong Attack Attacks
                    elif key[pygame.key.key_code(self.control_keys[self.player-1]["strong attack"])]:
                        if self.in_air and self.attack_cooldown("strong_jump_attack"):
                            self.attack_triggers["strong_jump_attack"]["trigger"] = True
                        elif key[pygame.key.key_code(self.control_keys[self.player-1]["down"])]:
                            if self.attack_cooldown("strong_attack_down"):
                                self.attack_triggers["strong_attack_down"]["trigger"] = True
                        elif key[pygame.key.key_code(self.control_keys[self.player-1]["up"])]:
                            if self.attack_cooldown("strong_attack_up"):
                                self.attack_triggers["strong_attack_up"]["trigger"] = True
                        else:
                            if self.attack_cooldown("strong_attack"):
                                self.attack_triggers["strong_attack"]["trigger"] = True

                    # Special Attack Attacks
                    elif key[pygame.key.key_code(self.control_keys[self.player-1]["special attack"])]:
                        if self.sp_level > 100:
                            if key[pygame.key.key_code(self.control_keys[self.player-1]["down"])]:
                                if self.attack_cooldown("special_attack_down") and "special_attack_down" \
                                        not in self.exclude_attacks:
                                    self.attack_triggers["special_attack_down"]["trigger"] = True
                            elif key[pygame.key.key_code(self.control_keys[self.player-1]["up"])]:
                                if self.attack_cooldown("special_attack_up") \
                                        and "special_attack_up" not in self.exclude_attacks:
                                    self.attack_triggers["special_attack_up"]["trigger"] = True
                            else:
                                if self.attack_cooldown("special_attack") and "special_attack" not in self.exclude_attacks:
                                    self.attack_triggers["special_attack"]["trigger"] = True
                            self.sp_level -= 100

                    for attack in self.attack_triggers.values():
                        if attack["trigger"]:
                            self.attacking = True

                    if self.attacking:
                        self.sounds.sounds_dict["slash"]["list"][0].play().set_volume(0.3)
        return dx

    def AI_Mechanics(self, target):
        # Variables
        distx = abs(self.rect.centerx - target.rect.centerx)
        disty = abs(self.rect.centery - target.rect.centery)
        key = pygame.key.get_pressed()
        SPEED = 7
        GRAVITY = 1.7
        dx = 0
        dy = 0
        self.running = False
        self.aiDelay += 1

        if not self.dead:
            if not self.attacking:
                if abs(distx) > 200:
                    self.running = True
                if self.aiDelay > self.aiDifficulty:
                    self.aiDelay = 0

                    # Flip
                    if self.rect.centerx <= target.rect.centerx:
                        self.flip = False
                    else:
                        self.flip = True

                    # Movement
                    if abs(distx) > 500 and self.stamina - self.stamina_cost >= 0:
                        # Dodging
                        if self.stamina > 20:
                            if not self.dash:
                                self.stamina -= self.stamina_cost
                                self.sounds.sounds_dict["dash"]["list"][0].play().set_volume(0.3)
                            self.dash = True

                    # Jumping
                    if target.rect.bottom < self.camera.boundaries[self.camera.index][0][0][1]:
                        if not self.jump_ai_delay[0]:
                            self.jump_ai_delay = [True, pygame.time.get_ticks()]
                        if pygame.time.get_ticks() - self.jump_ai_delay[1] > 200:
                            if self.rect.top > target.rect.top:
                                if self.jump.count(False):
                                    self.jump_ai_delay[1] = pygame.time.get_ticks()
                                    self.jump[self.jump.index(False)] = True
                                    self.vel_y = -30
                                    self.jumping = True
                                else:
                                    self.jump_ai_delay[0] = False

                    # Dropping down a platform
                    if self.rect.bottom < target.rect.bottom:
                        drop_down = False
                        for boundary in self.camera.boundaries[self.camera.index]:
                            if self.rect.bottom == boundary[0][1] and not self.in_air:
                                drop_down = True
                        if drop_down:
                            self.rect.y += 10

                    # Blocking
                    self.shield_cooldown()

                    if target.attacking:
                        if abs(distx) < 200:
                            if not self.in_air and not self.shield_broken:
                                self.block = True
                                self.create_shield.change_shield_color(self.shield_health, self.rect.center)
                    else:
                        self.block = False

                    # Attacks
                    if self.in_air:
                        if 200 < distx < 300 and disty < 150:
                            if self.attack_cooldown("strong_jump_attack"):
                                self.attack_triggers["strong_jump_attack"]["trigger"] = True
                        elif distx < 200 and disty < 100:
                            if self.attack_cooldown("normal_jump_attack"):
                                self.attack_triggers["normal_jump_attack"]["trigger"] = True

                    # Special Attack
                    elif self.sp_level > 100 and distx < 400 and disty < 200 and self.attack_cooldown("special_attack_down"):
                        self.attack_triggers["special_attack_down"]["trigger"] = True

                    # Strong Attacks
                    elif 150 < distx < 250 and disty < 150 and self.attack_cooldown("strong_attack"):
                        self.attack_triggers["strong_attack"]["trigger"] = True

                    elif 180 < distx < 250 and disty < 80 and self.attack_cooldown("strong_attack_up"):
                        self.attack_triggers["strong_attack_up"]["trigger"] = True

                    elif distx < 200 and disty < 50 and target.block and self.attack_cooldown("strong_attack_down"):
                        self.attack_triggers["strong_attack_down"]["trigger"] = True

                    elif abs(distx) < 200 and abs(disty) < 100:
                        # Combo Attacks
                        self.combo_attack_logic()

                for attack in self.attack_triggers.values():
                    if attack["trigger"]:
                        self.attacking = True

        # Define Gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Stamina regen
        if self.stamina < 100:
            self.stamina += 0.12
        if self.stamina > 100:
            self.stamina = 100

        # Attacking in air, holds you in air
        if self.attack_triggers["normal_jump_attack"]["trigger"] or self.attack_triggers["strong_jump_attack"]["trigger"]:
            dy = 0
            self.vel_y = 0

        # dx and dy are returned once calculations are done
        dx, dy = self.borders(self.screen.get_width(), self.screen.get_height(), dx, dy, target)

        if not dy:
            self.in_air = False
        else:
            self.in_air = True

        if self.running:
            dx += SPEED + (-2 * SPEED * self.flip)

        if self.dash:
            self.rect.x += 30 + (-60 * self.flip)

        # UPDATE POSITION OF RECTANGLE
        self.rect.x += dx
        self.rect.y += dy

    def knockback_method(self):
        if self.knockback:
            if self.block:
                print("Block:", True)
            if pygame.time.get_ticks() - self.knockback_duration < 600:
                self.rect.x += -8 + (16 * self.flip)
                if not self.check_once_knockback:
                    self.vel_y = - 30
                    self.check_once_knockback = True
            else:
                self.knockback = False
                self.check_once_knockback = False
        else:
            self.knockback_duration = pygame.time.get_ticks()

    def move(self, target):
        # Variables
        SPEED = 7
        GRAVITY = 1.7
        dx = 0
        dy = 0
        self.running = False
        key = pygame.key.get_pressed()
        dx = self.check_key_presses(key, dx, SPEED)

        # Screen Shake
        if self.shake_duration > 0:
            self.shake_duration -= 1
            self.shake = True
        else:
            self.shake = False

        # Knocbkack
        self.knockback_method()

        # SP
        self.sp_bar(target, "None")

        # Define Gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Stamina regen
        if self.stamina < 100:
            self.stamina += 0.12
        if self.stamina > 100:
            self.stamina = 100

        # Attacking in air, holds you in air
        if self.attack_triggers["normal_jump_attack"]["trigger"] or self.attack_triggers["strong_jump_attack"]["trigger"]:
            dy = 0
            self.vel_y = 0

        # dx and dy are returned once calculations are done
        dx, dy = self.borders(self.screen.get_width(), self.screen.get_height(), dx, dy, target)

        self.direction_system(key, target)

        # Checking if character is in air

        if not dy: self.in_air = False
        else: self.in_air = True

        # UPDATE POSITION OF RECTANGLE
        self.rect.x += dx
        self.rect.y += dy

    def sp_bar(self, target, key):
        if self.hit: self.sp_level += 0.5
        if target.hit: self.sp_level += 1
        if key == "special_attack":
            if self.attack_triggers["special_attack_down"]["trigger"] == True or self.attack_triggers["special_attack"]["trigger"] == True or self.attack_triggers["special_attack_up"]["trigger"] == True:
                self.sp_level -= 100
        if self.sp_level > 300:
            self.sp_level = 300
        if self.sp_level < 0:
            self.sp_level = 0

    def borders(self, SCREEN_WIDTH, SCREEN_HEIGHT, dx, dy, target):
        # Side Borders
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        # In case the character goes of the map
        if self.rect.bottom < -700:
            self.health = 0
        if self.rect.top > self.screen.get_height() + 400:
            self.health = 0


        # Take damage from lava on 2nd map
        if self.camera.index == 1 and self.rect.bottom > self.camera.boundaries[self.camera.index][0][0][1] + 70:
            self.vel_y = - 30
            self.health -= 2

        # Horizontal Movement
        rx = 0
        if self.camera.map_rect.left < 0:
            if self.rect.left <= 0 and self.running:
                rx += 7
                if self.camera.map_rect.left + rx > 0:
                    rx = - self.camera.map_rect.left
        if self.camera.map_rect.right > self.screen.get_width():
            if self.rect.right >= self.screen.get_width() and self.running:
                rx -= 7
                if self.camera.map_rect.right + rx < self.screen.get_width():
                    rx = self.screen.get_width() - self.camera.map_rect.right

        self.camera.mapTopLeft[self.camera.index][0] += rx
        for boundaries in self.camera.boundaries[self.camera.index]:
            for margins in boundaries:
                margins[0] += rx
        target.rect.x += rx

        # Vertical Movement
        resy = 0
        fy = 10

        # If you're in contact with the top of the screen
        if self.rect.top <= 10:
            if self.camera.map_rect.top + fy < 0:
                resy += fy
            else:
                resy += -self.camera.map_rect.top

        boundaries = [[[[0, 550]], [[66, 293], [450, 293]], [[934, 293], [1318, 293]], [[202, 105], [1160, 105]]],
                           [[[240, 540], [1062, 540]], [[534, 130], [620, 130]], [[-5, 318], [154, 318]],
                            [[1213, 272], [1372, 272]]],
                           [[[0, 550]], [[216, 290], [588, 290]], [[791, 290], [1163, 290]], [[310, 44], [974, 54]]],
                           [[[0, 600]]]]

        # When both players are on the ground the camera moves back into position
        if self.rect.bottom == self.camera.boundaries[self.camera.index][0][0][1] == target.rect.bottom:
            if self.camera.boundaries[self.camera.index][0][0][1] - fy < boundaries[self.camera.index][0][0][1]:
                resy += boundaries[self.camera.index][0][0][1] - self.camera.boundaries[self.camera.index][0][0][1]
            else:
                resy -= 10

        # Second map has no camera movmement
        if self.camera.index == 1:
            resy = 0

        # Update Y value for maps
        self.camera.mapTopLeft[self.camera.index][1] += resy

        # Moving the 'invisible' boundaries of platforms down
        onPlatform = False
        for boundaries in self.camera.boundaries[self.camera.index]:
            for margins in boundaries:
                if boundaries[0][1] == self.rect.bottom:
                    onPlatform = True
                margins[1] += resy
        if onPlatform:
            self.rect.y += resy

        # Islands and Stuff
        for boundary in self.camera.boundaries[self.camera.index]:
            if len(boundary) == 1:
                if self.rect.bottom + dy > boundary[0][1]:
                    self.vel_y = 0
                    dy = boundary[0][1] - self.rect.bottom
                    self.jump[0], self.jump[1] = False, False

            if len(boundary) == 2:
                if boundary[0][0] < self.rect.centerx < boundary[1][0]:
                    if self.rect.bottom <= boundary[0][1]:
                        if self.rect.bottom + dy > boundary[0][1]:
                            self.vel_y = 0
                            dy = boundary[0][1] - self.rect.bottom
                            self.jump[0], self.jump[1] = False, False

        return dx, dy

    def direction_system(self, key, target):
        # Ensure players face each other but not when moving
        if not self.dead:
            # Dash and Movement are separate
            if not self.dash and not self.attacking:
                # Flipping the character when moving
                if self.rect.centerx <= target.rect.centerx:
                    if not (key[pygame.key.key_code(self.control_keys[self.player-1]["left"])] or key[pygame.key.key_code(self.control_keys[self.player-1]["right"])] ):
                        self.flip = False
                    elif key[pygame.key.key_code(self.control_keys[self.player-1]["left"])]:
                        self.flip = True
                    elif key[pygame.key.key_code(self.control_keys[self.player-1]["right"])]:
                        self.flip = False

                elif self.rect.centerx > target.rect.centerx:
                    if not (key[pygame.key.key_code(self.control_keys[self.player-1]["right"])]  or key[pygame.key.key_code(self.control_keys[self.player-1]["left"])] ):
                        self.flip = True
                    elif key[pygame.key.key_code(self.control_keys[self.player-1]["left"])]:
                        self.flip = True
                    elif key[pygame.key.key_code(self.control_keys[self.player-1]["right"])]:
                        self.flip = False

            if self.dash:
                self.rect.x += 30 + (-60 * self.flip)

    # Attacks
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

    def attack_cooldown(self, attack):
        if attack not in self.attack_delay_list:
            return True
        else:
            if self.attack_delay_list[attack]["last_time_used"] is not None:
                if pygame.time.get_ticks() - self.attack_delay_list[attack]["last_time_used"] > self.attack_delay_list[attack]["delay"]:
                    return True
                else:
                    return False
            else:
                return True

    def shield_cooldown(self):
        if self.shield_health <= 0 and not self.shield_broken:
            self.shield_broken = True
            self.shield_cooldown_timer = pygame.time.get_ticks()
            self.block = False

        if self.shield_broken:
            if pygame.time.get_ticks() - self.shield_cooldown_timer > 4000:
                self.shield_health = 100
                self.shield_broken = False
                self.create_shield.current_color = pygame.Color(0, 0, 255)

    # Time
    def time_passed(self):
        return pygame.time.get_ticks() - self.update_time

class Ranged_Attack(pygame.sprite.Sprite):
    def __init__(self, flip, attack_animation_list, action, character_rect, character, opponent):
        super().__init__()
        self.screen = pygame.display.get_surface()

        # Data
        self.character = character
        self.opponent = opponent
        self.flip = flip
        self.attacking = True

        # Ranged Attacks
        self.attack_rect_list = []
        self.attacking_rectangle = None
        self.collision = False

        # Animations
        self.action = action
        self.frame_index = 0
        self.image = attack_animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.attack_animation_list = attack_animation_list

        # Clock
        self.update_time = pygame.time.get_ticks()

    def main(self, surface, offset, image_scale, target):
        self.mask_collisions(target)
        self.draw_ranged_attack(surface, offset, image_scale)
        self.update_ranged_attack(surface)
        self.attack_collisions(target)

    def draw_ranged_attack(self, surface, offset, image_scale):
        pass

    def update_ranged_attack(self, surface):
        pass

    def attack_collisions(self, target):
        pass

    def mask_collisions(self,target):
        self.mask = pygame.mask.from_surface(self.image)
        if self.rect.colliderect(target.rect):
            if self.mask.overlap(target.mask, (self.rect.x- target.rect.x, self.rect.y - target.rect.y)):
                self.collision = True

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


class Display_Character_Stats:
    def __init__(self, player, health, rect, stamina, sp_level):
        self.screen = pygame.display.get_surface()
        self.health = health
        self.stamina = stamina
        self.sp_level = sp_level
        self.player = player
        self.player_rect = rect
        self.player_image = load_image(rf"Images/Background Images/Player Stats/player_{self.player}.png")
        self.player_image = pygame.transform.scale_by(self.player_image, 0.2)

    def draw_everything(self, health, stamina, character_rect, sp_level):
        self.draw_player_label(character_rect)
        self.draw_health_bar(health)
        self.draw_health_label()
        self.draw_stamina_bar(stamina)
        self.draw_sp_bar(sp_level)

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
        text_surface = font.render(f"Health: {int(self.health)}%", False, "white")
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

    def draw_sp_bar(self, sp_level):
        self.sp_level = sp_level
        font = pygame.font.Font("./Fonts/retro.ttf", 40)
        text_surface = font.render(f"{int(self.sp_level)}%", False, "red")

        if self.player == 1: rect = pygame.Rect(150, 670, 300, 30)
        else: rect = pygame.Rect(900, 670, 300, 30)

        ratio = self.sp_level/300
        pygame.draw.rect(self.screen, "blue", (rect.x, rect.y, ratio * rect.width, rect.height))
        pygame.draw.rect(self.screen, "orange", rect, 2)
        self.screen.blit(text_surface, (rect.right + 20, rect.y - 5))


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = pos[0], pos[1]  # Getting the initial postions of the player
        self.vx, self.vy = random.randint(-4, 4), random.randint(-10, 0) * .1 # Setting random movement speeds for the particles
        self.rad = 10 # The radius is 10 pixels

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.rad) # Drawing the particles

    def update(self):
        # Updating the speed of the particles
        self.x += self.vx
        self.y += self.vy
        # 0.4% chance that the radius will decrease by 1
        if random.randint(0, 100) < 40:
            self.rad -= 1
        # If radius smaller than 0, then the sprite is killed
        if self.rad <= 0:
            self.kill()


class Dust(pygame.sprite.Group):
    def __init__(self, pos):
        pygame.sprite.Group.__init__(self)
        self.pos = pos # Getting the player's position
        for i in range(50): # Creating 50 particles
            self.add(Particle(self.pos))
        self.screen = pygame.display.get_surface()

    def update(self):
        # Updating the particles sprites and drawing them
        for particle in self.sprites():
            particle.update()
        self.draw()

    def draw(self):
        for particle in self.sprites():
            particle.draw(self.screen)