from dataclasses import dataclass
import threading
from typing import overload

import pygame

import time

@dataclass
class Rotation3d:
    x: int | float
    y: int | float
    z: int | float

@dataclass
class Rotation2d:
    x: int | float

    def __add__(self, other):
        if isinstance(other, Rotation2d):
            return Rotation2d(self.x + other.x) 
        raise Exception("You can only add 2 rotation2d's")

    def __post_init__(self) -> None:
        self.x = self.x % 360

@dataclass
class Position3d:
    x: int | float
    y: int | float
    z: int | float

    rot: Rotation3d

@dataclass
class Position2d:
    x: int | float
    y: int | float

    rot: Rotation2d

    def Rotate(self, other: Rotation2d):
        self.rot.x += other.x
    
    def __post_init__(self):
        self.rot.__post_init__()

    def __add__(self, other):
        if isinstance(other, Position2d):
            return Position2d(self.x + other.x, self.y + other.y, self.rot + other.rot)
        raise Exception("Can only add 2 Position2d's")

class BaseObject:
    """
    Base class for all objects in the project.

    Provides common functionalities like string representation, equality comparison,
    and hashing.

    This class cannot be used for arithmetic operations or comparisons
    like greater than, less than, etc.

    Do not directly call the constructor using `BaseObject()`. Use specific
    subclasses instead.
    """

    def __str__(self) -> str:
        """
        Returns a string representation of the object in the format:

        "ClassName(key1=value1, key2=value2, ...)"

        Example:
            >>> obj = BaseObject()
            >>> str(obj)
            "BaseObject()"
        """
        return f"{self.__class__.__name__}({', '.join([f'{key}={value}' for key, value in self.__dict__.items()])})"

    def __eq__(self, other) -> bool:
        """
        Checks if two objects are equal by comparing their internal dictionaries.

        Args:
            other: The object to compare with.

        Returns:
            True if the objects are of the same type and have the same internal state,
            False otherwise.
        """
        if type(other) == type(self):
            return self.__dict__ == other.__dict__
        return False

    def __hash__(self) -> int:
        """
        Calculates a hash value for the object based on its string representation.

        Used for efficient storage and retrieval in dictionaries and sets.
        """
        return hash(self.__str__())

    def __ne__(self, other) -> bool:
        """
        Checks if two objects are not equal by calling the `__eq__` method.
        """
        return not self.__eq__(other)

    def __gt__(self, other) -> bool:
        """
        Raises an exception as this class does not support comparison operations.
        """
        raise Exception("Cannot compare objects")

    def __lt__(self, other) -> bool:
        """
        Raises an exception as this class does not support comparison operations.
        """
        raise Exception("Cannot compare objects")

    def __ge__(self, other) -> bool:
        """
        Raises an exception as this class does not support comparison operations.
        """
        raise Exception("Cannot compare objects")

    def __le__(self, other) -> bool:
        """
        Raises an exception as this class does not support comparison operations.
        """
        raise Exception("Cannot compare objects")

    def __add__(self, other) -> float:
        """
        Raises an exception as this class does not support addition.
        """
        raise Exception("Cannot add objects")

    def __sub__(self, other) -> float:
        """
        Raises an exception as this class does not support subtraction.
        """
        raise Exception("Cannot subtract objects")

    def __enter__(self) -> object:
        """
        Returns the object itself, used for the `with` statement.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Does nothing, called by the `with` statement when exiting the context.
        """
        pass

    def __del__(self) -> None:
        """
        Does nothing, called when the object is garbage collected.
        """
        pass

    def __init__(self, *args, **kwargs) -> None:
        """
        Private constructor, should not be called directly. Use specific subclasses instead.
        """
        pass

class Timer(BaseObject):
    def __init__(self) -> None:
        self.elapsed = 0

        self.created = time.time() 

    def Set(self, time):
        self.created = time

    def Reset(self):
        self.created = time.time()
    
    @property
    def Elapsed(self):
        return time.time() - self.created
