import ctypes
import logging
import sys
import rich
import os
import sys
import glm
import sdl2
from abc import ABC, abstractmethod
from OpenGL import GL
from array import array

from shader import ShaderProgram


class OpenGLApp(ABC):
    """
    Basic Runnable OpenGL class to be implemented in other classes,
    and should be use using openGL 3 calls.
    """

    def __init__(
        self,
        width=640,
        height=480,
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
            super().__init__(800, 600, "My Application")

        def setup(self):
            # OpenGL Initialization
            GL.glClearColor(0.2, 0.2, 0.2, 0.0)
            GL.glEnable(GL.GL_DEPTH_TEST)
            GL.glEnable(GL.GL_MULTISAMPLE)

            # Pipeline (shaders)
            self.shader = ShaderProgram("SimplePipeline")
            self.shader.compile_shader()
            self.shader.link()

            # list uniforms
            rich.print(f"Available Uniforms: {self.shader.uniforms}")

            position = array("f", [-0.5, -0.5, 0.0, 0.5, -0.5, 0.0, 0.0, 0.5, 0.0])

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
            # print frame rate and frame time overriding the last console line
            rich.print(
                f"Frame rate: {self.frameCount/self.frameTime:.2f} FPS \t Frame time: {self.frameTime/self.frameCount:.2f} ms",
                end="\r",
            )

        def render(self):
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            with self.shader as shader:
                mat = glm.mat4()
                shader.set_uniform(b"MVP", mat)
                GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

                mat = (
                    glm.mat4()
                    * glm.translate(glm.vec3(0.5, 0.5, 0.0))
                    * glm.scale(glm.vec3(0.5))
                    * glm.rotate(glm.pi(), glm.vec3(0.0, 0.0, 1.0))
                )
                shader.set_uniform(b"MVP", mat)
                GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

                mat = (
                    glm.mat4()
                    * glm.translate(glm.vec3(-0.5, 0.5, 0.0))
                    * glm.scale(glm.vec3(0.3))
                    * glm.rotate(glm.pi(), glm.vec3(0.0, 0.0, 1.0))
                )
                shader.set_uniform(b"MVP", mat)
                GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

    # Run the application
    app = MyApplication()
    app.run()
