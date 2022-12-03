import ctypes
import rich
import os
import glm
import sdl2
from OpenGL import GL
from array import array
from model_util import Model
from camera import Camera
from shader import ShaderProgram
from basicGL3 import OpenGLApp
from texture import Texture

def flatten(l):
    return [item for sublist in l for item in sublist]

class Dice(Model):
    def __init__(self):
        self.vertices = []
        self.indices = []
        self.normals = []
        self.texcoords = []
        self.position = glm.vec3(0.0, 0.0, 0.0)
        self.rotation = glm.vec3(0.0, 0.0, 0.0)
        self.scale = glm.vec3(1.0, 1.0, 1.0)
        self.generate()

    def generate(self):
        self.attr_position = array(
            "f",
            flatten([                      
                 # Vertex positions
                [ 1,  1,  1],[ 1,  1, -1],[  1, -1,  1], # F A
                [ 1, -1,  1],[ 1,  1, -1],[  1, -1, -1], # F B
                [ 1,  1,  1],[-1,  1,  1],[  1, -1,  1], # R A
                [ 1, -1,  1],[-1,  1,  1],[ -1, -1,  1], # R B
                [ 1,  1,  1],[ 1,  1, -1],[ -1,  1,  1], # U A
                [-1,  1,  1],[ 1,  1, -1],[ -1,  1, -1], # U B
                [-1,  1,  1],[-1,  1, -1],[ -1, -1,  1], # L A
                [-1, -1,  1],[-1,  1, -1],[ -1, -1, -1], # L B
                [-1, -1,  1],[-1, -1, -1],[  1, -1,  1], # D A
                [ 1, -1,  1],[-1, -1, -1],[  1, -1, -1], # D B
                [-1, -1, -1],[-1,  1, -1],[  1, -1, -1], # B A
                [ 1, -1, -1],[-1,  1, -1],[  1,  1, -1], # B B
            ]),
        )

        self.indices = array(
            "I",
            [
                # Indices
                # Front
                2, 1, 0,
                5, 4, 3,
                # Right
                6, 7, 8,
                9, 10, 11,
                # Up
                12, 13, 14,
                15, 16, 17,
                # Left
                18, 19, 20,
                21, 22, 23,
                # Down
                24, 25, 26,
                27, 28, 29,
                # Back
                30, 31, 32,
                33, 34, 35,
            ],
        )

        self.attr_textureCoord = array(
            "f",
            flatten([     #Texture Coordinates
                [  0, 1/2],[0,  1],[1/3, 1/2], # F A
                [1/3, 1/2],[0,  1],[1/3,   1], # F B

                [ 0,   0],[0, 1/2],[1/3,   0], # R A
                [1/3,  0],[0, 1/2],[1/3, 1/2], # R B
                
                [1/3, 1/2],[1/3,  1],[2/3, 1/2], # U A
                [2/3, 1/2],[1/3,  1],[2/3,   1], # U B
                
                [1/3,  0],[1/3, 1/2],[2/3,   0], # L A
                [2/3,  0],[1/3, 1/2],[2/3, 1/2], # L B
                
                [2/3, 1/2],[2/3,  1],[1, 1/2], # D A
                [  1, 1/2],[2/3,  1],[1,   1], # D B
                
                [2/3,  0],[2/3, 1/2],[1,   0], # B A
                [  1,  0],[2/3, 1/2],[1, 1/2], # B B
            ]),
        )


    def load(self):
        """
        in vec3 attr_position;
        in vec2 attr_textureCoord;
        """
        self.vao = GL.glGenVertexArrays(1)
        self.vbo = GL.glGenBuffers(1)
        self.ebo = GL.glGenBuffers(1)
        self.tbo = GL.glGenBuffers(1)

        GL.glBindVertexArray(self.vao)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER,
            self.attr_position.itemsize * len(self.attr_position),
            ctypes.c_void_p(self.attr_position.buffer_info()[0]),
            GL.GL_STATIC_DRAW,
        )
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
        GL.glEnableVertexAttribArray(0)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.tbo)
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER,
            self.attr_textureCoord.itemsize * len(self.attr_textureCoord),
            ctypes.c_void_p(self.attr_textureCoord.buffer_info()[0]),
            GL.GL_STATIC_DRAW,
        )
        GL.glVertexAttribPointer(1, 2, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
        GL.glEnableVertexAttribArray(1)

        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        GL.glBufferData(
            GL.GL_ELEMENT_ARRAY_BUFFER,
            self.indices.itemsize * len(self.indices),
            ctypes.c_void_p(self.indices.buffer_info()[0]),
            GL.GL_STATIC_DRAW,
        )

        GL.glBindVertexArray(0)        


    def render(self):
        GL.glBindVertexArray(self.vao)
        GL.glDrawElements(GL.GL_TRIANGLES, len(self.indices), GL.GL_UNSIGNED_INT, None)
        GL.glBindVertexArray(0)

    def model_matrix(self):
        mat4 = glm.mat4(1.0)
        mat4 = glm.translate(mat4, self.position)
        mat4 = glm.rotate(mat4, glm.radians(self.rotation.x), glm.vec3(1.0, 0.0, 0.0))
        mat4 = glm.rotate(mat4, glm.radians(self.rotation.y), glm.vec3(0.0, 1.0, 0.0))
        mat4 = glm.rotate(mat4, glm.radians(self.rotation.z), glm.vec3(0.0, 0.0, 1.0))
        mat4 = glm.scale(mat4, self.scale)
        return mat4


class DiceApp(OpenGLApp):
    def __init__(self):
        super().__init__(800, 600, "The Dices Zone")
        self.camera = Camera()
        self.camera.position = glm.vec3(-24,-24,-24)
        self.camera.yaw = 45.0
        self.camera.pitch = 37.0
    def setup(self):
        # Lock the mouse
        sdl2.SDL_SetRelativeMouseMode(sdl2.SDL_TRUE)

        # OpenGL Initialization
        GL.glClearColor(0.2, 0.2, 0.2, 1)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)

        # Enable transparency
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        # Enable texture
        GL.glEnable(GL.GL_TEXTURE_2D)

        #Enable culling
        GL.glEnable(GL.GL_CULL_FACE)

        # Texture Clamp to border
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_BORDER)

        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST);

        # Pipeline (shaders)
        self.shader = ShaderProgram("SimpleTexture")
        self.shader.compile_shader()
        self.shader.link()

        # list uniforms
        rich.print(f"Available Uniforms: {self.shader.uniforms}")

        # Texture
        GL.glActiveTexture(GL.GL_TEXTURE0)  # set active texture
        self.texture = Texture(
            "./textures/dice.png",
        )  # load texture from file into active texture
        self.texture.load()  # load texture into GPU

        self.dice = Dice()
        self.dice.load()

    def render(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        with self.shader as s:
            s.set_uniform(b"view_matrix", self.camera.get_view_matrix())
            s.set_uniform(b"proj_matrix", self.camera.projection)
            s.set_uniform(b"textureSlot", 0)
            n = 10
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        self.dice.position = glm.vec3(i * 3 - n/2, j * 3 - n/2, k * 3 - n/2)
                        self.dice.rotation = glm.vec3(
                            glm.radians(i / n * 360) * 45 * glm.sin(self.frameCount / 100),
                            glm.radians(j / n * 360) * 45 * glm.sin(self.frameCount / 100),
                            glm.radians(k / n * 360) * 45 * glm.sin(self.frameCount / 100),
                        )
                        s.set_uniform(b"model_matrix", self.dice.model_matrix())
                        self.dice.render()

    def update(self):
        cameraSpeed = 0.25
        # get w a s d keys
        keys = sdl2.SDL_GetKeyboardState(None)
        self.camera.process_keyboard(keys, cameraSpeed)

        # get mouse movement
        x, y = ctypes.c_int(0), ctypes.c_int(0)
        sdl2.SDL_GetRelativeMouseState(ctypes.byref(x), ctypes.byref(y))
        self.camera.process_mouse_movement(x.value, y.value)

        rich.print(
            f"Camera Position: {self.camera.position}\n",
            end="\r",
        )


if __name__ == "__main__":
    app = DiceApp()
    app.run()
