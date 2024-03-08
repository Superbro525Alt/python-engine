from dataclasses import dataclass
from typing import List
import pygame
from logger import debug, warning
from surface import Screen
from utils import Color, Rotation2d, SquareSize
from utils import BaseObject, Position2d

class Sprite(BaseObject):
    def __init__(self, size: int | float = 0) -> None:
        self.length = size

    def Display(self, screen: Screen, pos: Position2d):
        warning("Unbound display method for base sprite class. Use inheritence for new sprites")

class Square(Sprite):
    def __init__(self, size: SquareSize = SquareSize(200), color: Color = Color(255, 0, 0)) -> None:
        super().__init__(size.length)
        self.size: SquareSize = size
        self.color: Color = color

    def Display(self, screen: Screen, pos: Position2d):
        screen.square(self.size, self.color, pos)

class Pixel(Sprite):
    def __init__(self, color: Color = Color(255, 0, 0)) -> None:
        super().__init__(1)
        self.col = color

    def Display(self, screen: Screen, pos: Position2d):
        screen.set_at(pos, self.col)

class SpriteCollection(BaseObject):
    def __init__(self, initial_sprites: List[Sprite] = []):
        self.sprites = initial_sprites
        
    def DisplayAll(self, screen: Screen, pos: Position2d):
        [sprite.Display(screen, pos) for sprite in self.sprites]

class PixelCollection(SpriteCollection):
    def __init__(self, initial_sprites: List[Pixel] = []):
        self.sprites = initial_sprites

    def DisplayAll(self, screen: Screen, pos: Position2d):
        i = 0
        for sprite in self.sprites:
            sprite.Display(screen, pos+Position2d(i, 0, Rotation2d(0)))
            i+=1

class Pixels(Sprite):
    def __init__(self, pixels: List[Pixel]) -> None:
        super().__init__(len(pixels))

        self.collection = PixelCollection(pixels)

    def Display(self, screen: Screen, pos: Position2d):
        self.collection.DisplayAll(screen, pos)

