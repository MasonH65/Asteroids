import pygame, sys, os, random
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from circleshape import *
from shot import *
from scoreboard import *
from powerups import SpeedPowerUp, ShieldPowerUp, RapidFirePowerUp

updateable = pygame.sprite.Group()
drawable = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()
powerups = pygame.sprite.Group()

Player.containers = (updateable, drawable)
Asteroid.containers = (asteroids, updateable, drawable)
AsteroidField.containers = (updateable)
Shot.containers = (shots, updateable, drawable)
SpeedPowerUp.containers = (powerups, updateable, drawable)
ShieldPowerUp.containers = (powerups, updateable, drawable)
RapidFirePowerUp.containers = (powerups, updateable, drawable)

HIGHSCORES_FILE = "highscores.txt"

def load_highscores():
    if not os.path.exists(HIGHSCORES_FILE):
        return []
    with open(HIGHSCORES_FILE, "r") as f:
        return [int(line.strip()) for line in f.readlines() if line.strip().isdigit()]

def save_highscores(highscores):
    with open(HIGHSCORES_FILE, "w") as f:
        for score in highscores:
            f.write(f"{score}\n")

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
    highscores = load_highscores()
    powerup_timer = 0
    last_powerup_type = None

    print('Starting Asteroids!')
    print(f'Screen width: {SCREEN_WIDTH}')
    print(f'Screen height: {SCREEN_HEIGHT}')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")  
        powerup_timer += dt
        if powerup_timer > POWERUP_SPAWN_RATE:
            powerup_timer = 0
            x = random.randint(POWERUP_RADIUS, SCREEN_WIDTH - POWERUP_RADIUS)
            y = random.randint(POWERUP_RADIUS, SCREEN_HEIGHT - POWERUP_RADIUS)
            types = [SpeedPowerUp, ShieldPowerUp, RapidFirePowerUp]
            if last_powerup_type is not None:
                types = [t for t in types if t.__name__ != last_powerup_type]
            chosen = random.choice(types)
            chosen(x, y)
            last_powerup_type = chosen.__name__
        for ast in asteroids:
            if ast.is_colliding(player):
                if getattr(player, 'shielded', False):
                    continue  
                print('Game over!')
                print(f'Your score was: {scoreboard.score}')
                highscores.append(scoreboard.score)
                highscores = sorted(highscores, reverse=True)[:10]  
                save_highscores(highscores)
                print('Highscores:')
                for i, hs in enumerate(highscores):
                    print(f"{i + 1}. {hs}")
                sys.exit()
        collisions = pygame.sprite.groupcollide(asteroids, shots, False, True, is_group_colliding)
        for col in collisions:
            col.split()
            scoreboard.score += 100
        for powerup in powerups:
            if player.is_colliding(powerup):
                if isinstance(powerup, ShieldPowerUp):
                    player.activate_shield(powerup.duration)
                elif isinstance(powerup, SpeedPowerUp):
                    player.activate_speed(powerup.multiplier, powerup.duration)
                elif isinstance(powerup, RapidFirePowerUp):
                    player.activate_rapid_fire(powerup.multiplier, powerup.duration)
                powerup.kill()
        for obj in updateable:
            obj.update(dt)
        for obj in drawable:
            obj.draw(screen)
        scoreboard.draw(screen)
        pygame.display.flip()
        dt = pulse.tick(60) / 1000

if __name__ == "__main__":
    main()