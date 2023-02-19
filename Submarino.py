import pygame
from pygame.locals import *
import random
import sys
from button import Button


pygame.init()

SCREEN = pygame.display.set_mode((800, 800))
pygame.display.set_caption("DeePy Adventure")


BG = pygame.image.load("C:/Users/Aluno/Downloads/Menu-System-PyGame-main/assets/Background.png")
Bc = pygame.image.load("C:/Users/Aluno/Downloads/Menu-System-PyGame-main/assets/Play Game.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("C:/Users/Aluno/Downloads/Menu-System-PyGame-main/assets/font.ttf", size)

#define font
font = pygame.font.SysFont('Bauhaus 93', 60)

# Musica
pygame.mixer.music.load('C:/Users/Aluno/Downloads/submarino/img/Creedence.mp3')
pygame.mixer.music.play(-1)

def play():
	while True:
		PLAY_MOUSE_POS = pygame.mouse.get_pos()

		SCREEN.fill("black")

		clock = pygame.time.Clock()
		fps = 60

		# define colours
		white = (255, 255, 255)

		# define game variables
		ground_scroll = 0
		scroll_speed = 4
		flying = False
		game_over = False
		pipe_gap = 300
		pipe_frequency = 2000  # milliseconds
		last_pipe = pygame.time.get_ticks() - pipe_frequency
		score = 0
		pass_pipe = False


		# load images
		ground_img = pygame.image.load('C:/Users/Aluno/Downloads/submarino/img/terra.png')
		bg = pygame.image.load('C:/Users/Aluno/Downloads/submarino/img/bg.png')
		button_img = pygame.image.load('C:/Users/Aluno/Downloads/submarino/img/restart.png')


		def draw_text(text, font, text_col, x, y):
			img = font.render(text, True, text_col)
			SCREEN.blit(img, (x, y))

		def reset_game():
			pipe_group.empty()
			flappy.rect.x = 100
			flappy.rect.y = int(800 / 2)
			score = 0
			pontos = 5
			return score


		class Bird(pygame.sprite.Sprite):
			def __init__(self, x, y, scale):
				pygame.sprite.Sprite.__init__(self)
				self.scale = scale
				self.images = []
				self.index = 0
				self.counter = 0
				for num in range(1, 3):
					img = pygame.image.load(f'C:/Users/Aluno/Downloads/submarino/img/submarino{num}.png')
					self.images.append(img)
				self.image = self.images[self.index]
				self.rect = self.image.get_rect()
				self.rect.center = [x, y]
				self.vel = 0
				self.clicked = False

			def update(self):

				if flying == True:
					# gravity
					self.vel += 0.5
					if self.vel > 8:
						self.vel = 8
					if self.rect.bottom < 768:
						self.rect.y += int(self.vel)

				if game_over == False:
					# jump
					if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
						clickSound = pygame.mixer.Sound('C:/Users/Aluno/Downloads/submarino/img/click.mp3')
						clickSound.play()
						self.clicked = True
						self.vel = -10
					if pygame.mouse.get_pressed()[0] == 0:
						self.clicked = False

					# handle the animation
					self.counter += 1
					flap_cooldown = 5

					if self.counter > flap_cooldown:
						self.counter = 0
						self.index += 1
						if self.index >= len(self.images):
							self.index = 0
					self.image = self.images[self.index]

					# rotate the bird
					self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
				else:
					self.image = pygame.transform.rotate(self.images[self.index], -90)

		class Pipe(pygame.sprite.Sprite):
			def __init__(self, x, y, position):
				pygame.sprite.Sprite.__init__(self)
				self.image = pygame.image.load('C:/Users/Aluno/Downloads/submarino/img/obstaculo.png')
				self.rect = self.image.get_rect()
				# position 1 is from the top, -1 is from the bottom
				if position == 1:
					self.image = pygame.transform.flip(self.image, False, True)
					self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
				if position == -1:
					self.rect.topleft = [x, y + int(pipe_gap / 2)]

			def update(self):
				self.rect.x -= scroll_speed
				if self.rect.right < 0:
					self.kill()

		class Button():
			def __init__(self, x, y, image):
				self.image = image
				self.rect = self.image.get_rect()
				self.rect.topleft = (x, y)

			def draw(self):

				action = False

				# get mouse position
				pos = pygame.mouse.get_pos()

				# check if mouse is over the button
				if self.rect.collidepoint(pos):
					if pygame.mouse.get_pressed()[0] == 1:
						action = True

				# draw button
				SCREEN.blit(self.image, (self.rect.x, self.rect.y))

				return action

		bird_group = pygame.sprite.Group()
		pipe_group = pygame.sprite.Group()

		flappy = Bird(100, int(800 / 2), scale=600)

		bird_group.add(flappy)

		# create restart button instance
		button = Button(800 // 2 - 50, 800 // 2 - 100, button_img)



		run = True
		while run:

			clock.tick(fps)

			# draw background
			SCREEN.blit(bg, (0, 0))

			SCREEN.blit(bg, (0, 650))
			bird_group.draw(SCREEN)
			bird_group.update()
			pipe_group.draw(SCREEN)

			# draw the ground
			SCREEN.blit(ground_img, (ground_scroll, 650))

			# check the score
			if len(pipe_group) > 0:
				if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
						and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
						and pass_pipe == False:
					pass_pipe = True
				if pass_pipe == True:
					if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
						score += 1
						pontoSound = pygame.mixer.Sound('C:/Users/Aluno/Downloads/submarino/img/ponto.mp3')
						pontoSound.play()
						pontos = 5
						while (score >= pontos and score<=12):
							pipe_gap = pipe_gap - 5
							pipe_frequency = pipe_frequency - 60  # milliseconds
							pontos = pontos + 5
						pass_pipe = False

			draw_text(str(score), font, white, float(800 / 2), 20)



			if game_over == False and flying == True:


				# look for collision
				if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
					game_over = True
					explosionSound = pygame.mixer.Sound('C:/Users/Aluno/Downloads/submarino/img/explosao.mp3')
					explosionSound.play()


				# check if bird has hit the ground
				if flappy.rect.bottom >= 650:
					game_over = True
					flying = False
					explosionSound = pygame.mixer.Sound('C:/Users/Aluno/Downloads/submarino/img/explosao.mp3')
					explosionSound.play()


				# generate new pipes
				time_now = pygame.time.get_ticks()
				if time_now - last_pipe > pipe_frequency:
					pipe_height = random.randint(-100, 100)
					btm_pipe = Pipe(800, int(800 / 2) + pipe_height, -1)
					top_pipe = Pipe(800, int(800 / 2) + pipe_height, 1)
					pipe_group.add(btm_pipe)
					pipe_group.add(top_pipe)
					last_pipe = time_now

				# draw and scroll the ground
				ground_scroll -= scroll_speed
				if abs(ground_scroll) > 50:
					ground_scroll = 0

				pipe_group.update()

			# check for game over and reset
			if game_over == True:
				pipe_gap = 300
				pipe_frequency = 2000

				if button.draw() == True:
					game_over = False
					score = reset_game()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
				if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
					flying = True

			pygame.display.update()

		PLAY_BACK = Button(image=None, pos=(640, 460),
						   text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

		PLAY_BACK.changeColor(PLAY_MOUSE_POS)
		PLAY_BACK.update(SCREEN)

		for event in pygame.event.get():
			while True:
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
						main_menu()

		pygame.display.update()


def main_menu():
	while True:
		SCREEN.blit(BG, (0, 0))

		MENU_MOUSE_POS = pygame.mouse.get_pos()

		MENU_TEXT = get_font(120).render("DeePy Adventure", True, "#ffffff")
		MENU_RECT = MENU_TEXT.get_rect(center=(400, 200))

		PLAY_BUTTON = Button(image=pygame.image.load("C:/Users/Aluno/Downloads/Menu-System-PyGame-main/assets/Play Rect.png"), pos=(400, 400),
							 text_input="PLAY", font=get_font(80), base_color="#ffffff", hovering_color="Green")

		QUIT_BUTTON = Button(image=pygame.image.load("C:/Users/Aluno/Downloads/Menu-System-PyGame-main/assets/Quit Rect.png"), pos=(400, 550),
							 text_input="QUIT", font=get_font(80), base_color="#ffffff", hovering_color="Red")

		SCREEN.blit(MENU_TEXT, MENU_RECT)

		for button in [PLAY_BUTTON, QUIT_BUTTON]:
			button.changeColor(MENU_MOUSE_POS)
			button.update(SCREEN)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
					play()
				if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
					pygame.quit()
					sys.exit()

		pygame.display.update()


main_menu()


pygame.quit()