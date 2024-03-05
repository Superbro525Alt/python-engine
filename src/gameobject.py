from typing import List, Optional, Type
from base import BaseComponent
from event import EventManager
from utils import BaseObject


class GameObject(BaseObject):
    def __init__(self) -> None:
        self.components: List[BaseComponent] = []

    def AddComponent(self, comp: BaseComponent) -> None:
        """
        Adds a component to the GameObject

        Args:
            comp: The component to add

        Returns:
            Nothing
        """
        self.components.append(comp)

    def GetComponent(self, comp_type: Type[BaseComponent]) -> BaseComponent | None:
        """
        Returns an instance of the requested component type from self.components, if found.

        Args:
            comp_type: The type of component to retrieve.

        Returns:
            An instance of the requested component type, or None if not found and not a subclass of BaseComponent.
        """
        for component in self.components:
            if isinstance(component, comp_type):
                if issubclass(type(component), BaseComponent):
                    return component

        return None

    def OnTick(self) -> None:
        """
        Calls the OnTick method of all attached components.

        This method iterates through the `components` list of the GameObject and
        calls the `OnTick` method of each component, passing the GameObject itself
        as an argument. This allows components to update their state or perform
        actions each game tick.
        """
        for component in self.components:
            component.OnTick(self)

    def __str__(self) -> str:
        l = self.__dict__.copy()
        l.pop("components") 
        s = f"{self.__class__.__name__}({', '.join([f'{key}={value}' for key, value in l.items()])}"

        if self.components != []:
            if (len(l.items()) != 0):
                s += ", "
            s += "components=["
            for comp in self.components:
                s += comp.__class__.__name__
                if (self.components.index(comp) != len(self.components) - 1):
                    s += ", "
            s+= "]"
        s += ")"

        return s
