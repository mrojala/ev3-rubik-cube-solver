from colorsys import rgb_to_hls

class Inspector:
    base = None
    hand = None
    lift = None

    color_names = [
        'orange',
        'red',
        'yellow',
        'blue',
        'green',
        'white',
        'white_center'
    ]

    def __init__(self, base, hand, lift):
        self.base = base
        self.hand = hand
        self.lift = lift

    def measure_face(self):
        face_rgbs = [[()] * 3 for i in range(3)]

        order = [(2, 1), (2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]

        for i in range(4):
            self.hand.push()
            face_rgbs[order[2 * i][0]][order[2 * i][1]] = self.hand.measure_side()
            self.base.semi_turn(5)
            face_rgbs[order[2 * i + 1][0]][order[2 * i + 1][1]] = self.hand.measure_corner()
            self.base.semi_turn()

        face_rgbs[1][1] = self.hand.measure_center()

        self.hand.rest()

        return face_rgbs

    def measure_cube(self):
        faces = [None] * 6

        for i in range(1, 5):
            self.lift.roll_gently()
            self.base.shake()
            faces[i % 4] = self.measure_face()

        self.base.turn()

        for i in range(4, 6):
            self.lift.roll_gently()
            self.base.shake()
            faces[i] = self.measure_face()
            self.lift.roll()

        self.base.turn(-1)

        return faces

    def get_color(self, rgb):
        hls = rgb_to_hls(*rgb)

        if hls[2] > -0.3:
            return 5

        if hls[2] < -0.6:
            return 1 if hls[0] < 0.05 else 0

        if hls[0] < 0.1:
            return 2

        return 3 if hls[0] > 0.45 else 4

    def identify_colors(self, face_rgbs):
        cube_colors = [[[self.get_color(face_rgbs[k][j][i]) for i in range(3)]  for j in range(3)] for k in range(6)]
        return cube_colors
