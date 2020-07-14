import pygame
import neat
import time
import os
import random
pygame.init()

# size of game window
WIN_WIDTH = 550
WIN_HEIGHT = 800

# center window
os.environ['SDL_VIDEO_CENTERED'] = '1'
###############


# scale2x makes images 2 times bigger
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png"))) 
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("Cascadia Code", 50)
# SCORE_FONT = pygame.font.SysFont("Cascadia Code", 50)


class Bird: #  for making flappy birds
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

		# FLAPPING BIRD
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
			self.img_count = 0 # RESET IMG COUNT

		if self.tilt <= -80:
			self.img = self.IMGS[1]
			self.img_count = self.ANIMATION_TIME*2

		rotated_image = pygame.transform.rotate(self.img, self.tilt)
		new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
		win.blit(rotated_image, new_rect.topleft)

	def get_mask(self):
		return pygame.mask.from_surface(self.img)


class Pipe: # the classic green mario pipes
	GAP = 200 
	VEL = 5

	def __init__(self, x):
		self.x = x
		self.height = 0
		self.gap = 100

		self.top = 0
		self.bottom = 0
		self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True) # flip pipe upside down
		self.PIPE_BOTTOM = PIPE_IMG

		self.passed = False # for collision and AI purposes
		self.set_height()

	def set_height(self):
		self.height = random.randrange(50,450)
		self.top = self.height - self.PIPE_TOP.get_height()
		self.bottom = self.height + self.GAP

	def move(self):
		self.x -= self.VEL

	def draw(self, win):
		win.blit(self.PIPE_TOP, (self.x, self.top))
		win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

	def collide(self, bird):
		bird_mask = bird.get_mask()
		top_mask = pygame.mask.from_surface(self.PIPE_TOP)
		bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

		top_offset = (self.x - bird.x, self.top - round(bird.y))# offset from top to bird
		bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

		b_point = bird_mask.overlap(bottom_mask, bottom_offset)
		t_point = bird_mask.overlap(top_mask, top_offset)

		if t_point or b_point: # everytime bird collides, return True
			return True

		return False

class Base: # this is the floor of the graphics
	VEL = 5
	WIDTH = BASE_IMG.get_width()
	IMG = BASE_IMG

	def __init__(self, y):
		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH

	def move(self):
		self.x1 -= self.VEL
		self.x2 -= self.VEL

		if self.x1 + self.WIDTH < 0:
			self.x1 = self.x2 + self.WIDTH

		if self.x2 + self.WIDTH < 0:
			self.x2 = self.x1 + self.WIDTH

	def draw(self, win):
		win.blit(self.IMG, (self.x1, self.y))
		win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, bird, pipes, base, score): # window, bird
	win.blit(BG_IMG, (0,0)) # blit = 'draw'

	for pipe in pipes:
		pipe.draw(win)

	text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
	win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

	base.draw(win)

	bird.draw(win)
	pygame.display.update()


def main():
	bird = Bird(230, 350)
	base = Base(730)
	pipes = [Pipe(700)]
	win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	clock = pygame.time.Clock()

	score = 0
	
	run = True
	while run: # this will run every fram ~ 30/s
		clock.tick(30) # at most, 30 ticks/frames per second

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		# bird.move()
		
		base.move()

		add_pipe = False
		rem = [] # for pipe removals after they've passed the left side of screen

		for pipe in pipes:
			if pipe.collide(bird): # check if bird mask has collided with pipe mask
				pass

			if pipe.x + pipe.PIPE_TOP.get_width() < 0:
				rem.append(pipe)

			if not pipe.passed and pipe.x + bird.img.get_width() < bird.x:
				pipe.passed = True
				add_pipe = True

			pipe.move()

		if add_pipe:
			score += 1
			pipes.append(Pipe(700))

		for r in rem:
			pipes.remove(r)
        
        # hitting the floor
		if bird.y + bird.img.get_height() >= 730:
			pass

		draw_window(win, bird, pipes, base, score)

	pygame.quit()
	quit()

main()