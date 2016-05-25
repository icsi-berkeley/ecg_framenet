"""
Classes for constructing and formatting ECG constructions from valence patterns.

Question: What to do with subcase of Transitive_action, etc.? 

"""

class HypothesizedConstruction(object):
	def __init__(self, frame, parent="ArgumentStructure", n=1):
		self.frame = frame
		self.parent = parent
		self.constituents = []
		self.n = n
		self.annotations = []

	def add_constituent(self, constituent):
		self.constituents.append(constituent)

	def add_annotations(self, annotations):
		self.annotations += annotations

	def format_to_cxn(self):
		annotations = "/* {} */\n".format(self.annotations)
		final = annotations 
		final += "construction {}_pattern_{}\n".format(self.frame, str(self.n))
		final += "     subcase of {}\n".format(self.parent)
		final += "     constructional\n"
		final += "      constituents\n"
		final += "        v: Verb\n" # HACK
		for constituent in self.constituents:
			if constituent.gf != "Ext":
				final += "        {}\n".format(constituent.format_constituent())
		final += "      meaning: {}\n".format(self.frame)
		final += "       constraints\n"
		final += "         self.m <--> v.m\n"  # HACK
		for constituent in self.constituents:
			final += "         {}\n".format(constituent.format_constraint())
		return final


class Constituent(object):
	""" Represnts an ECG construction constituent. Contains: name (POS), frame element (role binding), 
	and probabilities (omission, extraposition). P should be of the form [p1, p2]. """
	def __init__(self, pt, fe, gf, probabilities):
		self.pt = pt
		self.fe = fe
		self.gf = gf
		self.probabilities = probabilities 

	def format_constituent(self):
		return "{}: {} [{}, {}]".format(self.pt.lower(), self.pt, self.probabilities[0], self.probabilities[1])

	def format_constraint(self):
		if self.gf == "Ext":
			return "ed.profiledParticipant <--> self.m.{}".format(self.fe)
		return "self.m.{} <--> {}.m".format(self.fe, self.pt.lower())


