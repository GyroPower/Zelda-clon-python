import pygame 
from settings import *

class Tile(pygame.sprite.Sprite):
    
    def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILE_SIZE,TILE_SIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface 
        y = HITBOX_OFFSET[sprite_type][1]
        x = HITBOX_OFFSET[sprite_type][0]
        
        if self.sprite_type == "object":
            self.rect = self.image.get_rect(topleft=(pos[0],pos[1]-TILE_SIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(x,y)
        
        
        
    