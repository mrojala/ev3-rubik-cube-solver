class LiftMock:
    def push(self): pass
    def knock(self): pass
    def pull(self, speed=-300): pass
    def semi_pull(self): pass
    def roll(self): pass
    def roll_gently(self): pass
    def rest(self): pass


class BaseMock:
    def turn(self, k=1): pass
    def semi_turn(self, adjust=0): pass
    def shake(self): pass


class HandMock:
    def hold(self): pass
    def push(self): pass
    def rest(self): pass
    def get_rgb(self): pass
    def measure_center(self, adjust=0): pass
    def measure_corner(self, adjust=0): pass
    def measure_side(self, adjust=0): pass
