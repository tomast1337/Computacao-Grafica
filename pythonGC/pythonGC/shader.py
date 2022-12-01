import ctypes
import logging
import rich
import os
import sys
from abc import ABC, abstractmethod
from OpenGL import GL
import glm

from texture import Texture

shaderExtensions = {
    "vert": GL.GL_VERTEX_SHADER,
    "tesc": GL.GL_TESS_CONTROL_SHADER,
    "tese": GL.GL_TESS_EVALUATION_SHADER,
    "geom": GL.GL_GEOMETRY_SHADER,
    "frag": GL.GL_FRAGMENT_SHADER,
    "comp": GL.GL_COMPUTE_SHADER,
}

pipelines_folder_name = "pipelines"

def list_pipeline_shaders():
    """
    List all available pipeline in the pipeline folder
    """
    try:
        # get root path
        root_path = os.getcwd()
        pipelinePath = os.path.join(root_path, pipelines_folder_name)
        # list subfolders in the pipeline folder
        pipelineList = os.listdir(pipelinePath)
        # Remove all non folder from the list
        pipelineList = [
            x for x in pipelineList if os.path.isdir(os.path.join(pipelinePath, x))
        ]
        return pipelineList
    except Exception as e:
        logging.error(f"""
        Error while listing pipeline shaders:
        {e}
        Make sure you have a {pipelines_folder_name} folder in the root path of the project
        """)
        sys.exit(1)

def get_pipeline_path(pipeline_name:str)->str:
    # get the path of the current file
    root_path = os.getcwd()
    # get the path of the pipeline folder
    pipelinePath = os.path.join(root_path, "pipelines")
    return pipelinePath

class ShaderProgram:
    """
    Shader Program class:
    This class warps the OpenGL shader program creation ,linking and usage
    """

    def __init__(
        self,
        pipeline_name: str,
    ):
        if not pipeline_name in list_pipeline_shaders():
            raise Exception(
                f"Pipeline {pipeline_name} not found"
                "\nThe available pipelines are: {list_pipeline_shaders()}"
            )
        self.pipeline_name = pipeline_name
        self.program = None
        self.shaders = []
        self.uniforms = {}
        self.attributes = {}
        self.linked = False

    def compile_shader(self):
        """
        compile_shader()
        Compile the pipeline shader from the pipeline folder
        """
        # get the path of the pipeline folder
        pipelinePath = os.path.join(get_pipeline_path(self.pipeline_name), self.pipeline_name)
        # list all files in the pipeline folder
        pipelineFiles = os.listdir(pipelinePath)
        # Remove all non shader files from the list
        pipelineFiles = [
            x for x in pipelineFiles if x.split(".")[-1] in shaderExtensions
        ]

        # create a shader program
        self.program = GL.glCreateProgram()
        # create a list of shaders
        self.shaders = []
        # compile all shaders in the pipeline folder
        for shaderFile in pipelineFiles:
            # get the shader type from the file extension
            shaderType = shaderExtensions[shaderFile.split(".")[-1]]
            # create a shader
            shader = GL.glCreateShader(shaderType)
            # read the shader source code from the file
            with open(os.path.join(pipelinePath, shaderFile), "r") as f:
                shaderSource = f.read()
            # compile the shader
            GL.glShaderSource(shader, shaderSource)
            GL.glCompileShader(shader)
            # check if the shader compiled successfully
            if not GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS):
                raise Exception(
                    f"Error compiling shader {shaderFile}: {GL.glGetShaderInfoLog(shader).decode('utf-8')}"
                )

            # attach the shader to the program
            GL.glAttachShader(self.program, shader)
            # add the shader to the list of shaders
            self.shaders.append(shader)

    def link(self):
        """
        link()
        Link the shader program
        """
        # link the program
        GL.glLinkProgram(self.program)
        # check if the program linked successfully
        if not GL.glGetProgramiv(self.program, GL.GL_LINK_STATUS):
            raise Exception(
                f"Error linking shader program: {GL.glGetProgramInfoLog(self.program).decode('utf-8')}"
            )
        # get the number of active uniforms
        numUniforms = GL.glGetProgramiv(self.program, GL.GL_ACTIVE_UNIFORMS)
        # get the number of active attributes
        numAttributes = GL.glGetProgramiv(self.program, GL.GL_ACTIVE_ATTRIBUTES)
        # get the uniform names and locations
        for i in range(numUniforms):
            name, size, type = GL.glGetActiveUniform(self.program, i)
            location = GL.glGetUniformLocation(self.program, name)
            self.uniforms[name] = location
        # get the attribute names and locations
        for i in range(numAttributes):
            name, size, type = GL.glGetActiveAttrib(self.program, i)
            location = GL.glGetAttribLocation(self.program, name)
            self.attributes[name] = location
        self.linked = True

    def use(self):
        """
        use(self):
        Use the shader program
        """
        if not self.linked:
            self.compile_shader()
            self.link()
        GL.glUseProgram(self.program)

    def set_uniform(self, name: str, value):
        """
        set_uniform(self, name: str, value):
        Set a uniform value
        """
        if not self.linked:
            self.compile_shader()
            self.link()
        if not name in self.uniforms:
            raise Exception(f"Uniform {name} not found")
        if isinstance(value, int):
            GL.glUniform1i(self.uniforms[name], value)
        elif isinstance(value, float):
            GL.glUniform1f(self.uniforms[name], value)
        elif isinstance(value, list):
            if len(value) == 2:
                GL.glUniform2f(self.uniforms[name], *value)
            elif len(value) == 3:
                GL.glUniform3f(self.uniforms[name], *value)
            elif len(value) == 4:
                GL.glUniform4f(self.uniforms[name], *value)
        elif isinstance(value, glm.mat4):
            GL.glUniformMatrix4fv(self.uniforms[name], 1, GL.GL_FALSE, glm.value_ptr(value))
        elif isinstance(value, Texture):
            GL.glUniform1i(self.uniforms[name], value.get_unit())
        else:
            raise Exception(f"Uniform {name} type not supported")

    def __del__(self):
        """
        __del__(self):
        Delete the shader program and shaders
        """
        if self.program:
            GL.glDeleteProgram(self.program)
        for shader in self.shaders:
            GL.glDeleteShader(shader)
            

    def __enter__(self):
        """
        __enter__(self):
        Use the shader program
        Used for the with statement
        """
        self.use()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        __exit__(self, exc_type, exc_value, traceback):
        Unuse the shader program
        Used for the with statement
        """
        GL.glUseProgram(0)

if __name__ == "__main__":
    print("Available pipelines: ", list_pipeline_shaders())
    # print the absolute path of the pipeline folders
    for pipeline in list_pipeline_shaders():
        print(pipeline, ":", get_pipeline_path(pipeline))