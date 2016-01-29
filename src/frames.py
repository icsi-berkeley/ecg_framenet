""" 
@author: <seantrott@icsi.berkeley.edu>

This module defines the Frame object, as well as the associated SemType class, FrameElement class, and FrameBuilder.

Other associated Frame classes are defined in frame_relation and lexical_units.
"""

import xml.etree.ElementTree as ET
#from src.constructions import *
from src.frame_relation import FrameRelation
from src.lexical_units import *


class Node(object):
    """ Simple Node object, has parents and children. """
    def __init__(self, parents=[], children=[]):
        self.parents= parents
        self.children = children


class Frame(Node):
    """ Represents a single FrameNet frame. Includes:
    -Frame Name
    -Frame elements 
    -Frame lexical units 
    -Frame relations 
    -Frame parents 
    -Frame children 
    -Frame definition (text and XML)
    -Frame ID
    """
    def __init__(self, name, elements, lexicalUnits, relations, parents, children, definition, xml_def, ID):
        Node.__init__(self, parents=parents, children=children)
        self.name = name
        self.elements = elements
        self.lexicalUnits = lexicalUnits
        self.relations = relations
        self.fe_relations = []
        self.xml_definition = xml_def
        self.definition = definition
        self.ID = ID
        self.individual_valences = []
        self.group_realizations = []

    def add_valences(self, valences):
        self.individual_valences += valences

    def add_group_realizations(self, res):
        self.group_realizations += res
        
    def compatible_elements(self, e1, e2):
        return (e1.name not in e2.excludes) and (e2.name not in e1.excludes) and (e1.name != e2.name)

    def get_element(self, name):
        for element in self.elements:
            if element.name == name:
                return element

    def get_lu(self, lu_name):
        for lu in self.lexicalUnits:
            if lu.name == lu_name:
                return lu


    def add_fe_relation(self, relation):
        self.fe_relations.append(relation)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        elements = self.format_elements()
        formatted = "{} \n {}".format(self.name, elements)
        return self.name + " (Frame)"

    def __repr__(self):
        #elements = self.format_elements()
        formatted = """Name: {}
                    \nFrame Relations: {} 
                    \nElements: {} 
                    \nFrame Element Relations: {}
                    \nID: {}
                    \nLUs: {}""".format(self.name, self.relations, self.elements, self.fe_relations, self.ID, self.lexicalUnits)
        return formatted

    def format_elements(self):
        final = ""
        for element in self.elements:
            final += element.name + "\n"
        return final


class FrameElement(object):
    def __init__(self, name, abbrev, core, framename, semtype=None):
        self.name = name
        self.abbrev = abbrev
        self.coreType = core
        self.frame_name = framename
        self.semtype=semtype
        self.excludes = []
        self.requires = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name
    
    def set_semtype(self, sem):
        self.semtype = sem

    def add_excludes(self, excluded_element):
        self.excludes.append(excluded_element)

    def add_requires(self, required_element):
        self.requires.append(required_element)




class SemType(object):
    def __init__(self, name, ID):
        self.name = name
        self.ID = ID

def strip_definition(definition):
    # The encoding is necessary for python2.7
    encoded = ET.fromstring(definition.encode('utf-8'))
    return ''.join(encoded.itertext())


class FrameBuilder(object):
    def __init__(self, replace_tag):
        self.replace_tag = replace_tag
        self.lu_path = "fndata-1.6/lu/"

    def build_frame(self, xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        name = root.attrib['name']
        ID = int(root.attrib['ID'])
        elements = []
        lexemes = []
        relations = []
        parents = []
        children=[]
        definition = ""
        for child in root:
            tag = child.tag.replace(self.replace_tag, "")
            if tag == "FE":
                elements.append(self.build_FE(child, name))
            elif tag == "lexUnit":
                lu = self.build_LU(child, name)
                if lu:
                    lexemes.append(lu)
            elif tag == "frameRelation":
                relation = child.attrib['type']
                related = [r.text for r in child.getchildren()]
                if len(related) > 0:
                    if relation == "Inherits from":
                        parents += related
                    if relation == 'Is Inherited by':
                        children += related
                    fr = FrameRelation(relation, related)
                    #fr = FrameRelation(atts['type'])
                    #relations.append(fr)
                    relations.append(fr)
            elif tag == "definition":
                xml_def = child.text
                #definition_xml = ET.fromstring(child)
                definition = strip_definition(child.text)
        frame = Frame(name, elements, lexemes, relations, parents, children, definition, xml_def, ID)
        return frame

    def build_FE(self, child, name):
        atts = child.attrib
        element = FrameElement(atts['name'], atts['abbrev'], atts['coreType'], name)
        for c2 in child.getchildren():
            t = c2.tag.replace(self.replace_tag, "")
            if t == "semType":
                s = SemType(c2.attrib['name'], c2.attrib['ID'])
                element.set_semtype(s)
            if t == "excludesFE":
                element.add_excludes(c2.attrib['name'])
            if t == "requiresFE":
                element.add_requires(c2.attrib['name'])
        return element


    def build_LU(self, child, name):
        atts = child.attrib
        s = None
        for c2 in child.getchildren():
            t = c2.tag.replace(self.replace_tag, "")
            if t == "semType":
                s = SemType(c2.attrib['name'], c2.attrib['ID'])
        ID = atts['ID']
        lu = ShallowLU(atts['name'], atts['POS'], name, atts['ID'], atts['status'])
        if s:
            lu.set_semtype(s)
        return lu
        """
        if atts['status'] != "Problem":
            print(name)
            path = self.lu_path + "lu{}.xml".format(ID)
            lu = self.parse_lu_xml(path)
            if s:
                lu.set_semtype(s)
            return lu
        """










