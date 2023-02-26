class Piece:

    def __init__(self, type, name, is_white, position, coords) -> None:
        self.type = type
        self.name = name
        self.is_white = is_white
        self.position = position
        self.coords = coords
        self.has_moved = False
