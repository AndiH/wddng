#!/usr/bin/env python3
import svgwrite

import math
import random
import numpy as np

import itertools

from dice import createDiceOneColor
from helpers import readParams


def mmtopx(mm):
    return mm*3.543


def pxtomm(px):
    return px/3.543


params = readParams("../params.toml")
angle = params["dice"]["viewangle"]
basesize = params["dice"]["basesize"]
colors_andi = params["colors"]["ah"]
colors_andrea = params["colors"]["aw"]
allColors = colors_andi + colors_andrea


# documentWidth = nDicePerRow * 2 * basesize
documentWidth = (400, "mm")
# documentHeight = nDicePerRow * 1.6 * basesize
documentHeight = (100, "mm")
svg_document = svgwrite.Drawing(filename="drawing.svg", size=("{}{}".format(documentWidth[0], documentWidth[1]), "{}{}".format(documentHeight[0], documentHeight[1])))
svg_document.add(svg_document.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill='rgb(50,50,50)'))

nDicePerRow = documentWidth[0]/pxtomm(basesize)/2+6  # wtf!
nDicePerColumn = documentHeight[0]/pxtomm(basesize)/2+7  # tf!

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
for (i, j) in itertools.product(range(int(nDicePerRow) + 1), range(int(nDicePerColumn) + 1)):
    randomnumber = np.random.triangular(nDicePerRow/4, nDicePerRow/4, 3*nDicePerRow/4)
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
monogram = svg_document.g(id="monogram", transform="translate({},-40)".format(mmtopx(documentWidth[0])/2 - 278/2))
monogram.add(firstA)
monogram.add(secondA)
svg_document.add(monogram)

# ADD FOLD LINES
foldlines = svg_document.g(id="foldlines")
foldlines_left = svg_document.g(id="foldlines-left")
leftfoldtop = svgwrite.shapes.Line(start=("{}{}".format(documentWidth[0]/4, documentWidth[1]), "0mm"), end=("{}{}".format(documentWidth[0]/4, documentWidth[1]), "2mm"))
leftfoldbottom = svgwrite.shapes.Line(start=("{}{}".format(documentWidth[0]/4, documentWidth[1]), "{}{}".format(documentHeight[0]-2, documentHeight[1])), end=("{}{}".format(documentWidth[0]/4, documentWidth[1]), "{}{}".format(documentHeight[0], documentHeight[1])))
foldlines_left.add(leftfoldtop)
foldlines_left.add(leftfoldbottom)
foldlines.add(foldlines_left)
foldlines_right = foldlines_left.copy()
foldlines_right["id"] = "foldlines-right"
foldlines_right.translate(tx=mmtopx(documentWidth[0]/2))
foldlines.add(foldlines_right)
foldlines.stroke("black", width=1)
svg_document.add(foldlines)


svg_document.save()
