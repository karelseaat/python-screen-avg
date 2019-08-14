import pygame

FULL, RESOLUTION = False, (1024, 50)

hardwareFlag = (pygame.HWSURFACE | pygame.DOUBLEBUF)

pygame.init()


class tneopixel(list):

	n = 0
	surface = None

	# def setSurface(self):
		
	def __init__(self, length):
		self.n = length
		for x in xrange(0,length):
			self.append((0,0,0))

		self.surface = pygame.display.set_mode(RESOLUTION, hardwareFlag | pygame.SRCALPHA)

		if self.surface is not None:
			for index, x in enumerate(self):
				pygame.draw.rect(self.surface, (255,255,255), (9 + (index * 20),9,12 ,12), 1)
				pygame.draw.rect(self.surface, (0,0,0), (10 + (index * 20),10,10 ,10), 0)
				pygame.display.update()


	def write(self):
		if self.surface is not None:
			for index, x in enumerate(self):
				# print (10 + (index * 20),10,10 ,10)
				pygame.draw.rect(self.surface, x, (10 + (index * 20),10,10 ,10), 0)
				pygame.display.update()
