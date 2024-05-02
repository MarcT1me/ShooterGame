import Engine


class Camera:
    def __init__(self, pos=0, speed: float = 1):
        self.pos: Engine.vec3 = Engine.vec3(pos) + Engine.vec3(Engine.App.window.screen.get_size()//2, 0)
        self.vel: Engine.vec3 = Engine.vec3(0)
        self.speed: float = speed
    
    def __event__(self, event):
        self.vel = Engine.vec3(0)
        
        key_ues = False
        if Engine.App.key_list[Engine.K_w]:
            self.vel.y -= 1; key_ues = True
        if Engine.App.key_list[Engine.K_s]:
            self.vel.y += 1; key_ues = True
        if Engine.App.key_list[Engine.K_a]:
            self.vel.x -= 1; key_ues = True
        if Engine.App.key_list[Engine.K_d]:
            self.vel.x += 1; key_ues = True
        
        n_vec = Engine.normalize(self.vel)
        self.vel = Engine.vec3(0) if Engine.isnan(n_vec)[0] else n_vec
        
        if not key_ues:
            for key, joystick in Engine.App.joysticks.items():
                self.vel.x += joystick.get_axis(0)
                self.vel.y += joystick.get_axis(1)
    
    def __update__(self):
        self.pos += self.vel*self.speed*Engine.App.clock.delta
