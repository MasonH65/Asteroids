from circleshape import *
from constants import *
from shot import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.shielded = False
        self.shield_timer = 0
        self.speed_multiplier = 1.0
        self.speed_timer = 0
        self.rapid_fire_multiplier = 1.0
        self.rapid_fire_timer = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        if self.speed_multiplier > 1.0:
            pygame.draw.polygon(screen, (255, 255, 0), self.triangle()) 
        pygame.draw.polygon(screen, (65, 255, 0), self.triangle(), 2)
        if self.shielded:
            pygame.draw.circle(screen, (0, 0, 255), self.position, self.radius + 10, 3)

    def rotate(self, dt):
        self.rotation += (PLAYER_TURN_SPEED * dt)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(dt * -1)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(dt * -1)
        if keys[pygame.K_SPACE]:
            self.shoot()
        self.timer -= dt
        if self.shielded:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.shielded = False
        if self.speed_multiplier > 1.0:
            self.speed_timer -= dt
            if self.speed_timer <= 0:
                self.speed_multiplier = 1.0
        if self.rapid_fire_multiplier < 1.0:
            self.rapid_fire_timer -= dt
            if self.rapid_fire_timer <= 0:
                self.rapid_fire_multiplier = 1.0
        

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * self.speed_multiplier * dt

    def shoot(self):
        if self.timer > 0:
            pass
        else:
            color = (255, 0, 0) if self.rapid_fire_multiplier < 1.0 else (65, 255, 0)
            Shot(self.position.x, self.position.y, self.rotation, color)
            self.timer = PLAYER_SHOOT_COOLDOWN * self.rapid_fire_multiplier

    def activate_shield(self, duration):
        self.shielded = True
        self.shield_timer = duration

    def activate_speed(self, multiplier, duration):
        self.speed_multiplier = multiplier
        self.speed_timer = duration

    def activate_rapid_fire(self, multiplier, duration):
        self.rapid_fire_multiplier = multiplier
        self.rapid_fire_timer = duration