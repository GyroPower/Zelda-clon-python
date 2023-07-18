import pygame
from settings import * 

class MagicPlayer:
    
    def __init__(self,animation_player):
        self.animation_player = animation_player
         
    
    def heal(self,player,strength,cost,groups):
        
        
        if player.energy >= cost:
            player.health += strength
            player.energy -= cost 
            
            off_set = pygame.math.Vector2(0,-40)
            self.animation_player.generate_particles("aura",player.rect.center,groups)
            self.animation_player.generate_particles("heal",player.rect.center+off_set,
                                                     groups)
            
        else:
            print("you have no mana")    
            
        if player.health >= player.stats['health']:
            player.health = player.stats['health']
        
        
    
    def flame(self,player,strength,cost,groups):
        
        if player.energy >= cost:
            player.energy -= cost
            direction = player.status.split("_")[0] 

            
            offset_y =  pygame.math.Vector2(0,16)
            offset_x = pygame.math.Vector2(-15,0)
            
                # placement
            if "down" in direction:
                offset = pygame.math.Vector2(0,28)
                for i in range(5):
                    self.animation_player.generate_particles(
                        "flame",player.rect.midbottom + offset_x+offset,groups)
                    offset.y +=28
                
            elif "up" in direction:
                offset = pygame.math.Vector2(0,-28)
                
                for i in range(5):
                    self.animation_player.generate_particles(
                        "flame", player.rect.midtop + offset_x+offset,groups)
                    offset.y -=28
            
            elif "left" in direction:
                offset = pygame.math.Vector2(-28,0)
                for i in range(5):
                    self.animation_player.generate_particles(
                        "flame",player.rect.midleft +offset_y+offset,groups)
                    offset.x -=28
                
                
            elif "right" in direction:
                offset = pygame.math.Vector2(28,0)
                
                for i in range(5):
                    self.animation_player.generate_particles(
                        "flame", player.rect.midright + offset_y+offset,groups)
                    offset.x +=28
                
            