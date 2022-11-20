void mainImage( out vec4 fragColor, in vec2 fragCoord )
{   
    vec2 uvOriginal = fragCoord/iResolution.xy;
    vec2 uv = (2.0*fragCoord/iResolution.xy)-1.0;
    uv.x *= iResolution.x/iResolution.y;
    vec2 centro = vec2(0.0,0.0);
    float radius = .8;
    float pDistance = distance(uv,centro);
    // Time varying pixel color
    vec3 col = 0.5 + 0.5 
    * cos(iTime+uv.xyx+vec3(0,2,4)) 
    * step(pDistance,radius)
    * texture(iChannel0, uvOriginal).xyz;
   
    // Output to screen
    fragColor = vec4(col,1.0);
}