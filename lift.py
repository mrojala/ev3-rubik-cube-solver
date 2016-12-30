class Lift:
    motor = None
    
    def __init__(self, motor):
        self.motor = motor
        self.reset()
        
    def reset(self):
        self.pull()
        self.motor.position = 0
        
    def push(self):
        self.motor.run_timed(time_sp=1000, speed_sp=300)
        self.motor.wait_until('stalled')
        self.motor.stop_action = 'hold'
        self.motor.stop()
        
    def pull(self):
        self.motor.run_timed(time_sp=1000, speed_sp=-300)
        self.motor.wait_until('stalled')
        self.motor.stop_action = 'coast'
        self.motor.stop()        
        
    def roll(self):
        self.push()
        self.pull()
        self.push()
