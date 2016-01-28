"""
@author: <seantrott@icsi.berkeley.edu>

This file reads in the semtypes from semtypes.xml. Hypothetically, these could be integrated into the other classes. 
The only distinction from the simpler SemType object is that these are Nodes, so they include parent/children information.

This hasn't been fully integrated into the rest of the module, but can be used to generate an ECG ontology of semtypes.

"""

import xml.etree.ElementTree as ET
from src.frames import Node


class SemType(Node):
	""" Contains name, abbreviation, ID, definitions, parents, and children. """
	def __init__(self, name, abbrev, ID, definition, parents, children):
		Node.__init__(self, parents, children)
		self.name = name
		self.abbrev = abbrev
		self.ID = ID
		self.definition = definition


def read_semtypes(path="fndata-1.6/semTypes.xml"):
	""" Reads in semtypes.xml from given xml path and produces a list of semtypes. """
	sems = {}
	semtypes = []
	replace_tag = "{http://framenet.icsi.berkeley.edu}"
	s = ET.parse(path)
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
	return semtypes


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


#f = open("semtypes.ont", "w")


