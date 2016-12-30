class Hand:
    motor = None
    degree = None

    def __init__(self, motor):
        self.motor = motor

        self.degree = self.motor.count_per_rot / 360

        self.reset()

    def reset(self):
        self.motor.ramp_down_sp = 0 #3000
        self.motor.ramp_up_sp = 0 #100

        self.motor.stop_action = 'coast'
        self.motor.run_timed(time_sp=1000, speed_sp=-300)
        self.motor.wait_until('stalled')
        self.motor.stop()
        self.motor.position = 0

        self.motor.ramp_down_sp = 300
        self.motor.ramp_up_sp = 500

        self.rest()

    def hold(self):
        self.motor.stop_action = 'hold'
        self.motor.run_to_abs_pos(speed_sp=-1000, position_sp=0)
        self.motor.wait_while('running', timeout=2000)
        self.motor.stop()

    def rest(self):
        self.motor.stop_action = 'coast'
        self.motor.run_to_abs_pos(speed_sp=1000, position_sp=120*self.degree)
        self.motor.wait_while('running', timeout=2000)
        self.motor.stop()
