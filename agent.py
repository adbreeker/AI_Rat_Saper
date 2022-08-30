import pygame
import os
import sys

class Agent(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, pos):
        pygame.sprite.Sprite.__init__(self)
        self.view = 5 # ile pól przed sobą widzi saper
        self.image = pygame.image.load(os.path.join('images', 'ratAvatar.png')).convert_alpha()
        self.image_scaled = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image_scaled.get_rect(center = (pos_x, pos_y))
        self.pos_field = pos



    def move(self, window_size, margin, distance, direction, poschanger):

        if self.rect.right <= int(window_size) - margin*2 and direction == "RIGHT":
            self.pos_field += poschanger
            self.rect.centerx += distance

        if self.rect.left >= margin*2 and direction == "LEFT":
            self.pos_field += poschanger
            self.rect.centerx -= distance

        if self.rect.bottom <= int(window_size) - margin*2 and direction == "DOWN":
            self.pos_field += poschanger
            self.rect.centery += distance

        if self.rect.top >= margin*2 and direction == "UP":
            self.pos_field += poschanger
            self.rect.centery -= distance

