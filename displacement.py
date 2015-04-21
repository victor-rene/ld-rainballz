import math
from random import randint


class Displacement(object):

    def __init__(self):
        self.done = None
        self.vector = None
        self.frames = None
        self.period = None
        self.reset()
        
    def reset(self):
        self.done = False
        self.vector = randint(40, 60), randint(40, 60)
        self.frames = 0
        self.period = randint(270, 450)
        
    def step(self):
        if not self.done and self.frames < self.period:
            pct = float(self.frames) / self.period
            d_pct = pct if pct < .5 else 1 - pct
            dx = self.vector[0] * d_pct
            dy = self.vector[1] * d_pct
            a = 2 * math.pi * pct
            self.frames += 1
            self.done = self.frames >= self.period
            return math.cos(a) * dx, math.sin(a) * dy

if __name__ == '__main__':
    disp = Displacement()
    while not disp.done:
        print disp.step()
