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
        return "{} ({}) <--> {} ({})".format(self.fe1, self.superFrame, self.fe2, self.subFrame)

    def __repr__(self):
        return self.__str__()


class FramenetBuilder(object):
    def __init__(self, frames_path, relations_file_path, lu_path):
        self.frames_path = frames_path
        self.relations_file_path = relations_file_path
        self.lu_path = lu_path
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
        children = [i for i in root.getchildren() if i.attrib['name'] in ["Inheritance", "Using", "Causative_of"]]
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
        frame = fn.get_frame(frame_name)
        if type(frame.lexicalUnits[0]) == LexicalUnit:
            print("These lexical units have already been built.")
        else:
            new_units = []
            for unit in frame.lexicalUnits:
                if unit.status != "Problem":
                    ID = unit.ID 
                    path = self.lu_path + "lu{}.xml".format(ID)
                    new_units.append(self.parse_lu_xml(path, unit))
            frame.lexicalUnits = new_units



        
    def parse_lu_xml(self, xml_path, original): #, fn):
        replace_tag = "{http://framenet.icsi.berkeley.edu}"
        tree = ET.parse(xml_path)
        root = tree.getroot()
        name, POS, frame, ID = root.attrib['name'], root.attrib['POS'], root.attrib['frame'], root.attrib['ID']
        for child in root.getchildren():
            tag = child.tag.replace(replace_tag, "")
            if tag == "valences":
                valence = child
                break
            elif tag == "definition":
                definition = child.text
        valences = valence.getchildren()
        actual_valences = []
        for v in valences:
            valence_tag = v.tag.replace(replace_tag, "")
            if valence_tag == "FEGroupRealization":
                total = int(v.attrib['total'])
                group_realization = FEGroupRealization(frame, total, name)
                for realization in v.getchildren():
                    tag = realization.tag.replace(replace_tag, "")
                    if tag == "pattern":
                        subtotal = int(realization.attrib['total'])
                        valencePattern = ValencePattern(frame, subtotal, name)
                        valenceUnits = realization.getchildren()
                    
                        for vUnit in valenceUnits:
                            if vUnit.tag.replace(replace_tag, "") == "valenceUnit":
                                new_valence = Valence(frame, vUnit.attrib['GF'], vUnit.attrib['PT'], vUnit.attrib['FE'])
                                valencePattern.add_valenceUnit(new_valence)
                        group_realization.add_valencePattern(valencePattern)
                        #print(frame)
                        #print(ID)
                        #print(vUnit.attrib)
                actual_valences.append(group_realization)
        lu = LexicalUnit(name, POS, frame, ID, definition)
        lu.add_valences(actual_valences)
        lu.set_semtype(original.semtype)
        return lu



if __name__ == "__main__":
    fnb = FramenetBuilder("fndata-1.6/frame/", "fndata-1.6/frRelation.xml", "fndata-1.6/lu/")
    fn = fnb.read() #fnb.read()
    # fnb.build_relations()


