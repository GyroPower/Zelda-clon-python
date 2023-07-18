import pygame 
from settings import * 
from entity import Entity 
from support import import_folder
from debug import debug

class Enemy(Entity):
    def __init__(self,groups,monster_type,pos,obstacles_sprites,damage_player,
                 death_particles,add_exp):
        super().__init__(groups)
        
        # general setup 
        
        
        self.sprite_type = "enemy"
        self.status = "idle"
        self.monster_name = monster_type
        self.monster_stats = monster_data[monster_type]
        self.speed = self.monster_stats['speed']
        self.exp = self.monster_stats['exp']
        self.health = self.monster_stats['health']
        self.damage = self.monster_stats['damage']
        self.attack_type = self.monster_stats['attack_type']
        self.attack_radius = self.monster_stats['attack_radius']
        self.notice_radius = self.monster_stats['notice_radius']
        self.resistance = self.monster_stats['resistance']
        
        #graph setup 
        self.import_graphics(monster_type)
        self.image = self.animations[self.status][self.frame_index] 
        self.rect = self.image.get_rect(topleft=pos)

        #movement
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacles_sprites = obstacles_sprites

        # player interaction 
        self.can_attack = True 
        self.attack_timer = None 
        self.attack = True
        self.damage_player = damage_player
        self.trigger_death_particles = death_particles
        self.give_exp = add_exp
        
        # invincibility timer
        self.vulnerable = True 
        self.hit_time = None 
        self.invicibility_duration = 300 
        
        if monster_type == 'raccoon':
            time = 1000
        elif monster_type == "bamboo":
            time = 400
        elif monster_type == "spirit":
            time = 500 
        elif monster_type == "squid":
            time = 600
        
        self.attack_time = time 

    def import_graphics(self,monster_type):
        self.animations = {"idle":[],"move":[],"attack":[]}
        
        monster_path = "graphics/monsters/"+monster_type+"/"
        
        for animation in self.animations.keys():
            full_path = monster_path + animation
            self.animations[animation] = import_folder(full_path)
            
    def animation(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed 
        
        if self.frame_index >= len(animation): 
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    def actions(self,player):
        if self.status == "attack" and self.attack:
            self.attack = False
            self.damage_player(self.damage,self.attack_type)
        elif self.status == "move" or not self.vulnerable:
            self.direction = self.get_player_dis_direct(player)[1] 
        else:
            self.direction = pygame.math.Vector2()
    
    def get_player_dis_direct(self,player):
        
    
        player_vector = pygame.math.Vector2(player.rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        
        distance  = (player_vector - enemy_vector).magnitude()
        
        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()
        
        
        return (distance,direction)
    
    def get_status(self,player):
        distance = self.get_player_dis_direct(player)[0]
        
        if distance <= self.attack_radius and self.can_attack and self.vulnerable and player.vulnerable:
            
            if self.status != "attack":
                self.frame_index = 0
            self.attack_timer = pygame.time.get_ticks()
            self.status = "attack"
            
        elif distance <= self.notice_radius and self.vulnerable:
            self.status= "move"
        else:
            self.status = "idle"
        
       

    def get_damage(self,player,attack_type):
        
        if self.vulnerable:
            
            self.direction = self.get_player_dis_direct(player)
            
            if attack_type == "weapon":
                self.health -= player.get_full_weapon_damage()
            elif attack_type == "magic":
                self.health -= player.get_full_magic_damage()

            self.vulnerable = False
            self.hit_time = pygame.time.get_ticks()
    
    def hit_react(self):
        if not self.vulnerable:
            self.direction *= -self.resistance
         
    def check_death(self):
        if self.health <=0 :
            self.trigger_death_particles(self.monster_name,self.rect.center)
            self.kill()
            self.give_exp_to_player()
    
    def give_exp_to_player(self):
        self.give_exp(self.exp)
    
    def timer(self):
        
        
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_timer >= self.attack_time:
                self.can_attack = True 
                self.attack = True
        
        if not self.vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time >= self.invicibility_duration:
                self.vulnerable = True 
        
      
    def update(self):
        self.hit_react()
        self.move(self.speed)
        self.animation()
        self.timer()
        self.check_death()
        
        
    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)