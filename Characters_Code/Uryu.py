import pygame
from characters import Fighter, Ranged_Attack

class Uryu(Fighter):
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

        pygame.draw.rect(surface, (255, 0, 0), self.rect, 4)

    def time_passed(self):
        return pygame.time.get_ticks() - self.update_time

    def attack(self, surface, target):
        pass
        # # In case there's an error
        # if self.attacking and 0 == 1:
        #     self.attacking_rectangle = pygame.Rect(self.rect.centerx - (1.7 * self.rect.width * self.flip),
        #                                       self.rect.y * 1.125, 1.75 * self.rect.width, 0.75 * self.rect.height)
        #
        # #pygame.draw.rect(surface, (0, 255, 0), self.attacking_rectangle, 1)
        #
        #
        # # Rectangle collisions
        # if self.attacking_rectangle.colliderect(target.rect):
        #     target.hit = True
        #     target.frame_index = 0
        #
        #     # Taking Damage
        #     # Normal Attack Attacks
        #     if self.normal_attack:
        #         target.health -= 1
        #     elif self.normal_attack_up:
        #         target.health -= 1
        #     elif self.normal_attack_down:
        #         target.health -= 2
        #     elif self.normal_jump_attack:
        #         target.health -= 2
        #
        #     # Strong Attack Attacks
        #     elif self.strong_attack:
        #         target.health -= 2
        #     elif self.strong_attack_up:
        #         target.health -= 2
        #     elif self.strong_attack_down:
        #         target.health -= 2
        #
        #     # Special Attack Attacks
        #     elif self.special_attack:
        #         target.health -= 4
        #     elif self.special_attack_up:
        #         target.health -= 4
        #     elif self.special_attack_down:
        #         target.health -= 4
        #
        #     # Knock-back - Once
        #     if target.flip:
        #         target.rect.x += 25
        #         self.rect.x += 10
        #     else:
        #         target.rect.x -= 25
        #         self.rect.x -= 10

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
                self.Ranged_Uryu(self.flip, self.projectile_list, action, self.rect, "Uryu")

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
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 4:
                        self.attack_list_trigger[self.frame_index] = True
                        # Action = 7
                        init_ranged_attack(7)

                elif self.normal_attack_forward:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 3:
                        self.attack_list_trigger[self.frame_index] = True
                        # Action = 7
                        init_ranged_attack(7)

                elif self.normal_attack_up:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 3:
                        self.attack_list_trigger[self.frame_index] = True
                        # Action = 20
                        init_ranged_attack(20)

                elif self.normal_attack_down:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 4:
                        self.attack_list_trigger[self.frame_index] = True
                        # Action = 11
                        init_ranged_attack(11)

                elif self.normal_jump_attack:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 3:
                        self.attack_list_trigger[self.frame_index] = True
                        # Action = 23
                        init_ranged_attack(23)

                # Strong Attacks
                elif self.strong_attack:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 4:
                        self.attack_list_trigger[self.frame_index] = True
                        # Action = 7
                        init_ranged_attack(7)

                elif self.strong_attack_up:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 3:
                        self.attack_list_trigger[self.frame_index] = True
                        # Action = 3
                        init_ranged_attack(3)

                elif self.strong_attack_down:
                    if self.attack_list_trigger[self.frame_index] == False and 2 <= self.frame_index <= 6:
                        self.attack_list_trigger[self.frame_index] = True
                        if self.frame_index == 2:
                            # Action = 25
                            init_ranged_attack(25)

                elif self.strong_jump_attack:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 4:
                        self.attack_list_trigger[self.frame_index] = True
                        # Action = 6
                        init_ranged_attack(6)

                # Special Attacks
                elif self.special_attack:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 9:
                        self.attack_list_trigger[self.frame_index] = True
                        # Action = 1
                        init_ranged_attack(1)

                elif self.special_attack_up:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 3:
                        self.attack_list_trigger[self.frame_index] = True
                        # Action = 25
                        init_ranged_attack(11)

                elif self.special_attack_down:
                    if self.attack_list_trigger[self.frame_index] == False and self.frame_index == 0:
                        self.attack_list_trigger[self.frame_index] = True
                        # Action = 0
                        init_ranged_attack(0)


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
            self.update_action(24)
        elif self.knockback:
            self.update_action(16)
        elif self.hit:
            self.update_action(27)
        elif self.attacking:
            # Normal Attack Attacks
            if self.normal_attack:
                self.update_action(9)
            elif self.normal_attack_forward:
                self.update_action(14)
            elif self.normal_attack_up:
                self.update_action(19)
            elif self.normal_attack_down:
                self.update_action(8)
            elif self.normal_jump_attack:
                self.update_action(22)

                """ MIGHT ADD NORMAL ATTACK FORWARD """

            # Strong Attack Attacks
            elif self.strong_attack:
                self.update_action(10)
            elif self.strong_attack_up:
                self.update_action(12)
            elif self.strong_attack_down:
                self.update_action(5)
            elif self.strong_jump_attack:
                self.update_action(18)

            # Special Attack Attacks
            elif self.special_attack:
                self.update_action(2)
            elif self.special_attack_up:
                self.update_action(4)
            elif self.special_attack_down:
                self.update_action(21)

        elif self.dash:
            self.update_action(26)
        elif (self.jump[0] == True) or (self.jump[1] == True):
            self.update_action(17)
        elif self.running:
            self.update_action(15)
        elif self.block:
            self.update_action(28)
        else:
            self.update_action(24)  # IDLE
        #28  max
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


    class Ranged_Uryu(Ranged_Attack):
        def __init__(self, flip, attack_animation_list, action, character_rect, character):
            super().__init__(flip, attack_animation_list, action, character_rect, character)

            # Create Rectangle
            self.rect = self.create_rectangle(character_rect)  # To check the position of the character

            # Modifiers
            self.special_frameIndex_1 = 0
            self.special_frameIndex_2 = 3
            self.special_rangeImage_1 = self.attack_animation_list[self.action][self.special_frameIndex_1]
            self.special_rangeImage_2 = self.attack_animation_list[self.action][self.special_frameIndex_2]

        def create_rectangle(self, character_rect):
            if self.action == 0:
                rect = pygame.Rect(character_rect.centerx - 280 - (280 * character_rect.width * self.flip),
                                   character_rect.y - 50, 560,
                                   50 + character_rect.height)
            elif self.action == 1:
                rect = pygame.Rect(character_rect.centerx - (200 * character_rect.width * self.flip),
                                   character_rect.y + 20, 200,
                                   0.9 * character_rect.height)

            elif self.action == 7 or self.action == 11:
                rect = pygame.Rect(character_rect.centerx - (1.4 * character_rect.width * self.flip),
                                   character_rect.y + 20, 1.4 * character_rect.width,
                                   0.4 * character_rect.height)

            elif self.action == 23:
                rect = pygame.Rect(character_rect.centerx - (120 * self.flip),
                                   character_rect.y + 40, 120,
                                   0.8 * character_rect.height)

            elif self.action == 20:
                rect = pygame.Rect(character_rect.centerx - (120 * self.flip),
                                   character_rect.y - 80, 120,
                                   0.8 * character_rect.height)

            elif self.action == 6:
                rect = pygame.Rect(character_rect.centerx - 10 + (20 * self.flip),
                                   character_rect.y + character_rect.height, 60,
                                   1 * character_rect.height)

            elif self.action == 3:
                rect = pygame.Rect(character_rect.centerx - 20 - (20 * self.flip),
                                   character_rect.y - character_rect.height, 60,
                                   1 * character_rect.height)

            elif self.action == 25:
                rect = pygame.Rect(character_rect.centerx - (100 * self.flip),
                                   character_rect.y, 100,
                                   1 * character_rect.height)

            elif self.action == 11:
                rect = pygame.Rect(character_rect.centerx - (100 * self.flip),
                                   character_rect.y, 100,
                                   1 * character_rect.height)

            else:
                rect = pygame.Rect(character_rect.centerx - (1.7 * character_rect.width * self.flip),
                                   character_rect.y + 30, 1.9 * character_rect.width,
                                   0.7 * character_rect.height)

            return rect


        def draw_ranged_attack(self, surface, offset, image_scale):
            # Drawing Ranged Attacks
            img = pygame.transform.flip(self.image, self.flip, False)

            # Special Down
            if self.action == 0:
                surface.blit(img, (
                    self.rect.x - ((offset[0] - 43) * image_scale),
                    self.rect.y - ((offset[1] + 17) * image_scale)))
                pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)

            # Special Attack
            elif self.action == 1:
                # The first effect
                img_1 = pygame.transform.flip(self.special_rangeImage_1, self.flip, False)

                # The second effect
                img_2 = pygame.transform.flip(self.special_rangeImage_2, self.flip, False)

                surface.blit(img_1, (
                    self.rect.x - ((offset[0] + 7) * image_scale),
                    self.rect.y - (offset[1] * image_scale)))
                pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)

                surface.blit(img_2, (
                    self.rect.x - (offset[0] * image_scale),
                    self.rect.y - (offset[1] * image_scale)))
                pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)

            # Normal Attack + Strong Attack
            elif self.action == 7 or self.action == 11:
                surface.blit(img, (
                    self.rect.x - (offset[0] * image_scale),
                    self.rect.y - ((offset[1] + 17) * image_scale)))
                pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)

            # Normal Jump Attack
            elif self.action == 23 or self.action == 20:
                surface.blit(img, (
                    self.rect.x - (offset[0] * image_scale),
                    self.rect.y - ((offset[1] + 5) * image_scale)))
                pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)

            # Strong Jump Attack
            elif self.action == 6:
                surface.blit(img, (
                    self.rect.x - ((offset[0] + 15) * image_scale),
                    self.rect.y - (offset[1] * image_scale)))
                pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)

            # Strong Up
            elif self.action == 3:
                surface.blit(img, (
                    self.rect.x - ((offset[0] + 15) * image_scale),
                    self.rect.y - (offset[1] * image_scale)))
                pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)

            # Strong Down
            elif self.action == 25:
                surface.blit(img, (
                    self.rect.x - ((offset[0] + 10) * image_scale),
                    self.rect.y - (offset[1] * image_scale)))
                pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)

            else:
                surface.blit(img, (
                    self.rect.x - (offset[0] * image_scale),
                    self.rect.y - (offset[1] * image_scale)))
                pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)

        def update_ranged_attack(self, surface):
            animation_cooldown = 140

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
            if (pygame.time.get_ticks() - self.update_time) > animation_cooldown:
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

                if self.action == 6:
                    self.rect.y += 3000
                if self.action == 3:
                    self.rect.y -= 3000
                if self.action == 25:
                    self.rect.y += 5000
                if self.action == 0:
                    self.rect.y += 5000


            # Image movement
            # Jump Normal Attack
            if self.action == 23:
                self.rect.x += 2 + (-4 * self.flip)
                self.rect.y += 2

            # Normal Attack Up
            elif self.action == 20:
                self.rect.x += 2 + (-4 * self.flip)
                self.rect.y -= 2

            # Jump Strong
            elif self.action == 6:
                self.rect.y += 2

            # Strong Up
            elif self.action == 3:
                self.rect.y -= 2

            # Strong Up and Special Down
            elif self.action == 25 or self.action == 0:
                pass

            else:
                self.rect.x += 2 + (-4 * self.flip)

            # Off the screen
            if self.action == 7 and self.frame_index == 7:
                self.rect.x += 1500 - (3600 * self.flip)

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
