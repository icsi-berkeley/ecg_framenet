""" 
@author: <seantrott@icsi.berkeley.edu>

Simple class to define an Annotated sentence.
"""


class Annotation(object):
	""" Contains ID, status (Manual, etc.), the sentence itself, and the subCorpus source. """
	def __init__(self, ID, status, sentence, subCorpus):
		self.sentence = sentence
		self.ID = ID
		self.status = status
		self.subCorpus = subCorpus


	def __repr__(self):
		return self.sentence + "\n"