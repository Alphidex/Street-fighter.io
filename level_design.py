import pygame
from debug import debug
from GUI import *

class Level_Design:
    def __init__(self, player_1, player_2, fighters_pos, map_instance, mode):
        # Display
        self.screen = pygame.display.get_surface()
        self.mode = mode

        # Players
        self.p1 = player_1
        self.p2 = player_2
        self.fighters_pos = fighters_pos

        # Rounds
        self.start = False
        self.current_round = 1
        self.p1_rounds_won = 0
        self.p2_rounds_won = 0
        self.round_over = False
        self.round_duration_time = 3 * 60
        self.rnd_win_text = 1

        # Matches
        self.current_match = 1
        self.max_matches = 4
        self.match_lost = False
        self.quit = False

        # Beginning of round labels
        self.displayed_labels = 0
        self.fight_countdown_complete = False

        # Map instance
        self.map_instance = map_instance

        # Delay
        self.do_once_match = False
        self.update_timer = 0
        self.round_won_timer = 0
        self.match_won_timer = 0

    def run(self, p1_health, p2_health):
        self.check_for_won_rounds(p1_health, p2_health)
        self.won_rounds_circles()
        self.check_if_match_won()
        self.finish_game()

        if not self.fight_countdown_complete:
            self.display_fight_text()
        else:
            self.round_countdown()

    def round_countdown(self):
        font = pygame.font.Font("./Fonts/retro.ttf", 80)
        text = f"{self.round_duration_time // 60} : {self.round_duration_time % 60}"
        text_surface = font.render(text, False, "#db130f")
        rect = text_surface.get_rect(topleft=(620, 20))
        
        # Draw the countdown
        if self.round_duration_time >= 0:
            pygame.display.get_surface().blit(text_surface, rect.topleft)

            if pygame.time.get_ticks() - self.update_timer > 1000:
                self.round_duration_time -= 1
                self.update_timer = pygame.time.get_ticks()
        else:
            self.round_over = True

    def display_fight_text(self):
        font = pygame.font.Font("./Fonts/retro.ttf", 80)
        round_text = font.render(f"Round: {self.current_round}", True, "white")
        round_text_pos = (550, 300)
        fight_text = font.render(f"Fight!", True, "white")
        fight_text_pos = (550, 300)
        text_list = [round_text, fight_text]
        text_pos_list = [round_text_pos, fight_text_pos]

        # Start the timer
        if self.displayed_labels == 0:
            self.update_timer = pygame.time.get_ticks()
            self.displayed_labels += 1

        # Draw Text
        elif 1 <= self.displayed_labels <= 2:
            if pygame.time.get_ticks() - self.update_timer < 1400:
                self.screen.blit(text_list[self.displayed_labels - 1], text_pos_list[self.displayed_labels-1])
            else:
                self.update_timer = pygame.time.get_ticks()
                self.displayed_labels += 1

        elif self.displayed_labels == 3:
            self.fight_countdown_complete = True
        else: 
            self.fight_countdown_complete = False

    def check_for_won_rounds(self, p1_health, p2_health):
        if not self.round_over:
            if p1_health <= 0:
                self.p2_rounds_won += 1
                self.rnd_win_text = "Player 2"
                self.round_over = True
            elif p2_health <= 0:
                self.p1_rounds_won += 1
                self.round_over = True
                self.rnd_win_text = "Player 1"
            elif self.round_duration_time <= 0:
                if p1_health > p2_health:
                    self.p1_rounds_won += 1
                    self.rnd_win_text = "Player 1"
                else:
                    self.p2_rounds_won += 1
                    self.rnd_win_text = "Player 2"
                self.round_over = True
            self.round_won_timer = pygame.time.get_ticks()
        else:
            font = pygame.font.Font("./Fonts/retro.ttf", 100)
            text = font.render(f"{self.rnd_win_text} Won!", True, "green")

            if pygame.time.get_ticks() - self.round_won_timer < 1200 and self.p1_rounds_won <= 1 and self.p2_rounds_won <= 1:
                self.screen.blit(text, (550, 300))
                
            else:
                if self.p1_rounds_won <= 1 and self.p2_rounds_won <= 1:
                    self.displayed_labels = 0
                self.fight_countdown_complete = False
                self.p1.reset_character_state(self.fighters_pos[0])
                self.p2.reset_character_state(self.fighters_pos[1])
                self.round_duration_time = 180
                self.round_over = False
                self.current_round += 1

    def won_rounds_circles(self):
        circle_pos = [(450, 170), (490, 160), (830, 160), (870, 170)]

        if self.fight_countdown_complete:
            if self.p1_rounds_won > 0:
                for x in range(self.p1_rounds_won):
                    pygame.draw.circle(self.screen, "orange", circle_pos[x], 17)
            if self.p2_rounds_won > 0:
                for x in range(self.p2_rounds_won):
                    pygame.draw.circle(self.screen, "orange", circle_pos[x+2], 17)
                    
            for pos in circle_pos:
                pygame.draw.circle(self.screen, "orange", pos, 17, 2)

    def check_if_match_won(self):
        if self.mode == "PVE":
            if self.p1_rounds_won >= 2:
                if not self.do_once_match:
                    self.match_won_timer = pygame.time.get_ticks()
                    self.do_once_match = True
                self.match_won()
            if self.p2_rounds_won >= 2:
                self.match_lost = True
        else:
            if self.p1_rounds_won >= 2 or self.p2_rounds_won >= 2:
                if not self.do_once_match:
                    self.match_won_timer = pygame.time.get_ticks()
                    self.do_once_match = True
                self.match_won()

    def match_won(self):
        if self.mode == "PVE":
            if self.current_match < self.max_matches:
                # Draw match won text
                font = pygame.font.Font("./Fonts/retro.ttf", 120)
                text = font.render("Match Won!", False, "green")

                if pygame.time.get_ticks() - self.match_won_timer < 2000:
                    self.screen.blit(text, (550, 300))
                else:
                    self.current_round = 1
                    self.displayed_labels = 0
                    self.fight_countdown_complete = False
                    self.do_once_match = False
                    self.p1_rounds_won = 0
                    self.p2_rounds_won = 0
                    if self.current_match < self.max_matches:
                        self.map_instance.randomize_map(self.p1, self.p2)
                    self.current_match += 1
        else:
            # Draw match won text
            if self.p1_rounds_won >= 2:
                text = "Player 1"
            else:
                text = "Player 2"
            font = pygame.font.Font("./Fonts/retro.ttf", 80)
            text = font.render(f"{text} WON THE MATCH!", True, "red")

            if pygame.time.get_ticks() - self.match_won_timer < 2000:
                self.screen.blit(text, (200, 300))
            else:
                self.quit = True

    def finish_game(self):
        if self.mode == "PVE":
            if self.current_match >= self.max_matches and self.p1_rounds_won >= 2:
                # Draw match won text
                font = pygame.font.Font("./Fonts/retro.ttf", 90)
                text = font.render("Congratulations!", True, "black")

                if not self.do_once_match:
                    self.do_once_match = True
                    self.match_won_timer = pygame.time.get_ticks()

                if pygame.time.get_ticks() - self.match_won_timer < 2000:
                    self.screen.blit(text, (400, 300))
                else:
                    self.quit = True

            if self.match_lost:
                # Draw match won text
                font = pygame.font.Font("./Fonts/retro.ttf", 90)
                text = font.render("You Lost!", True, "black")

                if not self.do_once_match:
                    self.do_once_match = True
                    self.match_won_timer = pygame.time.get_ticks()

                if pygame.time.get_ticks() - self.match_won_timer < 2000:
                    self.screen.blit(text, (570, 300))
                else:
                    self.quit = True