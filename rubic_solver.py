import rpyc
from lift import Lift
from base import Base
from hand import Hand
from inspector import Inspector

conn = rpyc.classic.connect('ev3dev.local')
ev3 = conn.modules['ev3dev.ev3']

base = Base(ev3.LargeMotor('outB'))
hand = Hand(ev3.MediumMotor('outC'), ev3.ColorSensor('in1'))
lift = Lift(ev3.LargeMotor('outA'))
inspector = Inspector(base, hand, lift)

lift.roll_gently()


cube = inspector.measure_cube()


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
