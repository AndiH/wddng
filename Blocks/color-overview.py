#!/usr/bin/env python3
import svgwrite

from dice import createDiceOneColor
from helpers import readParams


params = readParams("../params.toml")
angle = params["dice"]["viewangle"]
basesize = 4 * params["dice"]["basesize"]
colors_andi = params["colors"]["ah"]
colors_andrea = params["colors"]["aw"]
allColors = colors_andi + colors_andrea

width = len(allColors) * 2 * basesize
height = 2.2 * basesize
overview_document = svgwrite.Drawing(filename="color-overview.svg", size=(str(width) + "px", str(height) + "px"), debug=True)
# overview_document.add(overview_document.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill='rgb(50,50,50)'))

for (i, c) in enumerate(allColors):
	print(c)
	dice = createDiceOneColor(overview_document, basesize, angle, c)
	dice.translate(tx = i * 2 * basesize, ty = 0.6 * basesize)
	overview_document.add(dice)
	overview_document.add(overview_document.text(c, insert = (basesize / 3.5 + i * 2 * basesize, basesize), style="font-size: {}; font-family: PT Sans; font-weight: bolder".format(basesize / 2.5)))

overview_document.save()
