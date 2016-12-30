import collections

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

    def move(self, movement):



    def roll():
        self.lift.roll()
        self.current_orientation = self.get_roll_neighbor(self.current_orientation):

    def turn(k=1):
        k %= 4
        self.base.turn(k)
        for i in range(k):
            self.current_orientation = self.get_turn_neighbor(self.current_orientation):

    def rotate_face_at_bottom(k=1):
        self.hand.hold()
        self.turn(k)
        self.hand.rest()

    def orient(self, new_orientation):
        path = self.get_action_path(self.current_orientation, new_orientation)

        for action in path:
            if action == 'roll':
                self.roll()
            if action == 'turn':
                self.turn()

    def get_action_path(self, orientation_from, orientation_to):
        # use breadth first search to find the sortest paths
        # these could be precalculated as well and stored

        visited = set()
        queue = collections.deque([orientation_from])
        parents = {}

        while queue:
            orientation = queue.popleft()
            if orientation == orientation_to:
                break

            neighbors = {
                'roll': self.get_roll_neighbor(orientation),
                'turn': self.get_turn_neighbor(orientation)
            }

            for action, neighbor in neighbors.items():
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    parents[neighbor] = (orientation, action)

        path = []
        current = orientation_to
        while current != orientation_from:
            current, action = parents[current]
            path.append(action)

        return list(reversed(path))

    def get_roll_neighbor(self, orientation):
        at_bottom = orientation[0]
        at_front = orientation[1]

        index = self.face_orders[at_front].index(at_bottom)
        index = (index + 1) % 4
        new_at_bottom = self.face_orders[at_front][index]

        return (new_at_bottom, at_front)

    def get_turn_neighbor(self, orientation):
        at_bottom = orientation[0]
        at_front = orientation[1]

        index = self.face_orders[at_bottom].index(at_front)
        index = (index + 3) % 4
        new_at_front = self.face_orders[at_bottom][index]

        return (at_bottom, new_at_front)
