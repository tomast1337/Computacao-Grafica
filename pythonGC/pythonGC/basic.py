from abc import ABC, abstractmethod
import sdl2
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import logging
import ctypes

"""
Basic Runnable OpenGL class to be implemented in other classes
"""
class BasicOpenGL(ABC):
    def __init__(self, width=640, height=480, title="Basic OpenGL",full_screen=False, fov=45, near=0.1, far=100.0):
        self.window_width = width
        self.window_height = height
        self.full_screen = full_screen
        self.window_title = title
        self.fov = fov
        self.near = near
        self.far = far
        self.running = False
        self.window = None
        self.context = None
        self.event = None

    def init(self):
        sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING) # Initialize SDL2
        
        if self.full_screen:
            sdl2.SDL_SetHint(sdl2.SDL_HINT_VIDEO_MINIMIZE_ON_FOCUS_LOSS, ctypes.c_char_p(b"0"))
            sdl2.SDL_SetWindowFullscreen(self.window, sdl2.SDL_WINDOW_FULLSCREEN)
            displayMode = ctypes.pointer(sdl2.SDL_DisplayMode())
            sdl2.SDL_GetCurrentDisplayMode(0, displayMode)
            self.window_width = displayMode.contents.w
            self.window_height = displayMode.contents.h
        logging.info(f"Display mode: {self.window_width}x{self.window_height}")
        
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 2) # Set OpenGL 2.1
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 1) # Set OpenGL 2.1
        sdl2.SDL_GL_SetAttribute( # Set OpenGL 2.1
            sdl2.SDL_GL_CONTEXT_PROFILE_MASK, sdl2.SDL_GL_CONTEXT_PROFILE_CORE)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER, 1) # Enable double buffering
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE, 24) # Set the depth buffer size
        sdl2.SDL_GL_SetSwapInterval(1) # Enable vsync
        self.window = sdl2.SDL_CreateWindow(self.window_title.encode( # Create the window
        ),
        sdl2.SDL_WINDOWPOS_CENTERED, # Center the window
        sdl2.SDL_WINDOWPOS_CENTERED, # Center the window
        self.window_width, # Set the window width
        self.window_height, # Set the window height
        sdl2.SDL_WINDOW_OPENGL) # Enable OpenGL
        if self.window is None: # Check if the window was created
            logging.error(f"Could not create window: {sdl2.SDL_GetError()}")
            sys.exit(-1)
        # Create the OpenGL context
        self.context = sdl2.SDL_GL_CreateContext(self.window)
        glEnable(GL_MULTISAMPLE)  # Enable multisampling
        glEnable(GL_DEPTH_TEST)  # Enable depth testing
        glClearColor(0., 0., 0., 1.)  # Set the clear color
        gluPerspective(self.fov,
                       self.window_width/self.window_height,  # Aspect ratio
                       self.near,  # Near clipping plane
                       self.far)  # Far clipping plane

        glTranslatef(0.0, 0.0, -20)  # Translate the scene

        # Show the window
        sdl2.SDL_ShowWindow(self.window)

        # set the window to fullscreen
        if self.full_screen:
            sdl2.SDL_SetWindowFullscreen(self.window, sdl2.SDL_WINDOW_FULLSCREEN)

    @abstractmethod
    def update(self):
        """
        Update the application state
        This method is called every frame
        and should be overwritten in the child class
        """
        raise NotImplementedError("This method should be overwritten in the child class")

    @abstractmethod
    def render(self):
        """
        Render the application
        This method is called every frame
        and should be overwritten in the child class
        """
        raise NotImplementedError("This method should be overwritten in the child class")

    def run(self):
        if self.running:
            logging.error("Application is already running")
            return
        self.running = True
        self.init()
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
            self.update() # Update the application state
            self.render() # Render the application
            sdl2.SDL_GL_SwapWindow(self.window) # Swap the window buffers
        self.quit()
        

    def quit(self):
        sdl2.SDL_GL_DeleteContext(self.context)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()
        logging.info("Application closed")


if __name__ == "__main__":
    class Test(BasicOpenGL):
        def __init__(self):
            """
            Esse exemplo desenha um triângulo que gira
            """
            super().__init__(
                width=800,
                height=600,
                title="Triangle test",
            )
            self.triangle = [
                [0.0, 1.0, 0.0],
                [-1.0, -1.0, 0.0],
                [1.0, -1.0, 0.0]
            ]

            self.colors = [
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0]
            ]
            self.angle = 0


        def update(self):
            # rotate the triangle
            self.angle += 1

        def render(self):
            # draw a triangle with red green and blue vertices
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            glPushMatrix()
            #glTranslatef(0.0, 0.0, -6)
            glRotatef(self.angle, self.angle, -self.angle, self.angle)
            glBegin(GL_TRIANGLES)
            for i in range(3):
                glColor3fv(self.colors[i])
                glVertex3fv(self.triangle[i])
            glEnd()
            glPopMatrix()
            
    t = Test()
    t.run()