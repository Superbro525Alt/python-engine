from collections import namedtuple
from threading import current_thread
from typing import List, Match, Optional, Type

import sys

import pygame
from camera import Camera2d
import event
from sprite import Sprite
import utils
from gameobject import GameObject
from base import BaseComponent
from dataclasses import dataclass

import math

@dataclass
class Velocity:
    """
    Represents a velocity with magnitude and direction.

    Attributes:
        magnitude: The speed of the movement (non-negative float).
        direction: The direction of the movement in degrees (0-360).
    """

    magnitude: float
    direction: float  # In degrees (0-360)

    def __post_init__(self):
        """
        Ensures direction is within the range of 0 to 360 degrees.
        """
        self.direction = self.direction % 360

    def __add__(self, other: "Velocity") -> "Velocity":
        """
        Adds another velocity vector to this one.

        Args:
            other: The velocity vector to add.

        Returns:
            A new Velocity object with the combined magnitude and direction.
        """

        dir1_rad = self.direction * math.pi / 180
        dir2_rad = other.direction * math.pi / 180

        resultant_mag = math.sqrt(
            self.magnitude**2
            + other.magnitude**2
            - 2 * self.magnitude * other.magnitude * math.cos(dir1_rad - dir2_rad)
        )

        resultant_dir = (
            math.atan2(
                math.sin(dir1_rad) + math.sin(dir2_rad),
                math.cos(dir1_rad) + math.cos(dir2_rad),
            )
            * 180
            / math.pi
        )

        resultant_dir = resultant_dir % 360

        return Velocity(resultant_mag, resultant_dir)


class VelocityControl(BaseComponent):
    """
    This component controls the velocity of a GameObject.

    Attributes:
        _state: Internal dictionary storing the current velocity.
    """

    def __init__(self, obj: GameObject, velocity: int = 0) -> None:
        """
        Initializes the VelocityControl component with a starting velocity.

        Args:
            velocity: The initial velocity (integer).
        """
        super().__init__(self._tick)

        self._state["velocity"] = velocity
        self._state["currentvelocity"] = Velocity(velocity, 0)
        self._state["last90vel"] = Velocity(0, 0)

        RequireComponent(obj, Transform, Transform())

    def _tick(self, entity: GameObject, event: List[event.Event]) -> None:
        """
        This method is called every game tick.

        Args:
            entity: The GameObject this component is attached to.
            event: A list of events that occurred during the tick.

        This method does not currently implement any functionality related to
        velocity control. It's intended to be overridden in subclasses.
        """
        pass

    def AddVelocity(self, vel: Velocity) -> None:
        """
        Adds a velocity to the current velocity.

        Args:
            vel: The velocity to add (Velocity object).

        Updates the internal velocity state with the combined velocity
        """

        self._state["currentvelocity"] += vel

    def SetVelocity(self, vel: Velocity, combine_angle: bool = True) -> None:
        """
        Sets the current velocity to the new velocity

        Args:
            vel: The velocity to add (Velocity object).

        Updated the internal state to match the new velocity
        """

        current_vel: Velocity = self._state["currentvelocity"]
        
        if combine_angle:
            self._state["currentvelocity"] = Velocity(current_vel.magnitude, ((current_vel.direction + vel.direction) / 2) % 360)
        else:
            self._state["currentvelocity"] = vel

class Controls(BaseComponent):
    """
    This component handles user input and controls the GameObject's movement.

    Attributes:
        _state: Internal dictionary storing the current speed.
    """

    def __init__(self, obj: GameObject):
        """
        Initializes the Controls component with a starting speed.
        """
        super().__init__(self._tick)

        self._state["speed"] = 1

        RequireComponent(obj, VelocityControl, VelocityControl(obj))

    def _tick(self, entity: GameObject, events: List[event.Event]) -> None:
        """
        This method is called every game tick.

        Args:
            entity: The GameObject this component is attached to.
            events: A list of events that occurred during the tick.

        Adds velocity to the gameobject based on controls
        """
        velcontrol: BaseComponent | None = entity.GetComponent(VelocityControl)

        if velcontrol is None:
            return

        if not isinstance(velcontrol, VelocityControl):
            return
        
        ks = []

        for _event in events:
            if type(_event) == event.Keydown:
                ks.append(_event)

        if len(ks) == 0:
            velcontrol.SetVelocity(Velocity(0, 0))
        
        v: List[int] = []
        for _event in ks:

            if event.match_key(_event, "w"):
                v.append(0) 
            elif event.match_key(_event, "d"):
                v.append(90)
            elif event.match_key(_event, "s"):
                v.append(180)
            elif event.match_key(_event, "a"):
                v.append(270)

        if len(v) != 0:
            velcontrol.SetVelocity(Velocity(self.state()["speed"], sum(v) / len(v)), False)
        else:
            velcontrol.SetVelocity(Velocity(0, 0))

class Transform(BaseComponent):
    def __init__(self, initial_pos: utils.Position2d = utils.Position2d(0, 0, utils.Rotation2d(0))):
        super().__init__(self._tick)
        
        self.pos = initial_pos

    def _tick(self, entity: GameObject, events: List[event.Event]) -> None:
        pass
    
    def SetPosition(self, new_pos: utils.Position2d):
        self.pos = new_pos

    def AddPosition(self, pos: utils.Position2d):
        self.pos.x += pos.x
        self.pos.y += pos.y
        self.pos.rot += pos.rot

        self.pos.__post_init__()

    def GetPos(self):
        return self.pos

class Model(BaseComponent):
    def __init__(self, obj: GameObject, sprite: Sprite = Sprite()):
        super().__init__(self._tick)

        RequireComponent(obj, Transform, Transform())
       
        self.sprite: Sprite = sprite

        t: BaseComponent | None = obj.GetComponent(Transform)
        
        if t is not None and isinstance(t, Transform):
            self.transform: Transform = t

    def _tick(self, entity: GameObject, events: List[event.Event]) -> None:
        pass

    def Render(self, screen: pygame.surface.Surface, camera: Camera2d):
        if (camera.IsVisible(self.transform.GetPos())):
            self.sprite.Display(screen) 

def RequireComponent(obj: GameObject, component: Type[BaseComponent], to_add: BaseComponent | None = None) -> bool:
    """
    Requires a component on a game GameObject

    Args:
        obj: GameObject.
        component: The type of component to check for
        to_add: The component to add if it doesn't exist (optional)
    """
    if obj.GetComponent(component) == None:
        if to_add != None:
            obj.AddComponent(to_add)
        return False
    return True

def MatchComponent(c1: BaseComponent, c2: Type[BaseComponent | None]) -> bool:
    """
    Checks if a component is of the same type as another component or subclass.

    Args:
        c1: The first component to compare.
        c2: The second component or type to compare against.

    Returns:
        True if c1 is an instance of c2 or a subclass of c2, False otherwise.
    """
    return isinstance(c1, c2)
