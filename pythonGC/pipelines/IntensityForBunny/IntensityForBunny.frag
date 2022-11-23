#version 400

in float intensity;
out vec4 color;

void main(void) 
{
    color = vec4(intensity, intensity, intensity, 1.0);
}
