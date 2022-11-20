import glm
import sdl2


class Camera:
    def __init__(
        self,
        position=glm.vec3(0.0, 0.0, 0.0),
        up=glm.vec3(0.0, 1.0, 0.0),
        yaw=-90.0,
        pitch=0.0,
        fov=45.0,
        width=800,
        height=600,
        near=0.1,
        far=100.0,
    ):
        self.position = position
        self.world_up = up
        self.yaw = yaw
        self.pitch = pitch
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.update_camera_vectors()
        self.projection = glm.perspective(glm.radians(fov), width / height, near, far)

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)

    def process_keyboard(self, keys, velocity):
        if keys[sdl2.SDL_SCANCODE_W]:
            self.position += self.front * velocity
        if keys[sdl2.SDL_SCANCODE_S]:
            self.position -= self.front * velocity
        if keys[sdl2.SDL_SCANCODE_A]:
            self.position -= self.right * velocity
        if keys[sdl2.SDL_SCANCODE_D]:
            self.position += self.right * velocity

    def process_mouse_movement(self, x_offset, y_offset, constrain_pitch=True):
        x_offset *= 0.1
        y_offset *= 0.1

        #invert y_offset
        y_offset *= -1

        self.yaw += x_offset
        self.pitch += y_offset

        if constrain_pitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0

        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = glm.vec3()
        front.x = glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        front.y = glm.sin(glm.radians(self.pitch))
        front.z = glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        self.front = glm.normalize(front)
        self.right = glm.normalize(glm.cross(self.front, self.world_up))
        self.up = glm.normalize(glm.cross(self.right, self.front))

    def get_projection_matrix(self, width, height):
        return glm.perspective(glm.radians(45.0), width / height, 0.1, 100.0)

    def update_projection_matrix(
        self, width=800, height=600, near=0.1, far=100.0, fov=45.0
    ):
        self.projection = glm.perspective(glm.radians(fov), width / height, near, far)
