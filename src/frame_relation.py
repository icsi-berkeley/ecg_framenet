""" 
@author: <seantrott@icsi.berkeley.edu>

Defines the FrameRelation class.
"""

class FrameRelation(object):
    """ Contains relation type (Inchoative Of, etc.) and the associated frames (Cause_motion, etc.). 

    If FrameNet.build_relation() has been called, related_frames will point to a list of actual Frame objects, vs. strings."""
    def __init__(self, relation_type, related_frames):
        self.relation_type = relation_type
        self.related_frames = related_frames

    def __str__(self):
        return self.relation_type

    def __repr__(self):
        related = [frame.name for frame in self.related_frames]
        return "{}: {}".format(self.relation_type, str(related))
