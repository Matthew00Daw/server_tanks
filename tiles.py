import pygame
from client.tilemap import TileMap

pygame.init()
 
dis=pygame.display.set_mode((500, 400))
pygame.display.update()
pygame.display.set_caption('Pygame')
 
game_over=False
tilemap = TileMap("resources\\tanks_sheet.png", (8, 4))
while not game_over:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over=True
    
    #dis.fill((255, 255, 0, 255))
    for i in range(4*8):
        surface = tilemap.get_tile(i)
        dis.blit(surface, (i*32, 0), pygame.Rect(0, 0, 32, 32))
        pygame.display.flip()
 
pygame.quit()
quit()