from src.frames import *


class TypeSystemException(Exception):
	def __init__(self, message):
		self.message = message

class FrameTypeSystem(object):
	def __init__(self, fn):
		self.roots = []
		self.build(fn)

	def build(self, fn):
		for frame in fn.frames:
			root_frame = self.get_root(frame, fn)
			#self.roots.append(self.get_root(frame, fn))
			if not root_frame in self.roots:
				self.roots.append(root_frame)

	def get_root(self, frame, fn):
		if len(frame.parents) > 0:
			new = fn.get_frame(frame.parents[0])
			return self.get_root(new, fn)
		else:
			return frame

	def get_siblings(self, frame, fn):
		parents = frame.parents
		siblings = []
		for i in parents:
			parent = fn.get_frame(i)
			siblings += parent.children
		return siblings

	def highest_common_supertype(self, f1, f2, fn):
		if f1 == f2:
			return f1
		elif fn.subtype(f1, f2):
			return f2
		elif fn.subtype(f2, f1):
			return f1
		elif fn.get_root(f1) != fn.get_root(f2):
			raise TypeSystemException("No shared supertype found...different roots.")
		else:
			f1_parents = f1.parents 
			f2_parents = f2.parents
			for i in f1_parents:
				frame = fn.get_frame(i)
				if i in f2_parents:
					return i
				return self.highest_common_supertype(frame, f2, fn)
			for i in f2_parents:
				frame = fn.get_frame(i)
				if i in f1_parents:
					return i
				return self.highest_common_supertype(frame, f1, fn)




class FrameNet(object):
	def __init__(self):
		self.name_to_frames = {}
		self.hierarchy = {}
		self.frames = []
		self.lexemes_to_frames = {}
		self.typesystem = None
		self.definitions_to_frames = {}
		self.xml_definitions_to_frames = {}
		self.ID_to_frames = {}
		self.untagged_lus = []

	def highest_common_supertype(self, f1, f2):
		try:
			return self.typesystem.highest_common_supertype(f1, f2, self)
		except TypeSystemException as e:
			print(e.message)
			return None

	def subtype_s(self, f1_s, f2_s):
		f1, f2 = self.get_frame(f1_s), self.get_frame(f2_s)
		return self.subtype(f1, f2)


	def subtype(self, f1, f2):
		self.get_root(f1) != self.get_root(f2)
		if f1.name in f2.children:
			return True
		#elif self.get_root(f1) != self.get_root(f2):
		#	return False
		else:
			for child in f2.children:
				child_frame = self.get_frame(child)
				if self.subtype(f1, child_frame):
					return True
			return False

	def get_frames_from_lu_set(self, lu_set):
		"""Takes in a set of lus and returns a dictionary of each lu mapped onto frames."""
		final = dict()
		for lu in lu_set:
			final[lu] = self.get_frames_from_lu(lu)
		return final

	def get_frames_from_lu(self, lu):
		if lu in self.lexemes_to_frames:
			return self.lexemes_to_frames[lu]
		else:
			raise Exception("LU {} not found.".format(lu))

	def get_root(self, frame):
		return self.typesystem.get_root(frame, self)

	def get_siblings(self, frame):
		return self.typesystem.get_siblings(frame, self)

	def get_frame(self, name):
		if name in self.name_to_frames:
			return self.name_to_frames[name]
		#raise Exception("Frame {} does not exist.".format(name))

	def get_frame_from_id(self, ID):
		return self.ID_to_frames[ID]

	def add_frame(self, frame):
		self.name_to_frames[frame.name] = frame
		self.frames.append(frame)
		for lu in frame.lexicalUnits:
			#lex = lu.name.split(".")[0]
			#TODO: How to represent?
			untag = lu.name.split(".")[0]
			self.untagged_lus.append(untag)
			lex = lu.name
			if lex not in self.lexemes_to_frames:
				self.lexemes_to_frames[lex] = []
			self.lexemes_to_frames[lex].append(frame)
			self.definitions_to_frames[frame.definition] = frame
			self.xml_definitions_to_frames[frame.xml_definition] = frame
			self.ID_to_frames[int(frame.ID)] = frame
		# hierarchy?

	def add_element(self, f1, f2):
		for element in f1.elements:
			if element not in f2.elements:
				f2.elements.append(element)

	def build_relations(self):
		for frame in self.frames:
			for relation in frame.relations:
				new_frames = []
				for fr in relation.related_frames:
					related = self.get_frame(fr)
					if related:
						new_frames.append(related)
						if relation.relation_type == "Inherits from":
							self.add_element(related, frame)
				relation.related_frames = new_frames

			new_elements = []
			for element in frame.elements:
				new_element = self.get_frame(element.name)
				element.frame = new_element
				
	def build_typesystem(self):
		self.typesystem = FrameTypeSystem(self)



	




