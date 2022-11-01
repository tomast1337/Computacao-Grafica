import colorsys

"""
Converts GL RGB 0-1 to HSL 360-100-100
"""


def RGB2HSL(rgb: tuple) -> tuple:
    r, g, b = rgb
    return colorsys.rgb_to_hls(r, g, b)


"""
Converts HSL 360-100-100 to GL RGB 0-255
"""


def HSL2RGB(hsl: tuple) -> tuple:
    h, s, l = hsl
    h /= 360
    s /= 100
    l /= 100
    return colorsys.hls_to_rgb(h, s, l)

if __name__ == "__main__":
    rgb = (0.54789, 0.4657, 0.9654)
    result = RGB2HSL(rgb)
    print(f"RGB: {rgb} -> HSL: {result}")
    hsl = (183, 50, 50)
    result = HSL2RGB(hsl)
    print(f"HSL: {hsl} -> RGB: {result}")
