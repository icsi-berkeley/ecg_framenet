from frames import *
from builder import *
from framenet import *

from nltk.corpus import wordnet as wn


from collections import OrderedDict


fnb = FramenetBuilder("fndata-1.6/frame/", "fndata-1.6/frRelation.xml")
fn = fnb.read() #fnb.read()



fn.build_relations()

#fts = FrameTypeSystem()
#fts.build(fn)

fn.build_typesystem()

def map_frame_elements(frame, tokens):
	if frame:
		print(frame + "\n")
		for element in frame.elements:
			if element.frame:
				print(element.frame)
				print(element.frame.lexicalUnits)
		#print(tokens)



def print_simple_analysis(analysis):
	for k, frame in analysis.items():
		if frame:
			print("{}: {}".format(k, frame.name))
		else:
			print(k)


def simple_analysis(msg):
	tokens = msg.split(" ")
	lemmas = [wn.morphy(token) if wn.morphy(token) else token for token in tokens]
	analysis = OrderedDict()
	for i in lemmas:
		if i in fn.lexemes_to_frames:
			analysis[i] = fn.lexemes_to_frames[i]
		else:
			analysis[i] = None
	for k, frame in analysis.items():
		print("\n")
		map_frame_elements(frame, analysis.keys())
	return analysis
	


def prompt():
	while True:
		msg = input("> ")
		if msg == "q":
			break
			quit()
		analysis = simple_analysis(msg)
		print_simple_analysis(analysis)




#if __name__ == "__main__":
#	prompt()