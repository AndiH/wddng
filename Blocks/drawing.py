#!/usr/bin/env python
import svgwrite
import spectra

import math
import random
import numpy as np

import itertools

angle = 30
BASESIZE = 10
colors_andi = ["#88d4ea", "#84acba", "#6792ab", "#9eb9bb", "#5e937d"] #, "#5e937d"
colors_andrea = ["#b58fc5", "#8787de", "#afd0fc", "#ea9ff2", "#8e9fcb"] #"#8787de", "#a0a0ec"
# colors_andrea = ["#a87395", "#ff8de1", "#6969bb"] #"#90bcb8", "#8d5fd3"
allColors = colors_andi + colors_andrea

def createDice(docu, color1 = "rgb(255, 0, 0)", color2 = "rgb(0, 255, 0)", color3 = "rgb(0, 0, 255)"):
	basebox = docu.rect(insert = (0, 0), size = (str(BASESIZE) + "px", str(BASESIZE) + "px"), fill = color1)

	left = basebox.copy()
	left.skewY(angle)

	right = basebox.copy()
	right.fill(color = color2)
	right.translate(tx = BASESIZE, ty = BASESIZE * math.tan(math.radians(angle)))
	right.skewY(-angle)

	center = basebox.copy()
	center.fill(color = color3)
	center.translate(tx = BASESIZE, ty = -BASESIZE * math.tan(math.radians(angle)))
	center.scale(sx = 2 / math.sqrt(2), sy = math.tan(math.radians(angle)) * math.sqrt(2))
	center.rotate(45)

	dice = svg_document.g()
	# dice.update("id = dice")
	dice.add(left)
	dice.add(right)
	dice.add(center)
	return dice

def createDiceOneColor(docu, color1):
	spectraColor1 = spectra.html(color1)
	# spectraColor2 = spectraColor1.brighten(17)
	spectraColor2 = spectra.lab(spectraColor1.to("lab").values[0] * 1.2, spectraColor1.to("lab").values[1], spectraColor1.to("lab").values[2])
	# spectraColor3 = spectraColor1.brighten(12)
	spectraColor3 = spectra.lab(spectraColor1.to("lab").values[0] * 1.1, spectraColor1.to("lab").values[1], spectraColor1.to("lab").values[2])
	return createDice(docu, spectraColor1.hexcode, spectraColor2.hexcode, spectraColor3.hexcode)

svg_document = svgwrite.Drawing(filename = "test-svgwrite.svg",
                                size = ("1200px", "1000px"))

rowofdice = svg_document.g()
for (i, j) in itertools.product(xrange(0,20), xrange(0,20)):
	randomnumber = np.random.triangular(0,0,20)
	colors = colors_andrea
	if (i <= randomnumber):
		colors = colors_andi
	random.shuffle(colors)
	# dice = createDice(svg_document, colors[0], colors[1], colors[2])
	dice = createDiceOneColor(svg_document, colors[0])
	offset = -BASESIZE if (j % 2 == 1) else 0
	dice.translate(tx = offset + i * 2 * BASESIZE, ty = j * BASESIZE * (1 + math.tan(math.radians(angle))))
	rowofdice.add(dice)

# rowofdice2 = rowofdice.copy()
# rowofdice2.translate(tx = -BASESIZE, ty = BASESIZE * (1 + math.tan(math.radians(angle))))
# rowofdice3 = rowofdice.copy()
# rowofdice3.translate(tx = 0, ty = 2 * BASESIZE * (1 + math.tan(math.radians(angle))))

svg_document.add(rowofdice)
# svg_document.add(rowofdice2)
# svg_document.add(rowofdice3)

svg_document.add(svg_document.text("Hello World",
                                   insert = (210, 110)))

# print(svg_document.tostring())

svg_document.save()

overview_document = svgwrite.Drawing(filename = "color-overview.svg", size = ("500px", "200px"))
for (i, c) in enumerate(allColors):
	print c
	dice = createDiceOneColor(overview_document, c)
	dice.translate(tx = i * 2 * BASESIZE, ty = BASESIZE)
	overview_document.add(dice)
	overview_document.add(overview_document.text(c, insert = (i * 2 * BASESIZE, BASESIZE), style="font-size: 4"))

overview_document.save()
