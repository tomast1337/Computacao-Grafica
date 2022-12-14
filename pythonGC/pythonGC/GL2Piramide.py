import ctypes
import logging
from math import cos, sin

import numpy as np
import sdl2
from basicGL2 import BasicOpenGLApp
from OpenGL.GL import *
from OpenGL.GLU import *

from color_util import HSL2RGB

PI = 3.1415926535897932384626433832795
class Piramide(BasicOpenGLApp):
    def __init__(self, full_screen=True):
        """
        Esse exemplo desenha quatro cubos, um em cada canto da tela rotacionando em torno de si mesmo.
        """
        super().__init__(
            width=800,
            height=600,
            title="Piramide test",
            full_screen=full_screen,
            far=10000000,
        )
        self.numero_de_lados = 3

        self.vertices = []  # vetrices da piramide
        self.faces = []  # faces da piramide
        self.cores = []  # cores da piramide

        self.angle = [0, 0, -PI / 4]
        self.camera = [0,0,-25]
        self.rebuild = True
        logging.info("Application started")
        if full_screen:
            logging.info("Full screen mode")

        # set projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800 / 600, 0.1, 1000)

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

        # rotate based on mouse position

        self.angle[0] = y.value
        self.angle[1] = x.value
        self.angle[2] = -PI / 4

        # get if w or s is pressed
        keys = sdl2.keyboard.SDL_GetKeyboardState(None)

        if keys[sdl2.SDL_SCANCODE_W]:
            self.camera[2] += 0.1
        if keys[sdl2.SDL_SCANCODE_S]:
            self.camera[2] -= 0.1

        self.camera[0] = 0
        self.camera[1] = 0

        if self.rebuild:
            self.rebuild = False
        else:
            return

        self.vertices = []  # vetrices da piramide
        self.faces = []  # faces da piramide
        self.faces_normals = []  # normais das faces da piramide

        # vertices da piramide
        # v??rtice do meio da base
        self.vertices.append((0, 0, 0))

        numero_de_lados = int(self.numero_de_lados)
        # v??rtices da base
        for i in range(numero_de_lados):
            self.vertices.append(
                (
                    cos(2 * i * PI / numero_de_lados),
                    sin(2 * i * PI / numero_de_lados),
                    0,
                )
            )

        self.vertices.append((0, 0, 1))

        # faces da piramide
        # base
        for i in range(1, numero_de_lados):
            self.faces.append((0, i, i + 1))
        self.faces.append((0, numero_de_lados, 1))

        # laterais
        for i in range(1, numero_de_lados):
            self.faces.append((i, i + 1, numero_de_lados + 1))
        self.faces.append((numero_de_lados, 1, numero_de_lados + 1))

        # normais das faces da piramide
        self.faces_normals = []
        for face in self.faces:
            # calcula a normal da face
            v1 = np.array(self.vertices[face[1]]) - np.array(self.vertices[face[0]])
            v2 = np.array(self.vertices[face[2]]) - np.array(self.vertices[face[0]])
            normal = np.cross(v1, v2)
            normal = normal / np.linalg.norm(normal)
            self.faces_normals.append(normal)

        # cores da piramide por face
        self.cores = []
        for _ in self.faces:
            self.cores.append((1, 0, 0))
            self.cores.append((1, 0, 0))
            self.cores.append((0, 1, 0))
            self.cores.append((0, 1, 0))
            self.cores.append((0, 0, 1))
            self.cores.append((0, 0, 1))

    def render(self):
        def draw_piramide():
            glBegin(GL_TRIANGLES)
            for face in self.faces:
                for v??rtice_index in face:
                    glColor3fv(self.cores[v??rtice_index])
                    glVertex3fv(self.vertices[v??rtice_index])

            glEnd()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        glTranslatef(*self.camera)
        glRotatef(self.angle[0], 1, 0, 0)
        glRotatef(self.angle[1], 0, 1, 0)
        glRotatef(self.angle[2], 0, 0, 1)
        draw_piramide()
        glPopMatrix()


if __name__ == "__main__":
    app = Piramide()
    app.run()
