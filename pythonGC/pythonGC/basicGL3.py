import ctypes
import logging
import random
import sys
import rich
import os
import sys
import glm
import sdl2
from abc import ABC, abstractmethod
from OpenGL import GL
from array import array
from camera import Camera

from shader import ShaderProgram


class OpenGLApp(ABC):
    """
    Basic Runnable OpenGL class to be implemented in other classes,
    and should be use using openGL 3 calls.
    """

    def __init__(
        self,
        width=800,
        height=600,
        title="OpenGL APP",
        full_screen=False,
    ):
        self.window_width = width
        self.window_height = height
        self.full_screen = full_screen
        self.window_title = title
        self.running = False
        self.window = None
        self.context = None
        self.event = None
        self.frameCount = 1
        self.frameTime = 1

    def init(self):
        sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)  # Initialize SDL2

        if self.full_screen:
            sdl2.SDL_SetHint(
                sdl2.SDL_HINT_VIDEO_MINIMIZE_ON_FOCUS_LOSS, ctypes.c_char_p(b"0")
            )
            sdl2.SDL_SetWindowFullscreen(self.window, sdl2.SDL_WINDOW_FULLSCREEN)
            displayMode = ctypes.pointer(sdl2.SDL_DisplayMode())
            sdl2.SDL_GetCurrentDisplayMode(0, displayMode)
            self.window_width = displayMode.contents.w
            self.window_height = displayMode.contents.h
        logging.info(f"Display mode: {self.window_width}x{self.window_height}")

        self.window = sdl2.SDL_CreateWindow(
            self.window_title.encode("utf-8"),
            sdl2.SDL_WINDOWPOS_CENTERED,
            sdl2.SDL_WINDOWPOS_CENTERED,
            self.window_width,
            self.window_height,
            sdl2.SDL_WINDOW_OPENGL,
        )

        sdl2.SDL_SetWindowResizable(self.window, sdl2.SDL_FALSE)

        if not self.window:
            rich.print(f"Could not create window: {sdl2.SDL_GetError()}")
            sys.exit(-1)
        self.context = sdl2.SDL_GL_CreateContext(self.window)
        # set the window to fullscreen
        if self.full_screen:
            sdl2.SDL_SetWindowFullscreen(self.window, sdl2.SDL_WINDOW_FULLSCREEN)

    def set_window_title(self, newTitle):
        sdl2.SDL_SetWindowTitle(self.window, newTitle.encode("utf-8"))

    @abstractmethod
    def update(self):
        """
        Update the application state
        This method is called every frame
        and should be overwritten in the child class
        """
        raise NotImplementedError(
            "update() method should be overwritten in the child class"
        )

    @abstractmethod
    def render(self):
        """
        Render the application
        This method is called every frame
        and should be overwritten in the child class
        """
        raise NotImplementedError(
            "render() method should be overwritten in the child class"
        )

    @abstractmethod
    def setup(self):
        """
        Setup the application
        This method is called once at the beginning
        and should be overwritten in the child class
        """
        raise NotImplementedError(
            "setup() method should be overwritten in the child class"
        )

    def run(self):
        if self.running:
            logging.error("Application is already running")
            return
        self.running = True
        self.init()
        self.setup()
        self.main_loop()
        self.quit()

    def main_loop(self):
        while self.running:
            self.event = sdl2.SDL_Event()
            while sdl2.SDL_PollEvent(self.event):
                if self.event.type == sdl2.SDL_QUIT:
                    self.running = False
                elif self.event.type == sdl2.SDL_KEYDOWN:
                    if self.event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                        self.running = False
            # update frame time
            self.frameTime = sdl2.SDL_GetTicks()
            self.update()  # Update the application state
            self.render()  # Render the application
            sdl2.SDL_GL_SwapWindow(self.window)  # Swap the window buffers
            self.frameCount += 1
        self.quit()

    def quit(self):
        sdl2.SDL_GL_DeleteContext(self.context)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()
        logging.info("Application closed")


if __name__ == "__main__":

    class MyApplication(OpenGLApp):
        def __init__(self):
            super().__init__(800, 600, "The Triangle Zone")
            self.camera = Camera()
            self.camera.position = glm.vec3(0.0, 0.0, 3.0)
            self.piramide_data = []
            PI = 3.1415
            for i in range(0, 256):
                self.piramide_data.append(
                    {
                        "position": glm.vec3(
                            random.uniform(-1.0, 1.0) * 100, # x
                            random.uniform(-1.0, 1.0) * 10, # y
                            random.uniform(-1.0, 1.0) * 100, # z
                        ),
                        "size": int(random.uniform(0, 2.0) * 5 + 3),
                        "iterations": int(random.uniform(0.0, 1.0) * 5),
                        "rotation": glm.vec3(
                            random.uniform(-1.0, 1.0) * PI * 10,
                            random.uniform(-1.0, 1.0) * PI * 10,
                            random.uniform(-1.0, 1.0) * PI * 10,
                        ),
                    }
                )

        def setup(self):

            # Lock the mouse
            sdl2.SDL_SetRelativeMouseMode(sdl2.SDL_TRUE)

            # OpenGL Initialization
            GL.glClearColor(0.2, 0.2, 0.2, 1)
            GL.glEnable(GL.GL_DEPTH_TEST)
            GL.glEnable(GL.GL_MULTISAMPLE)

            # Pipeline (shaders)
            self.shader = ShaderProgram("SimplePipeline")
            self.shader.compile_shader()
            self.shader.link()

            # list uniforms
            rich.print(f"Available Uniforms: {self.shader.uniforms}")

            position = array("f", [-0.1, -0.1, 0.0, 0.1, -0.1, 0.0, 0.0, 0.1, 0.0])

            color = array("f", [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0])

            self.triangleArrayBufferId = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(self.triangleArrayBufferId)
            GL.glEnableVertexAttribArray(0)
            GL.glEnableVertexAttribArray(1)

            idVertexBuff = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idVertexBuff)
            GL.glBufferData(
                GL.GL_ARRAY_BUFFER,
                len(position) * position.itemsize,
                ctypes.c_void_p(position.buffer_info()[0]),
                GL.GL_STATIC_DRAW,
            )
            GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)

            idColorBuff = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idColorBuff)
            GL.glBufferData(
                GL.GL_ARRAY_BUFFER,
                len(color) * color.itemsize,
                ctypes.c_void_p(color.buffer_info()[0]),
                GL.GL_STATIC_DRAW,
            )
            GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)

        def update(self):
            cameraSpeed = 1
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
                # draw a serpinski triangle
                def draw_triangle(position, size, iterations, rotation):
                    if iterations == 0:
                        return
                    mat = glm.mat4(1.0)
                    mat = glm.translate(mat, position)
                    mat = glm.scale(mat, glm.vec3(size))
                    mat = glm.rotate(mat, glm.radians(rotation.x), glm.vec3(1, 0, 0)) # x
                    mat = glm.rotate(mat, glm.radians(rotation.y), glm.vec3(0, 1, 0)) # y
                    mat = glm.rotate(mat, glm.radians(rotation.z), glm.vec3(0, 0, 1)) # z
                    shader.set_uniform(b"model_matrix", mat)
                    GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
                    draw_triangle(
                        position + glm.vec3(0, size, 0), size / 2, iterations - 1 , rotation
                    )
                    draw_triangle(
                        position + glm.vec3(-size, -size, 0), size / 2, iterations - 1 , rotation
                    )
                    draw_triangle(
                        position + glm.vec3(size, -size, 0), size / 2, iterations - 1 , rotation
                    )

                for data in self.piramide_data:
                    draw_triangle(
                        data["position"],
                        data["size"],
                        data["iterations"],
                        data["rotation"],
                    )

    # Run the application
    app = MyApplication()
    app.run()
