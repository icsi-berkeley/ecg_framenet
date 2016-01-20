from src.builder import *
import sys
from src.ecg_utilities import ECGUtilities as utils
#from src.ecg_utilities import format_valence_verb_cxn, format_schema, generate_cxns_for_lu, generate_cxns_from_patterns
#from src.ecg_utilities import generate_schemas_for_frames
#from src.ecg_utilities import generate_preps_from_types, generate_pps_from_roles
#from src.ecg_utilities import gather_lexicalUnits, generate_entity_tokens
from src.valence_data import *

if __name__ == "__main__":
	data_path = sys.argv[1]
	frame_path = data_path + "frame/"
	relation_path = data_path + "frRelation.xml"
	lu_path = data_path + "lu/"	
	fnb = FramenetBuilder(frame_path, relation_path, lu_path)
	fn = fnb.read() #fnb.read()
	fn.build_relations()
	fn.build_typesystem()



	
	
	