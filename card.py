import pygame
import common
pygame.init()


class Card(pygame.sprite.Sprite):
    def __init__(self, file, value):
        pygame.sprite.Sprite.__init__(self)
        self.file = file
        self.front = pygame.transform.scale(pygame.image.load(file), (60, 84))
        self.back = pygame.transform.scale(common.BACK, (60, 84))
        self.image = self.back
        self.rect = self.image.get_rect()
        self.dragging = self.image.get_rect()
        self.grabbed = False

        self.value = value

    def flip_image(self):
        if self.image == self.front:
            self.image = self.back
        else:
            self.image = self.front

    def change_grabbed(self, rect = None):
        if self.grabbed:
            self.grabbed = False
            if rect is not None:
                self.rect = rect
        else:
            self.grabbed = True
            self.rect = self.dragging
            print(self.value)

    def update(self):
        if self.grabbed:
            self.rect.center = pygame.mouse.get_pos()

    def copy(self):
        return Card(self.file, self.value)


