from dataclasses import dataclass

import pygame
from logger import debug
from utils import BaseObject, Position2d, Rotation2d, copy

@dataclass
class ViewportSize3d:
    x: float | int
    y: float | int

    dist: float | int

@dataclass
class ViewportSize2d:
    x: float | int
    y: float | int

    buffer: float | int = 5

class Camera2d(BaseObject):
    def __init__(self, size: ViewportSize2d, initial_pos: Position2d = Position2d(0, 0, Rotation2d(0))) -> None:
        self.realsize: ViewportSize2d = copy(size)
        self.pos: Position2d = initial_pos
        self.size = copy(size)

        self.size.x += self.size.buffer
        self.size.y += self.size.buffer

    def IsVisible(self, pos: Position2d, size: int | float) -> bool:
        vis: bool = False
        if (
            self.pos.x - (self.size.x / 2) < pos.x + (size / 2) and
            self.pos.x + (self.size.x / 2) > pos.x - (size / 2) and
            self.pos.y - (self.size.y / 2) < pos.y + (size / 2) and
            self.pos.y + (self.size.y / 2) > pos.y - (size / 2)
        ):
            vis = True
            # debug("Rendered at: " + self.GlobalToLocal(pos).__str__())

         
        return vis
    
    def Move(self, new_pos: Position2d):
        self.pos += new_pos

    def GlobalToLocal(self, global_pos: Position2d) -> Position2d:
        local_x = global_pos.x - self.pos.x
        local_y = global_pos.y - self.pos.y 

        return Position2d(local_x, local_y, global_pos.rot)
