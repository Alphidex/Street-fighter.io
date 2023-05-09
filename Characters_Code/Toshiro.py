import pygame
from characters import Fighter, Ranged_Attack

class Toshiro(Fighter):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, character_name):
        super().__init__(player, x, y, flip, data, sprite_sheet, animation_steps, character_name)

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
        self.attack_data = {
            "normal_attack": {"trigger": False, "cooldown":100, "frame_index":2, "damage": 1, "knockback": 1, "action":17, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - 30 - (120 * self.flip),
                                              self.rect.y - 20, 180, 1.2 * self.rect.height)},
            "normal_attack_up": {"trigger": False, "cooldown":100, "frame_index":2, "damage": 1, "knockback": 1, "action":16, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - 100 - (50 * self.flip),
                                              self.rect.y - 75, 250, 1.65 * self.rect.height)},
            "normal_attack_down": {"trigger": False, "cooldown":100, "frame_index":4<=self.frame_index<=6, "damage": 1, "knockback": 1, "action":8, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - 110,
                                              self.rect.y + 20, 220, 140)},
            "normal_jump_attack": {"trigger": False, "cooldown":100, "frame_index":2, "damage": 1, "knockback": 1, "action":15, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - 80 - (10 * self.flip),
                                                   self.rect.y - 10, 170, self.rect.height - 40)},
            "normal_attack_forward": {"trigger": False, "cooldown": 100, "frame_index": 2, "damage": 1,"knockback": 1, "action":13, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - (1.35 * self.rect.width * self.flip),
                                              self.rect.y * 1.09, 1.35 * self.rect.width, 0.35 * self.rect.height)},
            "strong_attack": {"trigger": False, "cooldown":100, "frame_index":5<=self.frame_index<=8, "damage": 1, "knockback": 1, "action":6, "range_attack":False, "rect":pygame.Rect(self.rect.centerx - 70 - (120 * self.flip),
                                              self.rect.y - 25, 260, 1.2 * self.rect.height)},
            "strong_attack_up": {"trigger": False, "cooldown":100, "frame_index":4<=self.frame_index<=6, "damage": 1, "knockback": 1, "action":5, "range_attack":True, "rect": pygame.Rect(self.rect.centerx - 40 - (70 * self.flip),
                                              self.rect.y - 40, 150, 1 * self.rect.height)},
            "strong_attack_down": {"trigger": False, "cooldown":100, "frame_index":6, "damage": 1, "knockback": 1, "action":4, "range_attack":True, "rect": pygame.Rect(self.rect.centerx - 10 - (130 * self.flip),
                                              self.rect.y + 20, 150, 140)},
            "strong_jump_attack": {"trigger": False, "cooldown":100, "frame_index":4, "damage": 1, "knockback": 1, "action":9, "range_attack":True, "rect": pygame.Rect(self.rect.x - 30 - (140 * self.flip),
                                                   self.rect.y, 200, 1.4 * self.rect.height)},
            "special_attack": {"trigger": False, "cooldown":100, "frame_index":3<=self.frame_index<=7, "damage": 1, "knockback": 1, "action":10, "range_attack":False, "rect":pygame.Rect(self.rect.centerx - 100,
                                              self.rect.y - 50, 265, 1.3 * self.rect.height)},
            "special_attack_up": {"trigger": False, "cooldown":100, "frame_index":4, "damage": 1, "knockback": 1, "action":11, "range_attack":True, "rect": pygame.Rect(self.rect.centerx - 20,
                                                   self.rect.y - 20, 160, 40 + self.rect.height)},
            "special_attack_down": {"trigger": False, "cooldown":100, "frame_index":16<=self.frame_index<=19, "damage": 1, "knockback": 1, "action":0, "range_attack":True, "rect": pygame.Rect(self.rect.centerx - 120,
                                                   self.rect.y - 20, 240, 20 + self.rect.height)}
        }

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
                scaled_image = pygame.transform.scale(temp_img, (
                    self.size[0] * self.image_scale, self.size[1] * self.image_scale))

                temp_animation_img_list.append(scaled_image)
                temp_projectile_img_list.append(scaled_image)

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
                self.rect.x - (self.offset[0] * self.image_scale * 1.07),
                self.rect.y - (self.offset[1] * self.image_scale)))

        pygame.draw.rect(surface, (255, 0, 0), self.rect, 4)

    # Attack Methods
    def update_attack_data(self):
        # Continuous declaration to update the values like Rect Position and Trigger Values
        self.attack_data = {
            "normal_attack": {"trigger": False, "cooldown": 100, "frame_index": 2, "damage": 1, "knockback": 1,
                              "action": 17, "range_attack": False,
                              "rect": pygame.Rect(self.rect.centerx - 30 - (120 * self.flip),
                                                  self.rect.y - 20, 180, 1.2 * self.rect.height)},
            "normal_attack_up": {"trigger": False, "cooldown": 100, "frame_index": 2, "damage": 1, "knockback": 1,
                                 "action": 16, "range_attack": False,
                                 "rect": pygame.Rect(self.rect.centerx - 100 - (50 * self.flip),
                                                     self.rect.y - 75, 250, 1.65 * self.rect.height)},
            "normal_attack_down": {"trigger": False, "cooldown": 100, "frame_index": 4 <= self.frame_index <= 6,
                                   "damage": 1, "knockback": 1, "action": 8, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - 110,
                                                       self.rect.y + 20, 220, 140)},
            "normal_jump_attack": {"trigger": False, "cooldown": 100, "frame_index": 2, "damage": 1, "knockback": 1,
                                   "action": 15, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - 80 - (10 * self.flip),
                                                       self.rect.y - 10, 170, self.rect.height - 40)},
            "normal_attack_forward": {"trigger": False, "cooldown": 100, "frame_index": 2, "damage": 1, "knockback": 1,
                                      "action": 13, "range_attack": False,
                                      "rect": pygame.Rect(self.rect.centerx - (1.35 * self.rect.width * self.flip),
                                                          self.rect.y * 1.09, 1.35 * self.rect.width,
                                                          0.35 * self.rect.height)},
            "strong_attack": {"trigger": False, "cooldown": 100, "frame_index": 5 <= self.frame_index <= 8, "damage": 1,
                              "knockback": 1, "action": 6, "range_attack": False,
                              "rect": pygame.Rect(self.rect.centerx - 70 - (120 * self.flip),
                                                  self.rect.y - 25, 260, 1.2 * self.rect.height)},
            "strong_attack_up": {"trigger": False, "cooldown": 100, "frame_index": 4 <= self.frame_index <= 6,
                                 "damage": 1, "knockback": 1, "action": 5, "range_attack": True,
                                 "rect": pygame.Rect(self.rect.centerx - 40 - (70 * self.flip),
                                                     self.rect.y - 40, 150, 1 * self.rect.height)},
            "strong_attack_down": {"trigger": False, "cooldown": 100, "frame_index": 6, "damage": 1, "knockback": 1,
                                   "action": 4, "range_attack": True,
                                   "rect": pygame.Rect(self.rect.centerx - 10 - (130 * self.flip),
                                                       self.rect.y + 20, 150, 140)},
            "strong_jump_attack": {"trigger": False, "cooldown": 100, "frame_index": 4, "damage": 1, "knockback": 1,
                                   "action": 9, "range_attack": True,
                                   "rect": pygame.Rect(self.rect.x - 30 - (140 * self.flip),
                                                       self.rect.y, 200, 1.4 * self.rect.height)},
            "special_attack": {"trigger": False, "cooldown": 100, "frame_index": 3 <= self.frame_index <= 7,
                               "damage": 1, "knockback": 1, "action": 10, "range_attack": False,
                               "rect": pygame.Rect(self.rect.centerx - 100,
                                                   self.rect.y - 50, 265, 1.3 * self.rect.height)},
            "special_attack_up": {"trigger": False, "cooldown": 100, "frame_index": 4, "damage": 1, "knockback": 1,
                                  "action": 11, "range_attack": True, "rect": pygame.Rect(self.rect.centerx - 20,
                                                                                          self.rect.y - 20, 160,
                                                                                          40 + self.rect.height)},
            "special_attack_down": {"trigger": False, "cooldown": 100, "frame_index": 16 <= self.frame_index <= 19,
                                    "damage": 1, "knockback": 1, "action": 0, "range_attack": True,
                                    "rect": pygame.Rect(self.rect.centerx - 120,
                                                        self.rect.y - 20, 240, 20 + self.rect.height)}
        }
        for key, value in self.attack_triggers.items():
            if key in self.attack_data.keys():
                self.attack_data[key]["trigger"] = value["trigger"]

    def attack_rectangle_collision(self, surface, target):
        # HIT-BOXES
        self.update_attack_data()

        for attack in self.attack_data.values():
            if attack["trigger"]:
                self.attacking_rectangle = attack["rect"]

        if self.attacking_rectangle is not None:
            # Rectangle collisions
            if self.attacking_rectangle.colliderect(target.rect):
                target.hit = True
                target.frame_index = 0

                # Taking Damage
                for attack in self.attack_data.values():
                    if attack["trigger"]:
                        target.health -= attack["damage"]

                # Knock-back - Once
                if target.flip:
                    target.rect.x += 25
                    self.rect.x += 10
                else:
                    target.rect.x -= 25
                    self.rect.x -= 10

    def attacks_management(self, surface, target):
        if self.range_attack:
            for instance in self.ranged_attack_instance_list:
                instance.main(surface, self.offset, self.image_scale, target)

                # Remove the instance variable from both the list and the Class (Ranged Attacks)
                if not instance.attacking:
                    self.ranged_attack_instance_list.remove(instance)
                    del instance

            if len(self.ranged_attack_instance_list) == 0:
                self.range_attack = False

        def init_ranged_attack(action):
            # Initialise the range attack
            self.range_attack = True
            self.ranged_attack_instance_list.append("ranged_attack_instance_"
                                                    + str(len(self.ranged_attack_instance_list)))

            self.ranged_attack_instance_list[len(self.ranged_attack_instance_list) - 1] = \
                self.Ranged_Toshiro(self.flip, self.projectile_list, action, self.rect, "Toshiro")

        def attack_effects():
            # Continuous knockback and effects
            if target.hit and not target.dead:
                if self.attack_data["special_attack"]["trigger"]:
                    target.rect.x += 2 + (-4 * self.flip)

        def attack_triggers():
            # The attacking rectangle will only activate at certain frame_indexes (with some having varying DPS):
            if self.frame_index < len(self.animation_list[self.action]):
                for attack in self.attack_data.values():
                    if attack["trigger"]:
                        if not self.attack_list_trigger[self.frame_index]\
                                and (self.frame_index == attack["frame_index"] or attack["frame_index"] == True):
                            if attack["range_attack"]:
                                init_ranged_attack(attack["action"])
                            self.attack_rectangle_collision(surface, target)
                            self.attack_list_trigger[self.frame_index] = True

        if self.attacking:
            # Knockback + other continuous effects
            attack_effects()

            # Initialize the attacks
            attack_triggers()

        # For hit-box purposes
        if self.attacking_rectangle != None:
            pygame.draw.rect(surface, (0, 255, 0), self.attacking_rectangle, 2)

    # Update the sprites and stats
    def update(self, target, surface):
        # Keeps proper track of attack triggers.
        self.update_attack_data()

        if self.health <= 0:
            self.health = 0
            self.dead = True
            self.update_action(25)
        elif self.knockback:
            self.update_action(3)
        elif self.hit:
            self.update_action(21)
        elif self.attacking:
            for attack in self.attack_data.values():
                if attack["trigger"]:
                    self.update_action(attack["action"])
        elif self.dash:
            self.update_action(28)
        elif (self.jump[0] == True) or (self.jump[1] == True):
            self.update_action(12)
        elif self.running:
            self.update_action(7)
        elif self.block:
            self.update_action(27)
        else:
            self.update_action(23)

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
                    self.attack_list_trigger = [False]

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
        if new_action != self.action:
            # update the animation settings
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update_animation(self, target):
        animation_cooldown = 90
        if self.knockback:
            if self.time_passed() > 200:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

                if self.frame_index >= 6:
                    self.knockback = False
                    self.frame_index = 0
            self.rect.x += -10 + (20 * self.flip)
        elif self.hit:
            if self.time_passed() > 150:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

                if self.frame_index > 1:
                    self.hit = False

                    # If you're attacking but ure hit earlier
                    self.attacking = False

                    for attack in self.attack_data.values():
                        attack["trigger"] = False

        elif self.attacking:
            for attack in self.attack_data.values():
                if attack["trigger"]:
                    if self.time_passed() > attack["cooldown"]:
                        self.frame_index += 1
                        self.update_time = pygame.time.get_ticks()

        else:
            if (pygame.time.get_ticks() - self.update_time) > animation_cooldown:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

    # Time
    def time_passed(self):
        return pygame.time.get_ticks() - self.update_time

    class Ranged_Toshiro(Ranged_Attack):
        def __init__(self, flip, attack_animation_list, action, character_rect, character):
            super().__init__(flip, attack_animation_list, action, character_rect, character)

            # Create Rectangle
            self.rect = self.create_rectangle(character_rect)  # To check the position of the character

        def create_rectangle(self, character_rect):
            # Strong Attack Up
            if self.action == 24:
                rect = pygame.Rect(character_rect.centerx - (100 * self.flip),
                                   character_rect.y - 50, 100, 0.8 * character_rect.height)
            # Strong Attack Down
            elif self.action == 20:
                rect = pygame.Rect(character_rect.centerx - (100 * self.flip),
                                   character_rect.y + 20, 100, 0.5 * character_rect.height)
            # Jump Strong Attack
            elif self.action == 19:
                rect = pygame.Rect(character_rect.centerx - (260 * self.flip),
                                   character_rect.y + 50, 260, 1.1 * character_rect.height)
            # Special Attack Up
            elif self.action == 18:
                rect = pygame.Rect(character_rect.centerx - (260 * self.flip),
                                   character_rect.y - 90, 200, 90 + character_rect.height)
            # Special Attack Down
            elif self.action == 26:
                rect = pygame.Rect(character_rect.centerx - 170,
                                   character_rect.y - 90, 340, 90 + character_rect.height)
            else:
                rect = pygame.Rect(character_rect.centerx - (260 * self.flip),
                                   character_rect.y - 50, 260, 0.7 * character_rect.height)
            return rect

        def draw_ranged_attack(self, surface, offset, image_scale):
            # Drawing Ranged Attacks
            img = pygame.transform.flip(self.image, self.flip, False)

            # Strong Attack Up
            if self.action == 24:
                surface.blit(img, (
                    self.rect.x - ((offset[0] - 7) * image_scale),
                    self.rect.y - ((offset[1] + 12) * image_scale)))
                pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)

            # Strong Attack Down
            elif self.action == 20:
                surface.blit(img, (
                    self.rect.x - (offset[0] * image_scale),
                    self.rect.y - ((offset[1] + 10) * image_scale)))
                pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)

            # Strong Jump Attack
            elif self.action == 19:
                surface.blit(img, (
                    self.rect.x - ((offset[0] - 20) * image_scale),
                    self.rect.y - ((offset[1] + 13) * image_scale)))
                pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)

            # Special Attack Up
            elif self.action == 18:
                surface.blit(img, (
                    self.rect.x - ((offset[0] - 20) * image_scale),
                    self.rect.y - ((offset[1] - 15) * image_scale)))
                pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)

            # Special Attack Down
            elif self.action == 26:
                surface.blit(img, (
                    self.rect.x - ((offset[0] - 45) * image_scale),
                    self.rect.y - ((offset[1] - 20) * image_scale)))
                pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)

            else:
                surface.blit(img, (
                    self.rect.x - (offset[0] * image_scale),
                    self.rect.y - ((offset[1] + 30) * image_scale)))
                pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)



        def update_ranged_attack(self, surface):
            animation_cooldown = 160
            # Refresh the image
            self.image = self.attack_animation_list[self.action][self.frame_index]

            # Increments the frame index
            if (pygame.time.get_ticks() - self.update_time) > animation_cooldown:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

            # Max index - Before collision
            if self.action == 20:  # Strong Attack Down
                if self.frame_index >= 1 and not self.collision:
                    self.frame_index = 1
            if self.action == 18:  # Special Up
                if self.frame_index >= 2 and not self.collision:
                    self.frame_index = 2

            if self.frame_index >= len(self.attack_animation_list[self.action]):
                # Strong Attack Up
                if self.action == 24:
                    self.frame_index = 3
                # Strong Jump Attack
                elif self.action == 19:
                    self.frame_index = 3
                else:
                    self.frame_index = 0

            # Image movement
            if self.action == 24:  # Strong Attack Up
                self.rect.x += 2 + (-4 * self.flip)
                self.rect.y -= 1.8
            elif self.action == 20 and self.frame_index == 3:  # Strong Attack Down
                self.rect.x = 1650 - (3200 * self.flip)
            elif self.action == 19:  # Strong Jump
                self.rect.y += 2
                self.rect.x += 2 + (-4 * self.flip)
            elif self.action == 18 and self.frame_index == 4:  # Special Up
                self.rect.x = 1650 - (3200 * self.flip)
            elif self.action == 26:
                if self.frame_index == 2:  # Special Up
                    self.rect.x = 1650 - (3200 * self.flip)
            else:
                self.rect.x += 2 + (-4 * self.flip)

            # Boundary
            if self.rect.left >= 1280 or self.rect.right <= 0:
                self.attacking = False

        def attack_collisions(self, target):
            if self.rect.colliderect(target.rect):
                if self.collision == False:
                    self.collision = True
                    target.hit = True
                    target.health -= 5
                    # Knock-back
                    if target.flip:
                        target.rect.x += 25
                    else:
                        target.rect.x -= 25