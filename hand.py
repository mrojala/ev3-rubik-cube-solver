class Hand:
    motor = None
    degree = None
    
    def __init__(self, motor):
        self.motor = motor
    
        self.degree = self.motor.count_per_rot / 360
        self.motor.ramp_down_sp = 0 #3000
        self.motor.ramp_up_sp = 0 #100
        
        self.reset()
        
    def reset(self):
        self.hold()
        
        self.motor.stop_action = 'coast'
        self.motor.stop()
        self.motor.position = 0
        self.motor.run_to_abs_pos(speed_sp=300, position=-120*self.degree)
        self.motor.wait_while('running', timeout=2000)
    
    def hold(self):
        self.motor.run_timed(time_sp=1000, speed_sp=-500)
        self.motor.wait_until('stalled')
        self.motor.stop_action = 'hold'
        self.motor.stop()        
        
    def stop(self):
        self.motor.stop_action = 'coast'
        self.motor.run_to_abs_pos(speed_sp=300, position_sp=-120*self.degree)
        