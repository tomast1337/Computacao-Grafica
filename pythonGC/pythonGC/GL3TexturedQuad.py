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

        quad_vertices = array(
            "f",
            [
                -0.5,
                -0.5,
                0.0,
                0.5,
                -0.5,
                0.0,
                0.5,
                0.5,
                0.0,
                -0.5,
                0.5,
                0.0,
            ],
        )

        quad_indices = array("I", [0, 1, 2, 3])

        quad_uvs = array("f", [0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0])

        self.quadArrayBufferId = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.quadArrayBufferId)
        
        # Vertex Buffer
        self.quadVertexBufferId = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.quadVertexBufferId)
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER,
            quad_vertices.itemsize * len(quad_vertices),
            ctypes.c_void_p(quad_vertices.buffer_info()[0]),
            GL.GL_STATIC_DRAW,
        )

        # UV Buffer
        self.quadUVBufferId = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.quadUVBufferId)
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER,
            quad_uvs.itemsize * len(quad_uvs),
            ctypes.c_void_p(quad_uvs.buffer_info()[0]),
            GL.GL_STATIC_DRAW,
        )

        # Index Buffer
        self.quadIndexBufferId = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.quadIndexBufferId)
        GL.glBufferData(
            GL.GL_ELEMENT_ARRAY_BUFFER,
            quad_indices.itemsize * len(quad_indices),
            ctypes.c_void_p(quad_indices.buffer_info()[0]),
            GL.GL_STATIC_DRAW,
        )

        # Unbind
        GL.glBindVertexArray(0)

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

    def render(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        with self.shader as s:
            s.set_uniform(b"view_matrix", self.camera.get_view_matrix())
            s.set_uniform(b"proj_matrix", self.camera.projection)
            s.set_uniform(b"model_matrix", glm.mat4(1.0))
            s.set_uniform(b"textureSlot", 1)

            GL.glBindVertexArray(self.quadArrayBufferId)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.quadVertexBufferId)
            GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.quadUVBufferId)
            GL.glVertexAttribPointer(1, 2, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
            GL.glEnableVertexAttribArray(0)





if __name__ == "__main__":
    app = TexturedQuad()
    app.run()
