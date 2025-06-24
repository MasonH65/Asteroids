from circleshape import *
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y, rotaion):
        super().__init__(x, y, SHOT_RADIUS)
        self.velocity = pygame.Vector2(0, 1).rotate(rotaion)

    def draw(self, screen):
        pygame.draw.circle(screen, 'white', self.position, self.radius, 2)

    def update(self, dt):
        self.position += (self.velocity * PLAYER_SHOOT_SPEED * dt)
        self.rect.center = (self.position.x , self.position.y)