from src.builder import *



"""

@author: Sean Trott
NOTES: Currently, filter_redundancies will check whether a given valence pattern 
has already been added to a list. If it has, it combines the totals.
"""

def collapse_valences_for_frame(frame, filter=True):
    initial_pattern = ValencePattern(frame.name, 0, None)
    s = [valence for valence in frame.individual_valences if valence.lexeme.split(".")[1] == "v"]
    if filter:
        s = filter_by_pp(s)
    by_total = sorted(s, key=lambda valence: valence.total, reverse=True)
    #for valence in frame.individual_valences:
    initial_pattern.add_valenceUnit(by_total[0])
    for i in by_total:
        if (i not in initial_pattern.valenceUnits) and (frame.get_element(i.fe).coreType == "Core"):
            add = True
            for j in initial_pattern.valenceUnits:
                base_element, element = frame.get_element(i.fe), frame.get_element(j.fe)
                if not frame.compatible_elements(base_element, element):
                    add = False
                if (i.pt == j.pt) and (i.fe == j.fe):
                    add = False
            if add:
                initial_pattern.add_valenceUnit(i)
    initial_pattern.total = sum(i.total for i in initial_pattern.valenceUnits)
    return initial_pattern


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

def hypothesize_constructions(frame):
    return frame


# Assumes frame lus have already been built
# The "equality" check in lexical_units.py checks for: gf==gf, pt==pt, and fe==fe
# One issue is that bound fe's don't match, like self_mover and theme.
def find_common_patterns(frame1, frame2):
    first = all_valences(frame1)
    second = all_valences(frame2)
    intersection = []
    for element in first:
        if element in second:
            intersection.append(element)
    for element in second:
        if element in first and element not in intersection:
            intersection.append(element)
    #intersection = [element for element in first if element in second]
    return intersection


# Returns a sorted list of all valence patterns for a given frame.
# The list is sorted by the valence pattern's "total".
def all_valences(frame, filter=False):

    total = get_valence_patterns(frame)

    if filter:
        total = filter_valences(total, frame)
        total = filter_by_pp_type(total)
    #return total
    return sorted(filter_redundancies(total), key=lambda valence: valence.total, reverse=True)


def get_valence_patterns(frame):
    patterns = []
    for re in frame.group_realizations:
        patterns += re.valencePatterns
    return patterns


def all_family_valences(topFrame, fn, fnb, filter=False):
    """ Returns a set of reduced valences for a family of frames, beginning with topFrame. """
    total = get_valence_patterns(topFrame)
    for child in topFrame.children:
        print("Building lus for {}".format(child))
        fnb.build_lus_for_frame(child, fn)
        print("Built lus for {}".format(child))
        child_frame = fn.get_frame(child)
        child_frame.propagate_elements()
        print("Propagated elements for {}".format(child))
        total += get_valence_patterns(child_frame)
    print("\n")
    #print("Now filtering redundancies in list....")
    
    print("Now filtering by PP type...")
    total = filter_by_pp_type(total)
    print("Now filtering by non-core elements according to {}...".format(topFrame.name))
    total = filter_valences(total, topFrame)
    total = list(set(total))
    print("Replacing frame names for all...")
    for i in total:
        i.frame = topFrame.name
    return total
    #return sorted(filter_redundancies(total), key=lambda valence: valence.total, reverse=True)



#Remove non-core, multiple constituents, and null instantiations 
#TO DO: remove multiple constituents (things that map onto same FE)
def filter_valences(all_valence_patterns, frame):
    new = []
    for pattern in all_valence_patterns:

        new_pattern = ValencePattern(pattern.frame, pattern.total, pattern.lexeme)
        new_units = []
        observed = []
        for valence in pattern.valenceUnits:
            add = True
            fe = frame.get_element(valence.fe)
            if fe:
                if fe.coreType != "Core":
                    add = False
                if valence.pt in ['CNI', 'INI', 'DNI']:
                    add = False
                if valence.fe in observed:
                    add = False

            else:
                add = False
            if add:
                new_units.append(valence)
                observed.append(valence.fe)

        new_pattern.add_valenceUnits(new_units)
        new_pattern.add_annotations(pattern.annotations)
        new.append(new_pattern)
    return new

def filter_redundancies(patterns):
    seen = []
    for pattern in patterns:
        if pattern not in seen:
            seen.append(pattern)
        else:
            index = seen.index(pattern)
            seen[index].total += pattern.total
            seen[index].add_annotations(pattern.annotations)
    #return list(set(patterns))
    return seen


# Filter out valences with the same valence type
def filter_by_pp_type(patterns):
    new_patterns = []
    for pattern in patterns:
        new_pattern = ValencePattern(pattern.frame, pattern.total, pattern.lexeme)
        for v in pattern.valenceUnits:
            #new_unit = ValenceUnit
            new_valence = v.clone() 
            pt = v.pt.replace("[", "-").split("-")[0]
            if pt == "PP":
                fe = v.fe
                pt = "{}-PP".format(fe)
                new_valence.pt = pt
            
            new_pattern.add_valenceUnit(new_valence)
        new_pattern.add_annotations(pattern.annotations)
        new_patterns.append(new_pattern)
    return new_patterns


def collapse_all(base, rest, frame):
    new_pattern = ValencePattern(base.frame, base.total, base.lu) #Actually amalgamation of lus
    new_pattern.valenceUnits = list(base.valenceUnits)
    for pattern in rest:
        new_pattern = collapse_patterns(new_pattern, pattern, frame)
    return new_pattern


# Takes in a "BASE" pattern and attempts to collapse it with another pattern
def collapse_patterns(base, second, frame):
    new_pattern = ValencePattern(base.frame, base.total, base.lu) #Actually amalgamation of lus
    new_pattern.valenceUnits = list(base.valenceUnits)
    #for pattern in second:
    for unit in second.valenceUnits:
        element = frame.get_element(unit.fe)
        add = True
        for base_unit in base.valenceUnits:
            base_element = frame.get_element(base_unit.fe)
            if not frame.compatible_elements(base_element, element):
                add = False
            if unit.pt == base_unit.pt:
                #add = False
                pass
            if unit in new_pattern.valenceUnits:
                add = False
        if add:
            new_pattern.add_valenceUnit(unit)
    return new_pattern


# Takes in the result of all_valences
def find_pp_roles(valences):
    roles = {}
    for value in valences:
        for i in value.valenceUnits:
            pt = i.pt.split("[")[0]
            if pt == "PP":
                if i.fe not in roles:
                    roles[i.fe] = []
                if i.pt not in roles[i.fe]:
                    roles[i.fe].append(i.pt)
    return roles


def invert_roles(roles):
    inverted = {}
    for k, v in roles.items():
        for prep in v:
            if prep not in inverted:
                inverted[prep] = []
            inverted[prep].append(k)
    return inverted