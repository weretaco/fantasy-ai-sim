import math
import os
import pygame


class Unit:
   position: tuple[int, int]
   target: tuple[int, int]

   real_pos: tuple[float, float]

   def __init__(self, position: tuple[int, int]):
      self.position = position
      self.target = [position[0], position[1]]
      self.real_pos = [float(position[0]), float(position[1])]

   def render(self, screen: pygame.Surface):
      pygame.draw.circle(screen, (255, 0, 0), self.position, 25)
      #pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((935, 515), (50, 50)))
   
   def move(self, timeElapsed: int):
      speed: float = 200.0
      dist: float = float(float(timeElapsed) * float(speed)) / float(1000.0)

      real_target = [float(self.target[0]), float(self.target[1])]

      remainingDist = math.hypot(real_target[0] - self.real_pos[0], real_target[1] - self.real_pos[1])

      print(f"Elapsed time: {timeElapsed}")
      print(f"Dist: {dist}, Remaining Dist: {remainingDist}")

      if remainingDist <= dist:
         self.real_pos = real_target
      else:
         self.real_pos = (self.real_pos[0] + ((real_target[0] - self.real_pos[0]) / remainingDist * dist),
                          self.real_pos[1] + ((real_target[1] - self.real_pos[1]) / remainingDist * dist))

      print(f"real pos: {self.real_pos}")

      self.position = (int(self.real_pos[0]), int(self.real_pos[1]))

      print(f"final pos: {self.position}")


class AIGame:
   units: [Unit]

   def __init__(self):
      self.units = []


def main():
   print("Welcome to the simulation!")

   game = AIGame()

   for test in game.units:
      print(test.x)

   SCREEN_WIDTH = 800
   SCREEN_HEIGHT = 600

   init()

   info = pygame.display.Info()
   #SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
   
   screen = create_window(SCREEN_WIDTH, SCREEN_HEIGHT)

   game_loop(screen, game)

   cleanup()

def init():
   os.environ["SDL_VIDEO_CENTERED"] = '1'

   pygame.init()

def create_window(width, height) -> pygame.Surface:
   #return pygame.display.set_mode((width, height), pygame.RESIZABLE)
   return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
   #return pygame.display.set_mode((width, height), pygame.FULLSCREEN)

def cleanup():
   pygame.quit()

def game_loop(screen: pygame.Surface, game: AIGame):
   playerPos = (500, 500)

   playerRect = pygame.Rect(playerPos, (50, 50))
   player = Unit(playerRect.center)

   running = True

   timeLastFrame = pygame.time.get_ticks()

   while running:

      timeThisFrame = pygame.time.get_ticks()
      timeElapsed = timeThisFrame - timeLastFrame
      timeLastFrame = timeThisFrame

      # TODO: Perhaps handle this using events instead
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
         if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()

            #game.units.append(Unit(mouse_pos))
            player.target = mouse_pos
         elif event.type == pygame.QUIT:
            running = False

      player.move(timeElapsed)

      renderFrame(screen, game, player, playerRect)

      pygame.display.update()

def renderFrame(screen: pygame.Surface, game: AIGame, player: Unit, playerRect: pygame.Rect):
   screen.fill((0, 0, 0))

   #pygame.draw.rect(screen, (255, 0, 0), pygame.Rect((935, 515), (50, 50)))

   player.render(screen)

   for u in game.units:
      u.render(screen)

   drawMap(screen, (960, 540), 10, 10, 100, playerRect)

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