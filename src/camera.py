from dataclasses import dataclass

import pygame
from utils import BaseObject, Position2d, Rotation2d

@dataclass
class ViewportSize3d:
    x: float | int
    y: float | int

    dist: float | int

@dataclass
class ViewportSize2d:
    x: float | int
    y: float | int

class Camera2d(BaseObject):
    def __init__(self, size: ViewportSize2d, initial_pos: Position2d = Position2d(0, 0, Rotation2d(0))) -> None:
        self.size: ViewportSize2d = size
        self.pos: Position2d = initial_pos

    def IsVisible(self, pos: Position2d) -> bool:
        vis: bool = False

        if self.pos.x + -(self.size.x / 2) < pos.x < self.pos.x + (self.size.x / 2) and self.pos.y + -(self.size.y / 2) < pos.y < self.pos.y + (self.size.y / 2):
            vis = True
         
        return vis
    
    def Move(self, new_pos: Position2d):
        self.pos += new_pos
