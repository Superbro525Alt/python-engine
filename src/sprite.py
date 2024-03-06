from typing import List
import pygame
from logger import warning
from utils import BaseObject


class Sprite(BaseObject):
    def __init__(self) -> None:
        pass

    def Display(self, screen: pygame.surface.Surface):
        warning("Unbound display method for base sprite class. Use inheritence for new sprites")

class Square(Sprite):
    pass

class SpriteCollection(BaseObject):
    def __init__(self, initial_sprites: List[Sprite] = []):
        self.sprites = initial_sprites
        
    def DisplayAll(self, screen: pygame.surface.Surface):
        [sprite.Display(screen) for sprite in self.sprites]
