import pygame 
from os import walk  
from csv import reader 
from settings import * 


def import_csv_layout(path):
    layout_map = []
    with open(path) as map:
        level = reader(map,delimiter=",")
        
        for row in level:
            layout_map.append(list(row))
            
        return layout_map
    
def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    
    tile_num_x =  int(surface.get_size()[0] / TILE_SIZE) 
    tile_num_y =  int(surface.get_size()[1] / TILE_SIZE)
    
    cut_tiles = []
    
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            
            new_surf = pygame.Surface((TILE_SIZE,TILE_SIZE),flags= pygame.SRCALPHA)
            
            new_surf.blit(surface,(0,0),pygame.Rect(x,y,TILE_SIZE,TILE_SIZE))
            cut_tiles.append(new_surf)
            
    return cut_tiles 

def import_folder(path):
    frames = []
    for _,__,image_files in walk(path):
        for image in image_files:
            full_path = path+"/"+image 
            image_surf = pygame.image.load(full_path).convert_alpha()
            frames.append(image_surf)
            
    return frames

def import_layers(path):
    layers = {}
    
    for __,_,layer_file in walk(path):
        for layer in layer_file:
            full_path = path+"/"+layer 
            
            layers[layer] = full_path
            
    return layers