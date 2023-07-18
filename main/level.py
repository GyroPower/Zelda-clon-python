import pygame 
from settings import *
from tile import Tile
from player import Player
from enemy import Enemy
from weapons import Weapon
from camera import YSortCameraGroup
from Ui import UI 
from support import import_folder,import_layers,import_csv_layout,import_cut_graphics
from particles import AnimationPlayer
from random import randint
from magic import MagicPlayer
from upgrade import Upgrade


class Level:
    
    def __init__(self):
        
        #sprite group setup 
        self.visible_sprites = YSortCameraGroup()
        self.collide_sprites = pygame.sprite.Group() 
        self.display_surf = pygame.display.get_surface()
        
        # attack sprites
        self.current_attack_player = None 
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        
        # UI
        self.ui = UI()
        self.game_paused = False 
        
        
        # map
        layers = import_layers("Level/levels/0/level-layers")
        
        for layer in layers:
            layout = import_csv_layout(layers[layer])
            self.create_map(layout,layer)
        
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)
        self.Upgrade = Upgrade(self.player)
            
    def create_weapon(self):
        self.current_attack_player= Weapon(self.player,
                                           [self.visible_sprites,self.attack_sprites])
        
    def destroy_attack(self):
        if self.current_attack_player:
            self.current_attack_player.kill()
            self.current_attack_player = None 
    
    def create_magic(self,style,strength,cost):
        
        if style == "heal":
            self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])
        elif style == "flame":
            self.magic_player.flame(self.player,strength,cost,[self.visible_sprites,self.attack_sprites])
    
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites= pygame.sprite.spritecollide(
                    attack_sprite,self.attackable_sprites,False)

                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "grass":
                            pos = target_sprite.rect.center
                            for leaf in range(randint(2,4)):
                                self.animation_player.create_grass_particles(
                                    pos,
                                    [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)
                            
                           
                            
    def damage_player(self,amount,attack_type):
        self.player.get_damage(amount)
        self.animation_player.generate_particles(attack_type,self.player.rect.center
                                                 ,self.visible_sprites)
    
    def trigger_death_particles(self,part_type,pos):
        self.animation_player.generate_particles(part_type,pos,self.visible_sprites)
                
    def add_exp(self,amount):
        self.player.exp += amount 
      
    def toggle_menu(self):
        self.game_paused = not self.game_paused
      
    def create_map(self,layout,type):
        # for row_index,row in enumerate(WORLD_MAP):
        #     for col_index, col in enumerate(row):
        #         x = col_index * TILE_SIZE
        #         y = row_index * TILE_SIZE
                
        #         if col == "X":
        #             Tile((x,y),[self.visible_sprites,self.collide_sprites])

        #         if col == "P":
        #             self.player = Player((x,y),[self.visible_sprites],self.collide_sprites)
        
        i = 0
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                
                if col != "-1":
                    y = row_index * TILE_SIZE
                    x = col_index * TILE_SIZE
                    
                    if type.__contains__("entities"):
                        if col == "394":
                            self.player = Player(
                                (x,y),
                                [self.visible_sprites],
                                self.collide_sprites,
                                self.create_weapon,
                                self.destroy_attack,
                                self.create_magic)
                        else:
                            if col == "390": monster = "bamboo"
                            elif col == "391":monster = "spirit"
                            elif col == "392": monster = "raccoon"
                            elif col == "393": monster = "squid"
                            
                            Enemy([self.visible_sprites,self.attackable_sprites],
                                  monster,(x,y),self.collide_sprites,self.damage_player,
                                  self.trigger_death_particles,self.add_exp)
                        
                    if type.__contains__("block_floor"):     
                        Tile((x,y),[self.collide_sprites],"invisible")
                   
                    if type.__contains__("grass"):
                        grass_tile_list = import_folder("graphics/grass")
                        surf = grass_tile_list[int(col)]
                        Tile((x,y),[self.visible_sprites,self.attackable_sprites,
                                    self.collide_sprites],"grass",surf)
                   
                    if type.__contains__("Objects"):
                        objects_tile_list = import_folder("graphics/objects")
                        surf = objects_tile_list[int(col)]
                        Tile((x,y),[self.visible_sprites,self.collide_sprites],
                             "object",surf)
        
                
    def run(self,dt):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        if self.game_paused:
            self.Upgrade.display()
        else:
            self.visible_sprites.enemy_update(self.player)
            self.visible_sprites.update()
            self.player_attack_logic()