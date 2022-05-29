let freq = 1.77,
    new_X = Math.sin(freq*X), // SPACE MAPPING
    new_Y = Math.sin(freq*Y), // SPACE MAPPING
    Radius = 0.34,
        rad = 0.2,
        render = 0.66,

value = rad - Math.sqrt(new_X*new_X + new_Y*new_Y + Z*Z + Radius*Radius - 2*Radius*Math.sqrt(new_X*new_X+new_Y*new_Y));
