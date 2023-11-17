import pygame
from characters import Fighter, Ranged_Attack

class Renji(Fighter):
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
        self.extend_animation = None
        # Attacks
        self.attack_data = self.get_attack_data()

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
                if y == 0 or y == 1:  # 300x300
                    temp_img = sprite_sheet.subsurface(x * 300, y * 300, 300,
                                                       300)
                    # Starts at 0
                    # Ends at 600
                elif y == 2:  # 200x200
                    temp_img = sprite_sheet.subsurface(x * 200, y * 200 + 200, 200,
                                                       200)
                    # Starts at 600
                    # Ends at 800
                elif y == 3:  # 160x160
                    temp_img = sprite_sheet.subsurface(x * 160, y * 160 + 320, 160,
                                                       160)
                    # Starts at 800
                    # Ends at 960
                elif y == 4:  # 300x160
                    temp_img = sprite_sheet.subsurface(x * 300, y * 160 + 320, 300,
                                                       160)
                    # Starts at 960
                    # Ends at 1120
                elif y == 5:  # 200x200
                    temp_img = sprite_sheet.subsurface(x * 200, y * 200 + 120, 200,
                                                   200)
                    # Starts at 1120
                    # Ends at 1320
                else:
                    temp_img = sprite_sheet.subsurface(x * self.size[0], y * self.size[1] + 360, self.size[0],
                                                   self.size[1])
                    # Starts at 1320

                scaled_image = pygame.transform.scale(temp_img, (
                    self.size[0] * self.image_scale, self.size[1] * self.image_scale))

                # Make Attacks Bigger
                if y == 0 or y == 1:
                    scaled_image = pygame.transform.scale(temp_img, (
                        300 * self.image_scale, 300 * self.image_scale))
                if y == 2 or y == 5:
                    scaled_image = pygame.transform.scale(temp_img, (
                        200 * self.image_scale, 200 * self.image_scale))
                if y == 4:
                    scaled_image = pygame.transform.scale(temp_img, (
                        300 * self.image_scale, 160 * self.image_scale))

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
        if self.action == 0:
            if not self.flip:
                surface.blit(img, (
                    self.rect.x - ((self.offset[0] + 67) * self.image_scale),
                    self.rect.y - ((self.offset[1] + 74) * self.image_scale)))
            else:
                surface.blit(img, (
                    self.rect.x - ((self.offset[0] + 66) * self.image_scale * 1.07),
                    self.rect.y - ((self.offset[1] + 74) * self.image_scale)))

        elif self.action == 2:
            if not self.flip:
                surface.blit(img, (
                    self.rect.x - ((self.offset[0] + 20) * self.image_scale),
                    self.rect.y - ((self.offset[1] + 20) * self.image_scale)))
            else:
                surface.blit(img, (
                    self.rect.x - ((self.offset[0] + 20) * self.image_scale * 1.07),
                    self.rect.y - ((self.offset[1] + 20) * self.image_scale)))

        elif self.action == 5:
            if not self.flip:
                surface.blit(img, (
                    self.rect.x - (self.offset[0] * self.image_scale),
                    self.rect.y - ((self.offset[1] + 16) * self.image_scale)))
            else:
                surface.blit(img, (
                    self.rect.x - ((self.offset[0] + 45) * self.image_scale),
                    self.rect.y - ((self.offset[1] + 16) * self.image_scale)))

        else:
            if not self.flip:
                surface.blit(img, (
                    self.rect.x - (self.offset[0] * self.image_scale),
                    self.rect.y - (self.offset[1] * self.image_scale)))
            else:
                surface.blit(img, (
                    self.rect.x - (self.offset[0] * self.image_scale * 1.07),
                    self.rect.y - (self.offset[1] * self.image_scale)))

    # Attack Methods
    def get_attack_data(self):
        data ={
            "normal_attack": {"trigger": False, "cooldown": 80, "frame_index": 2, "damage": 1.7, "knockback": 1,
                              "action": 17, "range_attack": False,
                              "rect": pygame.Rect(self.rect.centerx - 30 - (120 * self.flip), self.rect.y - 20, 180,
                                                  1.2 * self.rect.height)},
            "normal_attack_up": {"trigger": False, "cooldown": 75, "frame_index": 2, "damage": 1.6, "knockback": 1,
                                 "action": 16, "range_attack": False,
                                 "rect": pygame.Rect(self.rect.centerx - 80 - (70 * self.flip), self.rect.y - 50, 230,
                                                  50 + self.rect.height)},
            "normal_attack_down": {"trigger": False, "cooldown": 55, "frame_index": 3, "damage": 1.8, "knockback": 1,
                                   "action": 10, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - 140, self.rect.y + 70, 280, 90)},
            "normal_jump_attack": {"trigger": False, "cooldown": 85, "frame_index": 2, "damage": 1.4, "knockback": 1,
                                   "action": 18, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - 70 - (40 *self.flip), self.rect.y + 20, 180, 160)},
            "normal_attack_forward": {"trigger": False, "cooldown": 70, "frame_index": 2, "damage": 1, "knockback": 1,
                                      "action": 14, "range_attack": False,
                                      "rect": pygame.Rect(self.rect.centerx - 30 - (110 * self.flip), self.rect.y - 30,
                                                          170, self.rect.height + 60)},
            "strong_attack": {"trigger": False, "cooldown": 90,
                              "frame_index": self.frame_index == 2 or self.frame_index == 5, "damage": 5,
                              "knockback": 1, "action": 9, "range_attack": False,
                              "rect": pygame.Rect(self.rect.centerx - 70 - (120 * self.flip), self.rect.y - 25, 260,
                                                  30 + self.rect.height)},
            "strong_attack_up": {"trigger": False, "cooldown": 100, "frame_index": 5 <= self.frame_index <= 8,
                                 "damage": 2, "knockback": 1, "action": 6, "range_attack": False,
                                 "rect": pygame.Rect(self.rect.centerx - 135 + (10 * self.flip), self.rect.y - 40, 260,
                                                     0.4 * self.rect.height)},
            "strong_attack_down": {"trigger": False, "cooldown": 90, "frame_index": 3 <= self.frame_index <= 5,
                                   "damage": 1.5, "knockback": 1, "action": 7, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - 20 - (140 * self.flip), self.rect.y + 20, 180, 140)},
            "strong_jump_attack": {"trigger": False, "cooldown": 70, "frame_index": 3 <= self.frame_index <= 7,
                                   "damage": 2.75, "knockback": 1, "action": 5, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - (190 * self.flip), self.rect.y + 60, 190,
                                                       90 + self.rect.height)},
            "special_attack": {"trigger": False, "cooldown": 110, "frame_index": 2 <= self.frame_index <= 7,
                               "damage": 5, "knockback": 1, "action": 0, "range_attack": False,
                               "rect": pygame.Rect(self.rect.centerx - 200 - (180 * self.flip), self.rect.y - 50, 580,
                                                   70 + self.rect.height)},
            "special_attack_up": {"trigger": False, "cooldown": 110, "frame_index": 4, "damage": 26, "knockback": 1,
                                  "action": 11, "range_attack": False,
                                  "rect": pygame.Rect(self.rect.centerx - 130, self.rect.y - 150, 260,
                                                      150 + self.rect.height)},
            "special_attack_down": {"trigger": False, "cooldown": 110, "frame_index": 3 <= self.frame_index <= 12,
                                    "damage": 2.5, "knockback": 1, "action": 2, "range_attack": False,
                                    "rect": pygame.Rect(self.rect.centerx - 240, self.rect.y - 50,
                                                        480, 100 + self.rect.height)}
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
            # Continuous knockback and effects
            if target.hit and not target.dead:
                if self.attack_data["special_attack"]["trigger"]:
                    target.rect.x += 2 + (-4 * self.flip)

            # Normal
            if self.attack_data["normal_attack"]["trigger"]:
                if self.frame_index == 1:
                    self.rect.x += 5 - (12 * self.flip)

            if self.attack_data["normal_jump_attack"]["trigger"]:
                if 1 <= self.frame_index <= 2:
                    self.rect.x += 2.5 - (5 * self.flip)
                    self.rect.y += 5

            # Strong
            if self.attack_data["strong_attack"]["trigger"]:
                if 1 <= self.frame_index <= 7:
                    self.rect.x += 5 - (10 * self.flip)

            if self.attack_data["strong_jump_attack"]["trigger"]:
                if 3 <= self.frame_index <= 6:
                    self.rect.y -= 3
                    self.rect.x -= 3 - (6 * self.flip)

            if self.attack_data["strong_attack_down"]["trigger"]:
                if self.frame_index == 1:
                    self.extend_animation = pygame.time.get_ticks()

                if self.frame_index >= 2:
                    if pygame.time.get_ticks() - self.extend_animation < 400:
                        self.frame_index = 2

                    if self.frame_index == 2:
                        self.rect.x += 5 - (10 * self.flip)

        def attack_triggers():
            if self.frame_index < len(self.animation_list[self.action]):
                for attack in self.attack_data.values():
                    if attack["trigger"]:
                        self.frame_index_counter[1] = self.frame_index
                        if self.frame_index_counter[1]-self.frame_index_counter[0]>=1\
                                and (self.frame_index == attack["frame_index"] or attack["frame_index"] == True):
                            self.attack_rectangle_collision(surface, target)
                            self.frame_index_counter = [self.frame_index, self.frame_index]

        # Checks For Attacks
        if self.attacking:
            # Knockback + other continuous effects
            attack_effects()

            # Initialize the attacks
            attack_triggers()

    # Update sprites and stats
    def update(self, target, surface):
        # Keeps proper track of attack triggers.
        self.update_attack_data()

        if self.health <= 0:
            self.health = 0
            self.dead = True
            self.update_action(19)
        elif self.knockback:
            self.update_action(8)
        elif self.hit:
            self.update_action(21)
        elif self.attacking:
            for attack in self.attack_data.values():
                if attack["trigger"]:
                    self.update_action(attack["action"])
        elif self.dash:
            self.update_action(23)
        elif (self.jump[0] == True) or (self.jump[1] == True):
            self.update_action(13)
        elif self.running:
            self.update_action(12)
        elif self.block:
            self.update_action(22)
        else:
            self.update_action(20)  # IDLE

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

