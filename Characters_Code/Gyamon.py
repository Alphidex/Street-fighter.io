import pygame
from characters import Fighter, Ranged_Attack

class Gyamon(Fighter):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, character_name):
        super().__init__(player, x, y, flip, data, sprite_sheet, animation_steps, character_name)

        # Animations - 17 Rows
        self.action = 7
        self.frame_index = 0
        self.knockback_frame_index = 12
        self.strong_attack_hold_trigger = False
        # Animations
        self.animation_list = self.load_images(sprite_sheet, animation_steps, "animations")
        self.projectile_list = self.load_images(sprite_sheet, animation_steps, "projectiles")
        self.image = self.animation_list[self.action][self.frame_index]

        # Attacks
        self.attack_data = self.get_attack_data()
        self.exclude_attacks = ["special_attack_up"]

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
                if y == 0:
                    temp_img = sprite_sheet.subsurface(x * (self.size[0] + 140), y * (self.size[1] + 140),
                                                       self.size[0] + 140,
                                                       self.size[1] + 140)
                    scaled_image = pygame.transform.scale(temp_img, (
                        (self.size[0] + 140) * self.image_scale, (self.size[1] + 140) * self.image_scale))
                else:
                    temp_img = sprite_sheet.subsurface(x * (self.size[0]), y * (self.size[1]) + 140, self.size[0],
                                                       self.size[1])
                    scaled_image = pygame.transform.scale(temp_img, (
                        self.size[0] * self.image_scale, self.size[1] * self.image_scale))

                if y == 1 and (8 <= x <= 14):
                    temp_projectile_img_list.append(scaled_image)
                else:
                    temp_animation_img_list.append(scaled_image)

            animation_list.append(temp_animation_img_list)
            # Will create many empty lists (inefficient but acceptable)
            projectile_list.append(temp_projectile_img_list)

        if choice == "animations":
            return animation_list
        else:
            return projectile_list

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        if self.action == 0:
            if not self.flip:
                surface.blit(img, (
                    self.rect.x - ((self.offset[0] + 32) * self.image_scale),
                    self.rect.y - ((self.offset[1] + 110) * self.image_scale)))
            else:
                surface.blit(img, (
                    self.rect.x - ((self.offset[0] + 32) * self.image_scale * 1.9),
                    self.rect.y - ((self.offset[1] + 110) * self.image_scale)))
        else:
            if not self.flip:
                surface.blit(img, (
                    self.rect.x - (self.offset[0] * self.image_scale),
                    self.rect.y - ((self.offset[1] + 14) * self.image_scale)))
            else:
                surface.blit(img, (
                    self.rect.x - (self.offset[0] * self.image_scale),
                    self.rect.y - ((self.offset[1] + 14) * self.image_scale)))

    # Attack Methods
    def get_attack_data(self):
        data = {
            "normal_attack": {"trigger": False, "cooldown": 70, "frame_index": 3, "damage": 1, "knockback": 1, "action": 5, "range_attack": False, "rect": pygame.Rect(self.rect.centerx - (165 * self.flip), self.rect.y + 65, 165, 0.55 * self.rect.height)},
            "normal_attack_up": {"trigger": False, "cooldown": 70, "frame_index": 6, "damage": 1, "knockback": 1, "action": 2, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - (140 * self.flip), self.rect.y * 0.8, 120, 1.4 * self.rect.height)},
            "normal_attack_down": {"trigger": False, "cooldown": 60, "frame_index": 3, "damage": 1, "knockback": 1, "action": 6, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - 30 - (0 * self.flip), self.rect.y + 70, 140, 0.75 * self.rect.height)},
            "normal_jump_attack": {"trigger": False, "cooldown": 85, "frame_index": 3, "damage": 1, "knockback": 1, "action": 9, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - (1.4 * self.rect.width * self.flip),self.rect.y + 40, 1.5 * self.rect.width, 0.6 * self.rect.height)},
            "strong_attack": {"trigger": False, "cooldown": 100, "frame_index": 3, "damage": 1, "knockback": 1, "action": 8, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - (5 * self.rect.width * self.flip),self.rect.y, 5 * self.rect.width,1 * self.rect.height)},
            "strong_attack_up": {"trigger": False, "cooldown": 90, "frame_index": 5, "damage": 1, "knockback": 1, "action": 4, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - (1.65 * self.rect.width * self.flip),self.rect.y, 1.65 * self.rect.width,1 * self.rect.height)},
            "strong_attack_down": {"trigger": False, "cooldown": 90, "frame_index": 4, "damage": 1, "knockback": 1, "action": 3, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - (1.9 * self.rect.width * self.flip),self.rect.y + 50, 1.9 * self.rect.width, 0.7 * self.rect.height)},
            "strong_jump_attack": {"trigger": False, "cooldown": 70, "frame_index": 2, "damage": 1, "knockback": 1, "action": 13, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - 50 - (30 * self.flip),self.rect.y - 80, 1.3 * self.rect.width,1.4 * self.rect.height)},
            "special_attack": {"trigger": False, "cooldown": 100, "frame_index": 8<= self.frame_index<= 25, "damage": 1, "knockback": 1, "action": 0, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - (3.4 * self.rect.width * self.flip),self.rect.y * 0.9, 3.4 * self.rect.width,1.5 * self.rect.height)},
            "special_attack_down": {"trigger": False, "cooldown": 100, "frame_index": self.frame_index == 3 or self.frame_index == 8 or self.frame_index == 9, "damage": 1, "knockback": 1, "action": 1, "range_attack": True, "rect": pygame.Rect(self.rect.centerx - (1.83 * self.rect.width * self.flip),self.rect.y, 1.83 * self.rect.width, 1.15 * self.rect.height)}
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
                    target.frame_index = 0

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

            # # Pull effect for Strong Attacks
            # if self.strong_attack and not (-50 <= (target.rect.centerx - self.rect.centerx) <= 50):
            #     target.rect.x -= 20 + (40 * self.flip)
            #
            # # Moving During Attacks
            # if self.strong_attack_up:
            #     self.rect.x += 20 - (40 * self.flip)
            # if self.strong_attack_down:
            #     self.rect.x += 50 - (100 * self.flip)
            #
            # # Teleport if Special Attack Attack Down
            # if self.special_attack_down and self.frame_index == 8:
            #     self.rect.centerx = target.rect.centerx - 100 + (200 * self.flip)

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
                self.Ranged_Gyamon(self.flip, self.projectile_list, action, self.rect, "Gyamon", self.opponent)

        def attack_effects():
            # Continuous knockback and effects
            if target.hit and not target.dead:
                if self.attack_data["special_attack"]["trigger"]:
                    target.rect.x += 2 + (-4 * self.flip)

            # Normal
            if self.attack_data["normal_attack_down"]["trigger"]:
                self.rect.x += 13 - (26 * self.flip)

            if self.attack_data["normal_jump_attack"]["trigger"]:
                if 2 <= self.frame_index <= 4:
                    self.rect.x += 4 - (8 * self.flip)
                    self.rect.y += 5

            if self.attack_data["normal_attack_up"]["trigger"]:
                if 5 <= self.frame_index <= 8:
                    self.rect.x += 4 - (8 * self.flip)

            # Strong
            if self.attack_data["strong_attack"]["trigger"]:
                if not(-50 <= (target.rect.centerx - self.rect.centerx) <= 50):
                    target.rect.x -= 20 + (40 * self.flip)

            if self.attack_data["strong_attack_down"]["trigger"]:
                if 4 <= self.frame_index <= 6:
                    self.rect.x += 4 - (8 * self.flip)

            if self.attack_data["strong_jump_attack"]["trigger"]:
                self.rect.x += 3 - (6 * self.flip)
                self.rect.y -= 3

            # Special
            if self.attack_data["special_attack_down"]["trigger"]:
                if self.frame_index == 8:
                    self.rect.centerx = target.rect.centerx - 100 + (200 * self.flip)

        def attack_triggers():
            # The attacking rectangle will only activate at certain frame_indexes (with some having varying DPS):
            if self.frame_index < len(self.animation_list[self.action]):
                for attack in self.attack_data.values():
                    if attack["trigger"]:
                        if not self.attack_list_trigger[self.frame_index] \
                                and (self.frame_index == attack["frame_index"] or attack["frame_index"] == True):
                            if attack["range_attack"]:
                                if self.attack_data["special_attack_down"]["trigger"]:
                                    if self.frame_index == 3:
                                        init_ranged_attack(attack["action"])
                                else:
                                    init_ranged_attack(attack["action"])
                            self.attack_rectangle_collision(surface, target)
                            self.attack_list_trigger[self.frame_index] = True

        # Checks For Attacks
        if self.attacking:
            # Knockback + other continuous effects
            attack_effects()

            # Initialize the attacks
            attack_triggers()

    # Update the sprites and character states
    def update(self, target, surface):
        self.update_attack_data()

        if self.health <= 0:
            self.health = 0
            self.dead = True
            self.update_action(10)
        elif self.knockback:
            pass
        elif self.hit:
            self.update_action(12)
        elif self.attacking:
            for attack in self.attack_data.values():
                if attack["trigger"]:
                    self.update_action(attack["action"])
        elif self.dash:
            self.update_action(15)
        elif (self.jump[0] == True) or (self.jump[1] == True):
            self.update_action(11)
        elif self.running:
            self.update_action(14)
        elif self.block:
            self.update_action(16)
        else:
            self.update_action(7)  # IDLE

        animation_cooldown = 85

        # Update Image ------------------------------------------
        self.image = self.animation_list[self.action][self.frame_index]

        # Attacking Rectangle
        if self.attacking_rectangle is not None:
            pygame.draw.rect(self.screen, (255, 12, 31), self.attacking_rectangle, 3)

        # Update the animation frame index at certain milliseconds
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

    def update_animation(self, target):
        animation_cooldown = 85

        # Update the animations + adds animation cooldown (different values for different animations)
        if self.knockback:
            if self.time_passed() > 300:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

                if self.frame_index >= len(self.animation_list[self.action]):
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

                    self.normal_combo_count = 0

        elif self.attacking:
            for attack in self.attack_data.values():
                if attack["trigger"]:
                    if self.time_passed() > attack["cooldown"]:
                        self.frame_index += 1
                        self.update_time = pygame.time.get_ticks()
                # # Strong Attack Attacks
                # elif self.strong_attack:
                #     if (pygame.time.get_ticks() - self.update_time) > 100 and (self.frame_index != 4):  # - Pull attack
                #         self.frame_index += 1
                #         self.update_time = pygame.time.get_ticks()

        else:
            if (pygame.time.get_ticks() - self.update_time) > animation_cooldown:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

    # Time
    def time_passed(self):
        return pygame.time.get_ticks() - self.update_time

    class Ranged_Gyamon(Ranged_Attack):
        def __init__(self, flip, attack_animation_list, action, character_rect, character, opponent):
            super().__init__(flip, attack_animation_list, action, character_rect, character, opponent)

            # Create Rectangle
            self.rect = self.create_rectangle(character_rect)  # To check the position of the character

        def create_rectangle(self, character_rect):
            # Special Attack Down
            if self.action == 1:
                rect = pygame.Rect(
                    character_rect.centerx + 100 - ((1.5 * character_rect.width + 200) * self.flip),
                    character_rect.y - 55, 1.5 * character_rect.width,
                    1.4 * character_rect.height)

            return rect

        def draw_ranged_attack(self, surface, offset, image_scale):
            # Drawing Ranged Attacks
            img = pygame.transform.flip(self.image, self.flip, False)

            if self.action == 1:  # Special Attack Down
                surface.blit(img, (
                    self.rect.x + 20 - (offset[0] * image_scale),
                    self.rect.y - (offset[1] * image_scale)))
                pygame.draw.rect(surface, (143, 24, 199), self.rect, 4)

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
                self.frame_index = len(self.attack_animation_list[self.action]) - 1

            # Image movement
            self.rect.x += 15 + (-30 * self.flip)

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
                    if target.flip:
                        target.rect.x += 25
                    else:
                        target.rect.x -= 25