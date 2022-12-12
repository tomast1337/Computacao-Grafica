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
import math


class sphereModel(Model):
    def __init__(self, radius, slices, stacks):
        self.radius = radius
        self.slices = slices
        self.stacks = stacks
        self.attr_position = []
        self.indices = []
        self.normals = []
        self.tex_coords = []
        self.position = glm.vec3(0.0, 0.0, 0.0)
        self.rotation = glm.vec3(0.0, 0.0, 0.0)
        self.scale = glm.vec3(1.0, 1.0, 1.0)

    def load(self):
        latitude = 0
        longitude = 0
        vertices = []
        indices = []
        tex_coords = []
        normals = []

        for i in range(self.stacks + 1):
            latitude = math.pi * i / self.stacks
            sinLatitude = math.sin(latitude)
            cosLatitude = math.cos(latitude)

            for j in range(self.slices + 1):
                longitude = 2 * math.pi * j / self.slices
                sinLongitude = math.sin(longitude)
                cosLongitude = math.cos(longitude)

                x = cosLongitude * sinLatitude
                y = cosLatitude
                z = sinLongitude * sinLatitude

                vertices.append([x, y, z])
                normals.append([x, y, z])
                tex_coords.append([j / self.slices, i / self.stacks])

        for i in range(self.stacks):
            for j in range(self.slices):
                p1 = i * (self.slices + 1) + j
                p2 = p1 + (self.slices + 1)

                indices.append(p1)
                indices.append(p2)
                indices.append(p1 + 1)
                indices.append(p1 + 1)
                indices.append(p2)
                indices.append(p2 + 1)

        self.indices = array("I", indices)
        self.attr_position = array(
            "f", [item for sublist in vertices for item in sublist]
        )
        self.attr_textureCoord = array(
            "f", [item for sublist in tex_coords for item in sublist]
        )

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

        GL.glBindVertexArray(0)  # Unbind

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


class Earth(OpenGLApp):
    def __init__(self):
        super().__init__(800, 600, "Earth")
        self.camera = Camera()
        self.camera.position = glm.vec3(0.0, 0.0, 3.0)

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

        # texture filtering none
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)

        # Pipeline (shaders)
        self.shader = ShaderProgram("SimpleTexture")
        self.shader.compile_shader()
        self.shader.link()

        # list uniforms
        rich.print(f"Available Uniforms: {self.shader.uniforms}")

        # Texture
        GL.glActiveTexture(GL.GL_TEXTURE0)
        self.texture = Texture("./textures/world_map.png")
        self.texture.load()

        # Model
        self.model = sphereModel(0.5, 20, 20)
        self.model.load()
        self.model.rotation.x = 180

    def update(self):
        cameraSpeed = 0.1
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

    def render(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        with self.shader as s:
            self.model.rotation.y += 0.1
            s.set_uniform(b"model_matrix", self.model.model_matrix())
            s.set_uniform(b"view_matrix", self.camera.get_view_matrix())
            s.set_uniform(b"proj_matrix", self.camera.projection)
            self.model.render()
        GL.glBindVertexArray(0)


if __name__ == "__main__":
    app = Earth()
    app.run()
