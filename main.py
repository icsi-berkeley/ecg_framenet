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

import csv


def main(data_path):
	frame_path = data_path + "frame/"
	relation_path = data_path + "frRelation.xml"
	lu_path = data_path + "lu/"	
	fnb = FramenetBuilder(frame_path, relation_path, lu_path)
	fn = fnb.read() #fnb.read()
	fn.build_relations()
	fn.build_typesystem()
	return fn, fnb

def ecg_demo1():
	""" Returns list of ECG schemas from FrameNet frames. """
	return utils.generate_schemas_for_frames(fn.frames)

def ecg_demo2(frame="Motion", role="Manner", pos="V"):
	""" Returns dictionary of types/tokens, valence cxns, and prepositions for a frame. """
	return build_cxns_for_frame(frame, fn, fnb, role, pos)



if __name__ == "__main__":
	fn, fnb = main(sys.argv[1])

	#fnb.build_lus_for_frame("Motion_directional", fn)
	#s = fn.get_frame("Motion_directional")
	#s.propagate_elements()



	#valences = all_family_valences(s, fn, fnb, True)


	#fnb.build_lus_for_frame("Fluidic_motion", fn)
	#s = fn.get_frame("Fluidic_motion")

	#DEMO: Build list of frames with all their relations
	"""
	final_relations = [['Frame', 'Inherits from', 'Is Inherited by', 'Perspective on', 'Is Perspectivized in', 'Uses', 'Is Used by', 'Subframe of', 'Has Subframe(s)', 'Precedes', 'Is Preceded by', 'Is Inchoative of', 'Is Causative of', 'See also']]
	for frame in fn.frames:
		temp = [frame.name, None, None, None, None, None, None, None, None, None, None, None, None, None]
		for relation in frame.relations:
			if relation.relation_type in final_relations[0]:
				index = final_relations[0].index(relation.relation_type)
				s = [f.name for f in relation.related_frames]
				temp[index] = s
		final_relations.append(temp)

	"""



	#DEMO: Gets parents and children
	#inheritance = [[f.name, f.children, f.parents] for f in fn.frames]


	#DEMO: Build LUS for all frames, put in tuple format with annotations

	"""
	final = []
	for frame in fn.frames:
		print("Building lus for {}.".format(frame.name))
		fnb.build_lus_for_frame(frame.name, fn)
		for i in frame.annotations:
			mini = [i.sentence.encode('utf-8'), i.lu, i.frame]
			for k, v in i.text_to_valence.items():
				mini.append(k.encode('utf-8'))
				mini.append(v.fe.encode('utf-8'))
				mini.append(v.pt.encode('utf-8'))
				if v.pt in ['INI', 'DNI', 'CNI']:
					mini.append("---")
				else:
					mini.append(v.gf)
			final.append(mini)
	#"""


	# DEMO 2: Build LUS for frames, put annotations in tuple format
	# New line/row for each valence unit for each annotation
	
	final = []
	for frame in fn.frames:
		print("Building lus for {}.".format(frame.name))
		fnb.build_lus_for_frame(frame.name, fn)
		for i in frame.annotations:
			for k, v in i.text_to_valence.items():
				mini = [i.sentence.encode('utf-8'), i.lu.encode('utf-8'), i.frame.encode('utf-8')]
				mini.append(k.encode('utf-8'))
				mini.append(v.fe.encode('utf-8'))
				mini.append(v.pt.encode('utf-8'))
				if v.pt in ['INI', 'DNI', 'CNI']:
					mini.append("---".encode('utf-8'))
				else:
					mini.append(v.gf.encode("utf-8"))
				final.append(mini)
	



	

	# DEMO: Writing to CSV file
	#resultFile = open("output.csv", "w")
	#wr = csv.writer(resultFile, dialect="excel")
	#wr.writerows(final)

	
	# DEMO: SCHEMAS
	#schemas = utils.generate_schemas_for_frames(fn.frames)
	# Write these to a file


	# DEMO: CONSTRUCTIONS
	#total = build_cxns_for_frame("Motion", fn, fnb, "Manner", "V")

	#You can then write the values from the total dictionary into files:
	#* cxns_all: all valences converted 1-1 to cxns 
	#* cxns_collapsed: valences collapsed into smaller set 
	#* tokens: tokens created from these frames ("swarm.v", etc.)
	#* types: type-cxns ("Fluidic_motionType") created from these frames 
	#* pp: PP constructions that are specific to the frame (e.g., Instrument-PP)
	#* prep_types: General prepositional type constructions used for frame (E.g., "Instrument-Prep")
	#* prepositions: Preposition constructions that are used for that frame (E.g. "With-Preposition"[subcase of Instrument-Prep])
	# NOTE: The last three (pp, prep_types, and prepositions) are necessary for the collapsed cxns, since this filters by PP-type,
	# and collapses two valence units if they are PPs mapping onto the same FE.


	#DEMO: PREPOSITION CONSTRUCTIONS (distinct from build_cxns_for_frame, above)
	#prepositions = utils.build_prepositions(fn)
	
















	
	
	