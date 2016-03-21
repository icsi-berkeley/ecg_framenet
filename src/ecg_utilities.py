from src.hypothesize_constructions import *

class ECGUtilities(object):

	def format_schema(frame):
		semtype_to_frame = {'Physical_object': "Entity",
							'Artifact': "Artifact",
							'Living_thing': "Biological_entity"}
		forbidden = ['construction', 'Construction',
					'Situation', 'situation', 'map', "Map",
					"Form", "form",
					"Feature", "feature",
					"Constraints", "constraints",
					"Type", "type",
					"Constituents", "constituents",
					"Meaning", "meaning"]
		name = frame.name
		uses = []
		for relation in frame.relations:
			if relation.relation_type == "Uses":
				uses = [r for r in relation.related_frames]
				#print(relation.related_frames)
		causes = []
		for relation in frame.relations:
			if relation.relation_type == "Is Causative of":
				causes = [r for r in relation.related_frames]
		parents = None
		if len(frame.parents) > 0:
			parents = ", ".join(frame.parents)
		elements = []
		for i in frame.elements:
			tc = ""
			if i.semtype != None and i.semtype.name in semtype_to_frame:
				tc = ": {}".format(semtype_to_frame[i.semtype.name])
			if not i.name in forbidden:
				elements.append(i.name + tc)
			else:
				elements.append(i.name + "_fn" + tc)
		#elements = [i.name if not i.name in forbidden else "" for i in frame.elements]
		roles = " \n ".join(elements)
		final = "schema {} \n".format(name)
		if parents:
			final += "    subcase of {} \n".format(parents) 
		for use in uses:
			final += "    evokes {} as {} \n".format(use.name, use.name.lower())
		for cause in causes:
			final += "    evokes {} as {} \n".format(cause.name, cause.name.lower())
		final += "    roles \n"
		for role in elements:
			final += "       {} \n".format(role)

		if len(frame.fe_relations) > 0:
			final += "     constraints \n"
		for c in frame.fe_relations:
			f1, f2 = c.fe1, c.fe2
			if f1 in forbidden:
				f1 = f1 + "_fn"
			if f2 in forbidden:
				f2 = f2 + "_fn"
			if c.name == "Using":
				f1 = c.superFrame.lower() + "." + f1
			if c.name == "Causative_of":
				f2 = c.subFrame.lower() + "." + f2
				#print(f1)
			r = "       {} <--> {} \n".format(f1, f2)
			final += r
		return final

	def generate_schemas_for_frames(frames):
		returned = ""
		for frame in frames:
			returned += ECGUtilities.format_schema(frame) + "\n\n"
		return returned

	# This test is for verbs only
	def format_valence_verb_cxn(valence_pattern, n):
		final = ""
		name = valence_pattern.frame + "_pattern{}".format(n)
		final += "construction {} \n".format(name)
		final += "     subcase of ArgumentStructure\n"
		final += "	   constructional\n"
		final += "		constituents\n"
		final += "		v: Verb\n" # HACK
		for v in valence_pattern.valenceUnits:
			if v.gf != "Ext":
				pt = v.pt.replace("[", "-").replace("]", "")
				total = v.total
				ommission_prob = (total / valence_pattern.total)
				if pt in ['INI', 'DNI', 'CNI']:
					final += "		{}: {} [{}, .9]\n".format(pt.lower(), pt, ommission_prob)
				else:
					final += "		{}: {} [{}, .9]\n".format(pt.lower(), pt, ommission_prob)
		final += "	   meaning: {}\n".format(valence_pattern.frame)
		final += "		constraints\n"
		final += "		self.m <--> v.m\n"  # HACK
		for v in valence_pattern.valenceUnits:
			if v.gf == "Ext": #HACK
				final += "		ed.profiledParticipant <--> self.m.{}\n".format(v.fe)
			else:
				pt = v.pt.replace("[", "-").replace("]", "")
				#if pt.split("-")[0] == "PP":
				#	constituent = "{}-PP".format(v.fe)
				#	final += "		self.m.{} <--> {}.m\n".format(v.fe, constituent.lower())
				#	final += "		self.m.Theme <--> {}.m.Trajector\n".format(constituent.lower())
				#else:
				final += "		self.m.{} <--> {}.m\n".format(v.fe, pt.lower())
		return final



	# Requires a "built" lu - e.g., one with valence patterns, etc.
	def generate_cxns_for_lu(lu):
		returned = ""
		i = 1
		for realization in lu.valences:
			for pattern in realization.valencePatterns:
				returned += ECGUtilities.format_valence_verb_cxn(pattern, i) + "\n\n"
				i += 1
		return returned


	def generate_cxns_from_patterns(patterns, collapsed=True):
		returned = ""
		i = 1
		for pattern in patterns:
			if collapsed:
				returned += hypothesize_construction_from_collapsed_pattern(pattern, i).format_to_cxn() + "\n\n"
			else:
				returned += hypothesize_construction_from_pattern(pattern, i).format_to_cxn() + "\n\n"
			i += 1
		return returned


	# Takes in a mapping of prepositions onto the types of FEs they occur with.
	# {'PP[in]': ['Area', 'Goal', etc.]}
	# Could potentially be generalized to other POS.
	def generate_preps_from_types(types):
		returned = ""
		for k,v in types.items():
			name = k.split("[")[1].replace("]", "")
			prep = "construction {}-Preposition\n".format(name)
			#prep += "construction {}-Preposition".format()
			supers = ["{}-Preposition".format(supertype) for supertype in v]
			parents = ", ".join(supers)
			prep += "    subcase of {}\n".format(parents)
			prep += "    form\n"
			prep += "      constraints\n"
			prep += "        self.f.orth <-- \"{}\"\n".format(name)
			returned += prep + "\n\n"
		return returned

	# Takes as input a list of ROLES, which it creates PP constructions based on.
	def generate_pps_from_roles(roles):
		returned = ""
		for role in roles:
			pp = ""
			pp += "construction {}-PP\n".format(role)
			pp += "	 subcase of PP\n"
			pp += "	 constructional\n"
			pp += "	   constituents\n"
			pp += "      prep: {}-Preposition".format(role)
			returned += pp + "\n\n"
		return returned

	def generate_general_preps_from_roles(roles):
		returned = ""
		for role in roles:
			pp = ""
			pp += "general construction {}-Preposition\n".format(role)
			pp += "	 subcase of Preposition\n"
			returned += pp + "\n\n"
		return returned


	# Could probably be generalized into other things than entities
	# Based on an input frame, builds tokens sub of {Frame}Type
	# Each token is an lu from frame and sub-frames
	# role_name should be the role you want to modify in parent frame
	def generate_tokens(entity_frame, fn, role_name, pos):
		lus = ECGUtilities.gather_lexicalUnits(entity_frame, fn)
		returned = ""
		#seen = []
		for lu in lus:
			lexeme = lu.name.split(".")[0]
			if lu.pos == pos:# and lexeme not in seen:
				returned += "{} :: {}Type :: self.m.{} <-- \"{}\"".format(lexeme, lu.frame_name, role_name, lexeme)
				if lu.semtype:
					# This will only work for entities, Events will likely need a different role name
					pass
					#returned += " :: self.m.Type_fn <-- @{}".format(lu.semtype.name)
				returned += "\n"
				#seen.append(lexeme)
		return returned


	def generate_types(parent_frame, fn, role_name, pos_type):
		returned = ""
		types = ECGUtilities.gather_types(parent_frame, fn)
		returned += ECGUtilities.format_type_cxn(parent_frame, pos_type, role_name)
		#for frame in parent_frame.children:
		#	returned += ECGUtilities.format_type_cxn(fn.get_frame(frame), "{}Type".format(parent_frame.name), role_name)
		for frame in types:
			returned += ECGUtilities.format_type_cxn(frame, "{}Type".format(frame.parents[0]), role_name)
		return returned


	def gather_types(parent_frame, fn):
		all_types = []
		for frame in parent_frame.children:
			actual = fn.get_frame(frame)
			all_types.append(actual)
			all_types += ECGUtilities.gather_types(actual, fn)
		return all_types


	def format_type_cxn(frame, parent_cxn, role_name):
		returned = "construction {}Type\n".format(frame.name)
		returned += "     subcase of {}\n".format(parent_cxn)
		returned += "     meaning: {}\n".format(frame.name)
		returned += "       constraints\n"
		returned += "         self.m.{} <-- \"*\"\n".format(role_name)
		returned += "\n"
		return returned




	def gather_lexicalUnits(parent, fn):
		lus = list(parent.lexicalUnits)

		for frame in parent.children:
			actual = fn.get_frame(frame)
			lus += ECGUtilities.gather_lexicalUnits(actual, fn)
		return lus




