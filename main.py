import pygame
import neat
import time
import os
import random

WIN_WIDTH = 600
WIN_HEIGHT = 800

# scale2x makes images 2 times bigger
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png"))) 
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))


# make Bird class for future use
class Bird:
	IMGS = BIRD_IMGS
	MAX_ROTATION = 25 # degrees
	ROT_VEL = 20 # deg/frame?
	ANIMATION_TIME = 5 # 5 frames each birdX.pn image

	def __init__(self, x, y): # starting state of bird(s)
		self.x = x # starting position of bird in x
		self.y = y
		self.tilt = 0 # starting tilt of bird
		self.tick_count = 0
		self.vel = 0 
		self.height = self.y
		self.img_count = 0
		self.img = self.IMGS[0] # references bird img we loaded

	def jump(self):
		self.vel = -10.5 # TOP LEFT OF PYGAME SCREEN IS (0,0), so jumps are - and falls are + velocity
		self.tick_count = 0 # reset for new physics model
		self.height = self.y

	def move(self):
		self.tick_count += 1

		d = self.vel*self.tick_count + 1.5*self.tick_count**2 # our game physics...tick_count ~ seconds, in respect

		# terminal velocity of 16 pixels per frame
		if d >= 16: 
			d = 16

		if d < 0: # ????????
			d -= 2

		self.y = self.y + d

		if d < 0 or self.y < self.height + 50: # this tilts bird when he's falling
			if self.tilt < self.MAX_ROTATION:
				self.tilt = self.MAX_ROTATION
		else:
			if self.tilt > -90: # [deg]
				self.tilt -= self.ROT_VEL

	def draw(self, win):
		self.img_count += 1

		if self.img_count < self.ANIMATION_TIME:
			self.img = self.IMGS[0]
		elif self.img_count < self.ANIMATION_TIME*2:
			self.img = self.IMGS[1]
		elif self.img_count < self.ANIMATION_TIME*3:
			self.img = self.IMGS[2]
		elif self.img_count < self.ANIMATION_TIME*4:
			self.img = self.IMGS[1]
		elif self.img_count < self.ANIMATION_TIME*4 + 1:
			self.img = self.IMGS[0]
			self.img_count = 0