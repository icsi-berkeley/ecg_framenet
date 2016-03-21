"""
In beta. Attempting to formulate procedures to hypothesize/build
ECG constructions from valence data. So far, there are a couple of methods:

1) Directly from valence patterns --> one valence pattern generates one HypothesizedConstruction
    * hypothesize_construction_from_pattern({PATTERN}, {N=index in total list})
2) From an entire frame, using individual valences --> build custom "valence patterns" from compatible valence units.
    * CXNS = collapse_valences_to_cxns({FRAME}, {FILTER=boolean})
    * for cxn in CXNS: hypothesize_construction_from_collapsed_pattern(CXNS, {N=index})

Ideally, we'll want a third way:
3) Top-down processing, fitting valence patterns to the existing grammar.

"""

from src.hypothesis import *
from src.lexical_units import *


event_elements = ['Time', 'Place','Duration']

def hypothesize_construction_from_pattern(valence_pattern, n=1):
    hypothesis = HypothesizedConstruction(valence_pattern.frame, n=n)
    total = sum(i.total for i in valence_pattern.valenceUnits)
    for unit in valence_pattern.valenceUnits:
        #if unit.pt not in ["2nd", "pp[because of]"]:
        probabilities = [1.0, .9]  # Is this right? These are for doing direct fit for valence patterns, so maybe
        pt = unit.pt.replace("[", "-").replace("]", "")
        constituent = Constituent(pt, unit.fe, unit.gf, probabilities)
        hypothesis.add_constituent(constituent)
    return hypothesis


def hypothesize_construction_from_collapsed_pattern(valence_pattern, n=1):
    hypothesis = HypothesizedConstruction(valence_pattern.frame, n=n)
    total = sum(i.total for i in valence_pattern.valenceUnits)
    for unit in valence_pattern.valenceUnits:
        #if unit.pt not in ["2nd", "pp[because of]"]:
        ommission_prob = round((unit.total / valence_pattern.total), 3)
        if ommission_prob <= 0:
            ommission_prob = 0.001
        probabilities = [ommission_prob, .9]
        pt = unit.pt.replace("[", "-").replace("]", "")
        constituent = Constituent(pt, unit.fe, unit.gf, probabilities)
        hypothesis.add_constituent(constituent)
    return hypothesis




def collapse_with_seed(initial_pattern, other_list, frame):
    for i in other_list:
        if (i not in initial_pattern.valenceUnits) and (frame.get_element(i.fe).coreType == "Core") and i.pt not in ['INI', 'DNI', 'CNI']:
            add = True
            for j in initial_pattern.valenceUnits:
                base_element, element = frame.get_element(i.fe), frame.get_element(j.fe)
                if not frame.compatible_elements(base_element, element):
                    add = False
                if (i.pt == j.pt) or (i.fe == j.fe):
                    add = False
                if i.fe in event_elements:
                    add = False
            if add:
                initial_pattern.add_valenceUnit(i)
    initial_pattern.total = sum(i.total for i in initial_pattern.valenceUnits)
    return initial_pattern


def filter_collapsed_patterns(collapsed_patterns):
    new_list = []
    for g in collapsed_patterns:
        if g not in new_list:
            new_list.append(g)
    return new_list


def collapse_valences_to_cxns(frame, filter=True):
    all_patterns=[]
    s = [valence for valence in frame.individual_valences if valence.lexeme.split(".")[1] == "v"]
    if filter:
        s = filter_by_pp(s)
    by_total = sorted(s, key=lambda valence: valence.total, reverse=True)
    for i in by_total:
        initial_pattern = ValencePattern(frame.name, 0, None)
        if i.pt in ['INI', 'DNI', 'CNI']:
            continue
        initial_pattern.add_valenceUnit(i)
        all_patterns.append(collapse_with_seed(initial_pattern, by_total, frame))
    return filter_collapsed_patterns(all_patterns)      


def filter_by_pp(valences):
    """ Should return a reduced list with valence PT changed to more general PT, e.g. "Area-PP". """
    second = []
    for i in valences:
        new = i.clone()
        if i.pt.split("[")[0] == "PP":
            new.pt = "{}-PP".format(i.fe)
        if new not in second:
            second.append(new)
        else:
            second[second.index(new)].total += new.total
            second[second.index(new)].add_annotations(new.annotations)
    return second