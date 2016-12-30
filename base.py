class Base:
    motor = None

    right_angle = None

    def __init__(self, motor):
        self.motor = motor

        self.right_angle = self.motor.count_per_rot / 4

        self.motor.stop_action = 'brake'
        self.motor.ramp_down_sp = 1000
        self.motor.ramp_up_sp = 0
        self.motor.position = 0

    def turn(self, k):
        k = (k + 4) % 4

        new_position = self.motor.position
        new_position -= (new_position + self.right_angle / 2) % self.right_angle - + self.right_angle / 2
        new_position += k * self.right_angle

        over_turn = 0.15 * self.right_angle

        self.motor.run_to_abs_pos(speed_sp = 1000, position_sp=new_position + over_turn)
        self.motor.wait_while('running', timeout=2000)

        self.motor.run_to_abs_pos(speed_sp = 300, position_sp=new_position)
        self.motor.wait_while('running', timeout=2000)

        self.motor.stop()
