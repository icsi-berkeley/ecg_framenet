import xml.etree.ElementTree as ET
from src.frames import Node


class SemType(Node):
	def __init__(self, name, abbrev, ID, definition, parents, children):
		Node.__init__(self, parents, children)
		self.name = name
		self.abbrev = abbrev
		self.ID = ID
		self.definition = definition


sems = {}
semtypes = []
replace_tag = "{http://framenet.icsi.berkeley.edu}"
s = ET.parse("fndata-1.6/semTypes.xml")
root = s.getroot()
for semtype in root.getchildren():
	name, abbrev, ID = semtype.attrib['name'], semtype.attrib['abbrev'], semtype.attrib['ID']
	parents, children = [], []
	for c2 in semtype.getchildren():
		tag = c2.tag.replace(replace_tag, "")
		#print(tag)
		if tag == "definition":
			definition = c2.text
			#print(c2.text)
		elif tag == "superType":
			superType = c2.attrib['superTypeName']
			parents.append(superType)
			#print(c2.attrib['superTypeName'])
	s = SemType(name, abbrev, ID, definition, parents, children)
	semtypes.append(s)
	sems[name] = s

for semtype in semtypes:
	parents = semtype.parents
	if len(semtype.parents)>1:
		print(semtype.parents)
	for parent in parents:
		sem = sems[parent]
		sem.children.append(semtype.name)


def format_semtype_to_ontology(semtype):
	sub = ""
	name = semtype.name.replace(" ", "_")
	if len(semtype.parents) > 0:
		sub = "sub {}".format(semtype.parents[0])
	return "(type {} {})".format(name, sub).lower()

def write_to_file(ontfile, semtypes):
	ontfile.write("DEFS:")
	ontfile.write("\n\n")
	for semtype in semtypes:
		formatted = format_semtype_to_ontology(semtype)
		ontfile.write(formatted)
		ontfile.write("\n\n")
	ontfile.write("INSTS:")


f = open("semtypes.ont", "w")


