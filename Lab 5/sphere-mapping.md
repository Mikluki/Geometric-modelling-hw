let freq = 1.1,
    new_X = Math.sin(freq*X), // SPACE MAPPING
    new_Y = Math.sin(freq*Y), // SPACE MAPPING
    new_Z = Math.sin(freq*Z),
    rad = 0.85,
    render = 0.35,
    

    value = rad - Math.sqrt(new_X*new_X + new_Y*new_Y + new_Z*new_Z);
return value*render;
