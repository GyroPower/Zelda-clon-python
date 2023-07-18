from typing import Any
import pygame

class Weapon(pygame.sprite.Sprite):
    
    def __init__(self,player,groups):
        super().__init__(groups)
        
        self.sprite_type = "weapon"
        
        direction = player.status.split("_")[0] 
        
        full_path = f"graphics/weapons/{player.weapon}/{direction}.png"
        
        # graphic
        self.image = pygame.image.load(full_path).convert_alpha()
        offset_y =  pygame.math.Vector2(0,16)
        offset_x = pygame.math.Vector2(-15,0)
        
        # placement
        if "down" in direction:
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + offset_x)
        elif "up" in direction:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + offset_x)
        elif "left" in direction:
            self.rect = self.image.get_rect(midright = player.rect.midleft +offset_y)
        elif "right" in direction:
            self.rect = self.image.get_rect(midleft = player.rect.midright + offset_y)  
        
    
