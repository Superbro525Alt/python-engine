from event import EventManager
import utils


class BaseComponent(utils.BaseObject):
    """
    The base class for game components.

    Attributes:
        tick: A reference to the component's tick method.
        _state: Internal dictionary to store state information.
    """

    def __init__(self, tick):
        """
        Initializes the BaseComponent.

        Args:
            tick: The function to call on each game tick.
        """
        super().__init__()  # Assumes utils.BaseObject has an __init__ method
        self.tick = tick
        self._state = {}
        self.eventmanager = EventManager()

    def OnTick(self, entity) -> None:
        """
        Calls the component's tick method, passing the entity and an empty event list.

        Args:
            entity: The entity this component is attached to.
        """
        self.tick(entity, self.eventmanager.get())

    def state(self) -> dict:
        """
        Returns the component's internal state dictionary.

        Returns:
            A dictionary containing the component's state information.
        """
        return self._state
