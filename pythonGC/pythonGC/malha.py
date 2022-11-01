import ctypes
import logging
from math import cos, sin
import math
from random import random

import sdl2
from basicGL2 import BasicOpenGLApp
from OpenGL.GL import *
from OpenGL.GLU import *

from colorstuff import HSL2RGB

PI = 3.1415926535897932384626433832795


def funcOFxy(x, y):
    return random() / 5


class UVsphere(BasicOpenGLApp):
    def __init__(self, full_screen=False):
        """
        Esse exemplo desenha um prisma.
        """
        super().__init__(
            width=800,
            height=600,
            title="UVsphere",
            full_screen=full_screen,
            far=1000,
        )
        self.vertices = []
        self.faces = []
        self.cores = []

        r = 10
        for i in range(r):
            for j in range(r):
                self.vertices.append(
                    [i / r - 0.5, j / r - 0.5, funcOFxy(j + r / 2, i + r)]
                )

        for vertexIndex in range(len(self.vertices)):
            if vertexIndex % r == 0:
                continue  # exclui ultima linha

            if vertexIndex / r > r - 1:
                continue  # exclui ultima coluna

            vertexIndex = vertexIndex - 1
            # print(vertexIndex / r)
            bottom_face = [vertexIndex, vertexIndex + r, vertexIndex + 1]

            top_face = [vertexIndex + 1, vertexIndex + r + 1, vertexIndex + r]
            self.faces.append(bottom_face)
            self.faces.append(top_face)

        # color the faces, rainbow style
        hue_step = 360 / len(self.faces)
        current_hue = 0
        for face in self.faces:
            color = HSL2RGB((current_hue, random() * 50 + 25, random() * 50 + 10))
            # convert trupe to list
            color = list(color)
            print(color)
            self.cores.append(color)
            current_hue += hue_step

        # print(self.faces)

        self.angle = [0, 0, 0]
        self.camera = [0, 0, 0]

        if full_screen:
            logging.info("Full screen mode")

    def update(self):
        self.angle[0] += 1
        self.angle[1] += 0.01
        self.angle[2] += 1

    def render(self):
        # draw the uv sphere
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glPushMatrix()

        glTranslate(self.camera[0], self.camera[1], self.camera[2])

        glRotatef(self.angle[0], 1, 0, 0)
        glRotatef(self.angle[1], 0, 1, 0)
        glRotatef(self.angle[2], 0, 0, 1)

        glBegin(GL_TRIANGLES)
        for face in self.faces:
            glColor(
                self.cores[self.faces.index(face)][0],
                self.cores[self.faces.index(face)][1],
                self.cores[self.faces.index(face)][2],
            )
            glVertex(self.vertices[face[0]])
            glVertex(self.vertices[face[1]])
            glVertex(self.vertices[face[2]])
        glEnd()

        glPopMatrix()


if __name__ == "__main__":
    app = UVsphere()
    app.run()
