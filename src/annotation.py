""" 
@author: <seantrott@icsi.berkeley.edu>

Simple class to define an Annotated sentence.
"""


class Annotation(object):
	""" Contains ID, status (Manual, etc.), the sentence itself, and the subCorpus source. """
	def __init__(self, ID, status, sentence, subCorpus, lu, frame):
		self.sentence = sentence
		self.ID = ID
		self.status = status
		self.subCorpus = subCorpus
		self.fe_mappings = dict()
		self.text_to_valence = dict()
		self.lu = lu
		self.frame = frame

	def add_fe_mapping(self, name, text):
		""" Takes in a namne and text and puts it into the form {'FE': __text__}. """
		#if text not in self.valence_mappings:
		#	self.valence_mappings['text'] = dict()
		#self.add_valence_mapping['text'].update(value)
		mapping = {name: text}
		if name in self.fe_mappings:
			mapping[name] = "{} {}".format(self.fe_mappings[name], mapping[name])
		self.fe_mappings.update(mapping)

	def add_text_to_valence(self, ttv):
		self.text_to_valence.update(ttv)


	def __repr__(self):
		return self.sentence + "\n"