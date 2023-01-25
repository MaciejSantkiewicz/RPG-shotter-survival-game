import pygame,  sys
from pygame.math import Vector2 as vector
from os import walk
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, path, collision_sprites):
        super().__init__(pos, groups, path, collision_sprites)
        self.speed = 150

        self.can_get_hit = True
        self.hit_timer = None
        self.hit_time = None

        self.health = 100
        self.max_health =  self.health
        self.flip = "right"
        self.exp = 0
        self.max_exp = 100
        self.paused = False
        self.level_pause = 1
        self.level_up_status = False
        

    def import_assets(self, path):
        self.animations = {}

        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(folder[2], key = lambda string: int(string.split(".")[0])):
                    path = folder[0].replace('\\', "/") + "/" + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split("\\")[1]
                    self.animations[key].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()
        
        if not self.paused:
            if keys[pygame.K_d]:
                self.direction.x = 1
                self.save_direction = "right"
                self.status = "right_run"
                self.gun_direction = "right"
                self.flip = "right"

            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = "left_run"
                self.save_direction = "left"
                self.gun_direction = "left"
                self.flip = "left"
            else:
                self.direction.x = 0
                if self.save_direction == "right":
                    self.status = "right_idle"
                elif self.save_direction == "left":
                    self.status = "left_idle"
            
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.gun_direction = "up"
                self.save_direction = "up"
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.gun_direction = "down"
                self.save_direction = "down"
            else:
                self.direction.y = 0

            if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
                self.attacking = True
            else:
                self.attacking = False

            if keys[pygame.K_1]:
                self.current_weapon = "pistol"
            if keys[pygame.K_2]:
                self.current_weapon = "rifle"
            if keys[pygame.K_3]:
                self.current_weapon = "shotgun"
            if keys[pygame.K_4]:
                self.current_weapon = "sword"


    

    def can_get_hit_timer(self):
        if not self.can_get_hit:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time > 700:
                self.can_get_hit = True
    
    def experience(self):
        if self.exp >= self.max_exp:
            self.level_up_status = True
            self.exp = 0
            self.max_exp = int(self.max_exp * 1.2)


    def update(
        self,
        dt, 
        display_surface_not_used, 
        current_weapon,
        ):
        self.experience()
        self.animate(dt)
        self.input()
        self.can_get_hit_timer()
        self.move(dt)
        if self.paused == True:
            self.level_pause = 0
        else:
            self.level_pause = 1


                    
    
