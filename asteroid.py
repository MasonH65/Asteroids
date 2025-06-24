import random 
from constants import *
from circleshape import *


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, 'white', self.position, self.radius,2)

    def update(self, dt):
        self.position += (self.velocity * dt)
        self.rect.center = (self.position.x , self.position.y)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        rand_angle = random.uniform(20, 50)
        ast_1 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
        ast_2 = Asteroid(self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS)
        ast_1.velocity = pygame.Vector2.rotate(self.velocity, rand_angle) * 1.2
        ast_2.velocity = pygame.Vector2.rotate(self.velocity, -rand_angle) * 1.2