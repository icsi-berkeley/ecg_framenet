"""
This file is intended to be a repository of sample scripts/queries to run over FrameNet. 

@author: Sean Trott

The scripts will be coded as functions, so you can import them into "main" once you run ./build.sh,
as in:
from scripts import ....

"""


from src.lexical_units import *
from src.valence_data import *
from src.ecg_utilities import ECGUtilities as utils

def retrieve_pt(frame, pt="DNI"):
	""" Requires the lexical units in frame to have already been constructed by FrameNetBuilder,
	so that valence patterns are accessible. 
	Returns all valence units with specified phrase type."""
	if len(frame.lexicalUnits) > 0 and not type(frame.lexicalUnits[0]) == LexicalUnit:
		return
	else:
		returned = []
		patterns = all_valences2(frame)
		for valence in patterns:
			if valence.pt == pt:
				returned.append(valence)
		return returned


def lus_for_frames(frame_set, fn):
	""" Very simple function that returns a list of lexical unit objects for each frame in FRAME_SET.
	Input frames in FRAME_SET should be strings, not actual frame objects.

	>> lus_for_frames(['Motion', 'Cause_motion'], fn)
	[[move.v, go.v, ...], [cast.v, catapult.v, ....]]
	"""
	return [fn.get_frame(frame).lexicalUnits for frame in frame_set]



def build_cxns_for_frame(frame_name, fn, fnb, role_name, pos, filter_value=False):
	"""
	Takes in:
	-frame_name, e.g. "Motion"
	-FrameNet object (fn)
	-FrameNetBuilder object (fnb)
	-"filter_value" boolean: determines if you want to filter valence patterns
	-role_name: role to modify in types/tokens
	-pos: lexical unit POS to create tokens for (e.g., "V")

	Returns:
	-tokens
	-types
	-VP valences (non-collapsed)
	-VP valences (collapsed)
	-VP constructions (non-collapsed)
	-vP constructions (collapsed)
	"""

	pos_to_type = dict(V="LexicalVerbType",
					   N="NounType")

	frame = fn.get_frame(frame_name)
	fnb.build_lus_for_frame(frame_name, fn)

	# TODO: not working

	tokens = utils.generate_tokens(frame, fn, role_name, pos)

	types = utils.generate_types(frame, fn, role_name, pos_to_type[pos])	

	valences = all_valences(frame, filter_value)

	collapsed_valences = [collapse_all(valences[0], valences[1:], s)]

	cxns_all = utils.generate_cxns_from_patterns(valences)
	cxns_collapsed = utils.generate_cxns_from_patterns(collapsed_valences)


	returned = dict(tokens=tokens,
					types=types,
					valences=valences,
					collapsed_valences=collapsed_valences,
					cxns_all=cxns_all,
					cxns_collapsed=cxns_collapsed)

	return returned





"""




from src.builder import *
import sys
from src.ecg_utilities import ECGUtilities as utils
#from src.ecg_utilities import format_valence_verb_cxn, format_schema, generate_cxns_for_lu, generate_cxns_from_patterns
#from src.ecg_utilities import generate_schemas_for_frames
#from src.ecg_utilities import generate_preps_from_types, generate_pps_from_roles
#from src.ecg_utilities import gather_lexicalUnits, generate_entity_tokens
from src.valence_data import *

if __name__ == "__main__":
	data_path = sys.argv[1]
	frame_path = data_path + "frame/"
	relation_path = data_path + "frRelation.xml"
	lu_path = data_path + "lu/"	
	fnb = FramenetBuilder(frame_path, relation_path, lu_path)
	fn = fnb.read() #fnb.read()
	fn.build_relations()
	fn.build_typesystem()



	schemas = utils.generate_schemas_for_frames(fn.frames)
	schema_file = open("generated/schemas.grm", "w")
	schema_file.write(schemas)
	schema_file.close()
	
	s = fn.get_frame("Cure")
	fnb.build_lus_for_frame("Cure", fn)

	#lus = utils.gather_lexicalUnits(s, fn)




	#d = all_valences(s)
	#e = all_valences(t)

	#common = find_common_patterns(s, t)

	#tokens = utils.generate_tokens(s, fn, "Attribute", "N")
	#f = open("generated/entities.tokens", "w")
	#f.write(tokens)
	#f.close()


	#types = utils.generate_types(s, fn, "Attribute", "NounType")
	#f = open("generated/entities.tokens", "w")
	#f.write(tokens)
	#f.close()

	#mappings = lu_to_unique_patterns(s)
	#mappings = all_valences(s, False)
	#roles = find_pp_roles(mappings)

	#filtered = filter_by_pp_type(filtered)

	valences = all_valences(s, True)

	#d = collapse_patterns(valences[0], valences[1], s)

	valences = [collapse_all(valences[0], valences[1:], s)]
	#ordered = sorted(valences, key=lambda valence: valence.total, reverse=True)

	#inverted = invert_roles(roles)
	
	
	general = utils.generate_general_preps_from_roles(roles.keys())
	f1 = open("generated/preps.grm", "w")
	f1.write(general)
	f1.close()
	
	preps = utils.generate_preps_from_types(inverted)
	f = open("generated/preps.grm", "w")
	f.write(preps)
	f.close()

	pps = utils.generate_pps_from_roles(roles.keys())
	new = open("generated/pp.grm", "w")
	new.write(pps)
	new.close()
	
	#total =0
	#for k, v in roles.items():
	#	total += len(v)
	
	t = utils.generate_cxns_from_patterns(valences)
	f = open("generated/cxns.grm", "w")
	f.write(t)
"""
	