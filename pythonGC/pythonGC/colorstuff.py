def RGB2HSL(rgb):
    r, g, b = rgb
    r, g, b = r , g , b
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g) / df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df / mx) * 100
    l = (mx + mn) / 2 * 100
    return h, s, l

def HSL2RGB(hsl):
    h, s, l = hsl
    h, s, l = h / 360, s / 100, l / 100
    if s == 0.0:
        v = l
        return v, v, v
    if l < 0.5:
        var_2 = l * (1 + s)
    else:
        var_2 = (l + s) - (s * l)
    var_1 = 2 * l - var_2
    r = 255 * hue2rgb(var_1, var_2, h + (1 / 3))
    g = 255 * hue2rgb(var_1, var_2, h)
    b = 255 * hue2rgb(var_1, var_2, h - (1 / 3))
    return r, g, b