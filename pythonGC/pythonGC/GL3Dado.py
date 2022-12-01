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
        # generate a cube
        self.vertices = array(
            "f",
            [
                -0.5, -0.5,  -0.5, #F A
                0.5, -0.5,   -0.5, #F B
                0.5,  0.5,   -0.5, #F C
                -0.5, 0.5,   -0.5, #F D
                -0.5, -0.5,   0.5, #F E
                0.5,  -0.5,   0.5, #F F
                0.5,   0.5,   0.5, #F G
                -0.5,  0.5,   0.5, #F H
            ],
        )
        self.indices = array(
            "I",
            [
                0,
                1,
                2,
                0,
                2,
                3,
                4,
                6,
                5,
                4,
                7,
                6,
                4,
                5,
                1,
                4,
                1,
                0,
                3,
                2,
                6,
                3,
                6,
                7,
                1,
                5,
                6,
                1,
                6,
                2,
                4,
                0,
                3,
                4,
                3,
                7,
            ],
        )
        self.normals = array(
            "f",
            [
                0.0,
                0.0,
                -1.0,
                0.0,
                0.0,
                1.0,
                0.0,
                1.0,
                0.0,
                0.0,
                -1.0,
                0.0,
                -1.0,
                0.0,
                0.0,
                1.0,
                0.0,
                0.0,
            ],
        )
        """
        Dice texture is a 3 x 2 grid of 6 faces
        1/2, 1/3
        1/2, 2/3
        1/2, 1/3
        """
        self.texcoords = array(
            "f",
            [
                # 1
                0.0 , 1.0,
                0.0 , 1/2,
                1/3, 1/2,
                1/3, 1.0,
                1/3, 1/2,
                2/3, 1/2,
                # 2
                1/3, 1.0,
                1/3, 1/2,
                2/3, 1/2,
                1/3, 1.0,
                2/3, 1/2,
                2/3, 1.0,
                ## 3
                #2/3, 1.0,
                #2/3, 1/2,
                #1.0 , 1/2,
                #2/3, 1.0,
                #1.0 , 1/2,
                #1.0 , 1.0,
                ## 4
                #0.0 , 1/2,
                #0.0 , 0.0,
                #1/3, 0.0,
                #0.0 , 1/2,
                #1/3, 0.0,
                #1/3, 1/2,
                ## 5
                #1/3, 1/2,
                #1/3, 0.0,
                #2/3, 0.0,
                #1/3, 1/2,
                #2/3, 0.0,
                #2/3, 1/2,
                ## 6
                #2/3, 1/2,
                #2/3, 0.0,
                #1.0 , 0.0,
                #2/3, 1/2,
                #1.0 , 0.0,
                #1.0 , 1/2,
            ],
        )

    def load(self):
        """
        in vec3 attr_position;
        in vec2 attr_textureCoord;

        """
        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)

        self.vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER,
            self.vertices.itemsize * len(self.vertices),
            ctypes.c_void_p(self.vertices.buffer_info()[0]),
            GL.GL_STATIC_DRAW,
        )
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
        GL.glEnableVertexAttribArray(0)

        self.tbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.tbo)
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER,
            self.texcoords.itemsize * len(self.texcoords),
            ctypes.c_void_p(self.texcoords.buffer_info()[0]),
            GL.GL_STATIC_DRAW,
        )
        GL.glVertexAttribPointer(1, 2, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
        GL.glEnableVertexAttribArray(1)

        self.nbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.nbo)
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER,
            self.normals.itemsize * len(self.normals),
            ctypes.c_void_p(self.normals.buffer_info()[0]),
            GL.GL_STATIC_DRAW,
        )
        GL.glVertexAttribPointer(2, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
        GL.glEnableVertexAttribArray(2)

        self.ebo = GL.glGenBuffers(1)
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
        GL.glDrawElements(
            GL.GL_TRIANGLES, len(self.indices), GL.GL_UNSIGNED_INT, ctypes.c_void_p(0)
        )
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
        self.camera.position = glm.vec3(0.0, 0.0, 0.0)

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
            for i in range(10):
                for j in range(10):
                    for k in range(10):
                        self.dice.position = glm.vec3(i * 2 - 5, j * 2 - 5, k * 2 - 5)
                        self.dice.rotation = glm.vec3(
                            glm.radians(i / 10 * 360) * 45,
                            glm.radians(j / 10 * 360) * 45,
                            glm.radians(k / 10 * 360) * 45,
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
            f"Frame rate: {1/(self.frameTime/10000):.2f} FPS \t Frame time: {self.frameTime/self.frameCount:.2f} ms \t Camera Position: {self.camera.position}",
            end="\r",
        )


if __name__ == "__main__":
    app = DiceApp()
    app.run()
