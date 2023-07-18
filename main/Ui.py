from settings import *
import pygame 

class UI:
    def __init__(self) -> None:
        # general 
        self.display_surfa = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
        
        # bar setup 
        self.health_bar_rect = pygame.rect.Rect(10,20,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.energy_bar_rect = pygame.rect.Rect(10,40,ENERGY_BAR_WIDTH,BAR_HEIGHT)
        
        #convert weapon_dic
        self.weapon_graphics = []
        self.magic_graphics = []
        
        for magic in magic_data.values():
            path = magic['graphic']
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)
        
        for weapon in weapons_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)
                
    def show_bar(self,current_amount,max_amount,back_rect,color):
        pygame.draw.rect(self.display_surfa,UI_BG_COLOR,back_rect)
        
        ratio = current_amount / max_amount 
        current_width = back_rect.width * ratio 
        
        current_rect = back_rect.copy()
        current_rect.width = current_width
        
        #draw_rct 
        pygame.draw.rect(self.display_surfa,color,current_rect)
        pygame.draw.rect(self.display_surfa,UI_BORDER_COLOR,back_rect,3)
    
    def show_exp(self,exp):
        text_surf = self.font.render(str(int(exp)),False,TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomright=(WINDOW_WIDTH-15,WINDOW_HEIGHT-10))
        
        pygame.draw.rect(self.display_surfa,UI_BG_COLOR,text_rect.inflate(10,10))
        self.display_surfa.blit(text_surf,text_rect)
        
        pygame.draw.rect(self.display_surfa,UI_BORDER_COLOR,text_rect.inflate(10,10),3)
    
    def show_selection_box(self,left,top,change_param=False):
        bg_rect = pygame.rect.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surfa,UI_BG_COLOR,bg_rect)
        
        if change_param:
            pygame.draw.rect(self.display_surfa,UI_BORDER_COLOR_ON,bg_rect,3)
        else:
            pygame.draw.rect(self.display_surfa,UI_BORDER_COLOR,bg_rect,3)
        return bg_rect
    
    def weapon_overlay(self,weapon_index,change_param):
        
        bg_rect = self.show_selection_box(75,626,change_param)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=(bg_rect.centerx,bg_rect.centery))
        
        self.display_surfa.blit(weapon_surf,weapon_rect)
    
    def magic_overlay(self,magic_index,change_param):
        bg_rect = self.show_selection_box(10,630,change_param)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)
        self.display_surfa.blit(magic_surf,magic_rect)
        
    
    def display(self,player):
        self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
        self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOR)
        
        
        self.magic_overlay(player.magic_index,player.change_magic)
        self.weapon_overlay(player.weapon_index,player.change_weapon)
        self.show_exp(player.exp)
        