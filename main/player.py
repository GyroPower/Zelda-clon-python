import pygame 
from debug import debug
from os import walk
from support import import_folder
from settings import *
from entity import Entity 

class Player(Entity):
    
    def __init__(
        self,
        pos,
        groups,
        obstacles_sprites,
        create_weapon,destroy_weapon,
        create_magic):
        
        super().__init__(groups)
        self.image = pygame.image.load("graphics/test/player.png")
        self.rect =self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10,HITBOX_OFFSET['player'])
        self.sprite_type = "player"
        # stats
        self.stats = {"health":100,"energy":60,"attack":10,"magic":4,"speed":7}
        self.max_stats = {"health":300,"energy":140,"attack":20,"magic":10,"speed":10}
        self.upgrade_cost = {"health":100,"energy":100,"attack":100,"magic":100,"speed":100}
        
        
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 10000
        self.damage = self.stats['attack']
        self.magic_damage = self.stats['magic']
        # setup animations
        self.import_player_assets()
        
        self.status = "down"
        # movement
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = self.stats['speed']
        
        
        #collisions sprites 
        self.obstacles_sprites = obstacles_sprites
        
        # attack 
        self.attacking = False 
        self.attack_cooldown = 400
        self.attack_time = None 
        
        # vulnerability 
        self.vulnerable = True 
        self.invincible_time = 700
        self.invincible_timer = None 
        
        # magic setup 
        self.create_magic = create_magic
        self.magic_index =0
        self.magics = list(magic_data.keys())
        self.magic = self.magics[self.magic_index]
        self.change_magic = False 
        self.change_magic_cooldown = 400 
        self.change_magic_time = None 
        
        # weapon creation and choicing
        self.create_weapon = create_weapon
        self.destror_weapon = destroy_weapon
        self.weapon_index = 0
        self.weapons = list(weapons_data.keys())
        self.weapon = self.weapons[self.weapon_index]
        self.change_weapon = False 
        self.change_weapon_cooldown = 400 
        self.change_weapon_time = None 
    
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not self.attacking:
                if "attack" in self.status:
                    
                    self.status = self.status.replace("_attack","_idle")
                else:
                    self.status += "_idle" 
            
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0 
            
            if not "attack" in self.status:
                if "idle" in self.status:
                    self.status= self.status.replace("_idle","_attack")
                else:
                    self.status += "_attack"
    
    def get_value_by_index(self,index):
        return list(self.stats.values())[index]
    
    def get_cost_by_index(self,index):
        return list(self.upgrade_cost.values())[index]

    def animate(self):
        
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed 
        
        if self.frame_index >= len(animation): self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=(self.hitbox.center))
        
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def input(self):
        keys = pygame.key.get_pressed()
            
        if not self.attacking:
            
            
            # move
            if keys[pygame.K_d]:
                self.direction.x =1
                self.status = "right"
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = "left" 
            else:
                self.direction.x = 0 
                
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = "up" 
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = "down" 
            else:
                self.direction.y = 0 
            
            # attack 
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_weapon()
                
                
            # magic 
            if keys[pygame.K_c]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                
                
                style = self.magic
                strength = magic_data[self.magic]['strength']+self.stats['magic']
                cost = magic_data[self.magic]['cost']
                
                self.create_magic(style,strength,cost)
                
                
                
                
        
            if keys[pygame.K_e]:
                if not self.change_weapon:
                    self.change_weapon = True
                    self.change_weapon_time = pygame.time.get_ticks() 
                    self.weapon_index +=1
                    
                    
                    
                    if self.weapon_index >= len(self.weapons):
                        self.weapon_index = 0 
                    self.weapon = self.weapons[self.weapon_index]
            
            if keys[pygame.K_q]:
                if not self.change_weapon:
                    self.change_weapon = True
                    self.change_weapon_time = pygame.time.get_ticks() 
                    self.weapon_index -=1
                    
                    if self.weapon_index <0:
                        self.weapon_index = len(self.weapons)-1 
                    self.weapon = self.weapons[self.weapon_index]
                
            if keys[pygame.K_f]:
                if not self.change_magic:
                    self.change_magic = True
                    self.change_magic_time = pygame.time.get_ticks() 
                    self.magic_index +=1
                    
                    
                    
                    if self.magic_index >= len(self.magics):
                        self.magic_index = 0 
                    self.magic = self.magics[self.magic_index]
            
            if keys[pygame.K_v]:
                if not self.change_magic:
                    self.change_magic = True
                    self.change_magic_time = pygame.time.get_ticks() 
                    self.magic_index -=1
                    
                    
                    
                    if self.magic_index < 0:
                        self.magic_index = len(self.magics)-1
                    self.magic = self.magics[self.magic_index]
            
    def import_player_assets(self):
        player_path = "graphics/player/"
        
        self.animations = {
            "up":[],
            "down":[],
            "right":[],
            "left":[],
            
            "up_idle":[],
            "down_idle":[],
            "left_idle":[],
            "right_idle":[],
            
            "up_attack":[],
            "down_attack":[],
            "left_attack":[],
            "right_attack":[]
        }
        
        
        for animation in self.animations.keys():
            full_path = player_path+animation
            self.animations[animation] = import_folder(full_path)
    
    def get_full_weapon_damage(self):
        damage = weapons_data[self.weapon]['damage']
    
        return damage + self.damage
    
    def get_full_magic_damage(self):
        damage = magic_data[self.magic]['strength']
        
        return damage + self.magic_damage
    
    def get_damage(self,damage):
        if self.vulnerable:
            self.vulnerable = False 
            self.health -= damage 
            self.invincible_timer = pygame.time.get_ticks()
    
    def get_energy(self):
        if self.energy < self.stats['energy'] and not self.attacking:
            self.energy +=0.09
        elif self.energy >= self.stats['energy']:
            self.energy = self.stats['energy']
        
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        if self.attacking :
            if current_time - self.attack_time >= self.attack_cooldown + weapons_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destror_weapon()
        
        if self.change_weapon:
             
            if current_time - self.change_weapon_time >= self.change_weapon_cooldown:
                
                self.change_weapon = False
        
        if self.change_magic:
             
            if current_time - self.change_magic_time >= self.change_magic_cooldown:
                
                self.change_magic = False
        
        if not self.vulnerable:
            if current_time - self.invincible_timer >= self.invincible_time:
                self.vulnerable = True
    
    def update(self):
        
        self.cooldowns()
        self.input()
        self.move(self.stats['speed'])
        self.get_status()
        self.animate()
        self.get_energy()
        
        