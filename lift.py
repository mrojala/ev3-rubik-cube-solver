class Lift:
    motor = None
    pull_position = None
    push_position = None
    semi_push_position = None
    semi_pull_position = None
    state = None

    def __init__(self, motor):
        self.motor = motor
        self.reset()

    def reset(self):
        self.motor.stop_action = 'hold'

        self.motor.run_timed(time_sp=1000, speed_sp=300, timeout=1000)
        self.motor.wait_while('running')
        self.push_position = self.motor.position

        self.motor.run_timed(time_sp=1000, speed_sp=-300, timeout=1000)
        self.motor.wait_while('running')

        self.pull_position = self.motor.position

        self.semi_push_position = 0.4 * self.pull_position + 0.6 * self.push_position
        self.semi_pull_position = 0.7 * self.pull_position + 0.3 * self.push_position

        self.state = 'pull'

        self.motor.stop_action = 'coast'
        self.motor.stop()

    def push(self):
        if self.state != 'push':
            self.motor.stop_action = 'hold'
            self.motor.run_to_abs_pos(speed_sp=500, position_sp = self.push_position)
            self.motor.wait_while('running', timeout=1000)
            self.motor.stop()
            self.state = 'push'

    def knock(self):
#        if False: #self.state == 'pull':

        self.motor.stop_action = 'hold'
        self.motor.run_to_abs_pos(speed_sp=300, position_sp = self.semi_push_position)
        self.motor.wait_while('running', timeout=1000)
        self.state = 'knock'

        self.pull()

    def pull(self, speed=-300):
        if self.state != 'pull':
            self.motor.stop_action = 'coast'
            self.motor.run_to_abs_pos(speed_sp=speed, position_sp = self.pull_position)
            self.motor.wait_while('running', timeout=1000)
            self.motor.stop()
            self.state = 'pull'

    def semi_pull(self):
        if self.state == 'push':
            self.motor.stop_action = 'brake'
            self.motor.run_to_abs_pos(speed_sp=-200, position_sp = self.semi_pull_position)
            self.motor.wait_while('running', timeout=1000)
            self.motor.stop()
            self.state = 'semi_pull'

    def roll(self):
        self.push()
        self.semi_pull()
        self.push()

        #self.knock()
        #self.pull()
        #self.push()

    def roll_gently(self):
        self.push()
        self.semi_pull()
        #self.knock()
        self.pull()

    def rest(self):
        self.motor.stop_action = 'coast'
        self.motor.stop()
        self.state = 'rest'
