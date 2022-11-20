#version 400

in float intensity;
out vec4 color;

void main(void) 
{
    // Global ambient light
    vec3 ambient = vec3(0.1, 0.1, 0.1);

    color = vec4(ambient, .5);
}
