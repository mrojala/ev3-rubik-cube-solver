from sklearn.cluster import KMeans
from itertools import chain

class Inspector:
    base = None
    hand = None
    lift = None

    def __init__(self, base, hand, lift):
        self.base = base
        self.hand = hand
        self.lift = lift

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

        self.hand.rest()

        return face_rgbs

    def measure_cube(self):
        faces = [None] * 6

        for i in range(1, 5):
            self.lift.roll_gently()
            faces[i % 4] = self.measure_face()

        self.base.turn()

        for i in range(4, 6):
            self.lift.roll_gently()
            faces[i] = self.measure_face()
            self.lift.roll()

        self.base.turn(-1)

        return faces

    def identify_colors(self, face_rgbs):
        measured_rgb_colors = list(chain.from_iterable(chain.from_iterable(face_rgbs)))

        est = KMeans(n_clusters=6)
        est.fit(measured_rgb_colors)

        labels = est.labels_

        cube_colors = [[[labels[i + 3 * j + 9 * k] for i in range(3)]  for j in range(3)] for k in range(6)]
        return cube_colors
