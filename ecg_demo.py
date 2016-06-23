from main import *

def ecg_demo1():
    """ Returns list of ECG schemas from FrameNet frames. """
    return utils.generate_schemas_for_frames(fn.frames)

def ecg_demo2(frame="Motion", role="Manner", pos="V"):
    """ Returns dictionary of types/tokens, valence cxns, and prepositions for a frame. """
    return build_cxns_for_frame(frame, fn, fnb, role, pos)




# DEMO: SCHEMAS
#schemas = utils.generate_schemas_for_frames(fn.frames)
# Write these to a file


# DEMO: CONSTRUCTIONS
#total = build_cxns_for_frame("Motion", fn, fnb, "Manner", "V")

#You can then write the values from the total dictionary into files:
#* cxns_all: all valences converted 1-1 to cxns 
#* cxns_collapsed: valences collapsed into smaller set 
#* tokens: tokens created from these frames ("swarm.v", etc.)
#* types: type-cxns ("Fluidic_motionType") created from these frames 
#* pp: PP constructions that are specific to the frame (e.g., Instrument-PP)
#* prep_types: General prepositional type constructions used for frame (E.g., "Instrument-Prep")
#* prepositions: Preposition constructions that are used for that frame (E.g. "With-Preposition"[subcase of Instrument-Prep])
# NOTE: The last three (pp, prep_types, and prepositions) are necessary for the collapsed cxns, since this filters by PP-type,
# and collapses two valence units if they are PPs mapping onto the same FE.


#DEMO: PREPOSITION CONSTRUCTIONS (distinct from build_cxns_for_frame, above)
#prepositions = utils.build_prepositions(fn)