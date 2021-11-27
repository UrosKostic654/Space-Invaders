import sys
import os
import pygame
import random
from player import Player
from alien import Alien
from laser import Laser
from brick import Brick, shape
from boss import Boss

WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invaders!')

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
PURPLE = (79, 85, 221)
RED = (255, 0, 0)

# constants
FPS = 60
VEL = 4
MENU_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (522, 673))
GAME_OVER_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'game_over.png')), (425, 463))
LIVES_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'shooter.png')), (67, 34))

# alien characteristics
ALIEN_VEL = 1
ANIMATE_TIME = 400
ALIEN_LASER_WAIT = 1000
ALIEN_LASER_VEL = 3
ALIEN_START_Y = 100
BOSS_WAIT = 25000


def create_aliens():
    all_aliens = pygame.sprite.Group()
    x = 90
    y = ALIEN_START_Y
    for n in range(5):
        count = 1
        while count <= 10:
            if n < 1:
                all_aliens.add(Alien('small', (x, y)))
                x += 80
                count += 1
            elif n < 3:
                all_aliens.add(Alien('med', (x, y)))
                x += 80
                count += 1
            elif n < 5:
                all_aliens.add(Alien('big', (x, y)))
                x += 80
                count += 1
        else:
            x = 90
            y += 50

    return all_aliens


def alien_velocity(all_aliens):
    global ALIEN_VEL, ANIMATE_TIME

    if len(all_aliens) % 10 == 0:
        ALIEN_VEL += 1
        if ANIMATE_TIME != 100:
            ANIMATE_TIME -= 100

    if len(all_aliens) < 5:
        if len(all_aliens) % 1 == 0:
            ALIEN_VEL += 1
            ANIMATE_TIME -= 20

    return ALIEN_VEL


def alien_movement(aliens):
    for alien in aliens:
        alien.animate(ANIMATE_TIME)
        if alien.direction == 1:
            alien.rect.x += ALIEN_VEL
        else:
            alien.rect.x -= ALIEN_VEL

    for alien in aliens:
        if alien.rect.right >= WIDTH:
            aliens.update()
            break
        elif alien.rect.left <= 0:
            aliens.update()
            break


def check_alien_shot(alien_lasers, all_aliens):
    if len(all_aliens) > 0:
        random_alien = random.choice(all_aliens.sprites())
        alien_lasers.add(Laser(WHITE, random_alien.rect.center))
        return True


def create_block(x_start, y_start):
    walls = pygame.sprite.Group()
    size = 10
    for row_index, row in enumerate(shape):
        for col_index, col in enumerate(row):
            if col == 'x':
                x = x_start + col_index * size
                y = y_start + row_index * size
                block = Brick(size, PURPLE, x, y)
                walls.add(block)
    return walls


def create_wall(x_start, y_start):
    wall = []
    for n in range(5):
        wall.append(create_block(x_start, y_start))
        x_start += 164
    return wall


def detect_collision(aliens, player, alien_lasers, wall, boss):
    for alien in aliens:
        if pygame.sprite.spritecollide(alien, player.lasers, True):
            alien.kill()
            alien_velocity(aliens)
            player.score += alien.score

    if pygame.sprite.spritecollide(player, alien_lasers, True):
        player.lives -= 1
        if player.lives == 0:
            game_over(player)

    for block in wall:
        for brick in block:
            if pygame.sprite.spritecollide(brick, player.lasers, True):
                brick.kill()
            if pygame.sprite.spritecollide(brick, alien_lasers, True):
                brick.kill()
            if pygame.sprite.spritecollide(brick, aliens, False):
                brick.kill()

    for ship in boss:
        if pygame.sprite.spritecollide(ship, player.lasers, True):
            ship.kill()
            player.score += 500

    if pygame.sprite.spritecollide(player, aliens, False):
        player.lives = 0
        game_over(player)


def save_hiscore(player):
    with open('scores.txt', 'w+') as scores:
        score = scores.readline()
        score.strip('\n')
        scores.write(str(player.score))


def get_hiscore():
    try:
        with open('scores.txt', 'r') as hi_score:
            score = hi_score.readline()
    except FileNotFoundError:
        with open('scores.txt', 'r') as hi_score:
            score = hi_score.readline()
    finally:
        if score == '':
            score = 0

    return int(score)


def display_hud(player):
    lives_start_x = 10
    for life in range(player.lives - 1):
        WIN.blit(LIVES_IMG, (lives_start_x, 850))
        lives_start_x += 80

    pygame.font.init()
    myfont = pygame.font.Font(os.path.join('Assets', 'BarcadeBrawl.ttf'), 20)
    score = myfont.render(f'Score: {player.score}', False, WHITE)

    hiscore = myfont.render(f'Hiscore: {get_hiscore()}', False, PURPLE)

    WIN.blit(hiscore, (WIDTH - hiscore.get_size()[0], 10))
    WIN.blit(score, (0, 10))


def draw_window(player, aliens, alien_lasers, wall, boss):
    WIN.fill(BLACK)
    WIN.blit(player.image, player.rect)
    player.lasers.draw(WIN)

    aliens.draw(WIN)
    alien_lasers.draw(WIN)

    boss.draw(WIN)

    for block in wall:
        block.draw(WIN)

    display_hud(player)

    pygame.display.update()


def reset():
    global ALIEN_VEL, ANIMATE_TIME
    ALIEN_VEL = 1
    ANIMATE_TIME = 400


def main():
    player = Player((WIDTH//2, HEIGHT - 100), VEL, WIDTH)
    all_aliens = create_aliens()
    alien_lasers = pygame.sprite.Group()
    walls = create_wall(70, 670)
    boss = pygame.sprite.Group()

    alien_laser_time = pygame.time.get_ticks()
    boss_time = pygame.time.get_ticks()

    clock = pygame.time.Clock()

    while player.lives != 0:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.handle_movement(WHITE)
        alien_movement(all_aliens)

        if player.lasers:
            player.shoot_laser()

        current_time = pygame.time.get_ticks()
        if current_time - alien_laser_time > ALIEN_LASER_WAIT:
            check_alien_shot(alien_lasers, all_aliens)
            alien_laser_time = current_time

        current_time = pygame.time.get_ticks()
        global BOSS_WAIT
        if current_time - boss_time > BOSS_WAIT:
            boss.add(Boss())
            boss_time = current_time

        if boss:
            boss.update()

        if alien_lasers:
            alien_lasers.update(ALIEN_LASER_VEL, True)

        if not all_aliens:
            global ALIEN_START_Y
            if ALIEN_START_Y < 200:
                ALIEN_START_Y += 50
            all_aliens = create_aliens()
            if walls:
                for wall in walls:
                    wall.remove()
            walls = create_wall(60, 670)
            reset()

        detect_collision(all_aliens, player, alien_lasers, walls, boss)
        draw_window(player, all_aliens, alien_lasers, walls, boss)


def main_menu():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        WIN.fill(BLACK)
        WIN.blit(MENU_IMG, (200, 75))
        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            run = False
            main()


def game_over(player):
    global ALIEN_START_Y
    ALIEN_START_Y = 50
    time = pygame.time.get_ticks()
    wait = 3000
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.font.init()
        myfont = pygame.font.Font(os.path.join('Assets', 'BarcadeBrawl.ttf'), 20)

        score = myfont.render(f'Score: {player.score}', False, WHITE)
        hiscore = myfont.render(f'Hiscore: {get_hiscore()}', False, PURPLE)

        WIN.fill(BLACK)
        WIN.blit(GAME_OVER_IMG, (250, 100))
        WIN.blit(score, (WIDTH/2 - score.get_size()[0] / 2, 650))
        WIN.blit(hiscore, (WIDTH/2 - hiscore.get_size()[0] / 2, 700))
        pygame.display.update()

        current_time = pygame.time.get_ticks()
        if current_time - time > wait:
            run = False
            if player.score > get_hiscore():
                save_hiscore(player)
            reset()
            main_menu()


if __name__ == '__main__':
    main_menu()
