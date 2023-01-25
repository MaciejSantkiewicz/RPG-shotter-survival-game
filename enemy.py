import pygame
from pygame.math import Vector2 as vector
from os import walk
from entity import Entity
from weapon import Weapon
from random import randint


class Enemies:    #base class for every monster in the game, can be expanded
    def get_player_position(self):
        enemy_pos = vector(self.rect.center)
        player_pos = vector(self.player.rect.center)
        distance = (player_pos - enemy_pos).magnitude()
        self.save_direction = "right"
        self.is_killed = False

        
        if distance != 0:
            direction = (player_pos - enemy_pos).normalize()
        else:
            direction = vector()

        return (distance, direction)


    def face_player(self):
        distance, direction = self.get_player_position()
        if -1 < direction.y <1:
            if direction.x < 0:
                if distance > self.attack_radius:
                    self.attacking = False
                    self.status = "left_run"
                    self.animation_speed = 10
                    self.save_direction = "right"

                else:
                    self.attacking = True
                    self.status = "left_attack"
                    self.animation_speed = 4
                    if int(self.frame_index) == 1 and self.player.can_get_hit:
                        self.player.damage(self.monster_damage)
                        self.player.can_get_hit = False
                        self.player.hit_time =pygame.time.get_ticks()


            if direction.x > 0:
                if distance > self.attack_radius:
                    self.attacking = False
                    self.status = "right_run"
                    self.animation_speed = 10
                    self.save_direction = "left"
                else:
                    self.attacking = True
                    self.status = "right_attack"
                    self.animation_speed = 4
                    if int(self.frame_index) == 1 and self.player.can_get_hit:                       
                        self.player.damage(self.monster_damage)
                        self.player.can_get_hit = False
                        self.player.hit_time = pygame.time.get_ticks()



    def walk_to_player(self):
        distance, direction = self.get_player_position()
        if self.attack_radius < distance < self.walk_radius:
            self.direction = direction
        else:
            self.direction = vector()



class Monster(Entity, Enemies): #class for only red enemies appearing in the game
    def __init__(self, pos, groups, path, collision_sprites, player, speed):
        super().__init__(pos, groups, path, collision_sprites,)
        self.speed_boost = speed
        self.player = player
        self.attack_radius = 40 #all attributes can be changed
        self.walk_radius = 5000
        self.min_speed = 10 + self.speed_boost
        self.max_speed = 50 + self.speed_boost
        self.speed = randint(self.min_speed,self.max_speed)
        self.frame_index = 0
        self.monster_damage = 15
        self.health = 1
        self.is_killed = False

    def killed(self): #deletes the sprite if the player hit it with the weapon
        self.kill()
        self.is_killed = True
        return self.is_killed


        
    def update(self, dt, non1, non2):
        self.animate(dt)
        self.walk_to_player()
        self.face_player()
        self.move(dt)





