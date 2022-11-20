#version 400

in vec2 textureCoord;
out vec4 color;
uniform sampler2D textureSlot;

void main(void) 
{
    color = texture(textureSlot,textureCoord);
    //color = vec4(1.0);
}
