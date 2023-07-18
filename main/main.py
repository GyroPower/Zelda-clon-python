import pygame,sys,time 
from settings import * 
from level import Level
from debug import debug

class Game:
    
    def __init__(self):
        
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()
        pygame.display.set_caption("Zelda clon python")
        
    
    def run(self):
        prev_time = time.time()
        
        while True:
            dt = time.time() - prev_time
            prev_time = time.time()    
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()
                    
            self.screen.fill(WATER_COLOR)
            self.level.run(dt)
            pygame.display.update()
            self.clock.tick(FRAME_RATE)

            
if __name__ == "__main__":
    game = Game()
    game.run()