# board.py

from shape import Shape
from tetrominoes import Tetrominoes
from PyQt4 import QtCore, QtGui

class Board(QtGui.QFrame):
	BoardWidth = 10
	BoardHeight = 22
	Speed = 300
	
	def __init__(self, parent):
		QtGui.QFrame.__init__(self, parent)
		
		self.timer = QtCore.QBasicTimer()
		self.isWaitingAfterLine = False
		self.curPiece = Shape()
		self.nextPiece = Shape()
		self.curX = 0
		self.curY = 0
		self.numLinesRemoved = 0
		self.board = []
		
		self.setFocusPolicy(QtCore.Qt.StrongFocus)
		self.isStarted = False
		self.isPaused = False
		self.clearBoard()
		
		self.nextPiece.setRandomShape()
	
	def getShapeAt(self, x, y):
		return self.board[int((y * Board.BoardWidth) + x)]
		
	def setShapeAt(self, x, y, shape):
		self.board[int((y * Board.BoardWidth) + x)] = shape
	
	def getSelWidth(self):
		return self.contentsRect().width() / Board.BoardWidth
	
	def getSelHeight(self):
		return self.contentsRect().height() / Board.BoardHeight
	
	def start(self):
		if self.isPaused:
			return
		
		self.isStarted = True
		self.isWaitingAfterLine = False
		self.numLinesRemoved = 0
		self.clearBoard()
		
		self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), str(self.numLinesRemoved))
		
		self.newPiece()
		self.timer.start(Board.Speed, self)
	
	def pause(self):
		if not self.isStarted:
			return
		
		self.isPaused = not self.isPaused
		if self.isPaused:
			self.timer.stop()
			self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "paused")
		else:
			self.timer.start(Board.Speed, self)
			self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), str(self.numLinesRemoved))
		
		self.update()
	
	def paintEvent(self, event):
		painter = QtGui.QPainter(self)
		rect = self.contentsRect()
		
		boardTop = rect.bottom() - Board.BoardHeight * self.getSelHeight()
		
		for i in range(Board.BoardHeight):
			for j in range(Board.BoardWidth):
				shape = self.getShapeAt(j, Board.BoardHeight - i - 1)
				if shape != Tetrominoes.NoShape:
					self.drawSquare(painter, rect.left() + j * self.getSelWidth(), boardTop + i * self.getSelHeight(), shape)
		
		if self.curPiece.getShape() != Tetrominoes.NoShape:
			for i in range(4):
				x = self.curX + self.curPiece.getX(i)
				y = self.curY - self.curPiece.getY(i)
				self.drawSquare(painter, rect.left() + x * self.getSelWidth(), boardTop + (Board.BoardHeight - y - 1) * self.getSelHeight(), self.curPiece.getShape())
	
	def keyPressEvent(self, event):
		if not self.isStarted or self.curPiece.getShape() == Tetrominoes.NoShape:
			QtGui.QWidget.keyPressEvent(self, event)
			return
		
		key = event.key()
		if key == QtCore.Qt.Key_P:
			self.pause()
			return
		if self.isPaused:
			return
		elif key == QtCore.Qt.Key_Left:
			self.tryMove(self.curPiece, self.curX - 1, self.curY)
		elif key == QtCore.Qt.Key_Right:
			self.tryMove(self.curPiece, self.curX + 1, self.curY)
		elif key == QtCore.Qt.Key_Down:
			self.tryMove(self.curPiece.rotatedRight(), self.curX, self.curY)
		elif key == QtCore.Qt.Key_Up:
			self.tryMove(self.curPiece.rotatedLeft(), self.curX, self.curY)
		elif key == QtCore.Qt.Key_Space:
			self.dropDown()
		elif key == QtCore.Qt.Key_D:
			self.oneLineDown()
		else:
			QtGui.QWidget.keyPressEvent(self, event)
	
	def timerEvent(self, event):
		if event.timerId() == self.timer.timerId():
			if self.isWaitingAfterLine:
				self.isWaitingAfterLine = False
				self.newPiece()
			else:
				self.oneLineDown()
		else:
			QtGui.QFrame.timerEvent(self, event)
	
	def clearBoard(self):
		for i in range(Board.BoardHeight * Board.BoardWidth):
			self.board.append(Tetrominoes.NoShape)
	
	def dropDown(self):
		newY = self.curY
		while newY > 0:
			if not self.tryMove(self.curPiece, self.curX, newY - 1):
				break
			newY -= 1
		
		self.pieceDropped()
	
	def oneLineDown(self):
		if not self.tryMove(self.curPiece, self.curX, self.curY - 1):
			self.pieceDropped()
	
	def pieceDropped(self):
		for i in range(4):
			x = self.curX + self.curPiece.getX(i)
			y = self.curY - self.curPiece.getY(i)
			self.setShapeAt(x, y, self.curPiece.getShape())
		
		self.removeFullLines()
		
		if not self.isWaitingAfterLine:
			self.newPiece()
	
	def removeFullLines(self):
		numFullLines = 0
		
		rowsToRemove = []
		
		for i in range(Board.BoardHeight):
			n = 0
			for j in range(Board.BoardWidth):
				if not self.getShapeAt(j, i) == Tetrominoes.NoShape:
					n = n + 1
			if n == 10:
				rowsToRemove.append(i)
		
		rowsToRemove.reverse()
		
		for m in rowsToRemove:
			for k in range(m, Board.BoardHeight):
				for l in range(Board.BoardWidth):
					self.setShapeAt(l, k, self.getShapeAt(l, k + 1))
		
		numFullLines = numFullLines + len(rowsToRemove)
		
		if numFullLines > 0:
			self.numLinesRemoved = self.numLinesRemoved + numFullLines
			self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), str(self.numLinesRemoved))
			self.isWaitingAfterLine = True
			self.curPiece.setShape(Tetrominoes.NoShape)
			self.update()
	
	def newPiece(self):
		self.curPiece = self.nextPiece
		self.nextPiece.setRandomShape()
		self.curX = Board.BoardWidth / 2 + 1
		self.curY = Board.BoardHeight - 1 + self.curPiece.minY()
		
		if not self.tryMove(self.curPiece, self.curX, self.curY):
			self.curPiece.setShape(Tetrominoes.NoShape)
			self.timer.stop()
			self.isStarted = False
			self.emit(QtCore.SIGNAL("messageToStatusbar(QString)"), "Game over")
	
	def tryMove(self, newPiece, newX, newY):
		for i in range(4):
			x = newX + newPiece.getX(i)
			y = newY - newPiece.getY(i)
			if x < 0 or x >= Board.BoardWidth or y < 0 or y >= Board.BoardHeight:
				return False
			if self.getShapeAt(x, y) != Tetrominoes.NoShape:
				return False
		
		self.curPiece = newPiece
		self.curX = newX
		self.curY = newY
		self.update()
		return True
	
	def drawSquare(self, painter, x, y, shape):
		color = QtGui.QColor(Tetrominoes.getColor(shape))
		painter.fillRect(x + 1, y + 1, self.getSelWidth() - 2, self.getSelHeight() - 2, color)
		
		painter.setPen(color.light())
		painter.drawLine(x, y + self.getSelHeight() - 1, x, y)
		painter.drawLine(x, y, x + self.getSelWidth() - 1, y)
		
		painter.setPen(color.dark())
		painter.drawLine(x + 1, y + self.getSelHeight() - 1, x + self.getSelWidth() - 1, y + self.getSelHeight() - 1)
		painter.drawLine(x + self.getSelWidth() - 1, y + self.getSelHeight() - 1, x + self.getSelWidth() - 1, y + 1)
