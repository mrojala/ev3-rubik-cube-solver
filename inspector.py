#from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from itertools import chain

class Inspector:
    base = None
    hand = None
    lift = None

    # These are medians of multiple measurements
    base_color_rgbs = [
        [160.0, 70.0, 25.0],
        [146.0, 54.0, 21.0],
        [195.0, 197.0, 68.0],
        [25.0, 69.0, 76.0],
        [37.0, 117.0, 41.0],
        [195.0, 260.0, 180.0],
        [94, 139, 98]
    ]

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

        # push the cube to left side, roughly middle,
        # need to adjust measurement position when rotated
        self.hand.push()

        self.base.semi_turn(5)
        face_rgbs[2][0] = self.hand.measure_corner(2)
        self.base.semi_turn()
        face_rgbs[1][0] = self.hand.measure_side()
        self.base.semi_turn(-5)
        face_rgbs[0][0] = self.hand.measure_corner(3)
        self.base.semi_turn()
        face_rgbs[0][1] = self.hand.measure_side(9)
        self.base.semi_turn()
        face_rgbs[0][2] = self.hand.measure_corner(10)
        self.base.semi_turn()
        face_rgbs[1][2] = self.hand.measure_side(9)
        self.base.semi_turn()
        face_rgbs[2][2] = self.hand.measure_corner(6)
        self.base.semi_turn()
        face_rgbs[2][1] = self.hand.measure_side(5)
        face_rgbs[1][1] = self.hand.measure_center(7)

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

        #est = KMeans(n_clusters=6)
        #est.fit(measured_rgb_colors)
        #labels = est.labels_
        #cube_colors = [[[labels[i + 3 * j + 9 * k] for i in range(3)]  for j in range(3)] for k in range(6)]

        nbrs = NearestNeighbors(n_neighbors=1).fit(self.base_color_rgbs)
        labels = nbrs.kneighbors(measured_rgb_colors)[1]

        # red and orange get mixed easily, use the red channel only for the determination
        fixed_labels = [
            5 if labels[i][0] == 6
            else (
                  labels[i][0] if labels[i][0] > 1
                  else (0 if measured_rgb_colors[i][1] >= 60 else 1)
            ) for i in range(len(labels))
        ]
        cube_colors = [[[fixed_labels[i + 3 * j + 9 * k] for i in range(3)]  for j in range(3)] for k in range(6)]

        return cube_colors

    def get_cube_colors(self):
        measurements = []
        colorings = []
        for i in range(3):
            measurement = self.measure_cube()
            measurements.append(measurement)
            coloring = self.identify_colors(measurement)
            colorings.append(coloring)

        final_coloring = colorings[0]
        error_count = 0

        for i in range(3):
            for j in range(3):
                if final_coloring[i][j] != colorings[1][i][j] and final_coloring[i][j] != colorings[2][i][j]:
                    if colorings[1][i][j] != colorings[2][i][j]:
                        error_count += 1
                    else:
                        final_coloring[i][j] = colorings[1][i][j]

        return (final_coloring, error_count, measurements, colorings)
