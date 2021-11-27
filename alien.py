import pygame
import os

small_alien = [pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'tiny_alien_stand.png')), (35, 35)),
               pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'tiny_alien_step.png')), (35, 35))]
med_alien = [pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'med_alien_stand.png')), (40, 35)),
             pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'med_alien_step.png')), (40, 35))]
big_alien = [pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'big_alien_stand.png')), (42, 35)),
             pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'big_alien_step.png')), (42, 35))]


class Alien(pygame.sprite.Sprite):

    def __init__(self, alien_type, pos):
        super().__init__()
        self.type = alien_type
        self.state = 0
        if self.type == 'small':
            self.image = small_alien[self.state]
            self.score = 30
        elif self.type == 'med':
            self.image = med_alien[self.state]
            self.score = 20
        else:
            self.image = big_alien[self.state]
            self.score = 10
        self.rect = self.image.get_rect(center=pos)
        self.direction = 1
        self.time = pygame.time.get_ticks()

    def update(self):
        self.direction *= - 1
        self.rect.y += 10

    def change_state(self):
        if self.state == 1:
            self.state = 0
        else:
            self.state = 1

    def animate(self, speed):
        current_time = pygame.time.get_ticks()
        if current_time - self.time > speed:
            self.change_state()
            self.time = current_time
        if self.type == 'small':
            self.image = small_alien[self.state]
        elif self.type == 'med':
            self.image = med_alien[self.state]
        else:
            self.image = big_alien[self.state]
