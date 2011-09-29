# tetrominoes.py

class Tetrominoes(object):
	NoShape = 0
	ZShape = 1
	SShape = 2
	LineShape = 3
	TShape = 4
	SquareShape = 5
	LShape = 6
	MirroredLShape = 7
	
	ColorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC, 0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]
	
	CoordsTable = (
		(( 0,  0), ( 0,  0), ( 0,  0), ( 0,  0)),
		(( 0, -1), ( 0,  0), (-1,  0), (-1,  1)),
		(( 0, -1), ( 0,  0), ( 1,  0), ( 1,  1)),
		(( 0, -1), ( 0,  0), ( 0,  1), ( 0,  2)),
		((-1,  0), ( 0,  0), ( 1,  0), ( 0,  1)),
		(( 0,  0), ( 1,  0), ( 0,  1), ( 1,  1)),
		((-1, -1), ( 0, -1), ( 0,  0), ( 0,  1)),
		(( 1, -1), ( 0, -1), ( 0,  0), ( 0,  1))
	)

	@classmethod
	def getColor(cls, shape):
		return cls.ColorTable[shape]
	
	@classmethod
	def getCoords(cls, shape):
		return cls.CoordsTable[shape]