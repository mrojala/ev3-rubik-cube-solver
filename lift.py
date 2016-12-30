class Lift:
    motor = None
    pull_position = None
    push_position = None
    state = None

    def __init__(self, motor):
        self.motor = motor
        self.reset()

    def reset(self):
        self.motor.stop_action = 'hold'

        self.motor.run_timed(time_sp=1000, speed_sp=-300, timeout=2000)
        self.motor.wait_while('running')

        self.pull_position = self.motor.position

        self.motor.run_timed(time_sp=1000, speed_sp=300, timeout=2000)
        self.motor.wait_while('running')
        self.push_position = self.motor.position

        self.state = 'push'

    def push(self):
        if (self.state != 'push'):
            self.motor.stop_action = 'hold'
            self.motor.run_to_abs_pos(speed_sp=500, position_sp = self.push_position, timeout=2000)
            self.motor.wait_while('running')
            self.motor.stop()
            self.state = 'push'

    def pull(self):
        if (self.state != 'pull'):
            self.motor.stop_action = 'coast'
            self.motor.run_to_abs_pos(speed_sp=-300, position_sp = self.pull_position, timeout=2000)
            self.motor.wait_while('running')
            self.motor.stop()
            self.state = 'pull'

    def roll(self):
        self.push()
        self.pull()
        self.push()

    def relax(self):
        self.motor.stop_action = 'coast'
        self.motor.stop()
        self.state = 'relax'
