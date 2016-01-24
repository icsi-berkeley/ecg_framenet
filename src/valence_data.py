from src.builder import *

"""
NOTES: Currently, filter_redundancies will check whether a given valence pattern 
has already been added to a list. If it has, it checks whether the pattern in question 
has a higher total -- if so, it adds that new pattern and deletes the old one.
Questions --> should it combine the totals?
"""

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
    total = []
    for lu in frame.lexicalUnits:
        if lu.pos == "V":
            total += flatten_valence_patterns(lu)
            #total += lu.valenceUnits
    if filter:
        total = filter_valences(total, frame)
        total = filter_by_pp_type(total)
    return sorted(filter_redundancies(total), key=lambda valence: valence.total, reverse=True)


def flatten_valence_patterns(lu):
    flattened = [pattern for realization in lu.valences for pattern in realization.valencePatterns]
    return flattened


#Remove non-core, multiple constituents, and null instantiations 
#TO DO: remove multiple constituents (things that map onto same FE)
def filter_valences(all_valence_patterns, frame):
    new = []
    for pattern in all_valence_patterns:

        new_pattern = ValencePattern(pattern.frame, pattern.total, pattern.lu)
        new_units = []
        observed = []
        for valence in pattern.valenceUnits:
            add = True
            fe = frame.get_element(valence.fe)
            if fe.coreType != "Core":
                #print(valence.fe)
                #print(valence.pt)
                #pass
                add = False
                #print(valence.fe)
            #    add = False
            if valence.pt in ['CNI', 'INI', 'DNI']:
                add = False
            if valence.fe in observed:
                add = False
            if add:
                new_units.append(valence)
                observed.append(valence.fe)
        #if add:

        new_pattern.add_valenceUnits(new_units)
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
    #return list(set(patterns))
    return seen


# Filter out valences with the same valence type
def filter_by_pp_type(patterns):
    new_patterns = []
    for pattern in patterns:
        new_pattern = ValencePattern(pattern.frame, pattern.total, pattern.lu)
        for v in pattern.valenceUnits:
            #new_unit = ValenceUnit
            pt = v.pt.replace("[", "-").split("-")[0]
            if pt == "PP":
                fe = v.fe
                pt = "{}-PP".format(fe)
            new_valence = Valence(v.frame, v.gf, pt, v.fe)
            new_pattern.add_valenceUnit(new_valence)
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