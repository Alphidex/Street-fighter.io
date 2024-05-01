import pygame
from characters import Fighter, Ranged_Attack

class Sanji(Fighter):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, character_name, ai):
        super().__init__(player, x, y, flip, data, sprite_sheet, animation_steps, character_name, ai)

        # Animations - 16 Rows 17 columns
        # Idle
        self.action = 18
        self.frame_index = 0
        self.attacking_rectangle = None
        self.knockback_frame_index = 4
        # Animations
        self.animation_list = self.load_images(sprite_sheet, animation_steps, "animations")
        self.projectile_list = self.load_images(sprite_sheet, animation_steps, "projectiles")
        self.image = self.animation_list[self.action][self.frame_index]
        # Attacks
        self.attack_data = self.get_attack_data()

    #  Image Methods
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
                scaled_image = pygame.transform.scale(temp_img, (
                    self.size[0] * self.image_scale, self.size[1] * self.image_scale))

                temp_animation_img_list.append(scaled_image)

            projectile_list.append(temp_projectile_img_list)
            animation_list.append(temp_animation_img_list)

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
                self.rect.x - (self.offset[0] * self.image_scale),
                self.rect.y - (self.offset[1] * self.image_scale)))
        else:
            surface.blit(img, (
                self.rect.x - (self.offset[0] * self.image_scale * 1.36),
                self.rect.y - (self.offset[1] * self.image_scale)))

    # Attack Methods
    def get_attack_data(self):
        data = {
            "normal_attack": {"trigger": False, "cooldown": 80, "frame_index": 2, "damage": 1.3, "knockback": 1,
                              "action": 15, "range_attack": False,
                              "rect": pygame.Rect(self.rect.centerx - 75 + (10 * self.flip), self.rect.y - 20, 140,
                                                  1.2 * self.rect.height)},
            "normal_attack_up": {"trigger": False, "cooldown": 75, "frame_index": 3, "damage": 1.7, "knockback": 1,
                                 "action": 14, "range_attack": False,
                                 "rect": pygame.Rect(self.rect.centerx - 50 - (10 * self.flip), self.rect.y - 30, 110,
                                                     0.8 * self.rect.height)},
            "normal_attack_down": {"trigger": False, "cooldown": 55, "frame_index": 2 <= self.frame_index <= 5,
                                   "damage": 0.5, "knockback": 0.2, "action": 13, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - 70 + (10 * self.flip), self.rect.y + 20, 130, 140)},
            "normal_jump_attack": {"trigger": False, "cooldown": 85, "frame_index": 1 <= self.frame_index <= 4,
                                   "damage": 0.3, "knockback": 0.3, "action": 10, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - 40 - (50 * self.flip), self.rect.y - 10, 130,
                                                       self.rect.height + 30)},
            "normal_attack_forward": {"trigger": False, "cooldown": 70, "frame_index": 3, "damage": 1, "knockback": 1,
                                      "action": 11, "range_attack": False,
                                      "rect": pygame.Rect(self.rect.centerx - (1.35 * self.rect.width * self.flip),
                                                          self.rect.y - 30, 1.35 * self.rect.width,
                                                          0.4 * self.rect.height)},

            "strong_attack": {"trigger": False, "cooldown": 90, "frame_index": 3 <= self.frame_index, "damage": 2,
                              "knockback": 1, "action": 6, "range_attack": False,
                              "rect": pygame.Rect(self.rect.centerx - 100 - (30 * self.flip), self.rect.y - 20, 230,
                                                  -40 + self.rect.height)},
            "strong_attack_up": {"trigger": False, "cooldown": 100, "frame_index": 3 <= self.frame_index <= 4,
                                 "damage": 3, "knockback": 1, "action": 12, "range_attack": False,
                                 "rect": pygame.Rect(self.rect.centerx - 18 - (74 * self.flip), self.rect.y - 20, 110, 138)},
            "strong_attack_down": {"trigger": False, "cooldown": 90, "frame_index": 1 <= self.frame_index <= 8,
                                   "damage": 1, "knockback": 1, "action": 7, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - 100 + (20 * self.flip), self.rect.y + 10, 180, 100)},
            "strong_jump_attack": {"trigger": False, "cooldown": 70, "frame_index": 1 <= self.frame_index,
                                   "damage": 1.25, "knockback": 1, "action": 16, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.x - (30 * self.flip), self.rect.y, 130,
                                                       20 + self.rect.height)},

            "special_attack": {"trigger": False, "cooldown": 110, "frame_index": 3 <= self.frame_index <= 24,
                               "damage": 2, "knockback": 1, "action": 1, "range_attack": False,
                               "rect": pygame.Rect(self.rect.centerx - 75 - (5 * self.flip), self.rect.y - 20, 155,
                                                   30 + self.rect.height)},
            "special_attack_up": {"trigger": False, "cooldown": 110, "frame_index": 6 <= self.frame_index <= 14,
                                  "damage": 5, "knockback": 1, "action": 2, "range_attack": False,
                                  "rect": pygame.Rect(self.rect.centerx - 80 - (20 * self.flip),
                                                      self.rect.y - 110, 180, 110 + self.rect.height)},
            "special_attack_down": {"trigger": False, "cooldown": 110, "frame_index": 3 <= self.frame_index <= 41,
                                    "damage": 1.25, "knockback": 1, "action": 0, "range_attack": False,
                                    "rect": pygame.Rect(self.rect.centerx - 70 - (20 * self.flip),
                                                        self.rect.y - 20, 160, 30 + self.rect.height)}
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
        def attack_effects():
            # Normal
            if self.attack_data["normal_attack"]["trigger"]:
                if 1 <= self.frame_index <= 4:
                    self.rect.x += 2 - (4 * self.flip)

            if self.attack_data["normal_attack_down"]["trigger"]:
                if self.frame_index == 1:
                    self.position_checkpoint = self.rect.centerx
                    self.attack_effect_executions = 0

                if self.frame_index >= 2:
                    if self.attack_effect_executions == 0:
                        if abs(self.rect.centerx - self.position_checkpoint) < 100:
                            self.rect.x += 4 - (8 * self.flip)
                        else:
                            self.position_checkpoint = self.rect.centerx
                            self.attack_effect_executions = 1

                    if self.attack_effect_executions == 1:
                        if abs(self.rect.centerx - self.position_checkpoint) < 200:
                            self.rect.x -= 4 - (8 * self.flip)
                        else:
                            self.attack_effect_executions = 2

                        # In case it collides with wall to prevent infinite loop
                        if self.rect.left <= 0 or self.rect.right >= self.screen.get_width():
                            self.attack_effect_executions = 2

                    if self.attack_effect_executions < 2:
                        # Repeat animation
                        if self.frame_index > 5:
                            self.frame_index = 2

            if self.attack_data["normal_jump_attack"]["trigger"]:
                if self.frame_index <= 6:
                    self.rect.x += 4 - (8 * self.flip)
                    self.rect.y += 6

            # Strong
            if self.attack_data["strong_attack"]["trigger"]:
                if self.frame_index == 3:
                    self.position_checkpoint = self.rect.centerx
                    self.attack_effect_executions = 0

                if self.frame_index >= 4:
                    if self.attack_effect_executions == 0:
                        if abs(self.rect.centerx - self.position_checkpoint) < 1000:
                            self.rect.x += 4 - (8 * self.flip)
                            # Repeat animation
                            if self.frame_index >= 8:
                                self.frame_index = 4

                    if self.rect.left <= 0 or self.rect.right >= self.screen.get_width():
                        self.attack_effect_executions = 1

            if self.attack_data["strong_attack_up"]["trigger"]:
                if 1 <= self.frame_index <= 3:
                    self.rect.y -= 5
                    self.vel_y = 0

            if self.attack_data["strong_attack_down"]["trigger"]:
                if self.frame_index > 0:
                    self.rect.x += 6 - (12 * self.flip)

            if self.attack_data["strong_jump_attack"]["trigger"]:
                if self.in_air:
                    self.rect.x += 6 - (12 * self.flip)
                    self.rect.y += 8
                    if self.frame_index == 4:
                        self.frame_index = 1

            # Special
            if self.attack_data["special_attack"]["trigger"]:
                if self.frame_index > 2:
                    self.rect.x += 6 - (12 * self.flip)
                if self.rect.x > target.rect.x:
                    self.flip = True
                else:
                    self.flip = False

                # Knockback
                if target.hit and not target.dead:
                    if self.attack_data["special_attack"]["trigger"]:
                        target.rect.x += 4 + (-8 * self.flip)

            if self.attack_data["special_attack_up"]["trigger"]:
                if self.frame_index == 6:
                    self.position_checkpoint = self.rect.centerx
                    self.attack_effect_executions = 0
                if self.frame_index >= 7:
                    if self.attack_effect_executions == 0:
                        if abs(self.rect.centerx - self.position_checkpoint) < 100:
                            self.rect.x += 4 - (8 * self.flip)
                        else:
                            self.position_checkpoint = self.rect.centerx
                            self.attack_effect_executions = 1

                    if self.attack_effect_executions == 1:
                        if abs(self.rect.centerx - self.position_checkpoint) < 200:
                            self.rect.x -= 4 - (8 * self.flip)
                        else:
                            self.attack_effect_executions = 2

                        # In case it collides with wall to prevent infinite loop
                        if self.rect.left <= 0 or self.rect.right >= self.screen.get_width():
                            self.attack_effect_executions = 2

                    if self.attack_effect_executions < 2:
                        # Repeat animation
                        if self.frame_index > 11:
                            self.frame_index = 7

                if self.rect.x > target.rect.x:
                    self.flip = True
                else:
                    self.flip = False

            if self.attack_data["special_attack_down"]["trigger"]:
                if self.frame_index > 3:
                    self.rect.x += 2 - (4 * self.flip)
                if self.rect.x > target.rect.x:
                    self.flip = True
                else:
                    self.flip = False

        def attack_triggers():
            # The attacking rectangle will only activate at certain frame_indexes (with some having varying DPS):
            if self.frame_index < len(self.animation_list[self.action]):
                for attack in self.attack_data.values():
                    if attack["trigger"]:
                        self.frame_index_counter[1] = self.frame_index
                        if abs(self.frame_index_counter[1]-self.frame_index_counter[0])>=1\
                                and (self.frame_index == attack["frame_index"] or attack["frame_index"] == True):
                            self.attack_rectangle_collision(surface, target)
                            self.frame_index_counter = [self.frame_index, self.frame_index]

        # Checks For Attacks
        if self.attacking:
            #Knockback + other continuous effects
            attack_effects()

            # Initialize the attacks
            attack_triggers()

    # Update the sprites and stats
    def update(self, target, surface):
        # Keeps proper track of attack triggers.
        self.update_attack_data()

        if self.health <= 0:
            self.health = 0
            self.dead = True
            self.update_action(19)
        elif self.knockback:
            pass
            # self.update_action(4)
        elif self.hit:
            self.update_action(4)
        elif self.attacking:
            for attack in self.attack_data.values():
                if attack["trigger"]:
                    self.update_action(attack["action"])
        elif self.dash:
            self.update_action(21)
        elif (self.jump[0] == True) or (self.jump[1] == True):
            self.update_action(8)
        elif self.running:
            self.update_action(9)
        elif self.block:
            self.update_action(20)
        else:
            self.update_action(17)  # IDLE

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

            # Continue holding the blocking animation
            elif self.block and (not self.attacking):
                self.frame_index = len(self.animation_list[self.action]) - 1

            else:
                self.frame_index = 0
                # if the attack animation is finished
                if self.attacking:
                    # Updating attack list
                    self.frame_index_counter = [-1, 0]
                    self.attack_effect_executions = 0

                    self.attacking = False
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