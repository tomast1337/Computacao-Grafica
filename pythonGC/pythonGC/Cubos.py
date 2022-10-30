import ctypes
import logging
from math import sin

import sdl2
from basic import BasicOpenGLApp
from OpenGL.GL import *
from OpenGL.GLU import *


class Cubos(BasicOpenGLApp):
    def __init__(self, full_screen=False):
        """
        Esse exemplo desenha quatro cubos, um em cada canto da tela rotacionando em torno de si mesmo.
        """
        super().__init__(
            width=800, height=600, title="Cubes test", full_screen=full_screen
        )
        self.vertices = (  # Vertices of the cube
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, -1, 1),
            (-1, 1, 1),
        )
        self.linhas = (  # Lines of the cube
            (0, 1),
            (0, 3),
            (0, 4),
            (2, 1),
            (2, 3),
            (2, 7),
            (6, 3),
            (6, 4),
            (6, 7),
            (5, 1),
            (5, 4),
            (5, 7),
        )
        self.faces = (  # Faces of the cube
            (0, 1, 2, 3),
            (3, 2, 7, 6),
            (6, 7, 5, 4),
            (4, 5, 1, 0),
            (1, 5, 7, 2),
            (4, 0, 3, 6),
        )
        self.cores = (
            (1, 0, 0),
            (1, 1, 0),
            (0, 1, 0),
            (0, 1, 1),  # Colors of the cube
            (0, 0, 1),
            (1, 0, 1),
            (0.5, 1, 1),
            (1, 0, 0.5),
        )

        self.angle = [0, 0, 0]
        self.camera = [0, 0, 0]
        logging.info("Application started")
        if full_screen:
            logging.info("Full screen mode")

    def update(self):
        x, y = ctypes.c_int(0), ctypes.c_int(0)
        mouseClick = sdl2.mouse.SDL_GetMouseState(None, None)
        sdl2.mouse.SDL_GetMouseState(x, y)

        mousePos = [x.value - self.window_width / 2, y.value - self.window_height / 2]

        if mouseClick & 1:  # Left click
            self.camera[2] += 1
        elif mouseClick & 4:  # Right click
            self.camera[2] -= 1

        self.camera[0] = mousePos[0] / 100
        self.camera[1] = mousePos[1] / 100

        self.angle[0] += mousePos[0] / self.window_width * 10
        self.angle[1] += mousePos[1] / self.window_height * 10

        logging.debug(
            f"Camera position: {self.camera}",
        )
        logging.debug(
            f"Mouse position: {mousePos}",
        )

    def render(self):
        def desenhaCubo(self, singleColor=False):
            glBegin(GL_QUADS)
            i = 0
            for face in self.faces:
                if singleColor:
                    glColor3fv(self.cores[i])
                for vertex in face:
                    if not singleColor:
                        glColor3fv(self.cores[vertex])
                    glVertex3fv(self.vertices[vertex])
                i = i + 1
            glEnd()

        glClear(
            GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT
        )  # Clear the screen and the depth buffer
        for i in range(2):
            for j in range(2):
                glPushMatrix()
                # draw each cube in the center of each quadrant
                glTranslatef(
                    (i * 2 - 1) * 2 + self.camera[0],
                    (j * 2 - 1) * 2 - self.camera[1],
                    self.camera[2],
                )
                glRotatef(self.angle[0], i, j, 1)
                glRotatef(self.angle[1], 1, i, j)
                desenhaCubo(self)
                glPopMatrix()

        glFlush()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    exemplo = Cubos(full_screen=True)
    exemplo.run()
