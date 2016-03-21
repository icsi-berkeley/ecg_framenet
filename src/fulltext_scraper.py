import xml.etree.ElementTree as ET

replace_tag = "{http://framenet.icsi.berkeley.edu}"

def scrape_file(xmlpath):
	tree = ET.parse(xmlpath)
	text = ""
	root = tree.getroot()
	for child in root:
		tag = child.tag.replace(replace_tag, "")
		if tag == "sentence":
			for c2 in child.getchildren():
				text += c2.text.strip()
	return text


path = "fndata-1.6/fulltext/PropBank__ElectionVictory.xml"

d = scrape_file(path)
