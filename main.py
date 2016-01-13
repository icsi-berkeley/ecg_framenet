from src.builder import *
import sys




if __name__ == "__main__":
	frame_path = sys.argv[1]
	relation_path = sys.argv[2]
	fnb = FramenetBuilder(frame_path, relation_path)
	fn = fnb.read() #fnb.read()
	fn.build_relations()
	fn.build_typesystem()