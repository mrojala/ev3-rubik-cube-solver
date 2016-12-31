class Mover:
    base = None
    hand = None
    lift = None

    current_orientation = ('D', 'F')

    face_orders = {
        'D': ['F', 'R', 'B', 'L'],
        'F': ['U', 'R', 'D', 'L'],
        'L': ['U', 'F', 'D', 'B']
    }

    face_orders['U'] = list(reversed(face_orders['D']))
    face_orders['B'] = list(reversed(face_orders['F']))
    face_orders['R'] = list(reversed(face_orders['L']))

    def __init__(self, base, hand, lift):
        self.base = base
        self.hand = hand
        self.lift = lift

    def move(self, movements):
        """ Standardized movements, [DFRBLU][2']? """

        movements = [movements] if type(movements) == str else movements

        for movement in movements:
            new_bottom_face = movement[0]
            rotation_count = 1 if len(movement) == 1 else (2 if movement[1] == '2' else 3)

            self.change_bottom_face(new_bottom_face)
            self.rotate_face_at_bottom(rotation_count)

    def roll(self):
        self.lift.roll()
        self.current_orientation = self.get_roll_neighbor(self.current_orientation)

    def turn(self, k=1, is_held = False):
        k %= 4
        self.base.turn(k)
        if not is_held:
            for i in range(k):
                self.current_orientation = self.get_turn_neighbor(self.current_orientation)

    def rotate_face_at_bottom(self, rotation_count=1):
        self.hand.hold()
        self.turn(rotation_count, True)
        self.hand.rest()

    def change_bottom_face(self, new_bottom_face):
        at_bottom, at_front = self.current_orientation

        if at_bottom == new_bottom_face:
            return

        face_order = self.face_orders[at_bottom]

        if new_bottom_face not in face_order:
            self.roll()
            self.roll()
        else:
            turn_count = face_order.index(at_front) - face_order.index(new_bottom_face) - 1
            self.turn(turn_count)
            self.roll()

    def get_roll_neighbor(self, orientation):
        at_bottom, at_front = orientation

        index = self.face_orders[at_front].index(at_bottom)
        index = (index + 1) % 4
        new_at_bottom = self.face_orders[at_front][index]

        return (new_at_bottom, at_front)

    def get_turn_neighbor(self, orientation):
        at_bottom, at_front = orientation

        index = self.face_orders[at_bottom].index(at_front)
        index = (index + 3) % 4
        new_at_front = self.face_orders[at_bottom][index]

        return (at_bottom, new_at_front)
