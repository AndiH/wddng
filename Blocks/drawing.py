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

documentWidth = nDicePerRow * 2 * basesize
documentHeight = nDicePerRow * 1.6 * basesize
svg_document = svgwrite.Drawing(filename="drawing.svg", size=(str(documentWidth) + "px", str(documentHeight) + "px"))
# svg_document.add(svg_document.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill='rgb(50,50,50)'))

# GENERATE BASE DICES
for c in allColors:
    dice = createDiceOneColor(svg_document, basesize, angle, c)
    dice['id'] = c[0][1:]
    svg_document.defs.add(dice)

# CLIP PATH
squareClip = svg_document.defs.add(svg_document.clipPath(id='squareClip'))
squareClip.add(svg_document.rect((0, 0), ("100%", "100%")))

# GENERATE DICES (as references)
allDices = svg_document.g(id="allthedices",  clip_path='url(#squareClip)')
for (i, j) in itertools.product(range(nDicePerRow + 1), range(nDicePerRow + 1)):
    randomnumber = np.random.triangular(0, 0, nDicePerRow)
    colors = colors_andrea
    if (i <= randomnumber):
        colors = colors_andi
    random.shuffle(colors)
    offset = -basesize if (j % 2 == 1) else 0
    dice = svg_document.use(svg_document.g(id=colors[0][0][1:]))
    dice.translate(tx=offset + i * 2 * basesize, ty=j * basesize * (1 + math.tan(math.radians(angle))))
    allDices.add(dice)

svg_document.add(allDices)

rect = svg_document.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill='rgb(255,255,255)', opacity="0.2", id="whitener")
svg_document.add(rect)
# helloWorld = svg_document.text("Hello World", insert=("50%", "50%"), style="font-size: {}px; font-family: PT Sans; font-weight: bolder;".format(basesize * 3), fill="white", text_anchor='middle')
# # helloWorld['text-anchor'] = "middle"
# svg_document.add(helloWorld)

# ADD MONOGRAM
firstAcolor = random.choice(params["monogram"]["Aone_colors"])
secondAcolor = random.choice(params["monogram"]["Atwo_colors"])
firstA = svgwrite.path.Path(params["monogram"]["Aone"], fill=firstAcolor, stroke="none")
secondA = svgwrite.path.Path(params["monogram"]["Atwo"], fill=secondAcolor, stroke="none")
monogram = svg_document.g(id="monogram", transform="translate(-20,-60)")
monogram.add(firstA)
monogram.add(secondA)
svg_document.add(monogram)

# print(svg_document.tostring())

svg_document.save()
