"""
This file is intended to be a repository of sample scripts/queries to run over FrameNet. 

@author: Sean Trott

The scripts will be coded as functions, so you can import them into "main" once you run ./build.sh,
as in:
from scripts import retrieve_pt

"""


from src.lexical_units import *
from src.valence_data import *
from src.hypothesize_constructions import *
from src.ecg_utilities import ECGUtilities as utils

def retrieve_pt(frame, pt="DNI"):
	""" Requires the lexical units in frame to have already been constructed by FrameNetBuilder, so that valence patterns are accessible. 
	Returns all valence units with specified phrase type."""
	returned = []
	for lu in frame.lexicalUnits:
		for valence in lu.individual_valences:
			if valence.pt == pt:
				returned.append(valence)
	return returned


def find_cooccurring_fes(frame, elements):
	""" Returns a list of FE group realization objects featuring AT LEAST the fes specified in elements. 
	ELEMENTS should be a list. """
	return [realization for realization in frame.group_realizations if set(elements).issubset(realization.elements)]




def retrieve_fe(frame, fe):
	""" Requires the lexical units in frame to have already been constructed by FrameNetBuilder, so that valence patterns are accessible. 
	Returns all valence units matching fe."""
	return [valence for valence in frame.individual_valences if valence.fe == fe]


def lus_for_frames(frame_set, fn):
	""" Very simple function that returns a list of lexical unit objects for each frame in FRAME_SET.
	Input frames in FRAME_SET should be strings, not actual frame objects.

	>> lus_for_frames(['Motion', 'Cause_motion'], fn)
	[[move.v, go.v, ...], [cast.v, catapult.v, ....]]
	"""
	return [fn.get_frame(frame).lexicalUnits for frame in frame_set]


def get_valence_patterns(frame):
	patterns = []
	for re in frame.group_realizations:
		patterns += re.valencePatterns
	return patterns



def invert_preps(valences):
	returned = dict()
	for pattern in valences:
		if pattern.pt.split("[")[0].lower() == "pp":
			if pattern.pt not in returned:
				returned[pattern.pt] = []
			if pattern.fe not in returned[pattern.pt]:
				returned[pattern.pt].append(pattern.fe)
	return returned

def build_cxns_for_frame(frame_name, fn, fnb, role_name, pos, filter_value=False):
	"""
	Takes in:
	-frame_name, e.g. "Motion"
	-FrameNet object (fn)
	-FrameNetBuilder object (fnb)
	-"filter_value" boolean: determines if you want to filter valence patterns
	-role_name: role to modify in types/tokens
	-pos: lexical unit POS to create tokens for (e.g., "V")

	TO DO: add PP constructions?

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

	fnb.build_lus_for_frame(frame_name, fn)
	frame = fn.get_frame(frame_name)
	tokens, types = [], []
	tokens = utils.generate_tokens(frame, fn, role_name, pos)
	types = utils.generate_types(frame, fn, role_name, pos_to_type[pos])	



	valence_patterns = get_valence_patterns(frame)
	collapsed_valences = collapse_valences_to_cxns(frame)

	cxns_all = utils.generate_cxns_from_patterns(valence_patterns)
	cxns_collapsed = utils.generate_cxns_from_patterns(collapsed_valences)

	roles = [v.fe for v in frame.individual_valences if v.pt.split("[")[0].lower() == "pp"]
	types = invert_preps(frame.individual_valences)
	pp = utils.generate_pps_from_roles(roles)
	prep_types = utils.generate_general_preps_from_roles(roles)
	prepositions = utils.generate_preps_from_types(types, fn)

	returned = dict(tokens=tokens,
					types=types,
					valence_patterns=valence_patterns,
					collapsed_valences=collapsed_valences,
					cxns_all=cxns_all,
					cxns_collapsed=cxns_collapsed,
					pp = pp,
					prep_types=prep_types,
					prepositions = prepositions)
	return returned







def find_pattern_frequency(frame, target):
	""" Takes in a frame (with lus already built), and a target "Valence" object. Returns the 
	total frequency of that object in frame, which means:
	Total number of annotations across all lus for frame. """
	all_valences = all_individual_valences(frame)
	#target = all_valences[0]
	return sum(i.total for i in all_valences if i==target)


def pattern_across_frames(frames, target):
	""" Takes in multiple frames (a list) and finds frequency of target across them. """
	returned = dict()
	for frame in frames:
		returned[frame.name] = find_pattern_frequency(frame, target)
	return returned



	