# shape.py

from tetrominoes import Tetrominoes
import random

class Shape(object):
	def __init__(self):
		self.coords = [[0,0] for i in range(4)]
		self.pieceShape = Tetrominoes.NoShape
		
		self.setShape(Tetrominoes.NoShape)

	def getShape(self):
		return self.pieceShape

	def setShape(self, shape):
		table = Tetrominoes.getCoords(shape)
		for i in range(4):
			for j in range(2):
				self.coords[i][j] = table[i][j]

		self.pieceShape = shape

	def setRandomShape(self):
		self.setShape(random.randint(1, 7))

	def getX(self, index):
		return self.coords[index][0]

	def getY(self, index):
		return self.coords[index][1]

	def setX(self, index, x):
		self.coords[index][0] = x

	def setY(self, index, y):
		self.coords[index][1] = y

	def minX(self):
		m = self.coords[0][0]
		for i in range(4):
			m = min(m, self.coords[i][0])

		return m

	def maxX(self):
		m = self.coords[0][0]
		for i in range(4):
			m = max(m, self.coords[i][0])

		return m

	def minY(self):
		m = self.coords[0][1]
		for i in range(4):
			m = min(m, self.coords[i][1])

		return m

	def maxY(self):
		m = self.coords[0][1]
		for i in range(4):
			m = max(m, self.coords[i][1])

		return m

	def rotatedLeft(self):
		if self.pieceShape == Tetrominoes.SquareShape:
			return self

		result = Shape()
		result.pieceShape = self.pieceShape
		for i in range(4):
			result.setX(i, self.getY(i))
			result.setY(i, -self.getX(i))

		return result

	def rotatedRight(self):
		if self.pieceShape == Tetrominoes.SquareShape:
			return self

		result = Shape()
		result.pieceShape = self.pieceShape
		for i in range(4):
			result.setX(i, -self.getY(i))
			result.setY(i, self.getX(i))

		return result

