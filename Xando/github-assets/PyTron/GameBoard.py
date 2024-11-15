import pygame

class GameBoard:
	def __init__(self, gameObj, xTiles, yTiles, tileSize):
		self.game = gameObj
		self.xTiles = xTiles
		self.yTiles = yTiles
		self.tileSize = tileSize

		#2d array of tiles, -1 for wall, 0 for nothing, 1-4 for player ids
		self.board = [x[:] for x in [[0]*xTiles]*yTiles];

		#for debugging territory calculations: 0 is nothing, >=1 is the playerid who
		#controls this territory
		self.debugBoard = [x[:] for x in [[0]*xTiles]*yTiles];

		#set the walls
		for i in range(xTiles):
			self.board[0][i] = -1
			self.board[yTiles-1][i] = -1
		for i in range(1, yTiles-1):
			self.board[i][0] = -1
			self.board[i][xTiles-1] = -1

		#Walls can be drawn on the board using the line below.
		#self.addRectangleObstacle(int(xTiles/2.2), int(yTiles/2.2), xTiles-int(xTiles/2.2)-1, yTiles-int(xTiles/2.2)-1)

	def clearDebugBoard(self):
		#Empty the debug board (Populate with 0)
		for i in range(self.yTiles):
			for j in range(self.xTiles):
				self.debugBoard[i][j] = 0

	def addRectangleObstacle(self, x1, y1, x2, y2):
		#Add Rectangle Obstacles to a given location
		#The rectangle is defined by the two points, (x1, y1), (x2, y2)
		for i in range(x1,x2+1):
			self.board[y1][i] = -1
			self.board[y2][i] = -1
		for i in range(y1, y2+1):
			self.board[i][x1] = -1
			self.board[i][x2] = -1

	def draw(self):
		#Draw game board
		for i in range(self.yTiles):
			for j in range(self.xTiles):
				#Set block location
				x = j*self.tileSize+1
				y = i*self.tileSize+1
				#Set block size
				w = self.tileSize-2
				h = self.tileSize-2
				colour = None
				#Set wall colour
				if self.board[i][j] == -1:
					colour = (120,120,120)
				elif self.board[i][j] == 0: #nothing, draw debug board for AI visualization
					if self.debugBoard[i][j] > 0:
						#Set area control highlighting/colouring
						pcol = self.game.players[self.debugBoard[i][j]].colour
						colour = (pcol[0]*0.2, pcol[1]*0.2, pcol[2]*0.2)
					else:
						#Set empyt board colour
						colour = (0,0,0)
				else: #player
					#Set player colour
					colour = self.game.players[self.board[i][j]].colour
				#Draw block
				pygame.draw.rect(self.game.screen, colour, (x,y,w,h))

	def isObstacle(self, x, y):
		#Check for an obstacle or players path.
		try:
			return self.board[y][x] == -1 or self.board[y][x] > 0
		except:
			#Handle out of bound lookups (edge cases in AI bfs search).
			return True
