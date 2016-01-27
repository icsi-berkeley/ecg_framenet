class Annotation(object):
	def __init__(self, ID, status, sentence, subCorpus):
		self.sentence = sentence
		self.ID = ID
		self.status = status
		self.subCorpus = subCorpus


	def __repr__(self):
		return self.sentence