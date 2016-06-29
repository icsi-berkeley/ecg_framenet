"""
author: <seantrott@icsi.berkeley.edu>

Constructs a "FrameNet" object, and builds frame element relations.

"""

from os import listdir
from os.path import isfile, join
from src.frames import *
from src.framenet import FrameNet, FrameTypeSystem
import xml.etree.ElementTree as ET
from src.annotation import Annotation


replace_tag = "{http://framenet.icsi.berkeley.edu}"

class FrameElementRelation(object):
    """ Defines a relation between two FEs. """
    def __init__(self, fe1, fe2, name=None, superFrame=None, subFrame =None):
        self.fe1 = fe1
        self.fe2 = fe2
        self.name = name
        self.superFrame = superFrame
        self.subFrame = subFrame

    def __eq__(self, other):
        return (self.fe1==other.fe1) and (self.fe2 == other.fe2)


    def __str__(self):
        return "{} ({}) <--> {} ({})".format(self.fe1, self.superFrame, self.fe2, self.subFrame)

    def __repr__(self):
        return self.__str__()


class FramenetBuilder(object):
    """ Takes in a path to the frames directory, relations file, and lu directory. Call read() to read in frames. 

    To obtain LU valence information, call build_lus_for_frame, passing in the name of the frame, e.g. "Motion", and a FrameNet object, "fn".
    """
    def __init__(self, frames_path, relations_file_path, lu_path):
        self.frames_path = frames_path
        self.relations_file_path = relations_file_path
        self.lu_path = lu_path
        self.frame_builder = FrameBuilder("{http://framenet.icsi.berkeley.edu}")
        self.replace_tag = "{http://framenet.icsi.berkeley.edu}"

    def read(self):
        """ Builds FrameNet object. """
        fn = FrameNet()
        files = listdir(self.frames_path)
        for frame_file in files:
            if frame_file.split(".")[-1] == "xml":
                new_name = frame_file.replace("._", "")
                path = self.frames_path + new_name
                frame = self.frame_builder.build_frame(path)
                fn.add_frame(frame)
        self.read_relations(fn)
        return fn


    def read_relations(self, fn):
        """ Reads in FE relations. Currently restricted to Inheritance, Using, and Causative_of."""
        tree = ET.parse(self.relations_file_path)
        root = tree.getroot()
        children = [i for i in root.getchildren() if i.attrib['name'] in ["Inheritance", "Using", "Causative_of", "Perspective_on"]]
        #for relation_type in children:
        #print(relation_type.attrib)
        for relation_type in children:
            name = relation_type.attrib['name']
            for relation in relation_type.getchildren():
                subFrame = relation.attrib['subFrameName']
                #print(subFrame)
                superFrame = relation.attrib['superFrameName']
                current_frame = fn.get_frame(subFrame)
                if name == "Causative_of":
                    current_frame = fn.get_frame(superFrame)
                for element_relation in relation.getchildren():
                    parent = element_relation.attrib['superFEName']
                    child = element_relation.attrib['subFEName']
                    fr = FrameElementRelation(parent, child, name, superFrame, subFrame)
                    #if parent != child or name=="Using":
                    current_frame.add_fe_relation(fr)


    def build_lus_for_frame(self, frame_name, fn):
        """ Takes in a frame_name string, e.g. "Motion", and a FrameNet object "fn" and builds valence patterns. """
        frame = fn.get_frame(frame_name)
        if len(frame.lexicalUnits) <= 0:
            pass
            #print("No lexical units for {}.".format(frame_name))
        elif type(frame.lexicalUnits[0]) == LexicalUnit:
            print("These lexical units have already been built.")
        else:
            new_units = []
            for unit in frame.lexicalUnits:
                if unit.status != "Problem":
                    ID = unit.ID 
                    path = self.lu_path + "lu{}.xml".format(ID)
                    lu = self.parse_lu_xml(path, unit)
                    lu = self.match_annotations_with_valences(lu)
                    new_units.append(lu)
                    frame.add_valences(lu.individual_valences)
                    frame.add_group_realizations(lu.valences)
                    frame.add_fe_realizations(lu.fe_realizations)
                    frame.add_annotations(lu.annotations)
            frame.lexicalUnits = new_units




    def match_annotations_with_valences(self, lu):
        """ Matches annotation IDs with corresponding valence data. """
        for realization in lu.valences:
            for pattern in realization.valencePatterns:
                for annotation in lu.annotations:
                    if annotation.ID in pattern.annotationID:
                        pattern.add_annotation(annotation)
                        realization.add_annotation(annotation)
                        #print(pattern.annotations)
        for fe_realization in lu.fe_realizations:
            for annotation in lu.annotations:
                if annotation.ID in fe_realization.annotationID:
                    fe_realization.add_annotation(annotation)
                    for valence in fe_realization.valences:
                        if annotation.ID in valence.annotationIDs:
                            raw_text = annotation.fe_mappings[valence.fe]
                            valence.add_annotation(annotation)
                            annotation.add_text_to_valence({raw_text: valence})
        return lu




        
    def parse_lu_xml(self, xml_path, original): #, fn):
        """ Takes as input the xml_path and a ShallowLU object, and builds a more complex LexicalUnit object with valence data. """
        replace_tag = "{http://framenet.icsi.berkeley.edu}"
        tree = ET.parse(xml_path)
        root = tree.getroot()
        annotations = []
        name, POS, frame, ID = root.attrib['name'], root.attrib['POS'], root.attrib['frame'], root.attrib['ID']
        for child in root.getchildren():
            tag = child.tag.replace(replace_tag, "")
            if tag == "lexeme":
                # TODO: Fix this
                lexeme = child.attrib['name']
            if tag == "valences":
                valence = child
                actual_valences, individual_valences, fe_realizations = self.build_realizations(frame, name, valence.getchildren())
            if tag == "definition":
                definition = child.text
            if tag == "subCorpus":
                #print(child.attrib)
                annotations += self.build_annotations(child, name, frame)
        valences = valence.getchildren()
        lu = LexicalUnit(name, POS, frame, ID, definition, lexeme, original.status)
        if annotations:
            lu.add_annotations(annotations)
        lu.individual_valences += individual_valences
        lu.fe_realizations += fe_realizations
        lu.add_valences(actual_valences)
        lu.set_semtype(original.semtype)
        return lu

    def build_annotations(self, subcorpus, lu, frame):
        """ Builds annotations from a subcorpus. """
        name = subcorpus.attrib['name']
        annotations = []
        for child in subcorpus.getchildren():
            if "metaphor" in child.attrib.keys():
                print(child.attrib)
            for c2 in child.getchildren():
                tag = c2.tag.replace(self.replace_tag, "")
                if tag == "text":
                    sentence = c2.text
                    #print(sentence)
                    #print("\n")
                elif tag == "annotationSet":
                    if len(c2.attrib.keys()) > 3:
                        print(c2.attrib)
                    status = c2.attrib['status']
                    ID = int(c2.attrib['ID'])
                    if status in ["MANUAL", "AUTO_EDITED"]:
                        new = Annotation(ID, status, sentence, name, lu, frame)
                        
                        for c3 in c2.getchildren():
                            tag = c3.tag.replace(self.replace_tag, "")

                            if c3.attrib['name'] == "FE":
                                for c4 in c3.getchildren(): 
                                    tag = c4.tag.replace(self.replace_tag, "")
                                    name = c4.attrib['name'] #.encode('utf-8') # Encode it, otherwise it breaks on Windows
                                    if 'start' and 'end' in c4.attrib:
                                        start, end = int(c4.attrib['start']), int(c4.attrib['end'])
                                        raw_text = new.sentence[start:end+1].encode('utf-8').decode('utf-8')
                                        new.add_fe_mapping(name, raw_text)
                                        new.set_spans(name, (start, end))
                                    else:
                                        new.add_fe_mapping(name, c4.attrib['itype'])
                            elif c3.attrib['name'] == "Sent":
                                for c4 in c3.getchildren():
                                    tag = c4.tag.replace(self.replace_tag, "")
                                    if c4.attrib['name'] == "Metaphor":
                                        new.set_metaphor()
                            elif c3.attrib['name'] == "Target":
                                for c4 in c3.getchildren():
                                    if c4.attrib['name'] == "Target":
                                        start, end = int(c4.attrib['start']), int(c4.attrib['end'])
                                        new.set_target(new.sentence[start:end+1])



                        annotations.append(new)
            #print(child.tag)
        return annotations 

    def build_realizations(self, frame, name, valences):
        """ Builds FERealizations and FEGroupRealizations. """
        actual_valences = []
        individual_valences = []
        fe_realizations = []
        for v in valences:
            valence_tag = v.tag.replace(self.replace_tag, "")
            if valence_tag == "FERealization":
                total = int(v.attrib['total'])
                fe_realization = FERealization(frame, total, name)
                for realization in v.getchildren():
                    tag = realization.tag.replace(self.replace_tag, "")
                    if tag == "FE":
                        fe_realization.set_fe(realization.attrib['name'])
                    if tag == "pattern":
                        subtotal = int(realization.attrib['total'])
                        for valence in realization.getchildren():

                            if valence.tag.replace(self.replace_tag, "") == "valenceUnit":

                                individual_valence = Valence(frame, valence.attrib['GF'], valence.attrib['PT'], valence.attrib['FE'], name, total=subtotal)
                                #if name == "move.v":
                                #    print(individual_valence)
                                fe_realization.add_valence(individual_valence)
                                individual_valences.append(individual_valence)
                            elif valence.tag.replace(self.replace_tag, "") == "annoSet":
                                fe_realization.set_ID(int(valence.attrib['ID']))
                                individual_valence.add_annotationID(int(valence.attrib['ID']))

                fe_realizations.append(fe_realization)
            elif valence_tag == "FEGroupRealization":
                total = int(v.attrib['total'])
                group_realization = FEGroupRealization(frame, total, name)
                for realization in v.getchildren():
                    tag = realization.tag.replace(self.replace_tag, "")
                    if tag == "pattern":
                        subtotal = int(realization.attrib['total'])
                        valencePattern = ValencePattern(frame, subtotal, name)
                        valenceUnits = realization.getchildren()
                        for vUnit in valenceUnits:
                            if vUnit.tag.replace(self.replace_tag, "") == "valenceUnit":
                                new_valence = Valence(frame, vUnit.attrib['GF'], vUnit.attrib['PT'], vUnit.attrib['FE'], name)
                                if new_valence in individual_valences:
                                    new_valence.total = individual_valences[individual_valences.index(new_valence)].total
                                valencePattern.add_valenceUnit(new_valence)
                                group_realization.add_element(vUnit.attrib['FE'])
                            elif vUnit.tag.replace(self.replace_tag, "") == "annoSet":
                                #print(int(vUnit.attrib['ID']))
                                valencePattern.set_ID(int(vUnit.attrib['ID']))
                        group_realization.add_valencePattern(valencePattern)
                actual_valences.append(group_realization)
        return actual_valences, individual_valences, fe_realizations


if __name__ == "__main__":
    fnb = FramenetBuilder("fndata-1.6/frame/", "fndata-1.6/frRelation.xml", "fndata-1.6/lu/")
    fn = fnb.read() #fnb.read()
    # fnb.build_relations()


