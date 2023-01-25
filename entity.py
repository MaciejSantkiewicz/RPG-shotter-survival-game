import pygame, sys
from pygame.math import Vector2 as vector
from os import walk

class Entity(pygame.sprite.Sprite): #base class for all character in the game
    def __init__(self, pos, groups,  path, collision_sprites):
        super().__init__(groups)
        self.import_assets(path)

        self.frame_index = 0
        self.status = "right_idle"
        self.current_weapon = "pistol"
        self.level_pause = 1

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        self.pos = vector(self.rect.center)
        self.direction = vector()
        self.speed = 100
        self.save_direction = "right"

        self.hitbox = self.rect.inflate(-self.rect.width*0.4, self.rect.height / 2)
        self.collision_sprites = collision_sprites

        self.attacking = None
        self.animation_speed = 10

        self.health = 3
        self.monster_damage = None

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


    def move(self, dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * (self.speed*self.level_pause) * dt
        self.hitbox.centerx = self.pos.x
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")


        self.pos.y += self.direction.y * (self.speed*self.level_pause) * dt
        self.hitbox.centery = self.pos.y
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
        self.image = current_animation[int(self.frame_index)]

    def damage(self, monster_damage):
        self.health -= monster_damage
 
        if self.health <= 0:
            pygame.quit()
            sys.exit()

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0: # moving right 
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx

                else: # vertical
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery
    