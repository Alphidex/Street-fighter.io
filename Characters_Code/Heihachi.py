import pygame
from characters import *

class Heihachi(Fighter):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, character_name):
        super().__init__(player, x, y, flip, data, sprite_sheet, animation_steps, character_name)

        # Animations - 16 Rows 17 columns
        # Idle
        self.action = 16
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
                if y <= 1:
                    temp_img = sprite_sheet.subsurface(x * 300, y * 300, 300,
                                                       300)
                    scaled_image = pygame.transform.scale(temp_img, (
                        300 * self.image_scale, 300 * self.image_scale))
                else:
                    temp_img = sprite_sheet.subsurface(x * (self.size[0]), y * (self.size[1]) + 280, self.size[0],
                                                       self.size[1])
                    scaled_image = pygame.transform.scale(temp_img, (
                        self.size[0] * self.image_scale, self.size[1] * self.image_scale))

                # Extract the animations for the ranged attack
                if (y == 0 and x >= 11) or (y == 2 and x >= 7) or (y == 3 and x >= 10) or (y == 4 and x >= 7):
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
        # Special Attack Up and Down
        if self.action == 0 or self.action == 1:
            if not self.flip:
                surface.blit(img, (
                    self.rect.x - ((self.offset[0] + 67) * self.image_scale),
                    self.rect.y - ((self.offset[1] + 94) * self.image_scale)))
            else:
                surface.blit(img, (
                    self.rect.x - ((self.offset[0] + 60) * self.image_scale * 1.25),
                    self.rect.y - ((self.offset[1] + 94) * self.image_scale)))

        # Normal Attack Down
        elif self.action == 6:
            if not self.flip:
                surface.blit(img, (
                    self.rect.x - ((self.offset[0]) * self.image_scale),
                    self.rect.y - ((self.offset[1] + 50) * self.image_scale)))
            else:
                surface.blit(img, (
                    self.rect.x - ((self.offset[0]) * self.image_scale * 1.25),
                    self.rect.y - ((self.offset[1] + 50) * self.image_scale)))

        else:
            if not self.flip:
                surface.blit(img, (
                    self.rect.x - (self.offset[0] * self.image_scale),
                    self.rect.y - (self.offset[1] * self.image_scale)))
            else:
                surface.blit(img, (
                    self.rect.x - (self.offset[0] * self.image_scale * 1.25),
                    self.rect.y - (self.offset[1] * self.image_scale)))

        pygame.draw.rect(surface, (255, 0, 0), self.rect, 4)

    def time_passed(self):
        return pygame.time.get_ticks() - self.update_time

    def attack(self, surface, target):
        # HIT-BOXES

        # Normal Attack Attacks
        if self.normal_attack:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - (1.35 * self.rect.width * self.flip),
                                              self.rect.y * 1.09, 1.35 * self.rect.width, 0.35 * self.rect.height)
        elif self.normal_attack_up:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx + 25 - (120 * self.flip),
                                              self.rect.y - 100, 70, 1.35 * self.rect.height)
        elif self.normal_attack_down:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - 130,
                                              self.rect.y + 80, 260, 60)
        elif self.normal_jump_attack:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - 20 - (120 * self.flip),
                                                   self.rect.y - 20, 160, self.rect.height + 40)
        # Strong Attack Attacks
        elif self.strong_attack:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - (150 * self.flip),
                                              self.rect.y + 10, 150, 0.75 * self.rect.height)
        elif self.strong_attack_up:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - (90 * self.flip),
                                              self.rect.y - 33, 90, 0.9 * self.rect.height)
        elif self.strong_attack_down:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - 30 - (30 * self.flip),
                                              self.rect.y - 20, 90, self.rect.height + 40)
        elif self.strong_jump_attack:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - 30 - (60 * self.flip),
                                                   self.rect.y, 120, self.rect.height)
        # Special Attack Attacks
        elif self.special_attack:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - (1.4 * self.rect.width * self.flip),
                                              self.rect.y + 24, 1.4 * self.rect.width, 0.56 * self.rect.height)
        elif self.special_attack_up:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - 130,
                                                   self.rect.y - 150, 260, 150 + self.rect.height)
        elif self.special_attack_down:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - 150 - (1 * self.flip),
                                                   self.rect.y - 50, 300, 150 + self.rect.height)
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
            if (pygame.time.get_ticks() - self.update_time) > 80:
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
                self.Ranged_Heihachi(self.flip, self.projectile_list, action, self.rect, "Heihachi")

        # Checks For Attacks
        if self.attacking:
            # Continuous Knockback and effects
            # if target.hit and not target.dead:
            #     if self.special_attack:
            #         target.rect.x += 2 + (-4 * self.flip)

            # The attacking rectangle will only activate at certain frame_indexes (with some having varying DPS):
            if self.frame_index < len(self.animation_list[self.action]):
                # Normal Attack Attacks
                if self.normal_attack:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 1:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True
                elif self.normal_attack_up:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 2:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True
                elif self.normal_attack_down:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 1:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True
                elif self.normal_jump_attack:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 3:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True
                    # Some movement
                    if 3 < self.frame_index < 5:
                        self.rect.x -= 1.5 + (3 * self.flip)
                        self.rect.y -= 1 + (2 * self.flip)

                # Strong Attack Attacks
                elif self.strong_attack:
                    if self.attack_list_trigger[self.frame_index] == False and 2 <= self.frame_index <= 11:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True
                elif self.strong_attack_up:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 6:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True
                        # Initialise the range attack
                        init_ranged_attack(self.action)
                elif self.strong_attack_down:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 4:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True
                        # Initialise the range attack
                        init_ranged_attack(self.action)

                elif self.strong_jump_attack:
                    if self.attack_list_trigger[self.frame_index] == False and 3 <= self.frame_index <= 5:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True

                # Special Attack Attacks
                elif self.special_attack:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 9:
                        # Close attack part
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True
                        # Initialise the range attack
                        init_ranged_attack(self.action)

                elif self.special_attack_up:
                    self.attack(surface, target)
                    self.attack_list_trigger[self.frame_index] = True

                elif self.special_attack_down:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 10:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True

                        init_ranged_attack(self.action)

        # For hit-box purposes
        if self.attacking_rectangle != None:
            pygame.draw.rect(surface, (0, 255, 0), self.attacking_rectangle, 2)

    # Update the timer and sprite animations
    def update(self, target, surface):
        if self.health <= 0:
            self.health = 0
            self.dead = True
            self.update_action(15)
        elif self.knockback:
            pass
        elif self.hit:
            self.update_action(5)
        elif self.attacking:
            # Normal Attack Attacks
            if self.normal_attack:
                self.update_action(14)
            elif self.normal_attack_up:
                self.update_action(13)
            elif self.normal_attack_down:
                self.update_action(6)
            elif self.normal_jump_attack:
                self.update_action(8)

                """ MIGHT ADD NORMAL ATTACK FORWARD """

            # Strong Attack Attacks
            elif self.strong_attack:
                self.update_action(10)
            elif self.strong_attack_up:
                self.update_action(2)
            elif self.strong_attack_down:
                self.update_action(4)
            elif self.strong_jump_attack:
                self.update_action(7)

            # Special Attack Attacks
            elif self.special_attack:
                self.update_action(3)
            elif self.special_attack_down:
                self.update_action(0)
            elif self.special_attack_up:
                self.update_action(1)

        elif self.dash:
            self.update_action(19)
        elif (self.jump[0] == True) or (self.jump[1] == True):
            self.update_action(12)
        elif self.running:
            self.update_action(11)
        elif self.block:
            self.update_action(17)
        else:
            self.update_action(16)  # IDLE

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

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            # update the animation settings
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    class Ranged_Heihachi(Ranged_Attack):
        def __init__(self, flip, range_attack_animation_list, action, character_rect, character):
            super().__init__(flip, range_attack_animation_list, action, character_rect, character)

            # Create Rectangle
            self.rect = self.create_rectangle(character_rect)  # To check the position of the character

        def create_rectangle(self, character_rect):

            if self.character == "Heihachi":
                # Special Attack
                if self.range_action == 3:
                    rect = pygame.Rect(character_rect.centerx + 10 - (2 * character_rect.width * self.range_flip),
                                       character_rect.y + 5, 1.8 * character_rect.width,
                                       0.9 * character_rect.height)

                # Special Attack Down
                if self.range_action == 0:
                    rect = pygame.Rect(character_rect.centerx - (230 * self.range_flip),
                                       character_rect.y - 75, 230,
                                       75 + character_rect.height)

                # Strong Attack Up
                if self.range_action == 2:
                    rect = pygame.Rect(character_rect.centerx - (1.4 * character_rect.width * self.range_flip),
                                       character_rect.y + 15, 1.4 * character_rect.width,
                                       15 + character_rect.height)

                # Strong Attack Down
                if self.range_action == 4:
                    rect = pygame.Rect(character_rect.centerx - (1.5 * character_rect.width * self.range_flip),
                                       character_rect.y + 8, 1.5 * character_rect.width,
                                           1 * character_rect.height)
            return rect

        def draw_ranged_attack(self, surface, offset, image_scale):
            # Drawing Ranged Attacks
            img = pygame.transform.flip(self.range_image, self.range_flip, False)

            if self.character == "Heihachi":
                if self.range_action == 0:
                    surface.blit(img, (
                        self.rect.x - (offset[0] * image_scale + 150),
                        self.rect.y - (offset[1] * image_scale + 85)))
                    pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)

                else:
                    surface.blit(img, (
                        self.rect.x + 20 - (offset[0] * image_scale),
                        self.rect.y - (offset[1] * image_scale)))
                    pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)

        def update_ranged_attack(self, surface):
            animation_cooldown = 160
            # Refresh the image
            self.range_image = self.range_attack_animation_list[self.range_action][self.range_frame_index]

            if self.character == "Heihachi":
                # Increments the frame index
                if self.range_action == 2:  # Strong Attack Up
                    if (pygame.time.get_ticks() - self.update_time) > 120:
                        self.range_frame_index += 1
                        self.update_time = pygame.time.get_ticks()

                    # If the end of the animation is reached:
                    if self.range_frame_index >= len(self.range_attack_animation_list[self.range_action]):
                        self.range_frame_index -= 1
                        if self.range_flip:
                            self.rect.left = - 800
                        else:
                            self.rect.right = 1280 + 800

                elif self.range_action == 3:  # Special Attack
                    # Increments the frame index
                    if (pygame.time.get_ticks() - self.update_time) > 180:
                        self.range_frame_index += 1
                        self.update_time = pygame.time.get_ticks()

                    # If the end of the animation is reached:
                    if self.range_frame_index >= len(self.range_attack_animation_list[self.range_action]):
                        self.range_frame_index = len(self.range_attack_animation_list[self.range_action]) - 1
                elif self.range_action == 0:  # Special Attack Down
                    # Increments the frame index
                    if (pygame.time.get_ticks() - self.update_time) > 180:
                        self.range_frame_index += 1
                        self.update_time = pygame.time.get_ticks()

                    # If the end of the animation is reached:
                    if self.range_frame_index >= len(self.range_attack_animation_list[self.range_action]):
                        self.range_frame_index -= 1
                        if self.range_flip:
                            self.rect.left = - 800
                        else:
                            self.rect.right = 1280 + 800

                else:
                    # Strong Attack Down
                    if (pygame.time.get_ticks() - self.update_time) > 150:
                        self.range_frame_index += 1
                        self.update_time = pygame.time.get_ticks()

                    # If the end of the animation is reached:
                    if self.range_frame_index >= len(self.range_attack_animation_list[self.range_action]):
                        self.range_frame_index -= 1
                        if self.range_flip:
                            self.rect.left = - 800
                        else:
                            self.rect.right = 1280 + 800

                # Image movement
                self.rect.x += 2 + (-4 * self.range_flip)

        def attack_collisions(self, target):
            if self.rect.colliderect(target.rect):
                if not self.collision:
                    self.collision = True
                    target.hit = True
                    target.health -= 5
                    # Knock-back
                    if target.flip:
                        target.rect.x += 25
                    else:
                        target.rect.x -= 25