"""
@author: seantrott@icsi.berkeley.edu

Transform FN data into ECG constructions.

"""

import xml.etree.ElementTree as ET
from src.builder import *
from os import listdir

#fnb = FramenetBuilder("fndata-1.6/frame/", "fndata-1.6/frRelation.xml")
#fn = fnb.read() #fnb.read()

path = "fndata-1.6/lu/"

class LexicalUnitConstruction(LexicalUnit):
	def __init__(self, name, pos, frame, ID, definition):
		LexicalUnit.__init__(self, name, pos, frame.name, ID)
		self.frame = frame
		self.definition = definition
		self.ID = ID
		self.valences = [] # This could be a dictionary with frequency information

	def add_valence(self, valence):
		self.valences.append(valence)

	def add_valences(self, valences):
		self.valences += valences

class Valence(object):
	def __init__(self, frame, gf, pt, fe):
		self.frame = frame
		self.gf = gf
		self.pt = pt
		self.fe = fe

	def __repr__(self):
		return """Frame: {}, GF: {}, PT: {}, FE: {}\n""".format(self.frame.name, self.gf, self.pt, self.fe)


class FEGroupRealization(object):
	def __init__(self, frame, total):
		self.frame = frame
		self.total = total
		self.valenceUnits = {}

	def add_valenceUnit(self, valence):
		self.valenceUnits[valence.fe] = valence

	def __repr__(self):
		return str(self.valenceUnits)


# GF: Grammatical function
# PT: Phrase Type
# FE: Frame Element
def parse_lu_xml(xml_path): #, fn):
	replace_tag = "{http://framenet.icsi.berkeley.edu}"
	tree = ET.parse(xml_path)
	root = tree.getroot()
	name, POS, frame, ID = root.attrib['name'], root.attrib['POS'], root.attrib['frame'], root.attrib['ID']
	for child in root.getchildren():
		tag = child.tag.replace(replace_tag, "")
		if tag == "valences":
			valence = child
			break
		elif tag == "definition":
			definition = child.text
	valences = valence.getchildren()
	actual_valences = []
	for v in valences:
		valence_tag = v.tag.replace(replace_tag, "")
		if valence_tag == "FEGroupRealization":
			total = v.attrib['total']
			for realization in v.getchildren():
				tag = realization.tag.replace(replace_tag, "")
				valenceUnits = realization.getchildren()
				group_realization = FEGroupRealization(frame, total)
				for vUnit in valenceUnits:
					if vUnit.tag.replace(replace_tag, "") == "valenceUnit":
						new_valence = Valence(frame, vUnit.attrib['GF'], vUnit.attrib['PT'], vUnit.attrib['FE'])
						group_realization.add_valenceUnit(new_valence)
					#print(frame)
					#print(ID)
					#print(vUnit.attrib)
			actual_valences.append(group_realization)
	lu = LexicalUnitConstruction(name, POS, frame, ID, definition)
	lu.add_valences(actual_valences)
	return lu


def build_lexicalUnits(path, fn):
	lexicalUnits = {}
	files = listdir(path)
	total = len(files)
	i = 0
	for f in files:
		if i > 200:
			break
		if f.split(".")[-1] == "xml":
			#print("Parsing {}".format(f))
			fpath = path + f
			lu = parse_lu_xml(fpath, fn)
			if lu.name not in lexicalUnits:
				lexicalUnits[lu.name] = []
			lexicalUnits[lu.name].append(lu)
			i += 1
	return lexicalUnits









