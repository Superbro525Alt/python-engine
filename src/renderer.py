from dataclasses import dataclass
import threading
from typing import List, Tuple
from base import BaseComponent
from camera import Camera2d, ViewportSize2d
from components import MatchComponent, Model
from gameobject import GameObject
from logger import debug
from utils import BaseObject, Position2d, Rotation2d
import pygame

consts: dict[str, bool] = {"INIT": False}

def __init__():
    if not consts["INIT"]:
        debug("Initializing")
        pygame.init()
        consts["INIT"] = True

@dataclass
class Color:
    r: int
    b: int
    g: int

    def rgb(self) -> Tuple[int, int, int]:
        return (self.r, self.b, self.g)
    
    def string(self):
        return f"({self.r}, {self.g}, {self.b})"

@dataclass
class Resolution:
    width: int | float
    height: int | float

    def pygame(self):
        return (self.width, self.height)


class Renderer(BaseObject):
    def __init__(self, res: Resolution = Resolution(800, 600), color: Color = Color(0, 0, 0)) -> None:
        self.screen: pygame.surface.Surface = pygame.display.set_mode(res.pygame())
        self.color: Color = color

        debug("Color is " + self.color.string())
    
    def Render(self, gameobjects: List[GameObject], camera: Camera2d):
        self.screen.fill(self.color.rgb())

        for g in gameobjects:
            comp: BaseComponent | None = g.GetComponent(Model)
            if comp is not None:
                if isinstance(comp, Model):
                    model: Model = comp
                    model.Render(self.screen, camera)

        pygame.display.update()

        

class Engine(BaseObject):
    def __init__(self, renderer: Renderer | None = None, color: Color | None = None, camera: Camera2d | None = None, tpr: int | None = None, raw_tpr: float | int | None = None) -> None:
        __init__()
        
        if color is None:
            color = Color(255, 255, 255)
        if renderer is None:
            renderer = Renderer(color=color)
        if camera is None:
            camera = Camera2d(ViewportSize2d(10, 10))
        if tpr is None:
            tpr = 1

        self.renderer: Renderer = renderer
        self.gameobjects: List[GameObject] = []
        self.color: Color = color
        self.camera: Camera2d = camera

        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.tpr: int = tpr * pygame.display.get_current_refresh_rate()
        self.tick: int = 0

        self.raw_tpr = raw_tpr
            
    def Run(self, block=True):
        if block:
            self._run()
        else:
            threading.Thread(target=lambda: self._run(), daemon=True).start()

    def _run(self):
        while True:
            for g in self.gameobjects:
                g.OnTick()

            self.renderer.Render(self.gameobjects, self.camera)

            self.CheckNative()
            
            self.tick+=1

            if self.raw_tpr is not None:
                self.clock.tick(self.raw_tpr)
            else:
                self.clock.tick(self.tpr)

    def AddObject(self, obj: GameObject):
        self.gameobjects.append(obj)

    def exit(self):
        debug("Cleaning Up")

    def CheckNative(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                debug("Shutting Down")
                pygame.quit()
                self.exit()
                exit()
