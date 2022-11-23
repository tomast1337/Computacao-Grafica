import glm
from OpenGL import GL
from PIL import Image

def loadTexture( file_path:str):
    im:Image = Image.open(file_path)
    w, h = im.size
    if im.mode == "RGBA":
        modo = GL.GL_RGBA
        data = im.tobytes("raw", "RGBA", 0, -1)
    else:
        modo = GL.GL_RGB
        data = im.tobytes("raw", "RGB", 0, -1)
    textureId = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, textureId)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, modo, w, h, 0, modo, GL.GL_UNSIGNED_BYTE, data)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    return textureId


class Texture:
    def __init__(self, file_path:str):
        self.texturePath = file_path
        self.id = None

    def load(self):
        self.id = loadTexture(self.texturePath)
        print("Texture loaded: ", self.id)

    def bind(self, slot:int):
        if self.id is None:
            raise Exception("Texture not loaded")
        GL.glActiveTexture(GL.GL_TEXTURE0 + slot)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.id)

    def unbind(self, slot:int):
        if self.id is None:
            raise Exception("Texture not loaded")
        GL.glActiveTexture(GL.GL_TEXTURE0 + slot)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
    
    def get_unit(self, slot:int):
        return GL.GL_TEXTURE0 + slot

