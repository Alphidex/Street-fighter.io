import pygame
from characters import Fighter, Ranged_Attack

class Uryu(Fighter):
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
                if y == 0:
                    temp_img = sprite_sheet.subsurface(x * 250, y * 250, 250,
                                                   250)
                    scaled_image = pygame.transform.scale(temp_img, (
                        250 * self.image_scale, 250 * self.image_scale))
                else:
                    temp_img = sprite_sheet.subsurface(x * self.size[0], y * self.size[1] + 90, self.size[0],
                                                       self.size[1])
                    scaled_image = pygame.transform.scale(temp_img, (
                        self.size[0] * self.image_scale, self.size[1] * self.image_scale))

                temp_projectile_img_list.append(scaled_image)
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
                self.rect.x - (self.offset[0] * self.image_scale * 1.3),
                self.rect.y - (self.offset[1] * self.image_scale)))

    # Attack Methods
    def get_attack_data(self):
        data = {
            "normal_attack": {"trigger": False, "cooldown": 100, "frame_index": 4, "damage": 1.4, "knockback": 1,
                              "action": 9, "range_attack": True, "range_attack_action": 7},
            "normal_attack_up": {"trigger": False, "cooldown": 100, "frame_index": 3, "damage": 1.4, "knockback": 1,
                                 "action": 19, "range_attack": True, "range_attack_action": 20},
            "normal_attack_down": {"trigger": False, "cooldown": 100, "frame_index": 4, "damage": 1.6, "knockback": 1,
                                   "action": 8, "range_attack": True, "range_attack_action": 11},
            "normal_jump_attack": {"trigger": False, "cooldown": 100, "frame_index": 3, "damage": 1.3, "knockback": 1,
                                   "action": 22, "range_attack": True, "range_attack_action": 23},
            "normal_attack_forward": {"trigger": False, "cooldown": 100, "frame_index": 3, "damage": 1, "knockback": 1,
                                      "action": 14, "range_attack": True, "range_attack_action": 7},
            "strong_attack": {"trigger": False, "cooldown": 100, "frame_index": 4, "damage": 8, "knockback": 1,
                              "action": 10, "range_attack": True, "range_attack_action": 7},
            "strong_attack_up": {"trigger": False, "cooldown": 100, "frame_index": 3, "damage": 7, "knockback": 1,
                                 "action": 12, "range_attack": True, "range_attack_action": 3},
            "strong_attack_down": {"trigger": False, "cooldown": 100, "frame_index": 2 <= self.frame_index <= 6,
                                   "damage": 2, "knockback": 1, "action": 5, "range_attack": True,
                                   "range_attack_action": 25},
            "strong_jump_attack": {"trigger": False, "cooldown": 100, "frame_index": 4, "damage": 6, "knockback": 1,
                                   "action": 18, "range_attack": True, "range_attack_action": 6},
            "special_attack": {"trigger": False, "cooldown": 100, "frame_index": 9, "damage": 24, "knockback": 1,
                               "action": 2, "range_attack": True, "range_attack_action": 1},
            "special_attack_up": {"trigger": False, "cooldown": 100, "frame_index": 3, "damage": 27, "knockback": 1,
                                  "action": 4, "range_attack": True, "range_attack_action": 11},
            "special_attack_down": {"trigger": False, "cooldown": 100, "frame_index": 0, "damage": 29, "knockback": 1,
                                    "action": 21, "range_attack": True, "range_attack_action": 0}
        }
        return data

    def update_attack_data(self):
        # Continuous declaration to update the values like Rect Position and Trigger Values
        self.attack_data = self.get_attack_data()

        for key, value in self.attack_triggers.items():
            if key in self.attack_data.keys():
                self.attack_data[key]["trigger"] = value["trigger"]

    def attacks_management(self, surface, target):
        if self.range_attack:
            for attack in self.ranged_group.sprites():
                attack.main(surface, self.offset, self.image_scale, target)

            if len(self.ranged_group.sprites()) <= 0:
                self.range_attack = False

        def attack_triggers():
            # The attacking rectangle will only activate at certain frame_indexes (with some having varying DPS):
            if self.frame_index < len(self.animation_list[self.action]):
                for attack in self.attack_data.values():
                    if attack["trigger"]:
                        self.frame_index_counter[1] = self.frame_index
                        if self.frame_index_counter[1]-self.frame_index_counter[0]>=1\
                                and self.frame_index == attack["frame_index"]:
                            self.range_attack = True
                            self.ranged_group.add(self.Ranged_Uryu(self.flip, self.projectile_list, attack["range_attack_action"], self.rect, "Uryu",self.opponent, self.attack_data))
                            self.frame_index_counter = [self.frame_index, self.frame_index]

        # Checks For Attacks
        if self.attacking:
            # Initialize the attacks
            attack_triggers()

    # Update the sprites and stats
    def update(self, target, surface):
        # Keeps proper track of attack triggers.
        self.update_attack_data()

        if self.health <= 0:
            self.health = 0
            self.dead = True
            self.update_action(24)
        elif self.knockback:
            self.update_action(16)
        elif self.hit:
            self.update_action(27)
        elif self.attacking:
            for attack in self.attack_data.values():
                if attack["trigger"]:
                    self.update_action(attack["action"])
        elif self.dash:
            self.update_action(26)
        elif (self.jump[0] == True) or (self.jump[1] == True):
            self.update_action(17)
        elif self.running:
            self.update_action(15)
        elif self.block:
            self.update_action(28)
        else:
            self.update_action(24)

        # Update Image ------------------------------------------
        self.image = self.animation_list[self.action][self.frame_index]

        self.update_animation(target)

        # Checks for attacks like when it happens, etc.
        self.attacks_management(surface, target)

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

    class Ranged_Uryu(Ranged_Attack):
        def __init__(self, flip, attack_animation_list, action, character_rect, character, opponent, attack_data):
            super().__init__(flip, attack_animation_list, action, character_rect, character, opponent)

            # Create Rectangle
            self.rect = self.create_rectangle(character_rect)  # To check the position of the character

            # Modifiers
            self.special_frameIndex_1 = 0
            self.special_frameIndex_2 = 3
            self.special_rangeImage_1 = self.attack_animation_list[self.action][self.special_frameIndex_1]
            self.special_rangeImage_2 = self.attack_animation_list[self.action][self.special_frameIndex_2]

            # Attack
            self.attack_data = attack_data

        def create_rectangle(self, character_rect):
            if self.action == 0:  # Special Down
                rect = pygame.Rect(character_rect.centerx - 280,
                                   character_rect.y - 50, 560, 50 + character_rect.height)
            elif self.action == 1:  # Special Attack
                rect = pygame.Rect(character_rect.centerx - (200 * self.flip),
                                   character_rect.y + 20, 200, 140)

            elif self.action == 7:  # Strong Attack or Normal
                rect = pygame.Rect(character_rect.centerx - (140 * self.flip),
                                   character_rect.y + 20, 140, 74)

            elif self.action == 23:  # Normal Jump Attack
                rect = pygame.Rect(character_rect.centerx - (120 * self.flip),
                                   character_rect.y + 40, 120, -30 + character_rect.height)

            elif self.action == 20:  # Normal Up
                rect = pygame.Rect(character_rect.centerx - (120 * self.flip),
                                   character_rect.y - 80, 120, -30 + character_rect.height)

            elif self.action == 6:  # Strong Jump Attack
                rect = pygame.Rect(character_rect.centerx - 10 - (40 * self.flip),
                                   character_rect.bottom - 20, 60, character_rect.height)

            elif self.action == 3:  # Strong Up
                rect = pygame.Rect(character_rect.centerx - 20 - (20 * self.flip),
                                   character_rect.y - 100, 60, character_rect.height)

            elif self.action == 25:  # Strong Down
                rect = pygame.Rect(character_rect.centerx - (100 * self.flip),
                                   character_rect.y, 100, character_rect.height)

            elif self.action == 11:  # Special Up or Normal Down
                rect = pygame.Rect(character_rect.centerx - (140 * self.flip),
                                   character_rect.y, 140, 70)

            else:
                rect = pygame.Rect(character_rect.centerx - (220 * self.flip),
                                   character_rect.y + 30, 220, 80)

            return rect

        def draw_ranged_attack(self, surface, offset, image_scale):
            # Drawing Ranged Attacks
            img = pygame.transform.flip(self.image, self.flip, False)

            # Special Down
            if self.action == 0:
                surface.blit(img, (
                    self.rect.x - ((offset[0] - 43) * image_scale),
                    self.rect.y - ((offset[1] + 17) * image_scale)))

            # Special Attack
            elif self.action == 1:
                # The first effect
                img_1 = pygame.transform.flip(self.special_rangeImage_1, self.flip, False)

                # The second effect
                img_2 = pygame.transform.flip(self.special_rangeImage_2, self.flip, False)

                surface.blit(img_1, (
                    self.rect.x - ((offset[0] + 7) * image_scale),
                    self.rect.y - (offset[1] * image_scale)))

                surface.blit(img_2, (
                    self.rect.x - (offset[0] * image_scale),
                    self.rect.y - (offset[1] * image_scale)))

            # Normal Attack + Strong Attack
            elif self.action == 7 or self.action == 11:
                surface.blit(img, (
                    self.rect.x - (offset[0] * image_scale),
                    self.rect.y - ((offset[1] + 17) * image_scale)))

            # Normal Jump Attack
            elif self.action == 23 or self.action == 20:
                surface.blit(img, (
                    self.rect.x - (offset[0] * image_scale),
                    self.rect.y - ((offset[1] + 5) * image_scale)))

            # Strong Jump Attack
            elif self.action == 6:
                surface.blit(img, (
                    self.rect.x - ((offset[0] + 15) * image_scale),
                    self.rect.y - (offset[1] * image_scale)))

            # Strong Up
            elif self.action == 3:
                surface.blit(img, (
                    self.rect.x - ((offset[0] + 15) * image_scale),
                    self.rect.y - (offset[1] * image_scale)))

            # Strong Down
            elif self.action == 25:
                surface.blit(img, (
                    self.rect.x - ((offset[0] + 10) * image_scale),
                    self.rect.y - (offset[1] * image_scale)))

            else:
                surface.blit(img, (
                    self.rect.x - (offset[0] * image_scale),
                    self.rect.y - (offset[1] * image_scale)))

        def update_ranged_attack(self, surface):
            # Refresh the image
            self.image = self.attack_animation_list[self.action][self.frame_index]

            # Special Attack Mess-up
            if self.action == 1:
                self.special_rangeImage_1 = self.attack_animation_list[self.action][self.special_frameIndex_1]
                self.special_rangeImage_2 = self.attack_animation_list[self.action][self.special_frameIndex_2]

                # Splitting the spritesheet in 2 images
                if self.special_frameIndex_1 >= 2:
                    self.special_frameIndex_1 = 0
                if self.special_frameIndex_2 >= 6:
                    self.special_frameIndex_2 = 3

            # Increments the frame index
            for attack in self.attack_data.values():
                if attack["trigger"]:
                    if pygame.time.get_ticks() - self.update_time > attack["cooldown"]:
                        self.frame_index += 1

                        # Special Attack
                        if self.action == 1:
                            self.special_frameIndex_1 += 1
                            self.special_frameIndex_2 += 1

                        self.update_time = pygame.time.get_ticks()

            # Frames Before Collision
            if (self.action == 7 or self.action == 6 or self.action == 3) and not self.collision:
                if self.frame_index == 3:
                    self.frame_index = 0

            if self.action == 11:
                if not self.collision:
                    if self.frame_index >= 3:
                        self.frame_index = 3
                else:
                    if self.frame_index >= 5:
                        self.frame_index = 5

            # If the end of the animation is reached:
            if self.frame_index >= len(self.attack_animation_list[self.action]):
                self.frame_index = 0

                if self.action in [6, 3, 25, 0]:
                    self.kill()

            # Image movement
            # Jump Normal Attack
            if self.action == 23:
                self.rect.x += 8 + (-16 * self.flip)
                self.rect.y += 9

            # Normal Attack Up
            elif self.action == 20:
                self.rect.x += 9 + (-18 * self.flip)
                self.rect.y -= 10

            # Jump Strong
            elif self.action == 6:
                self.rect.y += 12

            # Strong Up
            elif self.action == 3:
                self.rect.y -= 12

            # Strong Up and Special Down
            elif self.action == 25 or self.action == 0:
                pass  # Do nothing

            else:
                self.rect.x += 10 + (-20 * self.flip)

            # Off the screen
            if self.action == 7 and self.frame_index == 7:
                self.kill()

            # Boundary
            if self.rect.left >= 1280 or self.rect.right <= 0:
                self.kill()

        def attack_collisions(self, target):
            if self.rect.colliderect(target.rect):
                if self.collision == False:
                    self.collision = True
                    for key, value in self.attack_data.items():
                        if value["trigger"]:
                            self.attack_name = key
                    if not target.block:
                        target.hit = True
                        target.health -= self.attack_data[self.attack_name]["damage"]
                    else:
                        target.shield_health -= 20

                    # Knock-back
                    target.rect.x+=25-50*self.flip
