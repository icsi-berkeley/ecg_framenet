from src.builder import *

fnb = FramenetBuilder("fndata-1.6/frame/", "fndata-1.6/frRelation.xml")
fn = fnb.read() #fnb.read()

schema_file = open("generated/schemas.grm", "w")


def format_schema(frame):
	semtype_to_frame = {'Physical_object': "Entity"}
	forbidden = ['construction', 'Construction',
				'Situation', 'situation', 'map', "Map",
				"Form", "form",
				"Feature", "feature",
				"Constraints", "constraints",
				"Type", "type",
				"Constituents", "constituents",
				"Meaning", "meaning"]
	name = frame.name
	uses = []
	for relation in frame.relations:
		if relation.relation_type == "Uses":
			uses = [r for r in relation.related_frames]
			#print(relation.related_frames)
	parents = None
	if len(frame.parents) > 0:
		parents = ", ".join(frame.parents)
	elements = []
	for i in frame.elements:
		tc = ""
		if i.semtype != None and i.semtype.name in semtype_to_frame:
			tc = ": {}".format(semtype_to_frame[i.semtype.name])
		if not i.name in forbidden:
			elements.append(i.name + tc)
		else:
			elements.append(i.name + "_fn" + tc)
	#elements = [i.name if not i.name in forbidden else "" for i in frame.elements]
	roles = " \n ".join(elements)
	final = "schema {} \n".format(name)
	if parents:
		final += "    subcase of {} \n".format(parents) 
	for use in uses:
		final += "    evokes {} as {} \n".format(use, use.lower())
	final += "    roles \n"
	for role in elements:
		final += "       {} \n".format(role)

	if len(frame.fe_relations) > 0:
		final += "     constraints \n"
	for c in frame.fe_relations:
		f1, f2 = c.fe1, c.fe2
		if f1 in forbidden:
			f1 = f1 + "_fn"
		if f2 in forbidden:
			f2 = f2 + "_fn"
		if c.name == "Using":
			f1 = c.superFrame.lower() + "." + f1
		r = "       {} <--> {} \n".format(f1, f2)
		final += r
	return final




frame = fn.frames[0]
#schema_file.write(format_schema(frame))

s = format_schema(frame)

"""
already_extant = ['Motion', "Perception", "Process",
  					"Artifact", "Vehicle",
  					"Entity", "Possession",
  					"Control"]
"""

already_extant = []

for frame in fn.frames:
	if not frame.name in already_extant:
		schema_file.write(format_schema(frame))
		schema_file.write("\n\n")
schema_file.close()
