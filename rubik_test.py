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

conn = rpyc.classic.connect('ev3dev.local')
ev3 = conn.modules['ev3dev.ev3']

base = Base(ev3.LargeMotor('outB'))
hand = Hand(ev3.MediumMotor('outC'), ev3.ColorSensor('in1'))
lift = Lift(ev3.LargeMotor('outA'))
inspector = Inspector(base, hand, lift)
mover = Mover(base, hand, lift)

cube = inspector.measure_cube()

# let's skip the measurements for a while
with open('data/sample_cube_rgb.json') as data_file:
    data = json.load(data_file)

cube = data['real']

solution_steps = get_solution(cube)

mover.move(solution_steps)







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
