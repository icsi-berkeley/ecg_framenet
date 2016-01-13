""" Testing: reading in FrameNet Frames and creating Python objects.


TO DO: get semtypes for:
1) Frames
2) frame elements
3) lexical units
"""

import xml.etree.ElementTree as ET


class Node(object):
    def __init__(self, parents=[], children=[]):
        self.parents= parents
        self.children = children


class Frame(Node):
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

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name
    
    def set_semtype(self, sem):
        self.semtype = sem

class LexicalUnit(object):
    def __init__(self, name, pos, framename, ID):
        self.name = name
        self.pos = pos
        self.frame_name = framename
        self.semtype = None
        self.ID = ID

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def set_semtype(self, sem):
        self.semtype = sem

class FrameRelation(object):
    def __init__(self, relation_type, related_frames):
        self.relation_type = relation_type
        self.related_frames = related_frames

    def __str__(self):
        return self.relation_type

    def __repr__(self):
        related = [frame.name for frame in self.related_frames]
        return "{}: {}".format(self.relation_type, str(related))

class SemType(object):
    def __init__(self, name, ID):
        self.name = name
        self.ID = ID

def strip_definition(definition):
    return ''.join(ET.fromstring(definition).itertext())


class FrameBuilder(object):
    def __init__(self, replace_tag):
        self.replace_tag = replace_tag

    def build_frame(self, xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        name = root.attrib['name']
        ID = root.attrib['ID']
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
                lexemes.append(self.build_LU(child, name))
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
        return element

    def build_LU(self, child, name):
        atts = child.attrib
        s = None
        for c2 in child.getchildren():
            t = c2.tag.replace(self.replace_tag, "")
            if t == "semType":
                s = SemType(c2.attrib['name'], c2.attrib['ID'])
        lu = LexicalUnit(atts['name'], atts['POS'], name, atts['ID'])
        if s:
            lu.set_semtype(s)
        return lu




"""
def parse_xml_frame(xml_path):
    replace_tag = "{http://framenet.icsi.berkeley.edu}"
    tree = ET.parse(xml_path)
    root = tree.getroot()
    name = root.attrib['name']
    ID = root.attrib['ID']
    elements = []
    lexemes = []
    relations = []
    parents = []
    children=[]
    definition = ""
    for child in root:
        tag = child.tag.replace(replace_tag, "")
        if tag == "FE":
            atts = child.attrib
            element = FrameElement(atts['name'], atts['abbrev'], atts['coreType'])
            for c2 in child.getchildren():
                t = c2.tag.replace(replace_tag, "")
                if t == "semType":
                    s = SemType(c2.attrib['name'], c2.attrib['ID'])
                    element.set_semtype(s)
            elements.append(element)
        elif tag == "lexUnit":
            atts = child.attrib
            s = None
            for c2 in child.getchildren():
                t = c2.tag.replace(replace_tag, "")
                if t == "semType":
                    s = SemType(c2.attrib['name'], c2.attrib['ID'])
            lu = LexicalUnit(atts['name'], atts['POS'])
            if s:
                lu.set_semtype(s)
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
    """






