import pygame
import os
import random


class Boss(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.side = self.choose_side()
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'boss.png')), (80, 35))
        if self.side == 1:
            pos = (0, 60)
        else:
            pos = (900, 60)
        self.rect = self.image.get_rect(center=pos)
        self.vel = 3

    def choose_side(self):
        side = [-1, 1]
        return random.choice(side)

    def update(self):
        self.rect.x += self.vel * self.side
        if self.rect.x < - 50 or self.rect.y > 950:
            self.kill()
