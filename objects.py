import pygame
import os
import random

class Object(pygame.sprite.Sprite):
    def __init__(self, walkable = 0):
        pygame.sprite.Sprite.__init__(self)
        self.walkable = walkable # flaga wskazująca czy saper jest w stanie przejsć przez dany obiekt

class Grass(Object):
    def __init__(self, pos_x, pos_y, width, height):
        super().__init__()
        self.image = pygame.image.load(os.path.join('images', 'tile.png'))
        self.image_scaled = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image_scaled.get_rect(center = (pos_x, pos_y))
        self.deley = 0



class Mine(Object):
    def __init__(self, pos_x, pos_y, width, height):
        super().__init__()
        self.time = random.randint(1, 10)  # czas do auto-detonacji?
        self.reach = random.randint(1, 3)
        self.defused = False
        # saper w wyborze będzie
        # brał pod uwagę jaka mina w jego zasięgu wzroku ma najwyższe te dwie wartości?
        self.image = pygame.image.load(os.path.join('images', 'mine.png')).convert_alpha()
        self.image_scaled = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image_scaled.get_rect(center=(pos_x, pos_y))
        self.deley = 0
        self.itr = self.set_recon_image()

    def defuse(self, width, height):
        self.defused = True
        self.image = pygame.image.load(os.path.join('images', 'mine_defused.png')).convert_alpha()
        self.image_scaled = pygame.transform.scale(self.image, (width, height))

    def move_away(self, width, height):
        self.defused = True
        self.image = pygame.image.load(os.path.join('images', 'mine_moved.png')).convert_alpha()
        self.image_scaled = pygame.transform.scale(self.image, (width, height))

    def its_rock(self, width, height):
        self.defused = True
        self.image = pygame.image.load(os.path.join('images', 'rock.png')).convert_alpha()
        self.image_scaled = pygame.transform.scale(self.image, (width, height))

    def set_recon_image(self):
        picker = random.randint(1,10)
        if picker == 1:
            return "./to_recognition/rock1.jpg"
        if picker == 2:
            return "./to_recognition/rock2.jpg"
        if picker == 3:
            return "./to_recognition/rock3.jpg"
        if picker == 4:
            return "./to_recognition/bomb1.jpg"
        if picker == 5:
            return "./to_recognition/bomb2.jpg"
        if picker == 6:
            return "./to_recognition/bomb3.jpg"
        if picker == 7:
            return "./to_recognition/bomb4.jpg"
        if picker == 8:
            return "./to_recognition/bomb5.jpg"
        if picker == 9:
            return "./to_recognition/bomb6.jpg"
        if picker == 10:
            return "./to_recognition/bomb7.jpg"



class Rock(Object):
    def __init__(self, pos_x, pos_y,width, height):
        super().__init__(1)
        self.image = pygame.image.load(os.path.join('images', 'rock.png')).convert_alpha()
        self.image_scaled = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image_scaled.get_rect(center=(pos_x, pos_y))
        self.deley = 1000


class Puddle(Object):
    def __init__(self, pos_x, pos_y, width, height):
        super().__init__()
        self.depth = random.randint(1, 3)  # im większa tym bardziej spowalnia sapera?
        self.image = pygame.image.load(os.path.join('images', 'puddle.png')).convert_alpha()
        self.image_scaled = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image_scaled.get_rect(center=(pos_x, pos_y))
        self.deley = 4
