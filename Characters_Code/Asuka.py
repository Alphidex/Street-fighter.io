import pygame
from characters import Fighter, Ranged_Attack, Create_Shield


class Asuka(Fighter):
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

        # Attacks
        self.attack_data = self.get_attack_data()

        self.attack_delay_list = {
            "normal_jump_attack": {"last_time_used": None, "delay": 3000},
            "strong_jump_attack": {"last_time_used": None, "delay": 3000},
            "strong_attack": {"last_time_used": None, "delay": 3000}
        }
        self.exclude_attacks = ["special_attack_up", "special_attack_down"]

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
                temp_img = sprite_sheet.subsurface(x * self.size[0], y * self.size[1], self.size[0],
                                                   self.size[1])
                scaled_image = pygame.transform.scale(temp_img, (self.size[0] * self.image_scale,
                                                                 self.size[1] * self.image_scale))

                # Extract the animations for the ranged attack
                if (y == 0 and x >= 10) or (y == 1 and x >= 7) or (y == 6 and x >= 2):
                    temp_projectile_img_list.append(scaled_image)
                else:
                    temp_animation_img_list.append(scaled_image)

            animation_list.append(temp_animation_img_list)
            projectile_list.append(temp_projectile_img_list)

        if choice == "animations":
            return animation_list
        else:
            return projectile_list

    def draw(self, surface):
        # Drawing the animation
        img = pygame.transform.flip(self.image, self.flip, False)
        # DIF OFFSET LIST: 1. Action nr, 2. X - Value, 3. Y - Value
        if not self.flip:
            surface.blit(img, (
                self.rect.x - (self.offset[0] * self.image_scale * 1.23),
                self.rect.y - (self.offset[1] * self.image_scale)))
        else:
            surface.blit(img, (
                self.rect.x - (self.offset[0] * self.image_scale * 1.3),
                self.rect.y - (self.offset[1] * self.image_scale)))

    def get_attack_data(self):
        data = {
            "normal_attack": {"trigger": False, "cooldown": 60, "frame_index": 1, "damage": 3, "knockback": 1,
                              "action": 12, "range_attack": False,
                              "rect": pygame.Rect(self.rect.centerx - (150 * self.flip), self.rect.y + 10, 140,
                                                  0.5 * self.rect.height)},
            "normal_attack_up": {"trigger": False, "cooldown": 75, "frame_index": 3, "damage": 2, "knockback": 1,
                                 "action": 10, "range_attack": False,
                                 "rect": pygame.Rect(self.rect.centerx - 150, self.rect.y - 30, 300,
                                                     1.28 * self.rect.height)},
            "normal_attack_down": {"trigger": False, "cooldown": 55, "frame_index": 3, "damage": 5, "knockback": 1,
                                   "action": 9, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - (135 * self.flip), self.rect.y + 95, 135,
                                                       0.4 * self.rect.height)},
            "normal_jump_attack": {"trigger": False, "cooldown": 85, "frame_index": 1, "damage": 1.4, "knockback": 1,
                                   "action": 6, "range_attack": True, "rect": None},
            "strong_attack": {"trigger": False, "cooldown": 90, "frame_index": 3, "damage": 6, "knockback": 1,
                              "action": 1, "range_attack": True,
                              "rect": pygame.Rect(self.rect.centerx - (170 * self.flip), self.rect.y * 1.125, 175,
                                                  0.75 * self.rect.height)},
            "strong_attack_up": {"trigger": False, "cooldown": 80, "frame_index": 2, "damage": 5, "knockback": 1,
                                 "action": 8, "range_attack": False,
                                 "rect": pygame.Rect(self.rect.centerx - 60 - (30 * self.flip), self.rect.y - 30, 150,
                                                     1.28 * self.rect.height)},
            "strong_attack_down": {"trigger": False, "cooldown": 80, "frame_index": 7, "damage": 7, "knockback": 1,
                                   "action": 2, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx + 10 - (194 * self.flip), self.rect.y - 10,
                                                       174, self.rect.height)},
            "strong_jump_attack": {"trigger": False, "cooldown": 80, "frame_index": 1, "damage": 6, "knockback": 1,
                                   "action": 6, "range_attack": True, "rect": None},
            "special_attack": {"trigger": False, "cooldown": 100, "frame_index": 3, "damage": 25, "knockback": 1,
                               "action": 0, "range_attack": True,
                               "rect": pygame.Rect(self.rect.centerx - (170 * self.flip), self.rect.y - 20, 200,
                                                   0.87 * self.rect.height)}
        }
        return data

    # Attack Methods
    def update_attack_data(self):
        # Continuous declaration to update the values like Rect Position and Trigger Values
        self.attack_data = self.get_attack_data()

        for key, value in self.attack_triggers.items():
            if key in self.attack_data.keys():
                self.attack_data[key]["trigger"] = value["trigger"]

        for attack in self.attack_data.values():
            if attack["trigger"]:
                self.attacking_rectangle = attack["rect"]

    def attacks_management(self, surface, target):
        # Range Attacks Management
        if self.range_attack:
            for attack in self.ranged_group.sprites():
                attack.main(surface, self.offset, self.image_scale, target)

            if len(self.ranged_group.sprites()) <= 0:
                self.range_attack = False

        def attack_effects():
            # Continuous Attack Movement
            if self.attack_data["normal_attack_up"]["trigger"]:
                self.rect.y -= 4.5
                self.rect.x -= 3.5 - (7 * self.flip)
                self.vel_y = 0

            if self.attack_data["strong_attack_down"]["trigger"]:
                target.shield_health = 0

            if self.attack_triggers["strong_attack_up"]["trigger"] and self.attack_effect_executions < 1:
                if abs(self.opponent.rect.centerx - self.rect.centerx) <= 500:
                    self.rect.centerx = self.opponent.rect.centerx + 60 - (120 * self.flip)
                    self.flip = not self.flip
                    self.attack_effect_executions += 1

        def attack_triggers():
            # The attacking rectangle will only activate at certain frame_indexes (with some having varying DPS):
            if self.frame_index < len(self.animation_list[self.action]):
                for attack in self.attack_data.values():
                    if attack["trigger"]:
                        self.frame_index_counter[1] = self.frame_index
                        if self.frame_index_counter[1] - self.frame_index_counter[0] >= 1 and self.frame_index == attack["frame_index"]:
                            if attack["range_attack"]:
                                # Initialise the range attack
                                self.range_attack = True
                                self.ranged_group.add(self.Ranged_Asuka(self.flip, self.projectile_list, self.action, self.rect, "Asuka",self.opponent))
                            self.frame_index_counter = [self.frame_index, self.frame_index]
                            self.attack_rectangle_collision(surface, target)
                            # Attack Movement Per Frame:
                            if self.attack_data["normal_attack"]["trigger"]:
                                self.rect.x += 5 - (10 * self.flip)

        # Checks For Attacks
        if self.attacking:
            # Knockback + other continuous effects
            attack_effects()
            
            # Initialize the attacks 
            attack_triggers()

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

                # Push - Once
                if target.flip:
                    target.rect.x += 25
                    self.rect.x += 10
                else:
                    target.rect.x -= 25
                    self.rect.x -= 10

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
                self.attack_triggers["strong_attack_down"]["trigger"] = True
                self.rect.x += 80 - (160 * self.flip)
            elif self.normal_combo_count == 2:
                if abs(self.opponent.rect.centerx - self.rect.centerx) <= 500:
                    self.rect.centerx = self.opponent.rect.centerx + 60 - (120 * self.flip)
                    self.flip = not self.flip
                self.attack_triggers["strong_attack_up"]["trigger"] = True
        self.normal_combo_count += 1
        self.normal_combo_timer = pygame.time.get_ticks()

    # Update the sprites and character states
    def update(self, target, surface):
        # Keeps proper track of attack triggers.
        self.update_attack_data()

        if self.health <= 0:
            self.health = 0
            self.dead = True
            self.update_action(11)
        elif self.hit:
            self.update_action(7)
        elif self.attacking:
            for attack in self.attack_data.values():
                if attack["trigger"]:
                    self.update_action(attack["action"])
        elif self.dash:
            self.update_action(13)
        elif self.jump[0] or self.jump[1]:
            self.update_action(4)
        elif self.running:
            self.update_action(5)
        elif self.block:
            self.update_action(15)
        else:
            self.update_action(3)  # IDLE

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
                    # Updating attack list
                    self.frame_index_counter = [-1, 0]
                    self.attack_effect_executions = 0

                    for key, value in self.attack_data.items():
                        if key in self.attack_delay_list.keys():
                            if value["trigger"]:
                                self.attack_delay_list[key]["last_time_used"] = pygame.time.get_ticks()

                    self.attacking = False
                    for attack in self.attack_data.values():
                        attack["trigger"] = False
                    for attack in self.attack_triggers.values():
                        attack["trigger"] = False

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

    class Ranged_Asuka(Ranged_Attack):
        def __init__(self, flip, attack_animation_list, action, character_rect, character, opponent):
            super().__init__(flip, attack_animation_list, action, character_rect, character, opponent)
            self.attack_data = {
                0: {"name": "special_attack", "damage": 25},
                1: {"name": "strong_attack", "damage": 5},
                6: {"name": "aerial_attack", "damage": 5}}

            # Create Rectangle
            self.rect = self.create_rectangle(character_rect)  # To check the position of the character

        def create_rectangle(self, character_rect):
            # Special Attack
            if self.action == 0:
                rect = pygame.Rect(character_rect.centerx - (2.5 * character_rect.width * self.flip),
                                   character_rect.y - 55, 2.5 * character_rect.width,
                                   1.4 * character_rect.height)

            # Strong Attack
            if self.action == 1:
                rect = pygame.Rect(character_rect.centerx - (0.85 * character_rect.width * self.flip),
                                   character_rect.y + 20, 95, 85)
            # Aerial Attack
            elif self.action == 6:
                rect = pygame.Rect(character_rect.centerx - (1 * character_rect.width * self.flip),
                                   character_rect.y + 55, 1 * character_rect.width,
                                   0.55 * character_rect.height)
            return rect

        def draw_ranged_attack(self, surface, offset, image_scale):
            # Drawing Ranged Attacks
            img = pygame.transform.flip(self.image, self.flip, False)
            offset_x = offset[0] * image_scale
            offset_y = offset[0] * image_scale

            if self.action == 0 and self.attacking:  # Special
                surface.blit(img, (
                    self.rect.x + 35 - offset_x,
                    self.rect.y + 10 - offset_y))
            elif self.action == 1:  # Strong
                surface.blit(img, (
                    self.rect.x - offset_x - 55 + (55 * self.flip),
                    self.rect.y - 45 - offset_y))
            elif self.action == 6:  # Aerial
                surface.blit(img, (
                    self.rect.x - 40 - offset_x + (10 * self.flip),
                    self.rect.y - 50 - offset_y))

        def update_ranged_attack(self, surface):
            animation_cooldown = 140

            # Refresh the image
            self.image = self.attack_animation_list[self.action][self.frame_index]

            # Increments the frame index
            if (pygame.time.get_ticks() - self.update_time) > animation_cooldown:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

            if self.action == 0:  # If Special Attack
                # If no collision
                if not self.collision:
                    if self.frame_index >= 3:
                        self.frame_index = 0
                else:
                    # If the special attack collides, then the animation ends
                    if self.frame_index >= len(self.attack_animation_list[self.action]) - 1:
                        self.kill()
            else:
                # If the end of the animation is reached:
                if self.frame_index >= len(self.attack_animation_list[self.action]) - 2:
                    self.frame_index = len(self.attack_animation_list[self.action]) - 2

            # Image movement
            self.rect.x += 15 + (-30 * self.flip)

            # Kill Image if outside the boreders:
            if self.rect.left > self.screen.get_width():
                self.kill()
            if self.rect.right < 0:
                self.kill()

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
