from multiprocessing import Value
import pygame 
from settings import * 

class Upgrade:
    
    def __init__(self,player):
        self.display_surf = pygame.display.get_surface()
        self.player = player 
        self.attribute_number = len(player.stats)
        self.attributes_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
        
        #selection system 
        self.selection_index = 0 
        self.selection_timer = None 
        self.can_move = True 
        
        #items dimension
        self.height = self.display_surf.get_size()[1] * 0.8
        self.width = self.display_surf.get_size()[0] // 6
        
        self.create_items()
        
    def input(self):
        keys = pygame.key.get_pressed()
        
        if self.can_move:
            
            if keys[pygame.K_LEFT]:
                self.selection_index -=1
                
                if self.selection_index<0:
                    self.selection_index = self.attribute_number - 1
                
                self.selection_timer = pygame.time.get_ticks()
                self.can_move = False 
                
            elif keys[pygame.K_RIGHT]:
                self.selection_index +=1
                
                if self.selection_index >= self.attribute_number:
                    self.selection_index = 0
                
                self.selection_timer = pygame.time.get_ticks()
                self.can_move = False 
            if keys[pygame.K_SPACE]:
                self.can_move = False 
                self.selection_timer = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)
    
    def create_items(self):
    
        self.item_list = []
        
        for item in range(self.attribute_number):
            index = item 
            full_width = self.display_surf.get_size()[0] 
            increment = full_width // self.attribute_number
            
            left = (item * increment) + (increment - self.width) // 2 
            top = self.display_surf.get_size()[1] * 0.1
            
            
            item = Item(left,top,self.width,self.height,index,self.font)
            self.item_list.append(item)
    
    def selection_cooldown(self):
        
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            
            if current_time - self.selection_timer >= 300:
                self.can_move = True
    
    def display(self):
        self.input()
        self.selection_cooldown()
        
        for item_index,item in enumerate(self.item_list):
            
            #get att
            name = self.attributes_names[item_index]
            value = self.player.get_value_by_index(item_index)
            max_value = self.max_values[item_index]         
            cost = self.player.get_cost_by_index(item_index)
               
            item.display(self.display_surf,self.selection_index,name,value,max_value,cost)    
        

class Item:
    
    def __init__(self,l,t,w,h,index,font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index 
        self.font = font 
        
    def display_names(self,surf,name,cost,selected):
        
        if selected:
            color = TEXT_COLOR_SELECTED
        else:
            color = TEXT_COLOR
        
        # title
        title_surf = self.font.render(name,False,color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))
        
        
        # cost
        cost_surf = self.font.render(str(cost),False,color)
        cost_rect = cost_surf.get_rect(midbottom = self.rect.midbottom + pygame.math.Vector2(0,-10))
        
        #draw
        surf.blit(title_surf,title_rect)
        surf.blit(cost_surf,cost_rect)
    
    def trigger(self,player):
        upgrade_att = list(player.stats.keys())[self.index]
        upgrade_cost = list(player.upgrade_cost.values())[self.index]
        
        if upgrade_cost != "max" and player.exp >= upgrade_cost:
            player.stats[upgrade_att] += int(player.stats[upgrade_att] * 0.15)
                
            
            if player.stats[upgrade_att] <= player.max_stats[upgrade_att]:
                
                if player.health == player.stats[upgrade_att]:
                    player.health += int(player.stats[upgrade_att] * 0.15)
                
                
                player.upgrade_cost[upgrade_att] += int(player.stats[upgrade_att] * 1.15)
                player.exp -= upgrade_cost
            else:
                player.stats[upgrade_att] = player.max_stats[upgrade_att]
                player.upgrade_cost[upgrade_att] = "max"
    
    def display_bar(self,surface,value,max_value,selected):
        top = self.rect.midtop + pygame.math.Vector2(0,60)
        bottom = self.rect.midbottom + pygame.math.Vector2(0,-60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR
        
        # bar_setup 
        full_height = bottom[1] - top[1]
        
        relative_num = (value) / max_value * full_height
        value_rect = pygame.Rect(top[0]-15,bottom[1]-relative_num,30,10)
                
        #draw 
        pygame.draw.line(surface,color,top,bottom,5)
        pygame.draw.rect(surface,color,value_rect)
    
    def display(self,surface,selection_num,name,value,max_value,cost):
        
        if selection_num == self.index:
            pygame.draw.rect(surface,UPGRADE_BG_COLOR_SELECTED,self.rect)
            pygame.draw.rect(surface,UI_BG_COLOR,self.rect,4)
        else:    
            pygame.draw.rect(surface,UI_BG_COLOR,self.rect)
            pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
            
        
        self.display_names(surface,name,cost,self.index==selection_num)
        self.display_bar(surface,value,max_value,self.index==selection_num)