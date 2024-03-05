from utils import BaseObject


class Sprite(BaseObject):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

class Square(Sprite):
    pass
