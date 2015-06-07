from numpy import loadtxt
from pymclevel import alphaMaterials

"""
Script for importing digital elevation model (DEM) into Minecraft/McEdit
June 2015 by Thunderstage

Partially based on jsa's "mountain_gen.py" - generating hilly & mountainous terrain in MCEdit.
Uses ASCII GRID import according to http://geospatialpython.com/2013/12/python-and-elevation-data-ascii-grid.html

"""

displayName = "DEM Generator v0.1"

inputs = (
	("Top layer:", alphaMaterials.Grass),
	("Depth of top layer:", (1,0,100)),
	("Foundation:", alphaMaterials.Stone),
#	("Horizontal exaggeration:", (1,1,100)),
	("Vertical offset:", (75,0,1000)),		# can be used to move minimum elevation to sea level
#	("Vertical exaggeration:", (1,1,100)),		# should be used if x-z coordinates are geographic
	("Vertical shrink:", (5,1,100)),		# used temporarily because steps in y currently equal steps in x-z
#	("ASCII GRID source file:", "C:\Users\admin\Documents\QGIS\McDemToronto\cdem4mc.asc"),	# don't know how to write file name input
)

def perform(level, box, options):
	top_layer = options["Top layer:"]
	top_layer_depth = options["Depth of top layer:"]
	foundation = options["Foundation:"]
#	horizontal_exaggeration = options["Horizontal exaggeration:"]
	vertical_offset = options["Vertical offset:"]
#	vertical_exaggeration = options["Vertical exaggeration:"]
	vertical_shrink = options["Vertical shrink:"]
#	ascii_grid_source_file = options["ASCII GRID source file:"]


#	myArray  = numpy.loadtxt(ascii_grid_source_file, skiprows=5)
	myArray  = loadtxt(r"C:\Users\admin\Documents\QGIS\McDemToronto\cdem4mc21.asc", skiprows=5)
	
#	x_max = (myArray.shape[1])/horizontal_exaggeration
#	z_max = (myArray.shape[0])/horizontal_exaggeration

	# not sure whether indices in file and array are running in consistent directions
	x_max = myArray.shape[0]
	z_max = myArray.shape[1]

	# DEM creation
	for x in range(0, x_max):
		for z in range(0, z_max):
			# currently, vertical step equals x-z steps (non-geographic), thus needs shrinking
			h = int((myArray[x][z] - vertical_offset)/vertical_shrink)
			if(h < 1):
				continue

			# for each block in column; use geo coord system (maxz-z instead of minz+z)
			for y in range(0, h): 
				if(y >= (h-top_layer_depth)):
					level.setBlockAt(box.minx + x, y, box.maxz - z, top_layer.ID)
					level.setBlockDataAt(box.minx + x, y, box.maxz - z, top_layer.blockData)
				else:
					level.setBlockAt(box.minx + x, y, box.maxz - z, foundation.ID)
					level.setBlockDataAt(box.minx + x, y, box.maxz - z, foundation.blockData)
		print("Completed row ", x, " out of ", x_max)

	# chunk update (not sure how this works)
	for chunk, slices, point in level.getChunkSlices(box):				
		chunk.chunkChanged()
