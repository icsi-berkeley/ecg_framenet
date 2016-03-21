"""
@author: <seantrott@icsi.berkeley.edu>

Initializes FrameNetBuilder and FrameNet objects.
"""

from src.builder import *
import sys
from src.ecg_utilities import ECGUtilities as utils
#from src.valence_data import *

from src.hypothesize_constructions import *

from scripts import *


def main(data_path):
	frame_path = data_path + "frame/"
	relation_path = data_path + "frRelation.xml"
	lu_path = data_path + "lu/"	
	fnb = FramenetBuilder(frame_path, relation_path, lu_path)
	fn = fnb.read() #fnb.read()
	fn.build_relations()
	fn.build_typesystem()
	return fn, fnb

if __name__ == "__main__":
	fn, fnb = main(sys.argv[1])

	

	# DEMO: SCHEMAS
	schemas = utils.generate_schemas_for_frames(fn.frames)
	# Write these to a file


	# DEMO: CONSTRUCTIONS
	total = build_cxns_for_frame("Motion", fn, fnb, "Manner", "V")

	#You can then write the values from the total dictionary into files:
	#* cxns_all: all valences converted 1-1 to cxns 
	#* cxns_collapsed: valences collapsed into smaller set 
	#* tokens: tokens created from these frames ("swarm.v", etc.)
	#* types: type-cxns ("Fluidic_motionType") created from these frames 
	
















	
	
	