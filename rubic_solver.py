import rpyc
from lift import Lift
from base import Base
from hand import Hand
from inspector import Inspector

conn = rpyc.classic.connect('ev3dev.local') # host name or IP address of the EV3
ev3 = conn.modules['ev3dev.ev3']      # import ev3dev.ev3 remotely

lift = Lift(ev3.LargeMotor('outA'))

lift.roll()

lift.pull()
lift.push()

lift.relax()

base = Base(ev3.LargeMotor('outB'))

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

inspector = Inspector(base, hand)

inspector.measure_face()
