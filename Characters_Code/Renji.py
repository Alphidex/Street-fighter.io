import pygame
from characters import Fighter, Ranged_Attack

class Renji(Fighter):
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

    # Extract images from Sprite Sheets
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
        else:
            if not self.flip:
                surface.blit(img, (
                    self.rect.x - (self.offset[0] * self.image_scale),
                    self.rect.y - (self.offset[1] * self.image_scale)))
            else:
                surface.blit(img, (
                    self.rect.x - (self.offset[0] * self.image_scale * 1.07),
                    self.rect.y - (self.offset[1] * self.image_scale)))

        pygame.draw.rect(surface, (255, 0, 0), self.rect, 4)

    def time_passed(self):
        return pygame.time.get_ticks() - self.update_time

    def attack(self, surface, target):
        # HIT-BOXES

        # Normal Attack Attacks
        if self.normal_attack:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - 30 - (120 * self.flip),
                                              self.rect.y - 20, 180, 1.2 * self.rect.height)
        elif self.normal_attack_forward:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - (1.35 * self.rect.width * self.flip),
                                              self.rect.y * 1.09, 1.35 * self.rect.width, 0.35 * self.rect.height)
        elif self.normal_attack_up:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - 100 - (50 * self.flip),
                                              self.rect.y - 75, 250, 1.65 * self.rect.height)
        elif self.normal_attack_down:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - 110,
                                              self.rect.y + 20, 220, 140)
        elif self.normal_jump_attack:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - 30 - (110 * self.flip),
                                                   self.rect.y - 30, 170, self.rect.height + 60)

        # Strong Attack Attacks
        elif self.strong_attack:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - 70,
                                              self.rect.y - 25, 260, 1.2 * self.rect.height)
        elif self.strong_attack_up:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - 135 + (10 * self.flip),
                                              self.rect.y - 40, 260, 0.4 * self.rect.height)
        elif self.strong_attack_down:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - 10,
                                              self.rect.y + 20, 140, 140)
        elif self.strong_jump_attack:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - (170 * self.flip),
                                                   self.rect.y + 60, 170, 1.4 * self.rect.height)
        # Special Attack Attacks
        elif self.special_attack:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - 240,
                                              self.rect.y - 50, 580, 1.3 * self.rect.height)
        elif self.special_attack_up:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - 130,
                                                   self.rect.y - 150, 260, 150 + self.rect.height)
        elif self.special_attack_down:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - 180 - (0 * self.flip),
                                                   self.rect.y - 50, 360, 150 + self.rect.height)
        # In case there's an error
        else:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - (1.7 * self.rect.width * self.flip),
                                              self.rect.y * 1.125, 1.75 * self.rect.width, 0.75 * self.rect.height)

        pygame.draw.rect(surface, (0, 255, 0), self.attacking_rectangle, 1)


        # Rectangle collisions
        if self.attacking_rectangle.colliderect(target.rect):
            target.hit = True
            target.frame_index = 0

            # Taking Damage
            # Normal Attack Attacks
            if self.normal_attack:
                target.health -= 1
            elif self.normal_attack_up:
                target.health -= 1
            elif self.normal_attack_down:
                target.health -= 2
            elif self.normal_jump_attack:
                target.health -= 2

            # Strong Attack Attacks
            elif self.strong_attack:
                target.health -= 2
            elif self.strong_attack_up:
                target.health -= 2
            elif self.strong_attack_down:
                target.health -= 2

            # Special Attack Attacks
            elif self.special_attack:
                target.health -= 4
            elif self.special_attack_up:
                target.health -= 4
            elif self.special_attack_down:
                target.health -= 4

            # Knock-back - Once
            if target.flip:
                target.rect.x += 25
                self.rect.x += 10
            else:
                target.rect.x -= 25
                self.rect.x -= 10

    def _update_animation(self, target):
        animation_cooldown = 90
        # Update the animations + adds animation cooldown (different values for different animations)
        if self.knockback:
            if (pygame.time.get_ticks() - self.update_time) > 200:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

                if self.frame_index >= 6:
                    self.knockback = False
                    self.frame_index = 0
            self.rect.x += -10 + (20 * self.flip)
        elif self.hit:
            if (pygame.time.get_ticks() - self.update_time) > 150:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

                if self.frame_index > 1:
                    self.hit = False

                    # If you're attacking but ure hit earlier
                    self.attacking = False
                    #
                    self.normal_attack = False
                    self.normal_attack_up = False
                    self.normal_attack_down = False
                    self.normal_combo_count = 0
                    self.normal_jump_attack = False
                    #
                    self.strong_attack = False
                    self.strong_attack_up = False
                    self.strong_attack_down = False
                    self.strong_jump_attack = False
                    #
                    self.special_attack = False
                    self.special_attack_down = False
                    self.special_attack_up = False

        # Normal Attack Attacks
        elif self.normal_attack:
            if (pygame.time.get_ticks() - self.update_time) > 200 : # 80:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        elif self.normal_attack_up:
            if (pygame.time.get_ticks() - self.update_time) > 200 :# 75:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        elif self.normal_attack_down:
            if (pygame.time.get_ticks() - self.update_time) > 200 :# 55:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        elif self.normal_jump_attack:
            if (pygame.time.get_ticks() - self.update_time) > 200 :## 85:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        # Strong Attack Attacks
        elif self.strong_attack:
            if (pygame.time.get_ticks() - self.update_time) > 200 :# 90:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        elif self.strong_attack_up:
            if (pygame.time.get_ticks() - self.update_time) > 200 :# 100:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        elif self.strong_attack_down:
            if (pygame.time.get_ticks() - self.update_time) > 200 :# 90:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        elif self.strong_jump_attack:
            if (pygame.time.get_ticks() - self.update_time) > 200 :# 70:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        # Special Attack Attacks
        elif self.special_attack:
            if (pygame.time.get_ticks() - self.update_time) > 200 :#110:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        elif self.special_attack_up:
            if (pygame.time.get_ticks() - self.update_time) > 300 :#110:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        elif self.special_attack_down:
            if (pygame.time.get_ticks() - self.update_time) > 300 :#110:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        else:
            if (pygame.time.get_ticks() - self.update_time) > animation_cooldown:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

    def _attack_checks(self, surface, target):
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
                self.Ranged_Attack(self.flip, self.projectile_list, action, self.rect, "Renji")

        # Checks For Attacks
        if self.attacking:
            # Continuous Knockback and effects
            # if target.hit and not target.dead:
            #     if self.special_attack:
            #         target.rect.x += 2 + (-4 * self.flip)

            # The attacking rectangle will only activate at certain frame_indexes (with some having varying DPS):
            if self.frame_index < len(self.animation_list[self.action]):
                # Normal Attacks
                if self.normal_attack:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 2:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True

                elif self.normal_attack_forward:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 2:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True

                elif self.normal_attack_up:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 2:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True

                elif self.normal_attack_down:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 3:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True

                elif self.normal_jump_attack:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 2:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True

                # Strong Attacks
                elif self.strong_attack:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 2 or self.frame_index == 5:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True

                elif self.strong_attack_up:
                    if self.attack_list_trigger[self.frame_index] == False and 5 <= self.frame_index <= 8:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True

                elif self.strong_attack_down:
                    if self.attack_list_trigger[self.frame_index] == False and 3 <= self.frame_index <= 5:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True

                elif self.strong_jump_attack:
                    if self.attack_list_trigger[self.frame_index] == False and 3 <= self.frame_index <= 7:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True

                # Special Attacks
                elif self.special_attack:
                    if self.attack_list_trigger[self.frame_index] == False and 2 <= self.frame_index <= 7:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True

                elif self.special_attack_up:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 4:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True

                elif self.special_attack_down:
                    if self.attack_list_trigger[self.frame_index] == False and 3 <= self.frame_index <= 12:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True


        # For hit-box purposes
        if self.attacking_rectangle != None:
            pygame.draw.rect(surface, (0, 255, 0), self.attacking_rectangle, 2)

    # Update the timer and sprite animations
    def update(self, target, surface):
        # Check what animation the player is performing
        # print("Character --> " + " Action:", self.action, "\n Frame Index:", self.frame_index, "\n\n")

        if self.health <= 0:
            self.health = 0
            self.dead = True
            self.update_action(19)
        elif self.knockback:
            self.update_action(8)
        elif self.hit:
            self.update_action(21)
        elif self.attacking:
            # Normal Attack Attacks
            if self.normal_attack:
                self.update_action(17)
            elif self.normal_attack_forward:
                self.update_action(14)
            elif self.normal_attack_up:
                self.update_action(16)
            elif self.normal_attack_down:
                self.update_action(10)
            elif self.normal_jump_attack:
                self.update_action(18)

                """ MIGHT ADD NORMAL ATTACK FORWARD """

            # Strong Attack Attacks
            elif self.strong_attack:
                self.update_action(9)
            elif self.strong_attack_up:
                self.update_action(6)
            elif self.strong_attack_down:
                self.update_action(7)
            elif self.strong_jump_attack:
                self.update_action(5)

            # Special Attack Attacks
            elif self.special_attack:
                self.update_action(0)
            elif self.special_attack_up:
                self.update_action(11)
            elif self.special_attack_down:
                self.update_action(2)

        elif self.dash:
            self.update_action(23)
        elif (self.jump[0] == True) or (self.jump[1] == True):
            self.update_action(12)
        elif self.running:
            self.update_action(13)
        elif self.block:
            self.update_action(22)
        else:
            self.update_action(20)  # IDLE

        animation_cooldown = 85

        # Update Image ------------------------------------------
        self.image = self.animation_list[self.action][self.frame_index]


        # Update the animation frame index at certain milliseconds
        self._update_animation(target)

        # Checks for attacks like when it happens, etc.
        self._attack_checks(surface, target)

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
                    #
                    self.normal_attack = False
                    self.normal_attack_forward = False
                    self.normal_attack_up = False
                    self.normal_attack_down = False
                    self.normal_jump_attack = False
                    #
                    self.strong_attack = False
                    self.strong_attack_up = False
                    self.strong_attack_down = False
                    self.strong_jump_attack = False
                    #
                    self.special_attack = False
                    self.special_attack_up = False
                    self.special_attack_down = False

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