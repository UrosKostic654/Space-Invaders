import pygame


class Laser(pygame.sprite.Sprite):

    def __init__(self, color, pos):
        super().__init__()
        self.image = pygame.Surface((3, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)

    def update(self, vel, is_alien):
        if is_alien:
            self.rect.y += vel
        else:
            self.rect.y -= vel
        if self.rect.y < 0 or self.rect.y > 900:
            self.kill()
