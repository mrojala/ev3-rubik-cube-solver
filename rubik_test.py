import rpyc

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
lift = Lift(ev3.LargeMotor('outA'))
hand = Hand(ev3.MediumMotor('outC'), ev3.ColorSensor('in1'))
inspector = Inspector(base, hand, lift)
mover = Mover(base, hand, lift)


a = inspector.measure_face()


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

# let's skip the measurements for a while
#with open('data/sample_cube_rgb.json') as data_file:
#    data = json.load(data_file)
#cube = data['real']

solution_steps = get_solution(cube)

mover.move(solution_steps)

