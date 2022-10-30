import ctypes
import logging
from math import cos, sin

import sdl2
from basic import BasicOpenGLApp
from OpenGL.GL import *
from OpenGL.GLU import *

PI = 3.1415926535897932384626433832795


class UVsphere(BasicOpenGLApp):
    def __init__(self, full_screen=False):
        """
        Esse exemplo desenha um prisma.
        """
        super().__init__(
            width=800,
            height=600,
            title="Prisma test",
            full_screen=full_screen,
            far=10000,
        )
        self.vertices = []
        self.faces = []
        self.uvs = []
        self.step_angle = PI * 2 / 32
        self.angle = [0, 0, 0]
        self.camera = [0, 0, 0]
        logging.info("Application started")

        if full_screen:
            logging.info("Full screen mode")

    def update(self):
        r = 0.5
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

        # create the faces
        latitude = 0
        while latitude < PI * 2 - self.step_angle:
            longitude = 0
            while longitude < PI * 2 - self.step_angle:
                self.faces.append(
                    [
                        int(longitude / self.step_angle)
                        + int(latitude / self.step_angle)
                        * int(PI * 2 / self.step_angle),
                        int(longitude / self.step_angle)
                        + int(latitude / self.step_angle + 1)
                        * int(PI * 2 / self.step_angle),
                        int(longitude / self.step_angle + 1)
                        + int(latitude / self.step_angle + 1)
                        * int(PI * 2 / self.step_angle),
                        int(longitude / self.step_angle + 1)
                        + int(latitude / self.step_angle)
                        * int(PI * 2 / self.step_angle),
                    ]
                )
                longitude += self.step_angle
            latitude += self.step_angle

        self.angle[0] += 1
        self.angle[1] += 1
        self.angle[2] += 1

    def render(self):
        # draw the uv sphere
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glPushMatrix()

        """
        glTranslatef(0, 0, -.5)
        glRotatef(self.angle[0], 1, 0, 0)
        glRotatef(self.angle[1], 0, 1, 0)
        glRotatef(self.angle[2], 0, 0, 1)
        glBegin(GL_POINTS)
        glColor3f(1, 1, 1)
        for vertex in self.vertices:
            glVertex3fv(vertex)
        glEnd()
        """

        glTranslatef(0, 0, -0.5)
        glRotatef(self.angle[0], 1, 0, 0)
        glRotatef(self.angle[1], 0, 1, 0)
        glRotatef(self.angle[2], 0, 0, 1)
        glBegin(GL_QUADS)
        for face in self.faces:
            # color based on the face vertcies
            for vertex in face:
                glColor3fv(self.vertices[vertex])
            for i in range(4):
                glVertex3fv(self.vertices[face[i]])
        glEnd()

        glPopMatrix()


if __name__ == "__main__":
    app = UVsphere()
    app.run()
