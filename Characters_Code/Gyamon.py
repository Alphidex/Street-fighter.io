import pygame
from characters import Fighter, Ranged_Attack

class Gyamon(Fighter):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, character_name, ai):
        super().__init__(player, x, y, flip, data, sprite_sheet, animation_steps, character_name, ai)

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
            "normal_attack": {"trigger": False, "cooldown": 70, "frame_index": 3, "damage": 1.5, "knockback": 1, "action": 5, "range_attack": False, "rect": pygame.Rect(self.rect.centerx - (165 * self.flip), self.rect.y + 65, 165, 0.55 * self.rect.height)},
            "normal_attack_up": {"trigger": False, "cooldown": 70, "frame_index": 6, "damage": 1.8, "knockback": 1, "action": 2, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - (140 * self.flip), self.rect.y * 0.8, 120, 1.4 * self.rect.height)},
            "normal_attack_down": {"trigger": False, "cooldown": 60, "frame_index": 3, "damage": 1.9, "knockback": 1, "action": 6, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - 30 - (0 * self.flip), self.rect.y + 70, 140, 0.75 * self.rect.height)},
            "normal_jump_attack": {"trigger": False, "cooldown": 85, "frame_index": 3, "damage": 1.4, "knockback": 1, "action": 9, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - (1.4 * self.rect.width * self.flip),self.rect.y + 40, 1.5 * self.rect.width, 0.6 * self.rect.height)},
            "strong_attack": {"trigger": False, "cooldown": 100, "frame_index": 3, "damage": 7, "knockback": 1, "action": 8, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - (5 * self.rect.width * self.flip),self.rect.y, 5 * self.rect.width,1 * self.rect.height)},
            "strong_attack_up": {"trigger": False, "cooldown": 90, "frame_index": 5, "damage": 6, "knockback": 1, "action": 4, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - (1.65 * self.rect.width * self.flip),self.rect.y, 1.65 * self.rect.width,1 * self.rect.height)},
            "strong_attack_down": {"trigger": False, "cooldown": 90, "frame_index": 4, "damage": 8, "knockback": 1, "action": 3, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - (1.9 * self.rect.width * self.flip),self.rect.y + 50, 1.9 * self.rect.width, 0.7 * self.rect.height)},
            "strong_jump_attack": {"trigger": False, "cooldown": 70, "frame_index": 2, "damage": 5, "knockback": 1, "action": 13, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - 50 - (30 * self.flip),self.rect.y - 80, 1.3 * self.rect.width,1.4 * self.rect.height)},
            "special_attack": {"trigger": False, "cooldown": 80, "frame_index": 8<= self.frame_index<= 25, "damage": 1.7, "knockback": 1, "action": 0, "range_attack":False, "rect": pygame.Rect(self.rect.centerx - (3.4 * self.rect.width * self.flip),self.rect.y * 0.9, 3.4 * self.rect.width,1.5 * self.rect.height)},
            "special_attack_down": {"trigger": False, "cooldown": 100, "frame_index": self.frame_index == 3 or self.frame_index == 8 or self.frame_index == 9, "damage": 1, "knockback": 18, "action": 1, "range_attack": True, "rect": pygame.Rect(self.rect.centerx - (1.83 * self.rect.width * self.flip),self.rect.y, 1.83 * self.rect.width, 1.15 * self.rect.height)}
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

    def attacks_management(self, surface, target):
        if self.range_attack:
            for attack in self.ranged_group.sprites():
                attack.main(surface, self.offset, self.image_scale, target)

            if len(self.ranged_group.sprites()):
                self.range_attack = False

        def attack_effects():
            # Normal
            if self.attack_data["normal_attack_down"]["trigger"]:
                self.rect.x += 13 - (26 * self.flip)

            if self.attack_data["normal_jump_attack"]["trigger"]:
                if 2 <= self.frame_index <= 4:
                    self.rect.x += 5 - (10 * self.flip)
                    self.rect.y += 6

            if self.attack_data["normal_attack_up"]["trigger"]:
                if 5 <= self.frame_index <= 8:
                    self.rect.x += 7 - (14 * self.flip)

            # Strong
            if self.attack_data["strong_attack"]["trigger"]:
                if not(-50 <= (target.rect.centerx - self.rect.centerx) <= 50):
                    target.rect.x -= 20 + (-40 * self.flip)

            if self.attack_data["strong_attack_down"]["trigger"]:
                if 4 <= self.frame_index <= 6:
                    self.rect.x += 7 - (14 * self.flip)

            if self.attack_data["strong_attack_up"]["trigger"]:
                if self.frame_index <= 6:
                    self.rect.x += 6 - (12 * self.flip)

            if self.attack_data["strong_jump_attack"]["trigger"]:
                self.rect.x += 4 - (8 * self.flip)
                self.rect.y -= 5

            # Special
            if self.attack_data["special_attack_down"]["trigger"]:
                if self.frame_index == 8:
                    self.rect.centerx = target.rect.centerx - 100 + (200 * self.flip)

        def attack_triggers():
            # The attacking rectangle will only activate at certain frame_indexes (with some having varying DPS):
            if self.frame_index < len(self.animation_list[self.action]):
                for attack in self.attack_data.values():
                    if attack["trigger"]:
                        self.frame_index_counter[1] = self.frame_index
                        if self.frame_index_counter[1] - self.frame_index_counter[0] >= 1\
                                and (self.frame_index == attack["frame_index"] or attack["frame_index"] == True):
                            if attack["range_attack"]:
                                if self.attack_data["special_attack_down"]["trigger"]:
                                    if self.frame_index == 9:
                                        self.range_attack = True
                                        self.Ranged_Gyamon(self.flip, self.projectile_list, self.action, self.rect, "Gyamon",
                                                           self.opponent)
                                else:
                                    self.range_attack = True
                                    self.Ranged_Gyamon(self.flip, self.projectile_list, self.action, self.rect,"Gyamon", self.opponent)
                            self.attack_rectangle_collision(surface, target)
                            self.frame_index_counter = [self.frame_index, self.frame_index]

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
            img = pygame.transform.scale_by(img, 2.5)

            if self.action == 1:  # Special Attack Down
                surface.blit(img, (self.rect.x - 500 + (150 * self.flip), self.rect.y - 460))

        def update_ranged_attack(self, surface):
            animation_cooldown = 140

            # Refresh the image
            self.image = self.attack_animation_list[self.action][self.frame_index]

            # Increments the frame index
            if (pygame.time.get_ticks() - self.update_time) > animation_cooldown:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

            # If the end of the animation is reached:
            if self.frame_index >= len(self.attack_animation_list[self.action]):
                self.kill()

        def attack_collisions(self, target):
            if self.rect.colliderect(target.rect):
                if self.collision == False:
                    self.collision = True
                    if not target.block:
                        target.hit = True
                        target.health -= 20
                    else:
                        target.shield_health -= 40

                    # Knock-back
                    target.rect.x += 15 - (30 * self.flip)