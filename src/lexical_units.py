""" 
@author: <seantrott@icsi.berkeley.edu>

This module defines a set of classes related to lexical units on FrameNet. 

"""

class ShallowLU(object):
	""" Just contains LU information from frame xml file (name, pos, etc.), without valence patterns. """
	def __init__(self, name, pos, frame_name, ID, status):
		self.name = name
		self.pos = pos
		self.frame_name = frame_name
		self.ID = ID
		self.status = status
		#self.definition = definition
		self.semtype = None

	def set_semtype(self, s):
		self.semtype = s

	def __repr__(self):
		return self.name

class LexicalUnit(object):
	""" Contains ShallowLU info, as well as valence pattern information:

	.valences: list of FEGroupRealization objects
	.fe_realizations: list of FERealization objects
	.individual_valences: list of Valence objects
	.annotations: list of annotated sentences for this LU.
	"""
	def __init__(self, name, pos, frame_name, ID, definition, lexeme):
		self.pos = pos
		self.name = name
		self.frame_name = frame_name
		self.ID = ID
		self.frame = frame_name
		self.definition = definition
		self.valences = [] 
		self.semtype = None
		self.fe_realizations = []
		self.individual_valences =[]
		self.lexeme = lexeme
		self.annotations = []

	def add_valence(self, valence):
		self.valences.append(valence)

	def add_valences(self, valences):
		self.valences += valences

	def get_fe_realization(self, fe):
		""" Takes in string FE ("Theme"), returns the fe_realization object matching. """
		for i in self.fe_realizations:
			if i.fe == fe:
				print(i.fe)

	def add_annotations(self, annotations):
		self.annotations += annotations

	def set_semtype(self, semtype):
		self.semtype = semtype

	def __repr__(self):
		return self.name

class Valence(object):
	""" Basic Valence object. Contains frame name, grammatical function (gf), phrase type (pt), and frame element (fe).
	Total is by default set to None, but a lexical unit's individual_valences and fe_realizations will have totals. 

	Also contains a list of associated annotations. """
	def __init__(self, frame, gf, pt, fe, lexeme, total=None):
		self.frame = frame
		self.gf = gf
		self.pt = pt
		self.fe = fe
		self.total = total
		self.annotations = []
		self.annotationIDs = []
		self.lexeme =lexeme

	def add_annotationID(self, ID):
		self.annotationIDs.append(ID)

	def add_annotation(self, annotation):
		if annotation not in self.annotations:
			self.annotations.append(annotation)

	def add_annotations(self, annotations):
		for annotation in annotations:
			self.add_annotation(annotation)

	def __repr__(self):
		return """Frame: {}, GF: {}, PT: {}, FE: {}, total: {}\n""".format(self.frame, self.gf, self.pt, self.fe, self.total)

	def __eq__(self, other):
		return self.gf == other.gf and self.pt == other.pt and self.fe==other.fe #and (self.frame == other.frame)


	def __hash__(self):
		return hash((self.gf, self.pt, self.fe))

class ValencePattern(object):
	""" Contains a list of valenceUnits (Valence objects), as well as associated annotations. This corresponds to a given valence pattern for an FEGroupRealization."""
	def __init__(self, frame, total, lu):
		self.frame = frame 
		self.total = total 
		self.valenceUnits = []
		self.lu = lu
		self.annotationID = []
		self.annotations = []

	def set_ID(self, ID):
		self.annotationID.append(ID)

	def add_annotation(self, annotation):
		if annotation not in self.annotations:
			self.annotations.append(annotation)

	def add_annotations(self, annotations):
		for annotation in annotations:
			self.add_annotation(annotation)
	def add_valenceUnit(self, valence):
		self.valenceUnits.append(valence)

	def add_valenceUnits(self, units):
		self.valenceUnits += units

	def __eq__(self, other):
		return (self.valenceUnits == other.valenceUnits)# and self.total == other.total

	def __repr__(self):
		return "Total: {}\nValences:{}\nLU: {}".format(self.total, str(self.valenceUnits), self.lu)

class FERealization(object):
	""" Contains a list of valences and associated annotations. These are valences for a Frame Element realization. """
	def __init__(self, frame, total, lexeme):
		self.frame = frame
		self.total = total
		self.lexeme = lexeme
		self.valences =[]
		self.fe =None
		self.annotationID = []
		self.annotations = []

	def add_annotation(self, annotation):
		if annotation not in self.annotations:
			self.annotations.append(annotation)

	def set_ID(self, ID):
		self.annotationID.append(ID)

	def add_valence(self, valence):
		self.valences.append(valence)

	def set_fe(self, fe):
		self.fe = fe

	def __repr__(self):
		return "Total: {}, lexeme: {}, fe: {}\n".format(self.total, self.lexeme, self.fe)


class FEGroupRealization(object):
	""" Contains valence patterns for an FE group realization (e.g., "Theme" and "Path" in the Motion frame). """
	def __init__(self, frame, total, lexeme):
		self.frame = frame
		self.total = total
		self.valencePatterns = []
		self.elements = []
		self.lu = lexeme
		

	def add_valencePattern(self, valencePattern):
		self.valencePatterns.append(valencePattern)
		#self.valenceUnits[valence.fe] = valence

	def add_element(self, element):
		if element not in self.elements:
			self.elements.append(element)

	def __repr__(self):
		return "Total: {} \nValence Patterns: {}".format(self.total, str(self.valencePatterns))



