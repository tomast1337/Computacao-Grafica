#version 400

layout (location=0) in vec3 attr_position;
layout (location=1) in float attr_intensity;
uniform mat4 MVP;
out float intensity;

void main(void) 
{
    gl_Position = MVP * vec4(attr_position,1.0);
    intensity = attr_intensity;
}
