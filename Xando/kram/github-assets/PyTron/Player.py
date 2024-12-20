import pygame
import random

class Player:
	def __init__(self, gameObj, colour, playerid, x, y, initialDirection):
		self.colour = colour # rgb colour of player
		self.playerid = playerid # player id indexed from 1
		self.game = gameObj

		self.posX = x
		self.posY = y
		
		# prev position is used for the input queue to prevent self collision
		self.prevPos = {'x':x, 'y':y}
		self.alive = True
		
		# list of directions inputs to be executed in subsequent frames
		self.directionQ = []
		self.maxDirectionQLen = 3
		
		# where to go when we draw the next frame
		self.direction = initialDirection

		gameObj.board.board[y][x] = playerid
	
	#direction definitions
	DIRECT_UP = 0
	DIRECT_RIGHT = 1
	DIRECT_DOWN = 2
	DIRECT_LEFT = 3

	def movePlayer(self):
		# move the player (change position) and update the game board
		if self.direction == Player.DIRECT_UP:
			self.game.board.board[self.posY-1][self.posX] = self.playerid
			self.posY = self.posY - 1
		elif self.direction == Player.DIRECT_RIGHT:
			self.game.board.board[self.posY][self.posX+1] = self.playerid
			self.posX = self.posX + 1
		elif self.direction == Player.DIRECT_DOWN:
			self.game.board.board[self.posY+1][self.posX] = self.playerid
			self.posY = self.posY + 1
		elif self.direction == Player.DIRECT_LEFT:
			self.game.board.board[self.posY][self.posX-1] = self.playerid
			self.posX = self.posX - 1

	def checkForCollision(self, direction):
		if self.wouldCollide(direction) == True:
			self.alive = False

	def wouldCollideSelf(self, nextDirection):
		'''Check if the player would collide with their previous position going a particular direction'''
		return (nextDirection == Player.DIRECT_UP and self.posY-1 == self.prevPos['y']) or \
			(nextDirection == Player.DIRECT_RIGHT and self.posX+1 == self.prevPos['x']) or \
			(nextDirection == Player.DIRECT_DOWN and self.posY+1 == self.prevPos['y']) or \
			(nextDirection == Player.DIRECT_LEFT and self.posX-1 == self.prevPos['x'])

	def wouldCollide(self, direction):
		'''check if a player would collide with an obstacle if they move in a particular direction'''
		return (direction == Player.DIRECT_UP and self.game.board.isObstacle(self.posX, self.posY-1)) or \
			(direction == Player.DIRECT_RIGHT and self.game.board.isObstacle(self.posX+1, self.posY)) or \
			(direction == Player.DIRECT_DOWN and self.game.board.isObstacle(self.posX, self.posY+1)) or \
			(direction == Player.DIRECT_LEFT and self.game.board.isObstacle(self.posX-1, self.posY))

	def directionToNextLocation(self, posX, posY, direction):
		'''converts current position and direction to the next position'''
		if direction == Player.DIRECT_UP: return (posX, posY-1)
		if direction == Player.DIRECT_RIGHT: return (posX+1, posY)
		if direction == Player.DIRECT_DOWN: return (posX, posY+1)
		if direction == Player.DIRECT_LEFT: return (posX-1, posY)

	def calculateDirectionTerritory(self, direction, opponentDirection):
		''' Given a directions, calculate a player's predicted territory,
			the number of positions he can reach before all other player.
			assumption: the next location based on direction and current 
				position is open for each player'''
		nplayers = len(self.game.players)
		
		# array of the total territory that a player controls, player 1 is index 0
		playerTerritory = [0]*nplayers
		qs = [[] for x in range(nplayers)] # 1 queue for the bfs search for each player

		# insert into queue the start location for the current player
		start = self.directionToNextLocation(self.posX, self.posY, direction)
		# the queue is an array of tuples: ((posx, posy), depth)
		qs[self.playerid-1].append((start, 0)) 
		
		#global hashmap of viewed locations. Updated once per bfs layer depth
		seenLocations = {start:self.playerid}
		
		# insert into queue the start location for the opponents
		for playerid in set(self.game.players)-set([self.playerid]):
			start = self.directionToNextLocation(self.game.players[playerid].posX, 
													self.game.players[playerid].posY, 
													opponentDirection)
			qs[playerid-1].append((start, 0))
		
		# start bfs here
		depth = 0
		while sum(map(len, qs)): #while we still have an element in any queue
			seenThisLayer = {}

			for player in range(nplayers):
				seenThisPlayerLayer = {}

				#loop guard: advance only one bfs layer for each player
				while qs[player] and qs[player][0][1] <= depth:
					a = qs[player].pop(0)
					curloc = a[0]

					if curloc not in seenThisLayer:
						seenThisLayer[curloc] = player # this player owns this location
					else:
						seenThisLayer[curloc] = -1 # already seen this layer, there has be a tie (marked by -1)
					
					# add adjacent open locations to the player's bfs queue
					for dir in range(0,4):
						loc = self.directionToNextLocation(curloc[0], curloc[1], dir)
						if loc not in seenLocations and loc not in seenThisPlayerLayer \
						and not self.game.board.isObstacle(loc[0], loc[1]):
							seenThisPlayerLayer[loc] = 1
							
							# a[1]+1: increase the depth by one for the added locations
							qs[player].append((loc, a[1]+1)) 

			#count territory and update the global seenLocations
			for loc in seenThisLayer:
				player = seenThisLayer[loc]
				seenLocations[loc] = player

				if player >= 0: #not a tie
					playerTerritory[player] += 1

			depth += 1
		
		# debug visualisation for bfs. Drawing logic is in GameBoard.py
		self.game.board.clearDebugBoard()
		for loc in seenLocations: self.game.board.debugBoard[loc[1]][loc[0]] = seenLocations[loc]+1

		return playerTerritory[self.playerid-1]

	# place holders for child classes
	def tick(self):
		pass

	def event(self, event):
		pass



class Human(Player):
	def __init__(self, gameObj, colour, playerid, x, y, initialDirection, controls):
		super(Human, self).__init__(gameObj, colour, playerid, x, y, initialDirection)

		#controls is a 4-tuple, up, right, down, left
		self.ctl_up = controls[0]
		self.ctl_right = controls[1]
		self.ctl_down = controls[2]
		self.ctl_left = controls[3]

	def event(self, event):
		if event.type == pygame.KEYDOWN and len(self.directionQ) < self.maxDirectionQLen:
			if event.key == self.ctl_up:
				self.directionQ.append(Player.DIRECT_UP)
			elif event.key == self.ctl_right:
				self.directionQ.append(Player.DIRECT_RIGHT)
			elif event.key == self.ctl_down:
				self.directionQ.append(Player.DIRECT_DOWN)
			elif event.key == self.ctl_left:
				self.directionQ.append(Player.DIRECT_LEFT)

	def tick(self): #perform moving and collision calculations here

		while self.directionQ and self.wouldCollideSelf(self.directionQ[0]):
			self.directionQ.pop(0)
		if self.directionQ:
			self.direction = self.directionQ.pop(0)
		while self.directionQ and self.directionQ[0] == self.direction:
			self.directionQ.pop(0)

		self.prevPos['x'] = self.posX
		self.prevPos['y'] = self.posY


class Computer(Player):
	def __init__(self, gameObj, colour, playerid, x, y, initialDirection):
		super(Computer, self).__init__(gameObj, colour, playerid, x, y, initialDirection)

	def tick(self):
		'''select next direction'''
		#self.strategyRandom()
		#self.stategyMostTerritoryWithRand()
		self.stategyMostTerritory()


	def strategyRandom(self):
		dir = list(range(0, 4))
		
		# 10% chance of changing directions
		if random.randint(1, 10) == 1:
			self.direction = dir[random.randint(0, len(dir)-1)]
		
		# if we would collide, pick a new random direction
		while dir and self.wouldCollide(self.direction):
			self.direction = dir.pop(random.randint(0, len(dir)-1))



	def stategyMostTerritory(self):
		maxArea = 0
		bestDirection = 0

		opponentId = (set(self.game.players)-set([self.playerid])).pop()
		
		for direction in range(0,4):
			if self.wouldCollide(direction): continue

			#generate random direction for opponent (assumes only 2 players)
			a = list(range(0,4))
			opdir = a.pop(random.randint(0, 3))
			while a and self.game.players[opponentId].wouldCollide(opdir):
				opdir = a.pop(random.randint(0, len(a)-1))

			area = self.calculateDirectionTerritory(direction, opdir)
			if area > maxArea:
				bestDirection = direction
				maxArea = area

		self.direction = bestDirection

	def stategyMostTerritoryWithRand(self):
		dirs = [] # list of possible directions
		opponentId = (set(self.game.players)-set([self.playerid])).pop()
		
		# test all possible directions for self
		for direction in range(0,4):
			if self.wouldCollide(direction): continue

			#generate random direction for opponent (assumes only 2 players)
			b = list(range(0,4))
			opdir = b.pop(random.randint(0, 3))
			while b and self.game.players[opponentId].wouldCollide(opdir):
				opdir = b.pop(random.randint(0, len(b)-1))
			
			# append direction tuple: (predictedTerritory, direction)
			dirs.append((self.calculateDirectionTerritory(direction, opdir), direction))
		
		# if we have more than one direction that wouldnt kill us
		if len(dirs) > 1:
			dirs.sort() # sort by order of predictedTerritory
			print(str(dirs))
			best = dirs[-1][0] # 'best' direction
			
		
			# if the current direction has the same value as the 'best' direction,
			# prefer staying in the same direction, makes movement less erratic
			i = len(dirs) - 2
			while i>=0: 
				if dirs[i][0] < best:
					break; #could not find current direction in top directions
				if dirs[i][1] == self.direction:
					return #direction stays the same
				i -= 1

			# if the next best move is within 10% of the value of the best move, there
			# is a 20% chance that we will select that move
			if dirs[-2][0] > dirs[-1][0]-dirs[-1][0]//10 and random.randint(1, 5) == 1:
				self.direction = dirs[-2][1]
				print("imperfect:", dirs[-2][0], "vs", dirs[-1][0])
			else:
				self.direction = dirs[-1][1]
		elif len(dirs) == 1: #only one valid direction
			self.direction = dirs[0][1]
