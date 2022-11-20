import ctypes
import logging
import sys
import rich
import os
import sys
import glm
import sdl2
from OpenGL import GL
from array import array
from model_util import Model
from camera import Camera
from shader import ShaderProgram
from basicGL3 import OpenGLApp


class StanfordBunnyModel(Model):
    def __init__(self):
        root_path = os.getcwd()
        model_path = os.path.join(root_path, "objs", "bun_zipper.ply")
        scale = 20
        state = 0
        vertexCount = 0
        faceCount = 0
        vertices = array("f")
        indices = array("I")
        with open(model_path, "r") as f:
            for line in f:
                parts = line.split()
                if state == 0:
                    if len(parts) > 0 and parts[0] == "end_header":
                        state = 1
                    else:
                        if len(parts) == 3 and parts[0] == "element":
                            if parts[1] == "vertex":
                                vertexCount = int(parts[2])
                            elif parts[1] == "face":
                                faceCount = int(parts[2])
                elif state == 1:
                    vertices.append(float(parts[0]) * scale)
                    vertices.append(float(parts[1]) * scale)
                    vertices.append(float(parts[2]) * scale)
                    vertices.append(float(parts[4]))
                    vertexCount -= 1
                    if vertexCount == 0:
                        state = 2
                else:
                    faceVertexCount = int(parts[0])
                    for i in range(2, faceVertexCount):
                        indices.append(int(parts[1]))
                        indices.append(int(parts[i]))
                        indices.append(int(parts[i + 1]))
                    faceCount -= 1
                    if faceCount == 0:
                        break

        self.N = len(indices)
        self.arrayBufferId = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.arrayBufferId)
        GL.glEnableVertexAttribArray(0)  # POSITION
        GL.glEnableVertexAttribArray(1)  # INTENSITY

        idBuffer = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idBuffer)
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER,
            len(vertices) * vertices.itemsize,
            ctypes.c_void_p(vertices.buffer_info()[0]),
            GL.GL_STATIC_DRAW,
        )
        stride = 3 * ctypes.sizeof(ctypes.c_float) + ctypes.sizeof(ctypes.c_uint32)
        intensityPointer = ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float))
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, None)
        GL.glVertexAttribPointer(
            1, 1, GL.GL_UNSIGNED_INT, GL.GL_FALSE, stride, intensityPointer
        )

        idIndex = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, idIndex)
        GL.glBufferData(
            GL.GL_ELEMENT_ARRAY_BUFFER,
            len(indices) * indices.itemsize,
            ctypes.c_void_p(indices.buffer_info()[0]),
            GL.GL_STATIC_DRAW,
        )

    def draw(self, shader):
        GL.glBindVertexArray(self.arrayBufferId)
        GL.glDrawElements(GL.GL_TRIANGLES, self.N, GL.GL_UNSIGNED_INT, None)


class StanfordBunnyApp(OpenGLApp):
    def __init__(self):
        super().__init__(title="My Application", full_screen=True)
        self.camera = Camera()
        self.camera.position = glm.vec3(0, 0, 10)

    def setup(self):
        # OpenGL Initialization
        GL.glClearColor(0.2, 0.5, 0.2, 1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)

        self.shader = ShaderProgram("IntensityForBunny")
        self.shader.compile_shader()
        self.shader.link()

        # list uniforms
        rich.print(f"Available Uniforms: {self.shader.uniforms}")

        self.model = StanfordBunnyModel()
        self.model.position = glm.vec3(0, 0, 0)
        self.model.rotation = glm.vec3(0.0, 0.0, 0.0)
        self.model.scale = glm.vec3(1.0, 1.0, 1.0)

        # Lock the mouse
        sdl2.SDL_SetRelativeMouseMode(sdl2.SDL_TRUE)

        # set camera projection to the screen size specs
        self.camera.update_projection_matrix(
            self.window_width,
            self.window_height,
            near=0.1,
            far=1000.0,
            fov=45.0,
        )

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
            f"Frame rate: {self.frameCount/self.frameTime:.2f} FPS \t Frame time: {self.frameTime/self.frameCount:.2f} ms \t Camera Position: {self.camera.position}",
            end="\r",
        )

    def render(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        with self.shader as shader:
            shader.set_uniform(b"view_matrix", self.camera.get_view_matrix())
            shader.set_uniform(b"proj_matrix", self.camera.projection)

            shader.set_uniform(b"model_matrix", self.model.get_model_matrix())
            self.model.draw(shader)


if __name__ == "__main__":
    app = StanfordBunnyApp()
    app.run()
