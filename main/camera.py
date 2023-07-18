from debug import debug
import pygame 
from player import Player

class YSortCameraGroup(pygame.sprite.Group):
    
    def __init__(self):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        
        self.half_width = self.display_surf.get_size()[0]//2
        self.half_height = self.display_surf.get_size()[1]//2
        
        
        
        self.floor_surf = pygame.image.load("graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))
        
    def center_camera(self,target:Player):
        self.offset.x = target.rect.centerx - self.half_width   
        self.offset.y = target.rect.centery - self.half_height   
    
    def custom_draw(self,target):
        
        self.center_camera(target)
        offset_pos_floor = self.floor_rect.topleft - self.offset 
        
        self.display_surf.blit(self.floor_surf,offset_pos_floor)
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery ):
            
            offset_pos = sprite.rect.topleft - self.offset
            
            self.display_surf.blit(sprite.image,offset_pos)
            
    def enemy_update(self,player):
        
        enemy_sprites = [sprite for sprite in self.sprites() if sprite.sprite_type == "enemy"]
        
        for sprite in enemy_sprites:
            sprite.enemy_update(player)