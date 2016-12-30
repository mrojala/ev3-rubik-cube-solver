class Base:
    motor = None
    
    def __init__(self, motor):
        self.motor = motor
        
        self.motor.stop_action = 'brake'
        self.motor.ramp_down_sp = 500
        self.motor.ramp_up_sp = 100
        self.motor.position = 0
        
    def turn(self, k):
        right_angle = self.motor.count_per_rot / 4
        
        new_position = self.motor.position
        new_position -= new_position % right_angle
        new_position += k * right_angle
        
        self.motor.run_to_abs_pos(speed_sp = 1000, position_sp=new_position)
        