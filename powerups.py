import pygame
from circleshape import CircleShape
from constants import *

class PowerUp(CircleShape):
    def __init__(self, x, y, powerup_type):
        super().__init__(x, y, POWERUP_RADIUS)
        self.color = (255, 255, 255)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)


class SpeedPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, "speed")
        self.color = (255, 255, 0)
        self.multiplier = 1.5
        self.duration = 5


class ShieldPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, "shield")
        self.color = (0, 0, 255)  
        self.duration = 5


class RapidFirePowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, "rapidfire")
        self.color = (255, 0, 255)  
        self.multiplier = 0.5 
        self.duration = 5



