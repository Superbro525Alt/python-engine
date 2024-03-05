import threading
from typing import List
from components import Model
from gameobject import GameObject
from utils import BaseObject
import pygame

class Renderer(BaseObject):
    def __init__(self) -> None:
        pass
    
    def Render(self, gameobjects: List[GameObject]):
        for g in gameobjects:
            if g.GetComponent(Model) is not None:
                pass
        

class Engine(BaseObject):
    def __init__(self, renderer: Renderer | None = None) -> None:
        if renderer is None:
            renderer = Renderer()

        self.renderer: Renderer = renderer
        self.gameobjects: List[GameObject] = []

    def Run(self, block=True):
        if block:
            self._run()
        else:
            threading.Thread(target=lambda: self._run(), daemon=True).start()

    def _run(self):
        while True:
            for g in self.gameobjects:
                g.OnTick()

    def AddObject(self, obj: GameObject):
        self.gameobjects.append(obj)
