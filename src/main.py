from components import Controls, Model, Transform
from gameobject import GameObject
from renderer import Engine
from sprite import Square


if __name__ == "__main__":
    g = GameObject()
    g.AddComponent(Controls(g))
    g.AddComponent(Model(g, Square()))

    e = Engine(raw_tpr=10)
    
    e.AddObject(g)

    e.Run(True)

