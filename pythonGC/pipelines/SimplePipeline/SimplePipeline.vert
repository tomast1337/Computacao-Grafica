#version 130

in vec3 position;
in vec3 color;
uniform mat4 model_matrix;
uniform mat4 view_matrix;
uniform mat4 proj_matrix;
out vec3 colorToFragmentShader;

void main(void) 
{
    gl_Position = proj_matrix * view_matrix * model_matrix * vec4(position, 1.0);
    colorToFragmentShader = color;
}
