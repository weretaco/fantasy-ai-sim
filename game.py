import math
import os
import pygame
import sys


class Unit:
   position: tuple[int, int]
   target: tuple[int, int]
   moving: bool

   real_pos: tuple[float, float]

   def __init__(self, position: tuple[int, int]):
      self.position = position
      self.target = [position[0], position[1]]
      self.moving = False
      self.real_pos = [float(position[0]), float(position[1])]

   def draw(self, screen: pygame.Surface, focus: tuple[int, int]):
      center = (screen.get_width() / 2, screen.get_height() / 2)

      pos = (center[0] + self.position[0] - focus[0], center[1] + self.position[1] - focus[1])

      pygame.draw.circle(screen, (255, 0, 0), pos, 25)

   def setTarget(self, target: tuple[int, int]):
      self.target = target
      self.moving = True
   
   def move(self, timeElapsed: int):
      if not self.moving:
         return

      speed: float = 200.0
      dist: float = float(float(timeElapsed) * float(speed)) / float(1000.0)

      real_target = [float(self.target[0]), float(self.target[1])]

      remainingDist = math.hypot(real_target[0] - self.real_pos[0], real_target[1] - self.real_pos[1])

      print(f"Elapsed time: {timeElapsed}")
      print(f"Dist: {dist}, Remaining Dist: {remainingDist}")

      if remainingDist <= dist:
         self.real_pos = real_target
         self.moving = False
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

   init()

   info = pygame.display.Info()

   #SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
   SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

   screen = create_window(SCREEN_WIDTH, SCREEN_HEIGHT)

   print(f"width: {screen.get_width()}, height: {screen.get_height()}")

   game_loop(screen, game)

   cleanup()

def init():
   os.environ["SDL_VIDEO_CENTERED"] = '1'

   pygame.init()

def create_window(width, height) -> pygame.Surface:
   #return pygame.display.set_mode((width, height), pygame.RESIZABLE)
   #return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
   return pygame.display.set_mode((width, height), pygame.FULLSCREEN)

def cleanup():
   print("Cleaning up...")
   #pygame.quit()
   sys.exit()
   print("Done cleaning up")

def game_loop(screen: pygame.Surface, game: AIGame):
   player = Unit([200, 200])

   running = True

   timeLastFrame = pygame.time.get_ticks()

   screenCenter = (screen.get_width() / 2, screen.get_height() / 2)

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
         print("Hello?!?!?!?!?")
         running = False

      # Process Events
      for event in pygame.event.get():
         if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()

            map_pos = (mouse_pos[0] - screenCenter[0] + player.position[0], mouse_pos[1] - screenCenter[1] + player.position[1])

            #game.units.append(Unit(mouse_pos))
            player.setTarget(map_pos)
         elif event.type == pygame.QUIT:
            running = False

      player.move(timeElapsed)

      renderFrame(screen, game, player)

      pygame.display.update()

   print("Exited loop")

def renderFrame(screen: pygame.Surface, game: AIGame, player: Unit):
   screen.fill((0, 0, 0))

   focus = player.position

   player.draw(screen, focus)

   for u in game.units:
      u.draw(screen)

   drawMap(screen, focus, 10, 10, 100)

def drawMap(screen: pygame.Surface, focus: tuple[int, int], width: int, height: int, tileSize: int):
   center = (screen.get_width() / 2, screen.get_height() / 2)

   halfTileSize = tileSize // 2
   start = (center[0] - focus[0] + halfTileSize, center[1] - focus[1] + halfTileSize)

   for i in range(width):
      for j in range(height):
         drawTile(screen, (start[0] + i * tileSize, start[1] + j * tileSize), tileSize)

def drawTile(screen: pygame.Surface, center: tuple[int, int], size: int):
   start = size // 2
   tileRect = pygame.Rect((center[0] - start, center[1] - start), (size, size))

   pygame.draw.rect(screen, (0, 255, 0), tileRect, 2)


main()