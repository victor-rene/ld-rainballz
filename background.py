import copy
import os
from random import randint

from kivy.clock import Clock
from kivy.graphics import Color, Mesh
from kivy.uix.widget import Widget

from displacement import Displacement


class Background(Widget):

    def __init__(self, **kw):
        super(Background, self).__init__(**kw)
        # self.frames = -1
        with self.canvas:
            self.clr = Color(0,.2,.2,mode='hsv')
            self.mesh = Mesh(mode='triangles', source='img/background.png')
        self.build_mesh()

    def build_mesh(self):
        self.vertices = []
        self.displacements = []
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        mesh_file = os.path.join(curr_dir, 'background.mesh')
        with open(mesh_file) as f:
            for line in f:
                coords = line.split(' ')
                i_max = len(coords)-1
                for i in range(0, i_max, 2):
                    self.vertices.extend([
                        self.x + float(coords[i]) * self.width,
                        self.y + float(coords[i+1]) * self.height,
                        float(coords[i]),
                        float(coords[i+1]) ])
                    self.displacements.append(Displacement())

        self.indices = []
        for i in range(0, 152, 1): # max_range = w x h - 1
            if i > 0 and (i+1) % 17 == 0:
                continue
            #1st triangle
            self.indices.append(i)
            self.indices.append(i+1)
            self.indices.append(i+17)
            # 2nd triangle
            self.indices.append(i+18)
            self.indices.append(i+17)
            self.indices.append(i+1)

        self.mesh.vertices = self.vertices
        self.mesh.indices = self.indices

        # TODO, index interior vertices for deformation
        # for y in range(10):
            # for x in range(17):
                # i = x + y * 10
                # if x in (0, 16) or y in (0, 9):
                    # continue
                # else:
                    # self.interior.append(i)

    def move(self):
        # self.frames += 1
        self.move_color()
        self.move_mesh()
        
    def move_color(self):
        h = self.clr.h
        h += 1 / 1000.
        while h > 1:
            h = h - 1
        self.clr.h = h

    def move_mesh(self):
        deformed = copy.deepcopy(self.vertices)
        n = len(self.vertices)
        for i in range(0, n, 4):
            # can be optimized
            j = i/4
            if j / 17 == 0 or j / 17 >= 9:
                continue
            if j % 17 == 0 or (j+1) % 17 == 0:
                continue
            disp = self.displacements[i/4]
            value = disp.step()
            if value is not None:
                dx, dy = value
                deformed[i] = self.vertices[i] + dx
                deformed[i+1] = self.vertices[i+1] + dy
            else:
                disp.reset()
        self.mesh.vertices = deformed
