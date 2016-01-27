class ShallowLU(object):
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
	def __init__(self, name, pos, frame_name, ID, definition, lexeme):
		self.pos = pos
		self.name = name
		self.frame_name = frame_name
		self.ID = ID
		self.frame = frame_name
		self.definition = definition
		self.valences = [] # This could be a dictionary with frequency information
		self.semtype = None
		self.fe_realizations = []
		self.individual_valences =[]
		self.lexeme = lexeme
		self.annotations = []

	def add_valence(self, valence):
		self.valences.append(valence)

	def add_valences(self, valences):
		self.valences += valences

	def add_annotations(self, annotations):
		self.annotations += annotations

	def set_semtype(self, semtype):
		self.semtype = semtype

	def __repr__(self):
		return self.name

class Valence(object):
	def __init__(self, frame, gf, pt, fe, total="N/A"):
		self.frame = frame
		self.gf = gf
		self.pt = pt
		self.fe = fe
		self.total = total
		self.annotations = []

	def add_annotation(self, annotation):
		if annotation not in self.annotations:
			self.annotations.append(annotation)

	def __repr__(self):
		return """Frame: {}, GF: {}, PT: {}, FE: {}, total: {}\n""".format(self.frame, self.gf, self.pt, self.fe, self.total)

	def __eq__(self, other):
		return self.gf == other.gf and self.pt == other.pt and self.fe==other.fe #and (self.frame == other.frame)

class ValencePattern(object):
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

	def add_valenceUnit(self, valence):
		self.valenceUnits.append(valence)

	def add_valenceUnits(self, units):
		self.valenceUnits += units

	def __eq__(self, other):
		return (self.valenceUnits == other.valenceUnits)# and self.total == other.total

	def __repr__(self):
		return "Total: {}\nValences:{}\nLU: {}".format(self.total, str(self.valenceUnits), self.lu)

class FERealization(object):
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
		self.elements.append(element)

	def __repr__(self):
		return "Total: {} \nValence Patterns: {}".format(self.total, str(self.valencePatterns))



