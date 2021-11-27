import pygame
from laser import Laser
import os


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, vel, width):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'shooter.png')), (67, 34))
        self.rect = self.image.get_rect(midbottom=pos)
        self.vel = vel
        self.max_x = width
        self.lasers = pygame.sprite.Group()
        self.lives = 3
        self.score = 0

    def handle_movement(self, color):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if self.rect.right < self.max_x:
                self.rect.x += self.vel
        if keys[pygame.K_LEFT]:
            if self.rect.x > 0:
                self.rect.left -= self.vel
        if keys[pygame.K_SPACE]:
            if len(self.lasers) < 1:
                self.lasers.add(Laser(color, self.rect.center))
                self.shoot_laser()

    def shoot_laser(self):
        self.lasers.update(10, False)
