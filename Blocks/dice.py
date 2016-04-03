import math
import spectra


def createDice(document, basesize, angle, color1="rgb(255, 0, 0)", color2="rgb(0, 255, 0)", color3="rgb(0, 0, 255)"):
    basebox = document.rect(insert=(0, 0), size=(str(basesize) + "px", str(basesize) + "px"), fill=color1)

    left = basebox.copy()
    left.skewY(angle)

    right = basebox.copy()
    right.fill(color=color2)
    right.translate(tx=basesize, ty=basesize * math.tan(math.radians(angle)))
    right.skewY(-angle)

    center = basebox.copy()
    center.fill(color=color3)
    center.translate(tx=basesize, ty=-basesize * math.tan(math.radians(angle)))
    center.scale(sx=2 / math.sqrt(2), sy=math.tan(math.radians(angle)) * math.sqrt(2))
    center.rotate(45)

    dice = document.g()
    # dice.update("id = dice")
    dice.add(left)
    dice.add(right)
    dice.add(center)
    return dice


def createDiceOneColor(document, basesize, angle, color):
    if type(color) is list:
        baseColor = spectra.html(color[0])
        if len(color) >= 2:
            lightColor = spectra.html(color[1])
        else:
            lightColor = spectra.lab(baseColor.to("lab").values[0] * 1.1, baseColor.to("lab").values[1], baseColor.to("lab").values[2])
        if len(color) == 3:
            lightestColor = spectra.html(color[2])
        else:
            lightestColor = spectra.lab(baseColor.to("lab").values[0] * 1.2, baseColor.to("lab").values[1], baseColor.to("lab").values[2])
    else:
        baseColor = spectra.html(color)
        lightColor = spectra.lab(spectra.html(color).to("lab").values[0] * 1.1, spectra.html(color).to("lab").values[1], spectra.html(color).to("lab").values[2])
        lightestColor = spectra.lab(spectra.html(color).to("lab").values[0] * 1.2, spectra.html(color).to("lab").values[1], spectra.html(color).to("lab").values[2])
    return createDice(document, basesize, angle, baseColor.hexcode, lightestColor.hexcode, lightColor.hexcode)


def spectraHslToSvgHsl(color):
    return "hsl({}, {}%, {}%)".format(color.values[0], color.values[1] * 100, color.values[2] * 100)


def createDiceOneColorHsl(document, basesize, angle, color):
    if type(color[0]) is list:
        baseColor = spectra.hsl(color[0][0], color[0][1], color[0][2])
        lightColor = spectra.hsl(color[1][0], color[1][1], color[1][2])
        if len(color[0]) is 2:
            lightestColor = spectra.hsl(color[2][0], color[2][1], color[2][2])
        else:
            lightestColor = spectra.hsl(color[0][0], color[0][1], color[0][2] + 0.07)
    else:
        baseColor = spectra.hsl(color[0], color[1], color[2])
        lightColor = spectra.hsl(color[0], color[1], color[2] * 1.1)
        lightestColor = spectra.hsl(color[0], color[1], color[2] * 1.15)
    return createDice(document, basesize, angle, baseColor.hexcode, lightestColor.hexcode, lightColor.hexcode)

