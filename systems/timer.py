class Timer():
    def __init__(self):
        self.global_time = 0.0
        self.current_second = 0
        
    def update(self,dt):
        self.global_time += dt
        if int(self.global_time) > self.current_second:
            self.current_second = int(self.global_time)
            
    def get_seconds(self):
        return self.current_second