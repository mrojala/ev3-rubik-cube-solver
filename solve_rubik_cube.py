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

# init
base = Base(ev3.LargeMotor('outB'))
hand = Hand(ev3.MediumMotor('outC'), ev3.ColorSensor('in1'))
lift = Lift(ev3.LargeMotor('outA'))
inspector = Inspector(base, hand, lift)
mover = Mover(base, hand, lift)

# measure cube
cube_rgbs = inspector.measure_cube()
cube_colors = inspector.identify_cube_colors(cube_rgbs)

# find solution path
(solution_steps, current_orientation) = get_solution(cube_colors)

# execute solution
mover.reset_orientation(current_orientation)
mover.move(solution_steps)
