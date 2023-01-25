import pygame
from pygame.math import Vector2 as vector
from pygame import math
from random import randint
from entity import Entity



class Sprite(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0, -self.rect.height * 0.2)


class Bullet(pygame.sprite.Sprite):
	def __init__(self, pos, direction, surf, groups, speed):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(center = pos)
		self.speed = speed
		self.pause = False
		


		self.pos = pygame.math.Vector2(self.rect.center)

		self.direction = direction

		self.mouse_pos_x, self.mouse_pos_y = pygame.mouse.get_pos()


	def update(self, dt, test1,test2):
		self.pos += self.direction * self.speed * dt
		self.rect.center = (round(self.pos.x), round(self.pos.y))

class Ammo(pygame.sprite.Sprite):
	def __init__(self, groups, pos, type):
		super().__init__(groups)
		self.pos = pos
		self.type = type
		self.image = pygame.image.load(f"sprites/ammo/{self.type}.png").convert_alpha() 
		self.rect = self.image.get_rect(center = (self.pos))

class EnemyWeapon(pygame.sprite.Sprite):
	def __init__(self, groups, pos, enemy):
		super().__init__(groups)
		self.enemy = enemy
		self.pos = pos
		self.image = pygame.image.load(f"sprites/guns/sword/sword.png").convert_alpha()
		self.base_image = pygame.image.load(f"sprites/guns/sword/sword.png").convert_alpha()

		self.rect = self.image.get_rect(center = (self.pos))

		self.flip_r = pygame.transform.rotate(self.image, 270)
		self.flip_l = pygame.transform.rotate(self.image, 90)





	def update(self, nono, ono, non):


		if self.enemy.status == "right_attack":
			self.rect.midleft = self.enemy.rect.midright
			self.rect.centerx -= 10
			if int(self.enemy.frame_index) == 1:
				self.image = self.flip_r
				self.rect.centerx += 10

		elif self.enemy.status == "left_attack":
			self.rect.midright = self.enemy.rect.midleft
			self.rect.centerx += 10
			if int(self.enemy.frame_index) == 1:
				self.image = self.flip_l
				self.rect.centerx -= 10
		else:
			self.image = self.base_image
			if self.enemy.direction.x < 0 or self.enemy.save_direction == "right":
				self.rect.center = self.enemy.rect.midleft
			elif self.enemy.direction.x > 0 or self.enemy.save_direction == "left":
				self.rect.center = self.enemy.rect.midright
			



		if self.enemy.is_killed == True:
			self.kill()


	

class SkillBox(pygame.sprite.Sprite):
	def __init__(self, groups, pos, status):
		super().__init__(groups)
		self.status = status
		self.active = False
		self.pos = pos
		self.image = pygame.image.load("sprites/skills/test.png").convert_alpha() 
		self.rect = self.image.get_rect(center = (pos))
		self.name = None
		self.select_type = 1


	def position(self):
		if self.status == False:
			self.rect.center = (-100, - 100)
			self.rect.size = (0,0)
			self.active = False
			if self.active == False:
				self.roll_value = randint(1,4)
		if self.status == True:
			if self.active == True:
				self.select_type = self.roll_value
				self.rect.center = self.pos
				if self.select_type == 1:
					self.image = pygame.image.load("sprites/skills/movespeed.png").convert_alpha() 
					self.name = "+10 Movement speed!"
				elif self.select_type == 2:
					self.image = pygame.image.load("sprites/skills/projectile.png").convert_alpha() 
					self.name = "+ 1 projectal to all weapons!"
				elif self.select_type == 3:
					self.image = pygame.image.load("sprites/skills/bulletspeed.png").convert_alpha() 
					self.name = "+20 bullet speed!"
				elif self.select_type == 4:
					self.image = pygame.image.load("sprites/skills/health.png").convert_alpha() 
					self.name = "+25 max health!"



		

	def update(self, pos, nono2, nono3):
		self.position()
		






		




