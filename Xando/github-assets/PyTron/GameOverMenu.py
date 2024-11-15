import pygame

class GameOverMenu:
	def __init__(self, gameObj, winner, matchType):
		#Collect menu info.
		self.game = gameObj
		self.winner = winner
		self.matchType = matchType


	def event(self, event):
		if event.type == pygame.KEYUP:
			#If enter is pressed switch to the main menu
			if event.key == pygame.K_RETURN:
				self.game.screen.fill((0,0,0))
				self.game.switchToMainMenu()


	def draw(self):
		#Set base font and text size
		titleFont = pygame.font.SysFont(None, 30)
		#Set text for game over menu
		winText = str(self.winner) + " wins!"
		stats1 = ""
		stats2 = ""
		stats3 = ""
		
		if self.matchType == 0:
			stats1 = "Player 1 Wins: " + str(self.game.PVP_Player1Wins)
			stats2 = "Player 2 Wins: " + str(self.game.PVP_Player2Wins)
			stats3 = "Ties: " + str(self.game.PVP_Tie)
		elif self.matchType == 1:
			stats1 = "Player Wins: " + str(self.game.PVE_PlayerWins)
			stats2 = "Bot Wins: " + str(self.game.PVE_BotWins)
			stats3 = "Ties: " + str (self.game.PVE_Tie)
		elif self.matchType == 2:
			stats1 = "Bot 1 Wins: " + str(self.game.EVE_Bot1Wins)
			stats2 = "Bot 2 Wins: " + str(self.game.EVE_Bot2Wins)
			stats3 = "Ties: " + str (self.game.EVE_Tie)
		
		#Build titles
		title = titleFont.render(winText, 1, (255, 255, 255))
		title2 = titleFont.render(stats1, 1, (255, 255, 255))
		title3 = titleFont.render(stats2, 1, (255, 255, 255))
		title4 = titleFont.render(stats3, 1, (255, 255, 255))
		title5 = titleFont.render("Press Enter to continue", 1, (255, 255, 255))
		
		title_width = title.get_rect().width
		title2_width = title2.get_rect().width
		title3_width = title3.get_rect().width
		title4_width = title4.get_rect().width
		title5_width = title5.get_rect().width
		print(stats1 + " " + stats2 + " " + stats3)

		#Draw title/Stats info
		self.game.screen.blit(title, ((self.game.scr_x / 2) - (title_width / 2), 120))
		self.game.screen.blit(title2, ((self.game.scr_x / 2) - (title2_width / 2), 150))
		self.game.screen.blit(title3, ((self.game.scr_x / 2) - (title3_width / 2), 180))
		self.game.screen.blit(title4, ((self.game.scr_x / 2) - (title4_width / 2), 210))
		self.game.screen.blit(title5, ((self.game.scr_x / 2) - (title5_width / 2), 240))
