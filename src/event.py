from dataclasses import dataclass
from functools import update_wrapper
import threading
from time import sleep
from typing import Any, List
from keyboard import add_hotkey, on_press, on_release
from pynput.keyboard import Key, Listener

EVENT_MAX: int = 1
EVENT_MIN: int = 0


@dataclass
class Event:
    """
    An object that represents an event with data.

    Args:
        id: The ID of the event (int).
        name: The name of the event (str).
        data: (Optional) The data (if needed) of the event (dict[str, Any]).
    """

    id: int
    name: str
    data: dict[str, Any] | None = None

    def __init__(self, id: int, name: str, data: dict[str, Any] | None = None):
        """
        Custom constructor to receive `data` argument optionally.

        Args:
            id: The ID of the event (int).
            name: The name of the event (str).
            data: (Optional) The data (if needed) of the event (dict[str, Any]).
        """
        self.id = id
        self.name = name

        if not EVENT_MIN <= id <= EVENT_MAX:
            raise Exception(
                f"""ID is not possible:
            Min id: {EVENT_MIN}
            Max id: {EVENT_MAX}"""
            )

        if data is not None:
            self.data = data
        else:
            self.data = {}

    def __post_init__(self):
        """Ensures the event ID is within the valid range."""
        if not EVENT_MIN <= self.id <= EVENT_MAX:
            raise Exception(
                f"""ID is not possible:
            Min id: {EVENT_MIN}
            Max id: {EVENT_MAX}"""
            )


@dataclass
class Keydown(Event):
    """
    An event representing a key press.

    Inherits all attributes and methods from `Event`.

    Args:
        key (string, optional): The key pressed. Defaults to "".
    """

    def __post_init__(self):
        """
        Updates the `data` dictionary with the key information.

        Calls the base class's `__post_init__` to ensure ID validation.
        """
        super().__post_init__()

        if self.data == None:
            self.data = {}


def match_key(key: Keydown, to_match: str):
    return key.name.lower() == to_match or key.name.upper() == to_match


class InputManager:
    """
    A class that listens for key presses and returns a list of KeyDown events.
    """

    def __init__(self):
        self.events: List[Keydown] = []

        self.listener = None

        self.listen()

    def listen(self):
        """
        Starts listening for key presses using the keyboard library and populates the internal events list.
        """

        def on_press_callback(event):
            try:
                if self.events.count(Keydown(1, event.char)) == 0:
                    self.events.append(Keydown(1, event.char))
            except:
                if self.events.count(Keydown(1, event.name)) == 0:
                    self.events.append(Keydown(1, event.name))

        def on_release_callback(event):
            try:
                for i in range(self.events.count(Keydown(1, event.char))):
                    self.events.remove(Keydown(1, event.char))
            except:
                for i in range(self.events.count(Keydown(1, event.name))):
                    self.events.remove(Keydown(1, event.name))
        
        self.listener = Listener(on_press_callback, on_release_callback)        
         
        self.listener.start()

    def get_events(self) -> List[Keydown]:
        """
        Returns the list of KeyDown events captured since the last call to get_events().
        After retrieving the events, the internal list is cleared.
        """

        events = self.events.copy()
        # threading.Thread(target=lambda: self.empty_events()).start()
        return events

    def add_hotkey(self, combination: str, callback):
        """
        Adds a hotkey for a callback
        """
        add_hotkey(combination, callback)

    def empty_events(self, timeout: float =0):
        """
        Clear events
        """

        sleep(timeout)
        self.events = []


class EventManager:
    """
    A class that manages events
    """

    def __init__(self) -> None:
        self.inputmanager = InputManager()
        self.events = []

    def get(self):
        e = self.events.copy()
        self.events = []
        return self.inputmanager.get_events() + e

    def add_event(self, event: Event):
        self.events.append(event)

