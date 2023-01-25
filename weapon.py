import pygame
from pygame.math import Vector2 as vector
from random import uniform, randint
from pygame import math


class Weapon(pygame.sprite.Sprite):
    def __init__(self, groups, create_bullet, player, paused, add_projectal, bullet_speed):
        super().__init__(groups)
        self.create_bullet = create_bullet
        self.can_shoot = True
        self.attack_speed = None
        self.no_ammo = False
        self.paused = paused   

        self.player = player
        self.image = pygame.image.load(f"sprites/guns/{self.player.current_weapon}/right.png").convert_alpha()


        self.rect = self.image.get_rect(midleft = (0, 0))
        

        self.pistol_ammo = 30
        self.rifle_ammo = 120
        self.shotgun_ammo = 60
        self.sword_ammo = 0
        self.add_projectal = add_projectal
        self.add_bullet_speed = bullet_speed
        self.current_ammo = self.pistol_ammo



        self.accuracy = uniform(-0.075, 0.075)
   
    def attack_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > self.attack_speed:
                self.can_shoot = True

    def draw_weapon(self, pos, direction, current_weapon):
        self.mouse_pos_x, self.mouse_pos_y = pygame.mouse.get_pos()
        self.current_weapon = current_weapon
        self.pos = pos
        self.weapon_direction = direction

        self.weapon_equiped()
        self.weapon_stats()
        self.image = pygame.image.load(f"sprites/guns/{self.current_weapon}/right.png").convert_alpha()

        self.flip_right = pygame.transform.flip(self.image, False, False)
        self.flip_left = pygame.transform.flip(self.image, True, False)
        self.flip_up = pygame.transform.flip(self.image, False, False)
        self.flip_down = pygame.transform.flip(self.image, True, False)

        self.flip_right_up = pygame.transform.rotate(self.flip_right, 90)
        self.flip_left_up = pygame.transform.rotate(self.flip_left, -90)

        self.flip_right_down = pygame.transform.rotate(self.flip_right, -90)
        self.flip_left_down = pygame.transform.rotate(self.flip_down, 90)


        self.flip_sword_r = pygame.transform.rotate(self.image, 90)
        self.flip_sword_l = pygame.transform.rotate(self.image, -90)

        if not self.current_weapon == "sword":
            if self.mouse_pos_x > 500 < 1200 and self.mouse_pos_y > 200 < 400:
                self.weapon_direction = "right"
                self.image = self.flip_right
                self.rect = self.image.get_rect(midleft = (self.player.rect.midright))

            elif self.mouse_pos_x < 500 > 0 and self.mouse_pos_y > 200 < 400:
                self.weapon_direction = "left"
                self.image = self.flip_left
                self.rect = self.image.get_rect(midright = (self.player.rect.midleft))

            if self.mouse_pos_y <= 200:
                self.weapon_direction = "up"
                if self.player.flip == "right":
                    self.image = self.flip_right_up
                elif self.player.flip == "left":
                    self.image = self.flip_left_up
                self.rect = self.image.get_rect(midbottom = (self.player.rect.midtop))

            elif self.mouse_pos_y > 500:
                self.weapon_direction = "down"
                if self.player.flip == "right":
                    self.image = self.flip_right_down
                elif self.player.flip == "left":
                    self.image = self.flip_left_down
                self.rect = self.image.get_rect(midtop = (self.player.rect.midbottom))
        elif self.current_weapon == "sword":
            if self.mouse_pos_x > 600:
                self.weapon_direction = "left"
                self.rect = self.image.get_rect(midleft = (self.player.rect.midright))
            elif self.mouse_pos_x < 600:
                self.weapon_direction = "right"
                self.rect = self.image.get_rect(midright = (self.player.rect.midleft))

        self.gun_projectiles.extend(self.add_projectal)

        

        if not self.paused:
            if not self.current_weapon == "sword":
                if self.player.attacking and self.can_shoot and not self.no_ammo:
                    if self.weapon_direction == "right":
                        for projectal in self.gun_projectiles:
                            self.accuracy = uniform(-self.spread, self.spread)
                            projectal = self.create_bullet(self.rect.midright, vector(1,self.accuracy), self.bullet_speed)

                        self.ammo_usage_per_weapon()
                        self.can_shoot = False
                        self.shoot_time = pygame.time.get_ticks()
                  

                    elif self.weapon_direction == "left":
                        for projectal in self.gun_projectiles:
                            self.accuracy = uniform(-self.spread, self.spread)
                            projectal = self.create_bullet(self.rect.midleft,  vector(-1,self.accuracy), self.bullet_speed)

                        self.ammo_usage_per_weapon()
                        self.can_shoot = False
                        self.shoot_time = pygame.time.get_ticks() 

                    elif self.weapon_direction == "up":
                        for projectal in self.gun_projectiles:
                            self.accuracy = uniform(-self.spread, self.spread)
                            projectal = self.create_bullet(self.rect.midtop,  vector(self.accuracy,-1), self.bullet_speed)


                        self.ammo_usage_per_weapon()
                        self.can_shoot = False
                        self.shoot_time = pygame.time.get_ticks() 

                    elif self.weapon_direction == "down":
                        for projectal in self.gun_projectiles:
                            self.accuracy = uniform(-self.spread, self.spread)
                            projectal = self.create_bullet(self.rect.midbottom,  vector(self.accuracy,1), self.bullet_speed)

                        self.ammo_usage_per_weapon()
                        self.can_shoot = False
                        self.shoot_time = pygame.time.get_ticks()


            elif self.current_weapon == "sword":
                print(self.player.attacking, self.can_shoot)
                if self.player.attacking and self.can_shoot:
                    if self.weapon_direction == "right":
                        self.image = self.flip_sword_r
                        self.rect.centerx -= 15
                    elif self.weapon_direction == "left":
                        self.image = self.flip_sword_l
                        self.rect.centerx += 15



        if self.current_ammo <= 0:
            self.no_ammo = True
        else:
            self.no_ammo = False
            





    def weapon_stats(self):
        if self.current_weapon == "pistol":
            self.gun_projectiles = ["1"]
            self.attack_speed = 500 
            self.spread = 0.04
            self.image = pygame.image.load(f"sprites/guns/pistol/right.png").convert_alpha()
            self.bullet_speed = 350 + self.add_bullet_speed
        if self.current_weapon == "rifle":
            self.gun_projectiles = ["1"]
            self.image = pygame.image.load(f"sprites/guns/rifle/right.png").convert_alpha()
            self.attack_speed = 200
            self.spread = 0.07
            self.bullet_speed = 500 + self.add_bullet_speed
        if self.current_weapon == "shotgun":
            self.gun_projectiles = ["1", "1", "1", "1", "1"]
            self.image = pygame.image.load(f"sprites/guns/shotgun/right.png").convert_alpha()
            self.attack_speed = 1000
            self.spread = 0.85
            self.bullet_speed = 400 + self.add_bullet_speed
        if self.current_weapon == "sword":
            self.gun_projectiles = [""]
            self.image = pygame.image.load(f"sprites/guns/sword/right.png").convert_alpha()
            self.attack_speed = 150
        

    def weapon_equiped(self):
        if self.current_weapon == "pistol":
            self.current_ammo = self.pistol_ammo


        if self.current_weapon == "rifle":
            self.current_ammo = self.rifle_ammo


        if self.current_weapon == "shotgun":
            self.current_ammo = self.shotgun_ammo

        if self.current_weapon == "sword":
            self.current_ammo = self.sword_ammo    

    def ammo_usage_per_weapon(self):
        if self.current_weapon == "pistol":
            self.pistol_ammo -= len(self.gun_projectiles)


        if self.current_weapon == "rifle":
            self.rifle_ammo -= len(self.gun_projectiles)


        if self.current_weapon == "shotgun":
            self.shotgun_ammo -= len(self.gun_projectiles)





        

        



    def update(self, pos, direction, current_weapon):
        self.attack_timer()
        self.draw_weapon(pos, direction, current_weapon)


