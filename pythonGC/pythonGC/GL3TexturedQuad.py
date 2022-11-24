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


class TexturedQuad(OpenGLApp):
    def __init__(self):
        super().__init__(800, 600, "The Triangle Zone")
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

        quad_position = array(
            "f", [0.8, -0.8, 0.0, -0.8, -0.8, 0.0, 0.8, 0.8, 0.0, -0.8, 0.8, 0.0]
        )

        quad_textureCoord = array("f", [1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0])
        
        self.squareArrayBufferId = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.squareArrayBufferId)
        GL.glEnableVertexAttribArray(0)
        GL.glEnableVertexAttribArray(1)

        self.quadArrayBufferId = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.quadArrayBufferId)
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER,
            quad_position.itemsize * len(quad_position),
            ctypes.c_void_p(quad_position.buffer_info()[0]),
            GL.GL_STATIC_DRAW,
        )
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, ctypes.c_void_p(0))

        self.quadTextureBufferId = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.quadTextureBufferId)
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER,
            quad_textureCoord.itemsize * len(quad_textureCoord),
            ctypes.c_void_p(quad_textureCoord.buffer_info()[0]),
            GL.GL_STATIC_DRAW,
        )
        GL.glVertexAttribPointer(1, 2, GL.GL_FLOAT, GL.GL_FALSE, 0, ctypes.c_void_p(0))



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
            s.set_uniform(b"view_matrix", self.camera.get_view_matrix())
            s.set_uniform(b"proj_matrix", self.camera.projection)
            s.set_uniform(b"model_matrix", glm.mat4(1.0))
            s.set_uniform(b"textureSlot", 0)

            GL.glBindVertexArray(self.squareArrayBufferId)
            GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, 0, 4)


if __name__ == "__main__":
    app = TexturedQuad()
    app.run()
