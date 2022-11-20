#version 400

layout (location=0) in vec3 attr_position;
layout (location=1) in float attr_intensity;
uniform mat4 proj_matrix;
uniform mat4 view_matrix;
uniform mat4 model_matrix;
out float intensity;

void main(void) 
{
    gl_Position = proj_matrix * view_matrix * model_matrix * vec4(attr_position, 1.0);
    intensity = attr_intensity;
}
