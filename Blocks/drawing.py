#!/usr/bin/env python3
import svgwrite

import math
import random
import numpy as np

import itertools

from dice import createDiceOneColor
from helpers import readParams


params = readParams("../params.toml")
angle = params["dice"]["viewangle"]
basesize = params["dice"]["basesize"]
colors_andi = params["colors"]["ah"]
colors_andrea = params["colors"]["aw"]
allColors = colors_andi + colors_andrea

nDicePerRow = 20

svg_document = svgwrite.Drawing(filename="test-svgwrite.svg", size=("1200px", "1000px"))

rowofdice = svg_document.g()
for (i, j) in itertools.product(range(nDicePerRow), range(nDicePerRow)):
    randomnumber = np.random.triangular(0, 0, nDicePerRow)
    colors = colors_andrea
    if (i <= randomnumber):
        colors = colors_andi
    random.shuffle(colors)
    # dice = createDice(svg_document, colors[0], colors[1], colors[2])
    dice = createDiceOneColor(svg_document, basesize, angle, colors[0])
    offset = -basesize if (j % 2 == 1) else 0
    dice.translate(tx=offset + i * 2 * basesize, ty=j * basesize * (1 + math.tan(math.radians(angle))))
    rowofdice.add(dice)

# rowofdice2 = rowofdice.copy()
# rowofdice2.translate(tx = -basesize, ty = basesize * (1 + math.tan(math.radians(angle))))
# rowofdice3 = rowofdice.copy()
# rowofdice3.translate(tx = 0, ty = 2 * basesize * (1 + math.tan(math.radians(angle))))

svg_document.add(rowofdice)
# svg_document.add(rowofdice2)
# svg_document.add(rowofdice3)

svg_document.add(svg_document.text("Hello World", insert=(210, 110)))

# print(svg_document.tostring())

svg_document.save()
