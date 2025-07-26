import os
import pygame

def main():
   print("Welcome to the simulation!")

   SCREEN_WIDTH = 800
   SCREEN_HEIGHT = 600

   init()

   info = pygame.display.Info()
   #SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
   
   screen = create_window(SCREEN_WIDTH, SCREEN_HEIGHT)

   game_loop(screen)

   cleanup()

def init():
   os.environ["SDL_VIDEO_CENTERED"] = '1'

   pygame.init()

def create_window(width, height):
   #return pygame.display.set_mode((width, height), pygame.RESIZABLE)
   return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
   #return pygame.display.set_mode((width, height), pygame.FULLSCREEN)

def cleanup():
   pygame.quit()

def game_loop(screen):
   playerPos = (500, 500)

   player = pygame.Rect(playerPos, (50, 50))

   running = True

   while running:

      keys = pygame.key.get_pressed()

      x = 0
      y = 0

      if keys[pygame.K_a]:
         x = -1
      elif keys[pygame.K_d]:
         x = 1
      elif keys[pygame.K_w]:
         y = -1
      elif keys[pygame.K_s]:
         y = 1
      elif keys[pygame.K_ESCAPE]:
         running = False

      if x != 0 or y != 0:
         player.move_ip(x, y)

      # Process Events
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            running = False
      
      renderFrame(screen, player)

      pygame.display.update()

def renderFrame(screen, player):
   screen.fill((0, 0, 0))

   pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((935, 515), (50, 50)))

   drawMap(screen, (960, 540), 10, 10, 100, player)

def drawMap(screen: pygame.Surface, center: tuple[int, int], width: int, height: int, tileSize: int, player: pygame.Rect):
   start = (center[0] - ((width - 1) * tileSize // 2), center[1] - ((height - 1) * tileSize // 2))
   playerOffset = ((width * tileSize // 2) - player.left, (height * tileSize // 2) - player.top)

   for i in range(width):
      for j in range(height):
         drawTile(screen, (start[0] + playerOffset[0] + i * tileSize, start[1] + playerOffset[1] + j * tileSize), tileSize)

def drawTile(screen: pygame.Surface, center: tuple[int, int], size: int):
   start = size // 2
   tileRect = pygame.Rect((center[0] - start, center[1] - start), (size, size))

   pygame.draw.rect(screen, (0, 255, 0), tileRect, 2)

main()