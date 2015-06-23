# coding unicode-escape
# Feel free to modify and use this filter however you wish. If you do,
# please give credit to SethBling.
# http://youtube.com/SethBling

from pymclevel import TAG_List
from pymclevel import TAG_Byte
from pymclevel import TAG_Int
from pymclevel import TAG_Compound
from pymclevel import TAG_Short
from pymclevel import TAG_Double
from pymclevel import TAG_String

displayName = "Find and Replace"

inputs = (
	("Find", "string"),
	("Replace", "string"),
)

def perform(level, box, options):
	find = options["Find"]
	replace = options["Replace"]

	for (chunk, slices, point) in level.getChunkSlices(box):
		for t in chunk.TileEntities:
			x = t["x"].value
			y = t["y"].value
			z = t["z"].value
			
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
				if t["id"].value == "Sign":
					for l in range(1, 5):
						line = t["Text" + str(l)].value
						newline = line.replace(find, replace)
						if line != newline:
							t["Text" + str(l)] = TAG_String(newline)
							chunk.dirty = True
				if t["id"].value == "Control":
					cmd = t["Command"].value
					newcmd = cmd.replace(find, replace)
					if newcmd != cmd:
						t["Command"] = TAG_String(newcmd)
						chunk.dirty = True
						