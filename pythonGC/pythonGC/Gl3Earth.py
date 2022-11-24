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
        self.vertices = []
        self.indices = []
        self.normals = []
        self.texcoords = []
        self.generate()
        super().__init__(self.vertices, self.indices, self.normals, self.texcoords)

    def generate(self):
        for i in range(self.stacks + 1):
            V = i / self.stacks
            phi = V * math.pi
            for j in range(self.slices + 1):
                U = j / self.slices
                theta = U * (math.pi * 2)
                x = math.cos(theta) * math.sin(phi)
                y = math.cos(phi)
                z = math.sin(theta) * math.sin(phi)
                self.vertices.append(x * self.radius)
                self.vertices.append(y * self.radius)
                self.vertices.append(z * self.radius)
                self.normals.append(x)
                self.normals.append(y)
                self.normals.append(z)
                self.texcoords.append(U)
                self.texcoords.append(V)
        for i in range(self.stacks):
            k1 = i * (self.slices + 1)
            k2 = k1 + self.slices + 1
            for j in range(self.slices):
                if i != 0:
                    self.indices.append(k1)
                    self.indices.append(k2)
                    self.indices.append(k1 + 1)
                if i != (self.stacks - 1):
                    self.indices.append(k1 + 1)
                    self.indices.append(k2)
                    self.indices.append(k2 + 1)
                k1 += 1
                k2 += 1

    def render(self):
        GL.glDrawElements(GL.GL_TRIANGLES, len(self.indices), GL.GL_UNSIGNED_INT, None)s
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

        # Pipeline (shaders)
        self.shader = ShaderProgram("SimpleTexture")
        self.shader.compile_shader()
        self.shader.link()

        # list uniforms
        rich.print(f"Available Uniforms: {self.shader.uniforms}")

        # Texture
        GL.glActiveTexture(GL.GL_TEXTURE0)
        self.texture = Texture("./textures/uv_grid_opengl.png")
        self.texture.load()

        # Model
        self.model = sphereModel(0.5, 20, 20)

    def render(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        with self.shader as s:
            s.set_uniform(b"model_matrix", glm.mat4(1.0))
            s.set_uniform(b"view_matrix", self.camera.get_view_matrix())
            s.set_uniform(b"proj_matrix", self.camera.projection)
            s.set_uniform(b"textureSlot", 0)
            self.model.render()

    def update(self):
        cameraSpeed = .1
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
    app = Earth()
    app.run()
