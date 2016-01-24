# framenet
Package for reading in FrameNet data and performing operations on it, such as creating ECG grammars.

If you're using BASH and want to build a customized FrameNet object, run:

$ ./build.sh

You can then retrieve a frame object by referencing the "fn" (FrameNet) object:

>> frame = fn.get_frame("Abandonment")

By default, the frames contain shallow information about lexical units (name, POS, etc). To retrieve the valence patterns,
you can use the "FrameNetBuilder" object:

>> fnb.build_lus_for_frame("Abandonment")

Now, the lexicalUnits field for the Abandomnent field will contain valnece pattern information:

>> frame.lexicalUnits[0].valences
...


