import pygame
from constants import *

class Scoreboard():
    def __init__(self, score):
        self.score = score
        self.font = pygame.font.SysFont(None, FONT_SIZE)

    def draw(self, screen):
        score_text = f'Score: {self.score}'
        rendered_text = self.font.render(score_text, True, FONT_COLOR)
        screen.blit(rendered_text, SCORE_POSITION)