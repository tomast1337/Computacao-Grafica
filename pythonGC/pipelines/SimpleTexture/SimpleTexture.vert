#version 400

layout (location=0) in vec3 attr_position;
layout (location=1) in vec2 attr_textureCoord;

out vec2 textureCoord;
uniform mat4 MVP;

void main(void) 
{
    gl_Position = MVP*vec4(attr_position,1.0);
    textureCoord = attr_textureCoord;
}
