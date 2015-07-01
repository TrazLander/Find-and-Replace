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

## displayName = ""

colorChr = "%%"

Mode = {
	"[F:T] Find and replace": 0,
	"[f:T] Add": 1,
	"       Iterate": 2,
	"       Toggle Wall Sign": 3,
	"[T]   Mass Find Replace": 4,
}

inputs = (
	("Signs    ", True ),
	("   Line 1", True ),
	("   Line 2", True ),
	("   Line 3", True ),
	("   Line 4", True ),
	("Command Blocks", True ),
	("Color Code Character", ("string","value=%%")),
	("Find", ("string","value=NONE","width=500")),
	("Text", ("string","value=NONE","width=500")),
	("[] = Arguments required for selected mode. Capital letter = required, lowercase = optional input.", "label"),
	("Mode", ("[F:T] Find and replace", "[f:T] Add", "       Iterate", "       Toggle Wall Sign", "[T]   Mass Find Replace")),
)

def perform(level, box, options):
	mode = Mode[options["Mode"]]
	sign = options["Signs    "]
	line1 = options["   Line 1"]
	line2 = options["   Line 2"]
	line3 = options["   Line 3"]
	line4 = options["   Line 4"]
	cb = options["Command Blocks"]
	global colorChr
	colorChr = options["Color Code Character"]
	find = options["Find"]
	replace = options["Text"]

	print "MODE " + str(mode)
	print "FIND " + find
	print repr("Replace " + replace)

	for (chunk, slices, point) in level.getChunkSlices(box):
		for t in chunk.TileEntities:
			x = t["x"].value
			y = t["y"].value
			z = t["z"].value
			
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:

				if mode == 3:
					numID = level.blockAt(x,y,z)
					dataID = level.blockDataAt(x,y,z)
					isStraight = True
					updData = 8

					if numID == 63:
						if dataID == 8:
							updData = 2
						elif dataID == 0:
							updData = 3
						elif dataID == 4:
							updData = 4
						elif dataID == 12:
							updData = 5
						else:
							isStraight = False

						if isStraight == True:
							level.setBlockAt(x,y,z,68)
							level.setBlockDataAt(x,y,z,updData)
							chunk.dirty = True
					elif numID == 68:
						level.setBlockAt(x,y,z,63)
						if dataID == 2:
							updData = 8
						elif dataID == 3:
							updData = 0
						elif dataID == 4:
							updData = 4
						elif dataID == 5:
							updData = 12
						level.setBlockDataAt(x,y,z,updData)
						chunk.dirty = True

				if t["id"].value == "Sign" and sign:
					if line1:
						line = t["Text1"].value
						newline = things(line, find, replace, mode, x, box.minx, box.maxx, y, box.miny, box.maxy, z, box.minz, box.maxz)
						if line != newline:
							t["Text1"] = TAG_String(newline)
							chunk.dirty = True
					if line2:
						line = t["Text2"].value
						newline = things(line, find, replace, mode, x, box.minx, box.maxx, y, box.miny, box.maxy, z, box.minz, box.maxz)
						if line != newline:
							t["Text2"] = TAG_String(newline)
							chunk.dirty = True
					if line3:
						line = t["Text3"].value
						newline = things(line, find, replace, mode, x, box.minx, box.maxx, y, box.miny, box.maxy, z, box.minz, box.maxz)
						if line != newline:
							t["Text3"] = TAG_String(newline)
							chunk.dirty = True
					if line4:
						line = t["Text4"].value
						newline = things(line, find, replace, mode, x, box.minx, box.maxx, y, box.miny, box.maxy, z, box.minz, box.maxz)
						if line != newline:
							t["Text4"] = TAG_String(newline)
							chunk.dirty = True

				if t["id"].value == "Control" and cb:
						cmd = t["Command"].value
						newcmd = things(cmd, find, replace, mode, x, box.minx, box.maxx, y, box.miny, box.maxy, z, box.minz, box.maxz)
						if newcmd != cmd:
							t["Command"] = TAG_String(newcmd)
							chunk.dirty = True

def things(line, find, replace, mode, x, minx, maxx, y, miny, maxy, z, minz, maxz):
	line = line.replace(unichr(167), colorChr)
	if mode == 0:
		if replace == "NONE":
			return formt(line.replace(find, ""))
		else:	
			if find == "NONE":
				return formt(replace)
			else:
				return formt(line.replace(find, replace))
	if mode == 1:
			return formt(line.replace(find, find + replace))
	if mode == 2:
		line = line.replace("[x+]", str(x - minx))
		line = line.replace("[x-]", str(maxx - x))
		line = line.replace("[y+]", str(y - miny))
		line = line.replace("[y-]", str(maxy - y))
		line = line.replace("[z+]", str(z - minz))
		line = line.replace("[z-]", str(maxz - z))
		return formt(line)
	if mode == 4:
		mass = replace.split(',')
		finD = ""
		alternate = True
		for m in mass:
			if alternate == True:
				finD = m
				alternate = False
			else:
				line = line.replace(finD, m)
				alternate = True
		return formt(line)
	return formt(line)



def formt(final):
	return final.replace(colorChr, unichr(167))

def error(reason):
	raise Exception(reason)
	stop = True