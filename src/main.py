from components import Controls, Model
from gameobject import GameObject
from renderer import Engine
from sprite import Pixel, Pixels, Square
from utils import Color, Position2d, Rotation2d

def tick(engine: Engine):
    engine.Camera.Move(Position2d(0.1, 0.1, Rotation2d(0))) 

if __name__ == "__main__":
    g = GameObject()
    g.AddComponent(Controls(g))
    g.AddComponent(Model(g, Square()))

    f = GameObject()
    f.AddComponent(Model(g, Pixels([Pixel(Color(0, 255, 0)), Pixel(Color(0, 255, 0)), Pixel(Color(0, 255, 0)), Pixel(Color(0, 255, 0))])))

    e = Engine(tpr=1, tick=tick)

    e.AddObject(g, 0)
    e.AddObject(f, 1)

    e.Run(True)

