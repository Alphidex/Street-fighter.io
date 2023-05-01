import pygame
from characters import Fighter, Ranged_Attack

class Zoro(Fighter):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, character_name):
        super().__init__(player, x, y, flip, data, sprite_sheet, animation_steps, character_name)

        # Animations - 23 Rows
        self.action = 20
        self.frame_index = 0
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
            #Will create many empty lists (inefficient but acceptable)
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
                self.rect.y - ((self.offset[1] + 25) * self.image_scale)))
        else:
            if not self.flip:
                surface.blit(img, (
                    self.rect.x - (self.offset[0] * self.image_scale),
                    self.rect.y - (self.offset[1] * self.image_scale)))
            else:
                surface.blit(img, (
                    self.rect.x - (self.offset[0] * self.image_scale * 1.3),
                    self.rect.y - (self.offset[1] * self.image_scale)))

    def time_passed(self):
        return pygame.time.get_ticks() - self.update_time

    def attack(self, surface, target):
        # HIT-BOXES

        # Normal Attack Attacks
        if self.normal_attack:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - (1.7 * self.rect.width * self.flip),
                                              self.rect.y * 1.125, 1.75 * self.rect.width, 0.75 * self.rect.height)
        elif self.normal_attack_up:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - (1.2 * self.rect.width * self.flip),
                                              self.rect.y, 1.2 * self.rect.width, 1.2 * self.rect.height)
        elif self.normal_attack_down:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - (1.4 * self.rect.width * self.flip),
                                              self.rect.y * 1.125, 1.4 * self.rect.width, 0.75 * self.rect.height)
        elif self.normal_jump_attack:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - 25 - (0.9 * self.rect.width * self.flip),
                                                   self.rect.y + 20, 1.60 * self.rect.width, 1.14 * self.rect.height)
        # Strong Attack Attacks
        elif self.strong_attack:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - 10 - (1.75 * self.rect.width * self.flip),
                                              self.rect.y * 1.125, 1.85 * self.rect.width, 0.75 * self.rect.height)
        elif self.strong_attack_up:
            self.attacking_rectangle = pygame.Rect(self.rect.x - 30 - (10 * self.flip),
                                              self.rect.y - 90, 1.8 * self.rect.width, 1.65 * self.rect.height)
        elif self.strong_attack_down:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - (1.3 * self.rect.width * self.flip),
                                              self.rect.y * 0.97, 1.4 * self.rect.width, 1.2 * self.rect.height)
        elif self.strong_jump_attack:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - 90 - (53 * self.flip),
                                                   self.rect.y + 28, 2.3 * self.rect.width, 1.1 * self.rect.height)
        # Special Attack Attacks
        elif self.special_attack:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip),
                                              self.rect.y * 1.115, 2 * self.rect.width, 0.87 * self.rect.height)
        elif self.special_attack_up:
            self.attacking_rectangle = pygame.Rect(self.rect.x - 63 - (20 * self.flip),
                                              self.rect.y - 43, 2.4 * self.rect.width, 1.45 * self.rect.height)
        elif self.special_attack_down:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - (1.7 * self.rect.width * self.flip),
                                              self.rect.y, 1.83 * self.rect.width, 1.15 * self.rect.height)
        # In case there's an error
        else:
            self.attacking_rectangle = pygame.Rect(self.rect.centerx - (1.7 * self.rect.width * self.flip),
                                              self.rect.y * 1.125, 1.75 * self.rect.width, 0.75 * self.rect.height)

        pygame.draw.rect(surface, (0, 255, 0), self.attacking_rectangle, 2)


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
                target.health -= 15
            elif self.special_attack_down:
                target.health -= 20

            # Knock-back
            if self.normal_attack or self.normal_attack_up or self.normal_attack_down:
                target.rect.x += 5 - (10 * self.flip)

    def _update_animation(self, target):
        animation_cooldown = 85
        # Update the animations + adds animation cooldown (different values for different animations)
        if self.knockback:
            if (pygame.time.get_ticks() - self.update_time) > 300:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

                if self.frame_index >= len(self.animation_list[self.action]):
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
                    self.special_attack_up = False
                    self.special_attack_down = False
        # Normal Attack Attacks
        elif self.normal_attack:
            if (pygame.time.get_ticks() - self.update_time) > 60:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        elif self.normal_attack_up:
            if (pygame.time.get_ticks() - self.update_time) > 60:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        elif self.normal_attack_down:
            if (pygame.time.get_ticks() - self.update_time) > 55:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        elif self.normal_jump_attack:
            if (pygame.time.get_ticks() - self.update_time) > 85:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        # Strong Attack Attacks
        elif self.strong_attack:
            if (pygame.time.get_ticks() - self.update_time) > 90:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        elif self.strong_attack_up:
            if (pygame.time.get_ticks() - self.update_time) >  90:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        elif self.strong_attack_down:
            if (pygame.time.get_ticks() - self.update_time) > 90:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        elif self.strong_jump_attack:
            if (pygame.time.get_ticks() - self.update_time) > 70:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        # Special Attack Attacks
        elif self.special_attack:
            if (pygame.time.get_ticks() - self.update_time) > 100:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        elif self.special_attack_up:
            if (pygame.time.get_ticks() - self.update_time) > 100:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        elif self.special_attack_down:
            if (pygame.time.get_ticks() - self.update_time) > 100:
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
                self.Ranged_Zoro(self.flip, self.projectile_list, action, self.rect, "Zoro")

        # Checks For Attacks
        if self.attacking:
            # Enemy knock-back for attacks (similar code in move function, COMBINE THEM)
            if target.hit and not target.dead:
                if self.strong_attack_up:
                    target.rect.y -= 10
                    target.vel_y = 0
                    if self.frame_index == 4:
                        target.hit = False
                        target.knockback = True
                        target.frame_index = target.knockback_frame_index
                if self.strong_attack:
                    target.rect.x += 6 + (-12 * self.flip)
                if self.special_attack:
                    target.rect.x += 2 + (-4 * self.flip)

            # The attacking rectangle will only activate at certain frame_indexes (with some having varying DPS):
            if self.frame_index < len(self.animation_list[self.action]):
                # Normal Attack Attacks
                if self.normal_attack:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 1:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True
                        self.rect.x += 7 - (14 * self.flip)
                elif self.normal_attack_up:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 2:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True
                        self.rect.x += 7 - (14 * self.flip)
                elif self.normal_attack_down:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 3:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True
                        self.rect.x += 7 - (14 * self.flip)
                elif self.normal_jump_attack:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 3:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True

                # Strong Attack Attacks
                elif self.strong_attack:
                    if self.attack_list_trigger[self.frame_index] == False and 2 <= self.frame_index <= 11:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True
                    # Attack Movement
                    if self.frame_index < len(self.animation_list[self.action]) - 4:
                        self.rect.x += 7 + (-14 * self.flip)
                elif self.strong_attack_up:
                    if self.attack_list_trigger[self.frame_index] == False and 1 <= self.frame_index <= 5:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True
                elif self.strong_attack_down:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 3:
                        init_ranged_attack(self.action)

                        # Does the Close Attack Part
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True
                elif self.strong_jump_attack:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 3:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True

                # Special Attack Attacks
                if self.special_attack:
                    if self.attack_list_trigger[self.frame_index] == False and 3 <= self.frame_index <= 11:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True
                    # Attack Movement
                    if 3 < self.frame_index < len(self.animation_list[self.action]) - 3:
                        self.rect.x += 7 + (-14 * self.flip)
                elif self.special_attack_up:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 4:
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True
                elif self.special_attack_down:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 3:
                        init_ranged_attack(self.action)

                        # Does the Close Attack Part
                        self.attack(surface, target)
                        self.attack_list_trigger[self.frame_index] = True
        # For hit-box purposes
        if self.attacking_rectangle != None:
            pygame.draw.rect(surface, (0, 255, 0), self.attacking_rectangle, 2)

    # Update the timer and sprite animations
    def update(self, target, surface):
        # print(player + " Action:", self.action, "\n Frame Index:", self.frame_index, "\n\n") -- For Debugging
        if self.health <= 0:
            self.health = 0
            self.dead = True
            self.update_action(19)
        elif self.knockback:
            pass
        elif self.hit:
            self.update_action(2)
        elif self.attacking:
            # Normal Attack Attacks
            if self.normal_attack:
                self.update_action(18)
            elif self.normal_attack_up:
                self.update_action(15)  # Changed
            elif self.normal_attack_down:
                self.update_action(9)
            elif self.normal_jump_attack:
                self.update_action(13)

            # Strong Attack Attacks
            elif self.strong_attack:
                self.update_action(1)
            elif self.strong_attack_up:
                self.update_action(14)
            elif self.strong_attack_down:
                self.update_action(4)
            elif self.strong_jump_attack:
                self.update_action(7)

            # Special Attack Attacks
            elif self.special_attack:
                self.update_action(5)
            elif self.special_attack_up:
                self.update_action(0)
            elif self.special_attack_down:
                self.update_action(8)  # Changed

        elif self.dash:
            self.update_action(22)
        elif (self.jump[0] == True) or (self.jump[1] == True):
            self.update_action(17)
        elif self.running:
            self.update_action(12)
        elif self.block:
            self.update_action(21)
        else:
            self.update_action(20)  # IDLE

        animation_cooldown = 85

        # Update Image ------------------------------------------
        self.image = self.animation_list[self.action][self.frame_index]

        # Update the animation frame index at certain milliseconds
        self._update_animation(target)

        # Checks for attacks like when it happens, etc.
        self._attack_checks(surface, target)

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

                if self.jumping:
                    self.jumping = False

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            # update the animation settings
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    class Ranged_Zoro(Ranged_Attack):
        def __init__(self, flip, attack_animation_list, action, character_rect, character):
            super().__init__(flip, attack_animation_list, action, character_rect, character)

            # Create Rectangle
            self.rect = self.create_rectangle(character_rect)  # To check the position of the character

        def create_rectangle(self, character_rect):
            if self.character == "Zoro":
                # Strong Attack
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
            img = pygame.transform.flip(self.range_image, self.flip, False)

            if self.character == "Zoro":
                if self.action == 4:
                    surface.blit(img, (
                        self.rect.x - (offset[0] * image_scale),
                        self.rect.y - 70 - (offset[1] * image_scale)))
                    pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)
                elif self.action == 8:
                    surface.blit(img, (
                        self.rect.x - (offset[0] * image_scale),
                        self.rect.y - 50 - (offset[1] * image_scale)))
                    pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)
                else:
                    surface.blit(img, (
                        self.rect.x - (offset[0] * image_scale),
                        self.rect.y - (offset[1] * image_scale)))
                    pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)

            else:
                surface.blit(img, (
                    self.rect.x - (offset[0] * image_scale),
                    self.rect.y - (offset[1] * image_scale)))
                pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)


        def update_ranged_attack(self, surface):
            animation_cooldown = 160
            # Refresh the image
            self.range_image = self.attack_animation_list[self.action][self.frame_index]

            if self.character == "Zoro":
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