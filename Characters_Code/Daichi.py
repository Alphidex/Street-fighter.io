import pygame
from characters import Fighter, Ranged_Attack
from debug import debug

class Daichi(Fighter):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, character_name, ai):
        super().__init__(player, x, y, flip, data, sprite_sheet, animation_steps, character_name, ai)

        # Animations - 16 Rows 17 columns
        # Idle
        self.action = 3
        self.frame_index = 0
        self.attacking_rectangle = None
        self.knockback_frame_index = 2
        # Animations
        self.animation_list = self.load_images(sprite_sheet, animation_steps, "animations")
        self.projectile_list = self.load_images(sprite_sheet, animation_steps, "projectiles")
        self.image = self.animation_list[self.action][self.frame_index]
        # Attacks
        self.attack_data = self.get_attack_data()
        self.exclude_attacks = ["special_attack_up"]

    # Image Methods
    def load_images(self, sprite_sheet, animation_steps, choice):
        animation_list = []
        projectile_list = []

        # Here y goes from 0 and then increments by 1 till the last animation
        # Here animations is the actual value (e.g: index 1 is 20)
        for y, animation in enumerate(animation_steps):
            temp_animation_img_list = []
            temp_projectile_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * (self.size[0]), y * (self.size[1]), self.size[0],
                                                   self.size[1])
                scaled_image = pygame.transform.scale(temp_img, (
                    self.size[0] * self.image_scale, self.size[1] * self.image_scale))

                # # Extract the animations for the ranged attack
                if (y == 0 and x >= 7) or (y == 1 and x >= 9):
                    temp_projectile_img_list.append(scaled_image)
                else:
                    temp_animation_img_list.append(scaled_image)

            animation_list.append(temp_animation_img_list)
            # Will create many empty lists (inefficient but acceptable)
            projectile_list.append(temp_projectile_img_list)

        if choice == "animations":
            return animation_list
        else:
            return projectile_list

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)

        if self.action == 10:
            if not self.flip:
                surface.blit(img, (
                    self.rect.x - (self.offset[0] * self.image_scale),
                    self.rect.y - ((self.offset[1] * self.image_scale) - 15)))
            else:
                surface.blit(img, (
                    self.rect.x - (self.offset[0] * self.image_scale),
                    self.rect.y - ((self.offset[1] * self.image_scale) - 15)))
        else:
            if not self.flip:
                surface.blit(img, (
                    self.rect.x - (self.offset[0] * self.image_scale),
                    self.rect.y - (self.offset[1] * self.image_scale)))
            else:
                surface.blit(img, (
                    self.rect.x - (self.offset[0] * self.image_scale),
                    self.rect.y - (self.offset[1] * self.image_scale)))

    # Attack Methods
    def get_attack_data(self):
        data = {
            "normal_attack": {"trigger": False, "cooldown": 140, "frame_index": 1, "damage": 1.7, "knockback": 1,
                              "action": 15, "range_attack": False,
                              "rect": pygame.Rect(self.rect.centerx - (1.35 * self.rect.width * self.flip),
                                                  self.rect.y * 1.125, 1.35 * self.rect.width, 0.5 * self.rect.height)},
            "normal_attack_up": {"trigger": False, "cooldown": 140, "frame_index": 2, "damage": 1.5, "knockback": 1,
                                 "action": 11, "range_attack": False,
                                 "rect": pygame.Rect(self.rect.centerx - 80 - (50 * self.flip), self.rect.y - 28, 220,
                                                     1.2 * self.rect.height)},
            "normal_attack_down": {"trigger": False, "cooldown": 140, "frame_index": 1, "damage": 1.6, "knockback": 1,
                                   "action": 10, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - (200 * self.flip), self.rect.y + 70, 200,
                                                       80)},
            "normal_jump_attack": {"trigger": False, "cooldown": 140, "frame_index": 3, "damage": 1.4, "knockback": 1,
                                   "action": 6, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - 30 - (30 * self.flip), self.rect.y - 20, 90,
                                                       self.rect.height + 40)},
            "strong_attack": {"trigger": False, "cooldown": 140, "frame_index": 2 <= self.frame_index <= 11, "damage": 0.7,
                              "knockback": 0.1, "action": 2, "range_attack": False,
                              "rect": pygame.Rect(self.rect.centerx - 150, self.rect.y + 10, 300, 105)},
            "strong_attack_up": {"trigger": False, "cooldown": 140, "frame_index": 6, "damage": 6.5, "knockback": 2,
                                 "action": 3, "range_attack": False,
                                 "rect": pygame.Rect(self.rect.centerx - 100 - (40 * self.flip), self.rect.y - 28, 240,
                                                     1.2 * self.rect.height)},
            "strong_attack_down": {"trigger": False, "cooldown": 140, "frame_index": 2 <= self.frame_index <= 5, "damage": 9, "knockback": 5,
                                   "action": 9, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - 30 - (30 * self.flip), self.rect.y - 20, 90,
                                                       self.rect.height + 40)},
            "strong_jump_attack": {"trigger": False, "cooldown": 140, "frame_index": 3 <= self.frame_index <= 5,
                                   "damage": 2, "knockback": 1, "action": 6, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - 30 - (30 * self.flip), self.rect.y - 20, 90,
                                                       self.rect.height + 40)},
            "special_attack": {"trigger": False, "cooldown": 140, "frame_index": 3, "damage": 20, "knockback": 1,
                               "action": 0, "range_attack": True,
                               "rect": pygame.Rect(self.rect.centerx - (1.7 * self.rect.width * self.flip),
                                                   self.rect.y - 10, 170, 10 + self.rect.height)},
            "special_attack_down": {"trigger": False, "cooldown": 140, "frame_index": 8, "damage": 30, "knockback": 1,
                                    "action": 1, "range_attack": True,
                                    "rect": None}
        }

        return data

    def update_attack_data(self):
        # Continuous declaration to update the values like Rect Position and Trigger Values
        self.attack_data = self.get_attack_data()

        for key, value in self.attack_triggers.items():
            if key in self.attack_data.keys():
                self.attack_data[key]["trigger"] = value["trigger"]

        for attack in self.attack_data.values():
            if attack["trigger"]:
                self.attacking_rectangle = attack["rect"]

    def attack_rectangle_collision(self, surface, target):
        # HIT-BOXES
        self.update_attack_data()

        if self.attacking_rectangle is not None:
            # Rectangle collisions
            if self.attacking_rectangle.colliderect(target.rect):
                if not target.block:
                    target.hit = True

                    # Taking Damage
                    for attack in self.attack_data.values():
                        if attack["trigger"]:
                            target.health -= attack["damage"]

                else:
                    target.shield_health -= 20

                # Knock-back - Once
                if target.flip:
                    target.rect.x += 25
                    self.rect.x += 10
                else:
                    target.rect.x -= 25
                    self.rect.x -= 10

    def attacks_management(self, surface, target):
        if self.range_attack:
            for attack in self.ranged_group.sprites():
                attack.main(surface, self.offset, self.image_scale, target)

            if len(self.ranged_group.sprites()) <= 0:
                self.range_attack = False

        def attack_effects():
            # Continuous knockback and effects
            if target.hit and not target.dead:
                if self.attack_data["special_attack"]["trigger"]:
                    target.rect.x += 2 + (-4 * self.flip)

            if self.attack_data["normal_jump_attack"]["trigger"] or self.attack_data["strong_jump_attack"]["trigger"]:
                if 1 < self.frame_index < 6:
                    if self.in_air:
                        self.rect.x += 2.5 - (5 * self.flip)
                        self.rect.y += 7
                        if self.frame_index > 4:
                            self.frame_index = 4

            # Normal
            if self.attack_data["normal_attack"]["trigger"]:
                if self.frame_index > 0:
                    self.rect.x += 2.5 - (5 * self.flip)

            if self.attack_data["normal_attack_up"]["trigger"]:
                if self.frame_index > 1:
                    self.rect.x += 4 - (8 * self.flip)

            if self.attack_data["normal_attack_down"]["trigger"]:
                if self.frame_index > 1:
                    self.rect.x += 8 - (16 * self.flip)

            # Strong
            if self.attack_data["strong_attack"]["trigger"]:
                if 1 < self.frame_index < 11:
                    self.rect.x += 3 - (6 * self.flip)

            if self.attack_data["strong_attack_up"]["trigger"]:
                if 5 < self.frame_index < 8:
                    self.rect.x += 3 - (6 * self.flip)

            if self.attack_data["strong_attack_down"]["trigger"]:
                if self.frame_index < 2:
                    self.rect.x += 4 - (8 * self.flip)
                    self.rect.y -= 8
                    self.vel_y = 0
                    if self.frame_index < 5:
                        self.rect.x += 6 - (12 * self.flip)

            # Special
            if self.attack_data["special_attack_down"]["trigger"]:
                if self.frame_index < 2:
                    self.rect.x += 3 - (6 * self.flip)

        def attack_triggers():
            # The attacking rectangle will only activate at certain frame_indexes (with some having varying DPS):
            if self.frame_index < len(self.animation_list[self.action]):
                for attack in self.attack_data.values():
                    if attack["trigger"]:
                        self.frame_index_counter[1] = self.frame_index
                        if self.frame_index_counter[1] - self.frame_index_counter[0] >= 1 \
                                and (self.frame_index == attack["frame_index"] or attack["frame_index"] == True):
                            if attack["range_attack"]:
                                # Initialise the range attack
                                self.range_attack = True
                                self.ranged_group.add(
                                    self.Ranged_Daichi(self.flip, self.projectile_list, self.action, self.rect, "Daichi",self.opponent))
                            self.frame_index_counter = [self.frame_index, self.frame_index]
                            self.attack_rectangle_collision(surface, target)

        # Checks For Attacks
        if self.attacking:
            # Knockback + other continuous effects
            attack_effects()

            # Initialize the attacks
            attack_triggers()

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
                self.attack_triggers["normal_attack_up"]["trigger"] = True
            elif self.normal_combo_count == 2:
                self.attack_triggers["strong_attack_down"]["trigger"] = True
        self.normal_combo_count += 1
        self.normal_combo_timer = pygame.time.get_ticks()

    # Update the sprites and character stats
    def update(self, target, surface):
        # Keeps proper track of attack triggers.
        self.update_attack_data()

        if self.health <= 0:
            self.health = 0
            self.dead = True
            self.update_action(12)
        elif self.hit:
            self.update_action(8)
        elif self.attacking:
            for attack in self.attack_data.values():
                if attack["trigger"]:
                    self.update_action(attack["action"])
        elif self.dash:
            self.update_action(16)
        elif (self.jump[0] == True) or (self.jump[1] == True):
            self.update_action(4)
        elif self.running:
            self.update_action(5)
        elif self.block:
            self.update_action(14)
        else:
            self.update_action(7)  # IDLE

        animation_cooldown = 85

        # Update Image ------------------------------------------
        self.image = self.animation_list[self.action][self.frame_index]

        # Update the animation frame index at certain milliseconds
        self.update_animation(target)

        # Checks for attacks like when it happens, etc.
        self.attacks_management(surface, target)

        # If the end of the animation is reached
        self.end_of_animation()

    def end_of_animation(self):
        # If the end of the animation is reached
        if self.frame_index >= len(self.animation_list[self.action]):
            # If dead then the last frame will keep playing
            if self.dead:
                self.frame_index = len(self.animation_list[self.action]) - 1

            elif self.block and (not self.attacking):
                self.frame_index = len(self.animation_list[self.action]) - 1

            else:
                self.frame_index = 0

                # if the attack animation is finished
                if self.attacking:
                    self.attacking = False
                    # Updating attack list
                    self.frame_index_counter = [-1, 0]
                    for attack in self.attack_data.values():
                        attack["trigger"] = False
                    for attack in self.attack_triggers.values():
                        attack["trigger"] = False

                # If dash is finished
                if self.dash:
                    self.dash = False

                if self.jumping:
                    self.jumping = False

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            # update the animation settings
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    # Time
    def time_passed(self):
        return pygame.time.get_ticks() - self.update_time

    class Ranged_Daichi(Ranged_Attack):
        def __init__(self, flip, attack_animation_list, action, character_rect, character, opponent):
            super().__init__(flip, attack_animation_list, action, character_rect, character, opponent)

            # Attacks
            self.stun_timer = 1500
            self.stun_time_started = None
            self.extend_animation = pygame.time.get_ticks()
            self.attack_data = {
                0: {"trigger": False, "name": "special_attack", "damage": 20, "animation_refresh_time": 150},
                1: {"trigger": False, "name": "special_attack_down", "damage": 23, "animation_refresh_time": 300}
            }

            # Create Rectangle
            self.rect = self.create_rectangle(character_rect)  # To check the position of the character

        def create_rectangle(self, character_rect):
            # Special Attack
            if self.action == 0:
                rect = pygame.Rect(character_rect.centerx - (2.2 * character_rect.width * self.flip),
                                   character_rect.y + 10, 2.2 * character_rect.width,
                                   1.2 * character_rect.height)

            # Special Attack  Down
            if self.action == 1:
                rect = pygame.Rect(character_rect.centerx - (1.5 * character_rect.width * self.flip),
                                   character_rect.y + 8, 1.5 * character_rect.width,
                                   1 * character_rect.height)
            return rect

        def draw_ranged_attack(self, surface, offset, image_scale):
            # Drawing Ranged Attacks
            img = pygame.transform.flip(self.image, self.flip, False)

            if self.action == 1 and self.frame_index >= 1:
                rect = img.get_bounding_rect()
                img = pygame.transform.scale(img, (rect.width * 3, rect.height * 3))

            if self.action == 0:
                surface.blit(img, (
                    self.rect.x - (offset[0] * image_scale) + 40,
                    self.rect.y - (offset[1] * image_scale) + 10))
            else:
                surface.blit(img, (
                    self.rect.x - (offset[0] * image_scale) + 40,
                    self.rect.y - (offset[1] * image_scale) - 10))

        def attack_effects(self):
            if self.action == 0:  # Special Attack
                if not self.collision:
                    if self.frame_index >= 3:
                        self.frame_index = 2
                else:
                    if pygame.time.get_ticks() - self.stun_time_started < self.stun_timer:
                        if self.frame_index >= 3:
                            self.frame_index = 3
                    else:
                        self.opponent.stun = False

                    if self.frame_index >= len(self.attack_animation_list[self.action]) - 1:
                        self.kill()

            if self.action == 1:  # Special Attack Down
                if self.frame_index > 0:
                    if pygame.time.get_ticks() - self.extend_animation < 1000:
                        self.frame_index = 0

                if self.frame_index >= len(self.attack_animation_list[self.action]) - 1:
                    self.frame_index = len(self.attack_animation_list[self.action]) - 1

            # Image movement
            self.rect.x += 15 + (-30 * self.flip)

            # Kill Image if outside the boreders:
            if self.rect.left > self.screen.get_width():
                self.kill()
            if self.rect.right < 0:
                self.kill()

        def update_ranged_attack(self, surface):
            # Refresh the image
            self.image = self.attack_animation_list[self.action][self.frame_index]

            if self.action == 0 or (self.action == 1 and self.frame_index >= 1):
                # Increments the frame index
                if (pygame.time.get_ticks() - self.update_time) > 150:
                    self.frame_index += 1
                    self.update_time = pygame.time.get_ticks()
            else:
                # Increments the frame index
                if (pygame.time.get_ticks() - self.update_time) > 300:
                    self.frame_index += 1
                    self.update_time = pygame.time.get_ticks()

            self.attack_effects()

        def attack_collisions(self, target):
            if self.rect.colliderect(target.rect):
                if not self.collision:
                    self.collision = True
                    if not target.block:
                        target.hit = True
                        target.health -= self.attack_data[self.action]["damage"]
                    else:
                        target.shield_health -= 20

                    # Knock-back
                    target.rect.x += 25 - (50 * self.flip)

                    if self.action == 0:
                        self.opponent.stun = True
                        self.stun_time_started = pygame.time.get_ticks()