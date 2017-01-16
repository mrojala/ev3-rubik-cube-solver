from colorsys import rgb_to_hls
from colors import Colors

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

        order = [(2, 1), (2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]

        for i in range(4):
            self.hand.push()
            self.base.semi_turn(7, 0)
            face_rgbs[order[2 * i][0]][order[2 * i][1]] = self.hand.measure_side()
            self.base.semi_turn(10)
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
            return Colors.WHITE

        if hls[2] < -0.6:
            # the sensor give almost no difference between red and orange
            # green channel seems to be the most reliable
            return Colors.RED if rgb[1] < 60 else Colors.ORANGE

        if hls[0] < 0.15:
            return Colors.YELLOW

        return Colors.BLUE if hls[0] > 0.45 else Colors.GREEN

    def identify_face_colors(self, face_rgbs):
        face_colors = [[self.get_color(face_rgbs[j][i]) for i in range(3)] for j in range(3)]
        return face_colors

    def identify_cube_colors(self, cube_rgbs):
        cube_colors = [self.identify_face_colors(cube_rgbs[k]) for k in range(6)]
        return cube_colors
