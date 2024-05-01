import pygame
from characters import Fighter, Ranged_Attack

class Ichigo(Fighter):
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
        self.exclude_attacks = ["special_attack_down"]

    # Image methods
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

                # Make Special Attack Attack Up bigger
                if y == 5 and x >= 10:
                    scaled_image = pygame.transform.scale(temp_img, (
                    self.size[0] * self.image_scale * 1.3, self.size[1] * self.image_scale * 1.3))

                # Append the images to a list
                if (y == 0 and x>= 13) or (y == 2 and x >= 9) or (y == 3 and x >= 8) or (y == 4 and x >= 8) or (y == 5 and x >= 10):
                    temp_projectile_img_list.append(scaled_image)
                else:
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
                self.rect.x - (self.offset[0] * self.image_scale * 1.15),
                self.rect.y - (self.offset[1] * self.image_scale)))

    # Attack Methods
    def get_attack_data(self):
        data = {
            "normal_attack": {"trigger": False, "cooldown": 80, "frame_index": 2, "damage": 1.8, "knockback": 1,
                              "action": 13, "range_attack": False,
                              "rect": pygame.Rect(self.rect.centerx - 30 - (140 * self.flip), self.rect.y - 20, 200,
                                                  1.2 * self.rect.height)},
            "normal_attack_up": {"trigger": False, "cooldown": 75, "frame_index": 2, "damage": 2, "knockback": 1,
                                 "action": 10, "range_attack": False,
                                 "rect": pygame.Rect(self.rect.centerx - 140, self.rect.y - 105, 280,
                                                     1.65 * self.rect.height)},
            "normal_attack_down": {"trigger": False, "cooldown": 55, "frame_index": 4, "damage": 1.6, "knockback": 1,
                                   "action": 9, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - 140, self.rect.y + 70, 280, 90)},
            "normal_jump_attack": {"trigger": False, "cooldown": 85, "frame_index": 2, "damage": 1.3, "knockback": 1,
                                   "action": 15, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - 30 - (110 * self.flip), self.rect.y - 40,
                                                       170, self.rect.height + 60)},
            "normal_attack_forward": {"trigger": False, "cooldown": 60, "frame_index": 1, "damage": 1, "knockback": 1,
                                      "action": 14, "range_attack": False,
                                      "rect": pygame.Rect(self.rect.centerx - (1.35 * self.rect.width * self.flip),
                                                          self.rect.y * 1.09, 1.35 * self.rect.width,
                                                          0.35 * self.rect.height)},
            "strong_attack": {"trigger": False, "cooldown": 90, "frame_index": 4 <= self.frame_index <= 10, "damage": 0.5,
                              "knockback": 1, "action": 1, "range_attack": False,
                              "rect": pygame.Rect(self.rect.centerx - 150 + (20 * self.flip), self.rect.y - 42, 280,
                                                  0.6 * self.rect.height)},
            "strong_attack_up": {"trigger": False, "cooldown": 100, "frame_index": 3, "damage": 7.5, "knockback": 1,
                                 "action": 3, "range_attack": True,
                                 "rect": pygame.Rect(self.rect.centerx - (90 * self.flip), self.rect.y - 33, 90,
                                                     0.9 * self.rect.height)},
            "strong_attack_down": {"trigger": False, "cooldown": 90, "frame_index": 4, "damage": 8, "knockback": 1,
                                   "action": 8, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - 130, self.rect.y + 20, 260, 140)},
            "strong_jump_attack": {"trigger": False, "cooldown": 70, "frame_index": 3, "damage": 6, "knockback": 1,
                                   "action": 2, "range_attack": True,
                                   "rect": pygame.Rect(self.rect.centerx - 30 - (60 * self.flip), self.rect.y, 120,
                                                       self.rect.height)},
            "special_attack": {"trigger": False, "cooldown": 110, "frame_index": 7, "damage": 22, "knockback": 1,
                               "action": 0, "range_attack": True,
                               "rect": pygame.Rect(self.rect.centerx - (1.4 * self.rect.width * self.flip),
                                                   self.rect.y + 24, 1.4 * self.rect.width, 0.56 * self.rect.height)},
            "special_attack_up": {"trigger": False, "cooldown": 110, "frame_index": 5, "damage": 22, "knockback": 1,
                                  "action": 5, "range_attack": True,
                                  "rect": pygame.Rect(self.rect.centerx - 130, self.rect.y - 150, 260,
                                                      150 + self.rect.height)}
            # "special_attack_down": {"trigger": False, "cooldown": 110, "frame_index": 10, "damage": 1, "knockback": 1, "action": ?, "range_attack":, "rect": pygame.Rect(self.rect.centerx - 150 - (1 * self.flip),self.rect.y - 50, 300, 150 + self.rect.height)}
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

            if self.attack_data["normal_attack"]["trigger"]:
                if self.frame_index == 2:
                    self.rect.x += 2 - (4*self.flip)

        def attack_triggers():
            # The attacking rectangle will only activate at certain frame_indexes (with some having varying DPS):
            if self.frame_index < len(self.animation_list[self.action]):
                for attack in self.attack_data.values():
                    if attack["trigger"]:
                        self.frame_index_counter[1] = self.frame_index
                        if self.frame_index_counter[1] - self.frame_index_counter[0] >= 1 \
                                and (self.frame_index == attack["frame_index"] or attack["frame_index"] == True):
                            if attack["range_attack"]:
                                self.range_attack = True
                                self.ranged_group.add(
                                    self.Ranged_Ichigo(self.flip, self.projectile_list, self.action, self.rect, "Ichigo",
                                                      self.opponent))

                            self.attack_rectangle_collision(surface, target)
                            self.frame_index_counter = [self.frame_index, self.frame_index]

        if self.attacking:
            # Knockback + other continuous effects
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
            self.update_action(16)
        elif self.knockback:
            self.update_action(6)
        elif self.hit:
            self.update_action(17)
        elif self.attacking:
            for attack in self.attack_data.values():
                if attack["trigger"]:
                    self.update_action(attack["action"])
        elif self.dash:
            self.update_action(20)
        elif (self.jump[0] == True) or (self.jump[1] == True):
            self.update_action(7)
        elif self.running:
            self.update_action(12)
        elif self.block:
            self.update_action(19)
        else:
            self.update_action(18)  # IDLE

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
                self.frame_index = 1

            else:
                self.frame_index = 0
                # if the attack animation is finished
                if self.attacking:
                    # Updating attack list
                    self.frame_index_counter = [-1,0]

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


    class Ranged_Ichigo(Ranged_Attack):
        def __init__(self, flip, attack_animation_list, action, character_rect, character, opponent):
            super().__init__(flip, attack_animation_list, action, character_rect, character, opponent)
            self.attack_data = {
                3: {"name": "strong_attack_up", "damage": 12},
                2: {"name": "strong_jump_attack", "damage": 10},
                0: {"name": "special_attack", "damage": 22},
                5: {"name": "special_attack_up", "damage": 25}
            }

            # Create Rectangle
            self.rect = self.create_rectangle(character_rect)  # To check the position of the character

        def create_rectangle(self, character_rect):
            if self.character == "Ichigo":
                # Strong Attack Up
                if self.action == 3:
                    rect = pygame.Rect(character_rect.centerx - (150 * self.flip),
                                   character_rect.y - 50, 150, 1.3 * character_rect.height)

                # Strong Jump Attack
                elif self.action == 2:
                    rect = pygame.Rect(character_rect.centerx - (150 * self.flip),
                                       character_rect.y - 50, 150, 1.3 * character_rect.height)

                # Special Attack
                elif self.action == 0:
                    rect = pygame.Rect(character_rect.centerx - (150 * self.flip),
                                       character_rect.y - 100, 150, 1.75 * character_rect.height)

                # Special Attack Up
                elif self.action == 5:
                    rect = pygame.Rect(character_rect.centerx - 150 + (40 * self.flip),
                                       character_rect.y - 50, 260, 0.7 * character_rect.height)
            return rect

        def draw_ranged_attack(self, surface, offset, image_scale):
            # Drawing Ranged Attacks
            img = pygame.transform.flip(self.image, self.flip, False)

            if self.character == "Ichigo":
                if self.action == 3:
                    surface.blit(img, (
                        self.rect.x - (offset[0] * image_scale),
                        self.rect.y - ((offset[1] - 10) * image_scale)))
                elif self.action == 0:
                    surface.blit(img, (
                        self.rect.x - (offset[0] * image_scale),
                        self.rect.y - ((offset[1] - 25) * image_scale)))
                elif self.action == 5:
                    surface.blit(img, (
                        self.rect.x - (offset[0] * image_scale),
                        self.rect.y - ((offset[1] + 30) * image_scale)))
                else:
                    surface.blit(img, (
                        self.rect.x - (offset[0] * image_scale),
                        self.rect.y - (offset[1] * image_scale)))

        def update_ranged_attack(self, surface):
            animation_cooldown = 160
            # Refresh the image
            self.image = self.attack_animation_list[self.action][self.frame_index]

            if self.character == "Ichigo":
                # Increments the frame index
                if (pygame.time.get_ticks() - self.update_time) > animation_cooldown:
                    self.frame_index += 1
                    self.update_time = pygame.time.get_ticks()

                # If the end of the animation is reached:
                if self.frame_index >= len(self.attack_animation_list[self.action]):
                    self.frame_index = len(self.attack_animation_list[self.action]) - 2

                if self.action == 2:
                    # Image movement
                    self.rect.x += 6 + (-12 * self.flip)
                    self.rect.y += 8

                elif self.action == 3:
                    # Image movement
                    self.rect.x += 6 + (-12 * self.flip)
                    self.rect.y -= 8

                elif self.action == 5:
                    self.rect.y -= 8

                else:
                    # Image movement
                    self.rect.x += 9 + (-18 * self.flip)

            if self.rect.left >= 1280 or self.rect.right <= 0:
                self.kill()

        def attack_collisions(self, target):
            if self.rect.colliderect(target.rect):
                if self.collision == False:
                    self.collision = True
                    if not target.block:
                        target.hit = True
                        target.health -= self.attack_data[self.action]["damage"]
                    else:
                        target.shield_health -= 20
                    # Knock-back
                    target.rect.x += 25-(50*self.flip)