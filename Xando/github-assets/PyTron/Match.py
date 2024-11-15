from GameOverMenu import GameOverMenu

class Match:
	def __init__(self, gameObj, matchType):
		#Save base Match data
		self.game = gameObj
		self.NumOfPlayers = len(self.game.players)
		self.gameActive = True
		self.matchType = matchType

	def tick(self):
		for playerid in self.game.players:
			if self.game.players[playerid].alive == True:
				self.game.players[playerid].tick() #update direction of players
		if self.checkForTie(self.game.players) is True:
			self.setTie() #See if a tie has occured
			return
		for playerid in self.game.players:
			if self.game.players[playerid].alive == True:
				#See if they player is about to collide with something
				self.game.players[playerid].checkForCollision(self.game.players[playerid].direction)
				if self.game.players[playerid].alive == True: #Check if player is alive after check
					self.game.players[playerid].movePlayer() #update positions
		self.checkForWinner() #Check for winner
		if self.gameActive == True:
			self.draw() #draw board

	def checkForWinner(self):
		alive = self.NumOfPlayers
		#See how many players are still alive
		for playerid in self.game.players:
			if self.game.players[playerid].alive == False:
				alive = alive - 1
		if alive == 0:
			# If no one is alive there has been a tie.
			self.setTie()
		elif alive <= 1:
			# If one player is alive, find the winner and end the game.
			self.gameActive = False
			winner = None
			for playerid in self.game.players:
				#Find and select the winner
				if self.game.players[playerid].alive == True:
					winner = playerid
					#Set Match Winner
					self.setWinner(winner)
			# Draw game over menu
			self.game.gameOverMenu = GameOverMenu(self.game, "Player " + str(winner), self.matchType)
			self.game.switchToGameOver()

	def checkForTie(self,listplayers):
		#Check to see if two players will collide on the same tick
		location = []
		for p in listplayers:
			player = self.game.players[p]
			if player.alive == True:
				#Get next location of each player
				loc = player.directionToNextLocation(player.posX,player.posY,player.direction)
				if loc in location:
					#Players will collide
					return True
				else:
					#Add to a list of locations to check against
					location.append(loc)
		return False

	def setWinner(self, winner):
		#Add one to the winning players win tally per game mode.
		#PVP
		if self.matchType == 0:
			if winner == 1:
				self.game.PVP_Player1Wins = self.game.PVP_Player1Wins + 1
			elif winner == 2:
				self.game.PVP_Player2Wins = self.game.PVP_Player2Wins + 1
		#PVE
		elif self.matchType == 1:
			if winner == 1:
				self.game.PVE_PlayerWins = self.game.PVE_PlayerWins + 1
			elif winner == 2:
				self.game.PVE_BotWins = self.game.PVE_BotWins + 1
		#EVE
		elif self.matchType == 2:
			if winner == 1:
				self.game.EVE_Bot1Wins = self.game.EVE_Bot1Wins + 1
			elif winner == 2:
				self.game.EVE_Bot2Wins = self.game.EVE_Bot2Wins + 1


	def setTie(self):
		#If a tie has occured, end the game add 1 to the tie counter per game mode
		#and draw the game over menu.
		self.gameActive = False
		if self.matchType == 0:
			self.game.PVP_Tie = self.game.PVP_Tie + 1
		elif self.matchType == 1:
			self.game.PVE_Tie = self.game.PVE_Tie + 1
		elif self.matchType == 2:
			self.game.EVE_Tie = self.game.EVE_Tie + 1
		self.game.gameOverMenu = GameOverMenu(self.game, "No one", self.matchType)
		self.game.switchToGameOver()

	def event(self, event):
		#Pass match events to players
		for playerid in self.game.players:
			self.game.players[playerid].event(event)

	def draw(self):
		#Draw game board
		self.game.screen.fill((0,0,0))
		self.game.board.draw()
