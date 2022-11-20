import ctypes
import logging
from math import cos, sin

import numpy as np
import sdl2
from basicGL2 import BasicOpenGLApp
from OpenGL.GL import *
from OpenGL.GLU import *

PI = 3.1415926535897932384626433832795


class Prisma(BasicOpenGLApp):
    def __init__(self, full_screen=True):
        """
        Esse exemplo desenha quatro cubos, um em cada canto da tela rotacionando em torno de si mesmo.
        """
        super().__init__(
            width=800,
            height=600,
            title="Prisma test",
            full_screen=full_screen,
            far=1000,
        )
        self.numero_de_lados = 3

        self.vertices = []  # vetrices da Prisma
        self.faces = []  # faces da Prisma
        self.cores = []  # cores da Prisma

        self.angle = [0, 0, 0]
        self.camera = [0, 0,-25]
        self.rebuild = True
        logging.info("Application started")
        if full_screen:
            logging.info("Full screen mode")

    def update(self):
        x, y = ctypes.c_int(0), ctypes.c_int(0)
        mouseClick = sdl2.mouse.SDL_GetMouseState(None, None)
        sdl2.mouse.SDL_GetMouseState(x, y)

       

        if mouseClick & 1:
            if self.numero_de_lados <= 3:
                self.numero_de_lados = 3
            else:
                self.numero_de_lados -= 1
                self.rebuild = True

        if mouseClick & 4:
            if self.numero_de_lados >= 64:
                self.numero_de_lados = 64
            else:
                self.numero_de_lados += 1
                self.rebuild = True

        # rotate based on mouse position

        self.angle[0] = y.value
        self.angle[1] = x.value
        self.angle[2] = 0

        camera_step = .5
        # get w , a , s , d , q , e keys
        keys = sdl2.keyboard.SDL_GetKeyboardState(None)
        if keys[sdl2.SDL_SCANCODE_W]:
            self.camera[2] += camera_step
        if keys[sdl2.SDL_SCANCODE_S]:
            self.camera[2] -= camera_step
        if keys[sdl2.SDL_SCANCODE_A]:
            self.camera[0] -= camera_step
        if keys[sdl2.SDL_SCANCODE_D]:
            self.camera[0] += camera_step
        if keys[sdl2.SDL_SCANCODE_Q]:
            self.camera[1] -= camera_step
        if keys[sdl2.SDL_SCANCODE_E]:
            self.camera[1] += camera_step
        

        self.camera[0] = 0
        self.camera[1] = 0

        if self.rebuild:
            self.rebuild = False
        else:
            return
        self.vertices = []  # vetrices da Prisma
        self.faces = []  # faces da Prisma
        self.faces_normals = []  # normais das faces da Prisma

        # vertices da Prisma
        # vértice do meio da base
        self.vertices.append((0, 0, 0.25))

        numero_de_lados = int(self.numero_de_lados)
        # vértices da base
        for i in range(numero_de_lados):
            self.vertices.append(
                (
                    cos(2 * i * PI / numero_de_lados),
                    sin(2 * i * PI / numero_de_lados),
                    0.25,
                )
            )

        self.vertices.append((0, 0, 0.75))

        # vertices do topo
        for i in range(numero_de_lados):
            self.vertices.append(
                (
                    cos(2 * i * PI / numero_de_lados),
                    sin(2 * i * PI / numero_de_lados),
                    0.75,
                )
            )

        # faces do Prisma
        # faces da base
        for i in range(numero_de_lados):
            self.faces.append((0, i + 1, (i + 1) % numero_de_lados + 1))

        # faces do topo
        for i in range(numero_de_lados):
            self.faces.append(
                (
                    numero_de_lados + 1,
                    numero_de_lados + 2 + i,
                    numero_de_lados + 2 + (i + 1) % numero_de_lados,
                )
            )

        # faces laterais
        for i in range(numero_de_lados):
            # pontos do quad
            p1 = i + 1
            p2 = (i + 1) % numero_de_lados + 1
            p3 = numero_de_lados + 2 + i
            p4 = numero_de_lados + 2 + (i + 1) % numero_de_lados

            tri_1 = (p1, p2, p3)
            tri_2 = (p2, p3, p4)

            self.faces.append(tri_1)
            self.faces.append(tri_2)

        # cores da Prisma para cada face
        self.cores = []
        for i in range(len(self.faces)):
            self.cores.append((1, 1, 0))
            self.cores.append((1, 0, 1))
            self.cores.append((0, 1, 1))

    def render(self):
        def draw_prisma():
            glBegin(GL_TRIANGLES)
            for face in self.faces:
                for vertex in face:
                    glColor3fv(self.cores[vertex])
                    glVertex3fv(self.vertices[vertex])
            glEnd()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for i in range(3):
            for j in range(3):
                glPushMatrix()
                glTranslatef(
                    (i * 2 - 1) * 2 + self.camera[0],
                    (j * 2 - 1) * 2 - self.camera[1],
                    self.camera[2],
                )
                glRotatef(self.angle[0], 1, 0, 0)
                glRotatef(self.angle[1], 0, 1, 0)
                glRotatef(self.angle[2], 0, 0, 1)
                draw_prisma()
                glPopMatrix()

        glFlush()


if __name__ == "__main__":
    app = Prisma()
    app.run()
