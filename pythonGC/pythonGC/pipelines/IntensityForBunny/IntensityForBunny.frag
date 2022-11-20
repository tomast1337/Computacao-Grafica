#version 400

in float intensity;
out vec4 color;

void main(void) 
{
    color = vec4(vec3(intensity), 0.5f);
}
