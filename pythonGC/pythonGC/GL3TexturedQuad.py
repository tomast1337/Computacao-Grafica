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
            "./textures/uv_grid_opengl.png"
        )  # load texture from file into active texture
        self.texture.load()  # load texture into GPU

        quad_position = array(
            "f", [0.8, -0.8, 0.0, -0.8, -0.8, 0.0, 0.8, 0.8, 0.0, -0.8, 0.8, 0.0]
        )  # 4 vertices, 3 coordinates each

        quad_textureCoord = array(
            "f", [1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0]
        )  # 4 vertices, 2 coordinates each

        self.squareArrayBufferId = GL.glGenVertexArrays(
            1
        )  # create a vertex array object
        GL.glBindVertexArray(self.squareArrayBufferId)  # bind the vertex array object
        # Enable the attribute arrays, so this tells the shader where to get the data
        GL.glEnableVertexAttribArray(0)  # enable the first attribute (position
        GL.glEnableVertexAttribArray(
            1 # this number must match the layout in the shader
        )  # enable the second attribute (texture coordinates),
        """ // Example in shader
        layout (location = 0) in vec3 position; // GL.glEnableVertexAttribArray(0)
        """ 

        self.quadArrayBufferId = GL.glGenBuffers(1)  # create a vertex buffer object
        GL.glBindBuffer(
            GL.GL_ARRAY_BUFFER, self.quadArrayBufferId
        )  # bind the vertex buffer object
        GL.glBufferData(  # copy the vertex data to the GPU
            GL.GL_ARRAY_BUFFER,  # target
            quad_position.itemsize * len(quad_position),  # size of the data
            ctypes.c_void_p(quad_position.buffer_info()[0]),  # pointer to the data
            GL.GL_STATIC_DRAW,  # usage
        )
        GL.glVertexAttribPointer(
            0,  # attribute index (location in the shader)
            3,  # number of coordinates, 3 describes a 3D vector
            GL.GL_FLOAT,  # type
            GL.GL_FALSE,  # normalized
            0,  # stride (0 = tightly packed)
            ctypes.c_void_p(0),  # array buffer offset
        )  # set the attribute pointer for the position attribute

        self.quadTextureBufferId = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.quadTextureBufferId)
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER,  # target
            quad_textureCoord.itemsize * len(quad_textureCoord),  # size of the data
            ctypes.c_void_p(quad_textureCoord.buffer_info()[0]),  # pointer to the data
            GL.GL_STATIC_DRAW,  # usage
        )
        GL.glVertexAttribPointer(
            1,  # attribute index (location in the shader)
            2,  # number of coordinates, in this case 2 (u,v)
            GL.GL_FLOAT,  # type
            GL.GL_FALSE,  # normalized
            0,  # stride (0 = tightly packed)
            ctypes.c_void_p(0),  # array buffer offset
        )  # set the attribute pointer for the texture coordinates attribute

    def update(self):
        cameraSpeed = 0.5
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

            s.set_uniform(b"textureSlot", 0)

            n = 25
            for latitude in range(0, n):
                for longitude in range(0, n):
                    pi = 3.14159265359
                    radius = n / 2
                    angleX = (latitude / n) * 2 * pi
                    angleY = (longitude / n) * 2 * pi
                    y = radius * glm.sin(angleX) * glm.cos(angleY)
                    z = radius * glm.sin(angleX) * glm.sin(angleY)
                    x = radius * glm.cos(angleX)

                    position = glm.vec3(x, y, z)
                    # rotate face camera
                    cameraX = self.camera.position.x
                    cameraY = self.camera.position.y
                    cameraZ = self.camera.position.z
                    rotation = glm.vec3(
                        0,
                        glm.atan2(cameraX - x, cameraZ - z),
                        0,
                    )
                    # the farther away bigger the quad
                    scale = glm.vec3(
                        (1 / (1 + glm.distance(position, self.camera.position)) * 2)
                    )
                    mat4 = glm.mat4(1.0)
                    mat4 = glm.translate(mat4, position)
                    mat4 = glm.rotate(mat4, rotation.x, glm.vec3(1, 0, 0))
                    mat4 = glm.rotate(mat4, rotation.y, glm.vec3(0, 1, 0))
                    mat4 = glm.rotate(mat4, rotation.z, glm.vec3(0, 0, 1))
                    mat4 = glm.scale(mat4, scale)
                    s.set_uniform(b"model_matrix", mat4)
                    GL.glBindVertexArray(self.squareArrayBufferId)
                    GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, 0, 4)


if __name__ == "__main__":
    app = TexturedQuad()
    app.run()
