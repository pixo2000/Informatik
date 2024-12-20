import pygame

class MainMenu:
	def __init__(self, gameObj):
		self.game = gameObj

		self.font = pygame.font.SysFont(None, 34)

		self.menuList = ['Player vs Player', 'Player vs Computer', 'Computer vs Computer']
		self.items = [] #text objects, a list of lists: [text, bitmap, (width, height), (posx, posy)]
		self.activeItem = 0
		self.activeColour = (30, 140, 255)
		self.inactiveColour = (255, 255, 255)
		
		#calculate the positions of the text elements (populates self.items)
		for i, item in enumerate(self.menuList):
			if i == self.activeItem:
				colour = self.activeColour
			else:
				colour = self.inactiveColour
			label = self.font.render(item, 1, colour)

			width = label.get_rect().width
			height = label.get_rect().height + 40

			posx = (self.game.scr_x / 2) - (width / 2)

			total_height = len(self.items) * height
			posy = (self.game.scr_y / 2) - (total_height / 2) + (i * height)

			self.items.append([item, label, (width, height), (posx, posy)])

	def eventTick(self, event):
		if event.type == pygame.KEYUP: #change the active menu entry
			prevActive = self.activeItem 
			
			#change the current active item. Use modular arithmatic to loop around the list.
			if event.key == pygame.K_UP:
				self.activeItem = ((self.activeItem-1) % len(self.items))
			elif event.key == pygame.K_DOWN:
				self.activeItem = ((self.activeItem+1) % len(self.items))
			
			#if we changed active entries, redraw the new active entry in blue and redraw the old one in black
			if prevActive != self.activeItem: 
				self.items[self.activeItem][1] = self.font.render(self.items[self.activeItem][0], 1, self.activeColour)
				self.items[prevActive][1] = self.font.render(self.items[prevActive][0], 1, self.inactiveColour)
				self.game.screen.fill((0,0,0))
				self.draw()
			
			#select the entry, start the match
			if event.key == pygame.K_RETURN:
				self.game.startMatch(self.activeItem) #match type is equal to the element's ID

	def draw(self):
		#Build title text
		titleFont = pygame.font.SysFont(None, 80)
		title = titleFont.render("PyTron", 1, (255, 255, 255))
		title_width = title.get_rect().width
		#draw title
		self.game.screen.blit(title, ((self.game.scr_x / 2) - (title_width / 2), 80))
		#draw selectable menu options
		for name, label, (width, height), (posx, posy) in self.items:
                	self.game.screen.blit(label, (posx, posy))
