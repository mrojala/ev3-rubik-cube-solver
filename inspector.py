class Inspector:
    base = None
    hand = None

    def __init__(self, base, hand):
        self.base = base
        self.hand = hand

    def measure_face(self):
        face_rgbs = [[()] * 3 for i in range(3)]

        self.base.semi_turn()
        face_rgbs[2][0] = self.hand.measure_corner()
        self.base.semi_turn()
        face_rgbs[1][0] = self.hand.measure_side()
        self.base.semi_turn()
        face_rgbs[0][0] = self.hand.measure_corner()
        self.base.semi_turn()
        face_rgbs[0][1] = self.hand.measure_side()
        self.base.semi_turn()
        face_rgbs[0][2] = self.hand.measure_corner()
        self.base.semi_turn()
        face_rgbs[1][2] = self.hand.measure_side()
        self.base.semi_turn()
        face_rgbs[2][2] = self.hand.measure_corner()
        self.base.semi_turn()
        face_rgbs[2][1] = self.hand.measure_side()
        face_rgbs[1][1] = self.hand.measure_center()

        return face_rgbs
