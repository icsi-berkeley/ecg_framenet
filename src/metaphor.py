from builder import *

fnb = FramenetBuilder("fndata-1.6/frame/", "fndata-1.6/frRelation.xml")
fn = fnb.read() #fnb.read()
fn.build_typesystem()
fn.build_relations()

s1 = fn.get_frame("Judicial_body")
s2 = fn.get_frame("Store")


class Mapping(object):
	def __init__(self, source, target):
		self.source = source
		self.target = target

class Metaphor(object):
	def __init__(self, source, target, shared_frame):
		self.source = source
		self.target = target
		self.shared_frame= shared_frame
		self.name = "{} as {}".format(target.name, source.name)
		#self.mappings = []

	"""
	def build_mappings(self):
		for element in self.shared_frame.elements:
			source = self.source.elements[self.source.elements.index(element)]
			target = self.target.elements[self.target.elements.index(element)]
			mapping = Mapping(source, target)
			self.mappings.append(mapping)
	"""

def suggest_metaphor(f1, f2, fn):
	supertype = fn.highest_common_supertype(f1, f2)
	if supertype:
		if isinstance(supertype, str):
			supertype = fn.get_frame(supertype)
		meta = Metaphor(f1, f2, supertype)
		return meta



		

s3 = fn.get_frame("Abandonment")
s4 = fn.get_frame("Event")