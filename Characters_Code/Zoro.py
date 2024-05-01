import pygame
from characters import Fighter, Ranged_Attack

class Zoro(Fighter):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, character_name, ai):
        super().__init__(player, x, y, flip, data, sprite_sheet, animation_steps, character_name, ai)

        # Animations - 23 Rows
        self.action = 20
        self.frame_index = 0
        self.knockback_frame_index = 4
        # Animations
        self.animation_list = self.load_images(sprite_sheet, animation_steps, "animations")
        self.projectile_list = self.load_images(sprite_sheet, animation_steps, "projectiles")
        self.image = self.animation_list[self.action][self.frame_index]
        # Attack
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
                # Some sprites have been cropped differently
                if y < 6:
                    temp_img = sprite_sheet.subsurface(x * self.size[0], y * self.size[1], self.size[0], self.size[1])
                    scaled_image = pygame.transform.scale(temp_img, (
                        self.size[0] * self.image_scale, self.size[1] * self.image_scale))
                elif y == 6:  # Since the sprites here have different sizes
                    temp_img = sprite_sheet.subsurface(x * 165, y * 165, 165, 165)
                    scaled_image = pygame.transform.scale(temp_img, (165 * self.image_scale, 165 * self.image_scale))
                else:
                    temp_img = sprite_sheet.subsurface(x * self.size[0], y * self.size[1] + 5, self.size[0],
                                                       self.size[1])
                    scaled_image = pygame.transform.scale(temp_img, (
                        self.size[0] * self.image_scale, self.size[1] * self.image_scale))

                # Extract the animations for the ranged attack
                if (y == 4 and x >= 8) or (y == 8 and x >= 7):
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
        img = pygame.transform.flip(self.image, self.flip, False)
        if self.action == 14:
            surface.blit(img, (
                self.rect.x - ((self.offset[0] + 6) * self.image_scale),
                self.rect.y - ((self.offset[1] + 40) * self.image_scale)))
        else:
            if not self.flip:
                surface.blit(img, (
                    self.rect.x - (self.offset[0] * self.image_scale),
                    self.rect.y - ((self.offset[1] + 14) * self.image_scale)))
            else:
                surface.blit(img, (
                    self.rect.x - (self.offset[0] * self.image_scale * 1.3),
                    self.rect.y - ((self.offset[1] + 14) * self.image_scale)))

    # Attack Methods
    def get_attack_data(self):
        data = {
            "normal_attack": {"trigger": False, "cooldown": 60, "frame_index": 1, "damage": 1.6, "knockback": 1,
                              "action": 18, "range_attack": False,
                              "rect": pygame.Rect(self.rect.centerx - (175 * self.flip),
                                                  self.rect.y + 20, 175, 110)},
            "normal_attack_up": {"trigger": False, "cooldown": 60, "frame_index": 2, "damage": 1.8, "knockback": 1,
                                 "action": 15, "range_attack": False,
                                 "rect": pygame.Rect(self.rect.centerx - (120 * self.flip),
                                                     self.rect.y, 120, 170)},
            "normal_attack_down": {"trigger": False, "cooldown": 55, "frame_index": 3, "damage": 1.5, "knockback": 1,
                                   "action": 9, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - (140 * self.flip),
                                                       self.rect.y + 20, 140, 110)},
            "normal_jump_attack": {"trigger": False, "cooldown": 85, "frame_index": 3, "damage": 1.7, "knockback": 1,
                                   "action": 13, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - 25 - (110 * self.flip),
                                                       self.rect.y + 20, 160, 160)},

            "strong_attack": {"trigger": False, "cooldown": 90, "frame_index": 2 <= self.frame_index <= 11, "damage": 0.9,
                              "knockback": 1, "action": 1, "range_attack": False,
                              "rect": pygame.Rect(self.rect.centerx - 10 - (165 * self.flip),
                                                  self.rect.y + 20, 185, 110)},
            "strong_attack_up": {"trigger": False, "cooldown": 90, "frame_index": 1 <= self.frame_index <= 5,
                                 "damage": 1.2, "knockback": 1, "action": 14, "range_attack": False,
                                 "rect": pygame.Rect(self.rect.x - 30 - (120 * self.flip),
                                                     self.rect.y - 90, 180, 230)},
            "strong_attack_down": {"trigger": False, "cooldown": 90, "frame_index": 3, "damage": 7, "knockback": 1,
                                   "action": 4, "range_attack": True,
                                   "rect": pygame.Rect(self.rect.centerx - (140 * self.flip),
                                                       self.rect.y + 10, 140, 170)},
            "strong_jump_attack": {"trigger": False, "cooldown": 70, "frame_index": 3, "damage": 8, "knockback": 1,
                                   "action": 7, "range_attack": False,
                                   "rect": pygame.Rect(self.rect.centerx - 90 - (50 * self.flip),
                                                       self.rect.y + 30, 230, 150)},

            "special_attack": {"trigger": False, "cooldown": 100, "frame_index": 3 <= self.frame_index <= 11,
                               "damage": 3.5, "knockback": 1, "action": 5, "range_attack": False,
                               "rect": pygame.Rect(self.rect.centerx - (200 * self.flip),
                                                   self.rect.y + 20, 200, 120)},
            "special_attack_up": {"trigger": False, "cooldown": 100, "frame_index": 4, "damage": 30, "knockback": 1,
                                  "action": 0, "range_attack": False,
                                  "rect": pygame.Rect(self.rect.x - 65,
                                                      self.rect.y - 45, 240, 200)},
            "special_attack_down": {"trigger": False, "cooldown": 100, "frame_index": 3, "damage": 35, "knockback": 1,
                                    "action": 8, "range_attack": True,
                                    "rect": pygame.Rect(self.rect.centerx - (185 * self.flip),
                                                        self.rect.y, 185, 160)}
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
                    target.rect.x += 4 + (-8 * self.flip)
                if self.attack_data["special_attack"]["trigger"]:
                    target.rect.x += 5 + (-10 * self.flip)

            if self.attack_data["normal_attack"]["trigger"]:
                if 1 <= self.frame_index <= 2:
                    self.rect.x += 5 - (10 * self.flip)

            if self.attack_data["normal_attack_down"]["trigger"]:
                if 4 <= self.frame_index <= 5:
                    self.rect.x += 7 - (14 * self.flip)

            if self.attack_data["normal_jump_attack"]["trigger"]:
                if self.frame_index >= 2:
                    self.rect.x += 7 - (14 * self.flip)
                    self.rect.y += 9

            if self.attack_data["normal_attack_up"]["trigger"]:
                self.rect.x += 7 - (14 * self.flip)
                self.rect.y -= 7
                self.vel_y = 0

            # Strong
            if self.attack_data["strong_attack"]["trigger"]:
                self.rect.x += 8 - (16 * self.flip)

            # Special
            if self.attack_data["special_attack"]["trigger"]:
                if 3 <= self.frame_index <= 6:
                    self.rect.x += 8 - (16 * self.flip)


        def attack_triggers():
            # The attacking rectangle will only activate at certain frame_indexes (with some having varying DPS):
            if self.frame_index < len(self.animation_list[self.action]):
                for attack in self.attack_data.values():
                    if attack["trigger"]:
                        self.frame_index_counter[1] = self.frame_index
                        if self.frame_index_counter[1]-self.frame_index_counter[0]>=1\
                            and (self.frame_index == attack["frame_index"] or attack["frame_index"] == True):
                            if attack["range_attack"]:
                                self.range_attack = True
                                self.ranged_group.add(
                                    self.Ranged_Zoro(self.flip, self.projectile_list, self.action, self.rect, "Zoro",
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
            self.update_action(19)
        elif self.knockback:
            pass
        elif self.hit:
            self.update_action(2)
        elif self.attacking:
            for attack in self.attack_data.values():
                if attack["trigger"]:
                    self.update_action(attack["action"])
        elif self.dash:
            self.update_action(22)
        elif (self.jump[0] == True) or (self.jump[1] == True):
            self.update_action(17)
        elif self.running:
            self.update_action(12)
        elif self.block:
            self.update_action(21)
        else:
            self.update_action(20)

        # Update Image ------------------------------------------
        self.image = self.animation_list[self.action][self.frame_index]

        # Update the animation frame index at certain milliseconds
        self.update_animation(target)

        # Checks for attacks like when it happens, etc.
        self.attacks_management(surface, target)

        # If the end of animation is reached ...
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

    class Ranged_Zoro(Ranged_Attack):
        def __init__(self, flip, attack_animation_list, action, character_rect, character, opponent):
            super().__init__(flip, attack_animation_list, action, character_rect, character, opponent)

            # Create Rectangle
            self.rect = self.create_rectangle(character_rect)  # To check the position of the character

        def create_rectangle(self, character_rect):
            #  Strong Attack
            if self.action == 4:
                rect = pygame.Rect(character_rect.centerx - (1.7 * character_rect.width * self.flip),
                                                              character_rect.y + 50, 1.83 * character_rect.width,
                                                              0.5 * character_rect.height)
            # Special Attack
            elif self.action == 8:
                rect = pygame.Rect(character_rect.centerx - (1.7 * character_rect.width * self.flip),
                                   character_rect.y + 30, 1.9 * character_rect.width,
                                   0.7 * character_rect.height)

            return rect

        def draw_ranged_attack(self, surface, offset, image_scale):
            # Drawing Ranged Attacks
            img = pygame.transform.flip(self.image, self.flip, False)
            if self.action == 4:
                surface.blit(img, (
                    self.rect.x - (offset[0] * image_scale),
                    self.rect.y - 70 - (offset[1] * image_scale)))
            elif self.action == 8:
                surface.blit(img, (
                    self.rect.x - (offset[0] * image_scale),
                    self.rect.y - 50 - (offset[1] * image_scale)))
            else:
                surface.blit(img, (
                    self.rect.x - (offset[0] * image_scale),
                    self.rect.y - (offset[1] * image_scale)))

        def update_ranged_attack(self, surface):
            animation_cooldown = 160
            # Refresh the image
            self.image = self.attack_animation_list[self.action][self.frame_index]

            # Increments the frame index
            if (pygame.time.get_ticks() - self.update_time) > animation_cooldown:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

            # If the end of the animation is reached:
            if self.frame_index >= len(self.attack_animation_list[self.action]):
                self.frame_index = 0

            # Image movement
            self.rect.x += 15 + (-30 * self.flip)

            if self.rect.left >= 1280 or self.rect.right <= 0:
                self.kill()

        def attack_collisions(self, target):
            if self.rect.colliderect(target.rect):
                if self.collision == False:
                    self.collision = True
                    if not target.block:
                        target.hit = True
                        target.health -= 5
                    else:
                        target.shield_health -= 20

                    # Knock-back
                    target.rect.x+=25-50*self.flip