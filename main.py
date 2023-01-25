import pygame, sys
from settings import *
from player import Player
from pygame.math import Vector2 as vector
from weapon import Weapon
from pytmx.util_pygame import load_pygame
from sprite import Sprite, Bullet, SkillBox, Ammo, EnemyWeapon
from enemy import Monster
from random import randint


class AllSprites(pygame.sprite.Group): #class that loads and updates all sprites on the screen
    def __init__(self):
        super().__init__()
        self.offset = vector()
        self.display_surface = pygame.display.get_surface()
        self.bg = pygame.image.load("map/map.png").convert()
        


    def customize_draw(self, player):  #function for "camera" that follows the player
        self.offset.x = player.rect.centerx - WINDOW_WIDTH/2 
        self.offset.y = player.rect.centery - WINDOW_HEIGHT/2

        self.display_surface.blit(self.bg, -self.offset)

        for sprite in self.sprites():
            offset_rect = sprite.image.get_rect(center = sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image,offset_rect)



class Game(): #game loop class
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bullet_surf = pygame.image.load("sprites/muzzle/bullet.png").convert_alpha()
        self.clock = pygame.time.Clock()

        self.all_sprites = AllSprites()
        self.obstacles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.ammo_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.weapon_group = pygame.sprite.Group()

        
        self.pause = False
        self.speed_boost = 0
        
        

        self.setup()

        self.enemies_timer = pygame.event.custom_type() 
        pygame.time.set_timer(self.enemies_timer, 5000)

        self.enemy_speed_boost_timer = pygame.event.custom_type() 
        pygame.time.set_timer(self.enemy_speed_boost_timer, 10000)

        self.spawn_limit = len(self.monsters)
        self.max_monster = 12 
        self.can_spawn = True
        self.general_font = pygame.font.Font('font/font.ttf',50)
        self.exp_bonus = 10



       


    def create_bullet(self, pos, direction, speed): #creates projectiles for all weapons
        Bullet(pos, direction, self.bullet_surf, [self.all_sprites, self.bullets], speed,)


    def setup(self):

        self.weapon_create_bullet = self.create_bullet
        self.tmx_map = load_pygame('map/map.tmx')
        
		
		# tiles
        for x, y, surf in self.tmx_map.get_layer_by_name('Border').tiles():
            Sprite((x * 64, y * 64),surf,[self.all_sprites, self.obstacles])

		# objects
        for obj in self.tmx_map.get_layer_by_name('Object'):
            Sprite((obj.x, obj.y),obj.image,[self.all_sprites, self.obstacles])

        for obj in self.tmx_map.get_layer_by_name('Entities'):
            if obj.name == "Player":
                self.player = Player(
                    pos = (obj.x, obj.y), 
                    groups = [self.all_sprites, self.player_group], 
                    path = PATHS["player"], 
                    collision_sprites = self.obstacles,

                    )
            

        

        self.weapon = Weapon([self.all_sprites, self.weapon_group ], self.weapon_create_bullet, self.player, self.pause, [], 0)
        
        self.skill_box = SkillBox(self.all_sprites, (self.player.pos[0], self.player.pos[1]-150), self.pause)
   



        
        
           
 
    def display_stats(self):  
        self.weapon_d_image = pygame.image.load(f"sprites/guns/{self.player.current_weapon}/right.png").convert_alpha()
        scaled_w = self.weapon_d_image.get_width()
        scaled_h = self.weapon_d_image.get_height()
    
        self.scaled_image = pygame.transform.scale(self.weapon_d_image,(scaled_w*4, scaled_h*4))
        self.weapon_d_rect = self.weapon_d_image.get_rect(bottomleft = (100, WINDOW_HEIGHT - 100))
        self.display_surface.blit(self.scaled_image, self.weapon_d_rect)

        self.font = pygame.font.Font('font/font.ttf',50)
        self.display_weapon_name = f"{self.player.current_weapon}"
        self.display_weapon_name_surf = self.font.render(self.display_weapon_name.capitalize(), False ,"Black" )
        self.display_weapon_name_rect =  self.display_weapon_name_surf.get_rect(midleft = (100, WINDOW_HEIGHT - 30))
        self.display_surface.blit(self.display_weapon_name_surf, self.display_weapon_name_rect)

        self.display_player_health = f"Health: {self.player.health} / {self.player.max_health}"
        self.display_player_health_surf = self.font.render(self.display_player_health, False ,"Black" )
        self.display_player_health_rect =  self.display_player_health_surf.get_rect(midleft = (700, WINDOW_HEIGHT - 30))
        self.display_surface.blit(self.display_player_health_surf, self.display_player_health_rect)

        self.display_monster_count = f"Monsters left: {self.spawn_limit}"
        self.d_m_c_surf = self.font.render(self.display_monster_count, False, 40)
        self.d_m_c_rect = self.d_m_c_surf.get_rect(midbottom = (WINDOW_WIDTH/2, 50))
        self.display_surface.blit(self.d_m_c_surf, self.d_m_c_rect)

        self.display_speed = f"Speed: {self.player.speed}"
        self.d_s_surf = self.font.render(self.display_speed, False, 40)
        self.d_s_rect = self.d_m_c_surf.get_rect(midleft = (100, 50))
        self.display_surface.blit(self.d_s_surf, self.d_s_rect)

        self.display_exp = f"Experience: {self.player.exp}/{self.player.max_exp}"
        self.exp_surf = self.font.render(self.display_exp, False, 40)
        self.exp_rect = self.exp_surf .get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT - 100))
        self.display_surface.blit(self.exp_surf, self.exp_rect)

        if self.player.current_weapon == "pistol":  
            self.ammo = self.weapon.pistol_ammo
        elif self.player.current_weapon == "rifle":
            self.ammo = self.weapon.rifle_ammo
        elif self.player.current_weapon == "shotgun":
            self.ammo = self.weapon.shotgun_ammo
        self.ammo_text = f"Ammo: {self.ammo}"
        self.ammo_surf = self.font.render(self.ammo_text, False ,"Black" )
        self.ammo_rect = self.ammo_surf.get_rect(midleft = (300, WINDOW_HEIGHT - 30))
        self.display_surface.blit(self.ammo_surf, self.ammo_rect)

  
    def bullet_collison(self):

        if self.player.current_weapon == "sword" and self.player.attacking:
            for bullet in self.weapon_group.sprites():
                sprites = pygame.sprite.spritecollide(bullet, self.monsters, False)
                for sprite in sprites:
                    sprite.killed()

        for obstacle in self.obstacles.sprites():
            pygame.sprite.spritecollide(obstacle, self.bullets, True)
        
        for bullet in self.bullets.sprites():
            sprites = pygame.sprite.spritecollide(bullet, self.monsters, False)
            for sprite in sprites:
                sprite.killed()

            ammo_change = randint(1,5)
            ammo_picks_chances = randint(1,100)
            ammo_types = ["","rifleammo", "shotgunammo", "pistolammo", "lvlbox", "medkit"]
            if ammo_picks_chances <= 30:
                ammo_pick = 3
            elif ammo_picks_chances > 30 <= 45:
                ammo_pick = 2
            elif ammo_picks_chances > 45 <= 70:
                ammo_pick = 1
            elif ammo_picks_chances > 70 <= 90:
                ammo_pick = 5
            elif ammo_picks_chances > 90 <= 100: 
                ammo_pick = 4


            
            if sprites:
                if ammo_change == 1:
                    Ammo([self.all_sprites, self.ammo_group], bullet.pos, ammo_types[ammo_pick])
                bullet.kill()

                self.player.exp = self.player.exp + (10 + self.exp_bonus) 

    
    def collect_ammo(self):
        for ammo in self.ammo_group.sprites():
            sprites = pygame.sprite.spritecollide(ammo, self.player_group, False)
            if sprites:
                if ammo.type == "rifleammo":
                    self.weapon.rifle_ammo += 120
                if ammo.type == "shotgunammo":
                    self.weapon.shotgun_ammo += 30
                if ammo.type == "pistolammo":
                    self.weapon.pistol_ammo += 60
                if ammo.type == "lvlbox":
                    self.add_exp = self.player.max_exp - self.player.exp
                    self.player.exp += self.add_exp
                if ammo.type == "medkit":
                    self.heal = 100
                    self.max_heal = self.heal + self.player.health
                    if self.max_heal > self.player.max_health:
                        self.player.health = self.player.max_health
                ammo.kill()


    
    def spawn_enemies(self):
        for obj in self.tmx_map.get_layer_by_name('Entities'):
            if obj.name == "Enemy":
                self.enemy = Monster(
                    pos = (obj.x, obj.y), 
                    groups = [self.all_sprites, self.monsters],
                    path = PATHS["enemy"], 
                    collision_sprites = self.obstacles,
                    player = self.player,
                    speed = self.speed_boost
                            )
        for enemy in self.monsters.sprites():
            weapons = EnemyWeapon(self.all_sprites, enemy.rect.midright, enemy = enemy)

                



            

            



    def run(self):
        while True:
			# event loop 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == self.enemies_timer and self.spawn_limit < self.max_monster and self.can_spawn:
                    self.spawn_enemies()
                    self.max_monster += 1
                if event.type == self.enemy_speed_boost_timer and self.spawn_limit > 0:
                    self.speed_boost = self.speed_boost + 2
                    self.exp_bonus = int(self.exp_bonus*1.2)
                    
            keys = pygame.key.get_pressed()
            


            self.spawn_limit = len(self.monsters)


            

            dt = self.clock.tick() / 1000
            self.skill_box.status = self.pause

            self.all_sprites.update(dt, 
                self.display_surface, 
                self.player.current_weapon,
                )
            
            self.weapon.draw_weapon(
                self.player.rect.center,  
                self.player.save_direction,
                self.player.current_weapon,
                )




            
            self.display_surface.fill("black")
            self.all_sprites.customize_draw(self.player)

            self.bullet_collison()
            self.collect_ammo()
            self.display_stats()

            self.roll_skill = True
            self.can_roll = True


            if self.player.level_up_status == True:
                self.pause = True
                self.skill_box.active = True
                self.player.attacking = False

                self.skill_box.pos = (self.player.pos[0], self.player.pos[1]-150)
                self.can_spawn = False
                self.player.paused = True
                for bullet in self.bullets.sprites():
                    bullet.speed = 0
                if self.spawn_limit > 0:
                    for monster in self.monsters.sprites():
                        monster.speed = 0

            if self.pause == True and self.skill_box.active:
                self.display_bonus = f"{self.skill_box.name}"
                self.display_bonus_surf = self.general_font.render(self.display_bonus, False, 40)
                self.display_bonus_rect = self.display_bonus_surf .get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2+50))
                self.display_surface.blit(self.display_bonus_surf, self.display_bonus_rect)

                if keys[pygame.K_ESCAPE] or keys[pygame.K_SPACE]:
                    if self.skill_box.select_type == 1:
                        self.player.speed += 10
  
                    if self.skill_box.select_type == 2:
                        self.weapon.add_projectal.append("X")

                    if self.skill_box.select_type == 3:
                        self.weapon.add_bullet_speed += 20 

                    if self.skill_box.select_type == 4:
                        self.player.max_health += 25 
                        self.heal = 25
                        self.player.health += self.heal
                        self.max_heal = self.heal + self.player.health
                        if self.max_heal > self.player.max_health:
                            self.player.health = self.player.max_health     

                        
                    self.pause = False
                    self.player.paused = False
                    for bullet in self.bullets.sprites():
                        bullet.speed = 800
                    if self.spawn_limit > 0:
                        for monster in self.monsters.sprites():
                            monster.speed = randint(50,80)
                    self.can_spawn = True
                    self.player.level_up_status = False

            

            


            pygame.display.update()
if __name__ == '__main__':
	game = Game()
	game.run()