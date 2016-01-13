"""
author: <seantrott@icsi.berkeley.edu>

Constructs a "FrameNet" object, and builds frame element relations.

"""

from os import listdir
from os.path import isfile, join
from src.frames import *
from src.framenet import FrameNet, FrameTypeSystem
import xml.etree.ElementTree as ET

replace_tag = "{http://framenet.icsi.berkeley.edu}"

class FrameElementRelation(object):
	def __init__(self, fe1, fe2, name=None, superFrame=None, subFrame =None):
		self.fe1 = fe1
		self.fe2 = fe2
		self.name = name
		self.superFrame = superFrame
		self.subFrame = subFrame

	def __eq__(self, other):
		return (self.fe1==other.fe1) and (self.fe2 == other.fe2)


	def __str__(self):
		return "{} <--> {}".format(self.fe1, self.fe2)

	def __repr__(self):
		return self.__str__()


class FramenetBuilder(object):
	def __init__(self, frames_path, relations_file_path):
		self.frames_path = frames_path
		self.relations_file_path = relations_file_path
		self.frame_builder = FrameBuilder("{http://framenet.icsi.berkeley.edu}")

	def read(self):
		fn = FrameNet()
		files = listdir(self.frames_path)
		for frame_file in files:
			if frame_file.split(".")[-1] == "xml":
				path = self.frames_path + frame_file
				frame = self.frame_builder.build_frame(path)
				fn.add_frame(frame)


		self.read_relations(fn)

		return fn


	def read_relations(self, fn):
		tree = ET.parse(self.relations_file_path)
		root = tree.getroot()
		children = [i for i in root.getchildren() if i.attrib['name'] in ["Inheritance", "Using"]]
		#for relation_type in children:
		#print(relation_type.attrib)
		for relation_type in children:
			name = relation_type.attrib['name']
			for relation in relation_type.getchildren():
				subFrame = relation.attrib['subFrameName']
				#print(subFrame)
				superFrame = relation.attrib['superFrameName']
				current_frame = fn.get_frame(subFrame)
				for element_relation in relation.getchildren():
					parent = element_relation.attrib['superFEName']
					child = element_relation.attrib['subFEName']
					fr = FrameElementRelation(parent, child, name, superFrame, subFrame)
					#if parent != child or name=="Using":
					current_frame.add_fe_relation(fr)

		




if __name__ == "__main__":
	fnb = FramenetBuilder("fndata-1.6/frame/", "fndata-1.6/frRelation.xml")
	fn = fnb.read() #fnb.read()
	# fnb.build_relations()


