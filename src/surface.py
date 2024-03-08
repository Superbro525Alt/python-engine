import pygame
from logger import debug
from utils import BaseObject, Color, Position2d, Resolution, Rotation2d, SquareSize, copy

class Screen(BaseObject):
    def __init__(self, res: Resolution):
        self._screen: pygame.surface.Surface = pygame.display.set_mode(res.pygame())

    def fill(self, color: Color):
        self._screen.fill(color.rgb())

    def set_at(self, pos: Position2d, col: Color):
        self.square(SquareSize(1), col, pos)

    def square(self, size: SquareSize, color: Color, pos: Position2d):
        """Draws a square on the Pygame surface with center-based positioning.

        Args:
            size (SquareSize): Object defining the length of the square's sides.
            color (Color): Object defining the RGB color (and optional alpha) of the square.
            pos (Position2d): Object defining the center coordinates of the square.
        """
        size = copy(size)

        pos += Position2d(self._screen.get_width() / 2 - size.length / 2, self._screen.get_height() / 2 - size.length / 2, Rotation2d(0))

        pygame.draw.rect(self._screen, color.rgb(), pygame.Rect(pos.x, pos.y, size.length, size.length))
