from __future__ import annotations
import ctypes
import os
import glm
from OpenGL import GL
from array import array
from shader import ShaderProgram

models_extensions = {
    "ply": ".ply",
    "obj": ".obj",
}


class Model:
    """
    Model class:
    This class warps OpenGL model loading and rendering
    """

    def __init__(
        self,
        vertices,
        faces,
        colors=None,
        uvs=None,
        position: glm.vec3 = glm.vec3(0.0, 0.0, 0.0),
        rotation: glm.vec3 = glm.vec3(0.0, 0.0, 0.0),
        scale: glm.vec3 = glm.vec3(1.0, 1.0, 1.0),
    ):
        if faces is None or vertices is None:
            raise Exception("Faces and vertices cannot be None")
        self.vertices = array("f", vertices)
        self.faces = array("I", faces) 
        self.colors = array("f", colors) if colors else None # array of floats
        self.uvs = array("f", uvs) if uvs else None # array of floats

        self.position = position
        self.rotation = rotation
        self.scale = scale

        # create the vertex array
        self.vao = GL.glGenVertexArrays(1)
        # bind the vertex array
        GL.glBindVertexArray(self.vao)
        # create the vertex buffer
        self.vbo = GL.glGenBuffers(1)
        # bind the vertex buffer
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        # create the vertex buffer data
        self.vbo_data = array("f", [])
        for i in range(len(self.vertices)):
            self.vbo_data.append(self.vertices[i])
            if self.colors:
                self.vbo_data.append(self.colors[i])
        # upload the vertex buffer data
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER,
            len(self.vbo_data) * self.vbo_data.itemsize,
            ctypes.c_void_p(self.vbo_data.buffer_info()[0]),
            GL.GL_STATIC_DRAW,
        )
        # create the element buffer
        self.ebo = GL.glGenBuffers(1)
        # bind the element buffer
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        # upload the element buffer data
        GL.glBufferData(
            GL.GL_ELEMENT_ARRAY_BUFFER,
            len(self.faces) * self.faces.itemsize,
            ctypes.c_void_p(self.faces.buffer_info()[0]),
            GL.GL_STATIC_DRAW,
        )
        # set the vertex attribute pointer
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
        # enable the vertex attribute pointer
        GL.glEnableVertexAttribArray(0)
        # unbind the vertex array
        GL.glBindVertexArray(0)

    def open_from_file(self, file_path: str) -> Model:
        """
        Static method to open a model from a file
        """
        # verify if the file extension is supported
        if not file_path.endswith(models_extensions.values()):
            raise Exception(f"File extension not supported: {file_path}")
        # verify if the file exists
        if not os.path.isfile(file_path):
            raise Exception(f"File not found: {file_path}")
        file_extension = file_path.split(".")[-1]
        if file_extension == models_extensions["ply"]:
            Model = Model.open_ply(file_path)
        elif file_extension == models_extensions["obj"]:
            Model = Model.open_obj(file_path)
        else:
            raise Exception(f"File extension not supported: {file_path}")

    def open_ply(file_path: str):
        """
        Static method to open a ply model from a file
        """
        # verify if the file exists
        if not os.path.isfile(file_path):
            raise Exception(f"File not found: {file_path}")
        # open the file
        with open(file_path, "r") as f:
            # read the file
            file_content = f.read()
            # split the file content into lines
            file_content = file_content.split("\n")
            # remove all empty lines
            file_content = [x for x in file_content if x]
            # remove all comments
            file_content = [x for x in file_content if not x.startswith("comment")]
            # remove all empty lines
            file_content = [x for x in file_content if x]
            # get the header
            header = file_content[0:3]
            # get the number of vertices
            n_vertices = int(header[0].split(" ")[2])
            # get the number of faces
            n_faces = int(header[1].split(" ")[2])
            # get the number of colors
            n_colors = int(header[2].split(" ")[2])
            # get the vertices
            vertices = file_content[3 : 3 + n_vertices]
            # get the faces
            faces = file_content[3 + n_vertices : 3 + n_vertices + n_faces]
            # get the colors
            colors = file_content[
                3 + n_vertices + n_faces : 3 + n_vertices + n_faces + n_colors
            ]
            # convert the vertices to a list of floats
            vertices = [float(x) for x in vertices[0].split(" ")]
            # convert the faces to a list of ints
            faces = [int(x) for x in faces[0].split(" ")]
            # convert the colors to a list of floats
            colors = [float(x) for x in colors[0].split(" ")]
            # convert the vertices to a numpy array
            vertices = array("f", vertices)
            # convert the faces to a numpy array
            faces = array("I", faces)
            # convert the colors to a numpy array
            colors = array("f", colors)
            # create the model
            return Model(vertices, faces, colors)

    def open_obj(file_path: str):
        """
        Static method to open a obj model from a file
        """
        # verify if the file exists
        if not os.path.isfile(file_path):
            raise Exception(f"File not found: {file_path}")
        # open the file
        with open(file_path, "r") as f:
            # read the file
            file_content = f.read()
            # split the file content into lines
            file_content = file_content.split("\n")
            # remove all empty lines
            file_content = [x for x in file_content if x]
            # remove all comments
            file_content = [x for x in file_content if not x.startswith("#")]
            # remove all empty lines
            file_content = [x for x in file_content if x]
            # get the vertices
            vertices = [x for x in file_content if x.startswith("v ")]
            # get the faces
            faces = [x for x in file_content if x.startswith("f ")]
            # get the colors
            colors = [x for x in file_content if x.startswith("c ")]
            # convert the vertices to a list of floats
            vertices = [float(x) for x in vertices[0].split(" ")[1:]]
            # convert the faces to a list of ints
            faces = [int(x) for x in faces[0].split(" ")[1:]]
            # convert the colors to a list of floats
            colors = [float(x) for x in colors[0].split(" ")[1:]]
            # convert the vertices to a numpy array
            vertices = array("f", vertices)
            # convert the faces to a numpy array
            faces = array("I", faces)
            # convert the colors to a numpy array
            colors = array("f", colors)
            # create the model
            return Model(vertices, faces, colors)

    def get_model_matrix(self) -> glm.mat4:
        """
        Method to get the model matrix
        """
        # get the model matrix
        model = glm.mat4()
        # translate the model
        glm.translate(model, self.position)
        # rotate the model
        glm.rotate(model, (self.rotation.x), glm.vec3(1.0, 0.0, 0.0))
        glm.rotate(model, (self.rotation.y), glm.vec3(0.0, 1.0, 0.0))
        glm.rotate(model, (self.rotation.z), glm.vec3(0.0, 0.0, 1.0))
        # scale the model
        glm.scale(model, self.scale)
        # return the model matrix
        return model

    def set_position(self, position: glm.vec3):
        """
        Set the model location
        """
        self.position = position

    def set_rotation(self, rotation: glm.vec3):
        """
        Set the model rotation
        """
        self.rotation = rotation

    def set_scale(self, scale: glm.vec3):
        """
        Set the model scale
        """
        self.scale = scale
