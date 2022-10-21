import ctypes
import logging
from math import cos, sin

import sdl2
from basic import BasicOpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

PI = 3.1415926535897932384626433832795


class UVsphere(BasicOpenGL):
    def __init__(self, full_screen=False):
        """
        Esse exemplo desenha um prisma.
        """
        super().__init__(
            width=800,
            height=600,
            title="Prisma test",
            full_screen=full_screen,
            far=1000,
        )
        self.vertices = []
        self.faces = []
        self.uvs = []
        self.step_angle = PI * 2 / 60
        self.angle = [0, 0, 0]
        self.camera = [0, 0, 0]
        logging.info("Application started")

        if full_screen:
            logging.info("Full screen mode")

    def update(self):
        r = 1
        self.vertices = []
        self.faces = []
        self.uvs = []
        latitude = 0
        while latitude < PI * 2:
            longitude = 0
            while longitude < PI * 2:
                x = r * cos(longitude) * sin(latitude)
                y = r * sin(longitude) * sin(latitude)
                z = r * cos(latitude)
                self.vertices.append([x, y, z])
                self.uvs.append([longitude / (PI * 2), latitude / (PI * 2)])
                longitude += self.step_angle
            latitude += self.step_angle

        for i in range(len(self.vertices) - 1):
            self.faces.append(
                [i, i + 1, i + len(self.vertices) + 1, i + len(self.vertices)]
            )

        self.angle[0] += 1
        self.angle[1] += 1
        self.angle[2] += 1

    def render(self):
        # draw the uv sphere
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        glPushMatrix()
        glTranslatef(0.0, 0.0, -6)
        
        glRotatef(self.angle[0], 1, 0, 0)
        glRotatef(self.angle[1], 0, 1, 0)
        glRotatef(self.angle[2], 0, 0, 1)
        
        glBegin(GL_POINTS)
        for vertex in self.vertices:
            glColor3f(1, 1, 1)
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()
        
        glPopMatrix()
        


if __name__ == "__main__":
    app = UVsphere()
    app.run()
