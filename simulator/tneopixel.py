import pygame

FULL, RESOLUTION = False, (300, 300)

hardwareFlag = (pygame.HWSURFACE | pygame.DOUBLEBUF)

pygame.init()
# pygame.display.set_mode(..., flags = pygame.NOFRAME)

def myCeil(x):
    return int(x) + int((x>0) and (x - int(x)) > 0)

class tneopixel(list):

	n = 0
	surface = None

	rowlength = 5

	def __init__(self, length):
		self.n = length
		for x in range(0, length):
			self.append((0,0,0))

		self.surface = pygame.display.set_mode(RESOLUTION, hardwareFlag | pygame.SRCALPHA | pygame.NOFRAME)

		if self.surface is not None:
			for index, x in enumerate(self):
				pygame.draw.rect(self.surface, (255, 255, 255), (9 + ((index + 1) % self.rowlength * 20), 9 + (myCeil((index + 1)/self.rowlength) * 20), 12, 12), 1)
				pygame.draw.rect(self.surface, (0, 0, 0), (10 + ((index + 1) % self.rowlength * 20), 10 + (myCeil((index + 1)/self.rowlength) * 20), 10, 10), 0)
				pygame.display.update()



	def write(self):
		if self.surface is not None:
			for index, x in enumerate(self):
				pygame.draw.rect(self.surface, x, (10 + ((index + 1) % self.rowlength * 20), 10 + (myCeil((index + 1)/self.rowlength) * 20), 10, 10), 0)
				pygame.display.update()
