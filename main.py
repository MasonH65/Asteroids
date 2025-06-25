import pygame, sys
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from circleshape import *
from shot import *
from scoreboard import *

updateable = pygame.sprite.Group()
drawable = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()
Player.containers = (updateable, drawable)
Asteroid.containers = (asteroids, updateable, drawable)
AsteroidField.containers = (updateable)
Shot.containers = (shots, updateable, drawable)

def is_group_colliding(sprite1, sprite2):
    return sprite1.is_colliding(sprite2)

def main():
    pygame.init()
    pulse = pygame.time.Clock() 
    dt = 0
    score = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    scoreboard = Scoreboard(score)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    print('Starting Asteroids!')
    print(f'Screen width: {SCREEN_WIDTH}')
    print(f'Screen height: {SCREEN_HEIGHT}')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")  
        for ast in asteroids:
            if ast.is_colliding(player):
                print('Game over!')
                print(f'Your score was: {scoreboard.score}')
                sys.exit()
        collisions = pygame.sprite.groupcollide(asteroids, shots, False, True, is_group_colliding)
        for col in collisions:
            col.split()
            scoreboard.score += 100
        for obj in updateable:
            obj.update(dt)
        for obj in drawable:
            obj.draw(screen)
        scoreboard.draw(screen)
        pygame.display.flip()
        dt = pulse.tick(60) / 1000

if __name__ == "__main__":
    main()