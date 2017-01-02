import rpyc
import json
from itertools import chain
import numpy as np

from lift import Lift
from base import Base
from hand import Hand
from inspector import Inspector
from mover import Mover
from solver import get_solution
from mocks import LiftMock, BaseMock, HandMock

lift, base, hand = LiftMock(), BaseMock(), HandMock()

conn = rpyc.classic.connect('ev3dev.local')
ev3 = conn.modules['ev3dev.ev3']

base = Base(ev3.LargeMotor('outB'))
hand = Hand(ev3.MediumMotor('outC'), ev3.ColorSensor('in1'))
lift = Lift(ev3.LargeMotor('outA'))
inspector = Inspector(base, hand, lift)
mover = Mover(base, hand, lift)



#(final_coloring, error_count, measurements, colorings) = inspector.get_cube_colors()
#assert error_count == 0

cube = inspector.measure_cube()
final_coloring = inspector.identify_colors(cube)

(solution_steps, current_orientation) = get_solution(final_coloring)

mover.reset_orientation(current_orientation)
mover.move(solution_steps)



final_coloring = [[[2, 5, 5], [0, 3, 0], [1, 5, 5]],
 [[0, 4, 2], [2, 2, 4], [3, 1, 1]],
 [[0, 2, 3], [0, 4, 0], [2, 4, 1]],
 [[0, 4, 0], [3, 5, 5], [3, 3, 5]],
 [[1, 3, 4], [3, 1, 1], [4, 2, 2]],
 [[3, 5, 4], [1, 0, 1], [5, 2, 4]]]


mover.move(solution_steps)

 p: F
 s: U
 k: R
 o: B
 va: L
 vi: D



 ['F',
 'U',
 "D'",
 'B2',
 "R'",
 'B',
 'D2',
 "L'",
 'U2',
 'L',
 'U',
 'R2',
 'F2',
 'B2',
 'U2',
 'B2',
 'L2',
 "D'",
 'F2',
 'L2']

# let's skip the measurements for a while
#with open('data/sample_cube_rgb.json') as data_file:
#    data = json.load(data_file)
#cube = data['real']

solution_steps = get_solution(cube)

mover.move(solution_steps)



a = inspector.measure_face()

inspector.identify_colors([a] * 6)



#old tests


lift.roll_gently()


cube = inspector.measure_cube()

lift.rest()

inspector.identify_colors(cube)

inspector.measure_face()

with open('data/sample_cube_rgb.json') as data_file:
    data = json.load(data_file)

measured_rgb_colors = list(chain.from_iterable(chain.from_iterable(data['measured'])))
real_colors = list(chain.from_iterable(chain.from_iterable(data['real'])))

def which_color(c):
    return filter(lambda i: real_colors[i] == c, range(len(real_colors)))

def filter_measured_colors(c):
    return [measured_rgb_colors[j] for j in which_color(c)]

def get_color_rgb(c):
    return list(np.median(np.array(filter_measured_colors(c)), axis=0))

{k: get_color_rgb(v) for k, v in data['colors'].items()}


lift.roll()

lift.roll_gently()

lift.pull()
lift.push()

lift.semi_pull()

lift.rest()

lift.pull()


lift.knock()


base.turn(1)
base.turn(3)

base.semi_turn()


hand = Hand(ev3.MediumMotor('outC'), ev3.ColorSensor('in1'))

hand.hold()

hand.rest()

hand.measure_center()

hand.measure_side()

base.semi_turn()
hand.measure_corner()
base.semi_turn()

inspector = Inspector(base, hand, lift)

inspector.measure_face()

cube = inspector.measure_cube()
