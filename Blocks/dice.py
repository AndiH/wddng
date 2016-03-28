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


def createDiceOneColor(document, basesize, angle, color1):
    spectraColor1 = spectra.html(color1)
    # spectraColor2 = spectraColor1.brighten(17)
    spectraColor2 = spectra.lab(spectraColor1.to("lab").values[0] * 1.2, spectraColor1.to("lab").values[1], spectraColor1.to("lab").values[2])
    # spectraColor3 = spectraColor1.brighten(12)
    spectraColor3 = spectra.lab(spectraColor1.to("lab").values[0] * 1.1, spectraColor1.to("lab").values[1], spectraColor1.to("lab").values[2])
    return createDice(document, basesize, angle, spectraColor1.hexcode, spectraColor2.hexcode, spectraColor3.hexcode)
