#version 130

in vec3 position;
uniform mat4 model_matrix;
uniform mat4 view_matrix;
uniform mat4 proj_matrix;

void main(void) 
{
    gl_Position = vec4(position,1.0) * model_matrix * view_matrix * proj_matrix;
}
