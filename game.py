import os
import pygame

from random import randrange

from unit import *
from worldmap import *


class AIGame:
   screen: pygame.Surface
   world_map: WorldMap
   player: Unit
   units: [Unit]

   def __init__(self):
      self.screen = None
      self.world_map = None
      self.player = None
      self.units = []

   def run(self):
      print("Welcome to the simulation!")

      self.init()
      self.main_loop()
      self.cleanup()


   # TODO: Maybe move everything in init() into the constructor   
   def init(self):
      os.environ["SDL_VIDEO_CENTERED"] = '1'

      pygame.init()

      info = pygame.display.Info()

      #SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
      SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

      # TODO: Make player and enemy colors instance variables
      #       that are passed in the constructor
      self.screen = self.create_window(SCREEN_WIDTH, SCREEN_HEIGHT)

      print(f"width: {self.screen.get_width()}, height: {self.screen.get_height()}")

      self.world_map = WorldMap(20, 20, 100)

      enemyColor = (255, 0, 0)

      self.units.append(Unit((800, 800), enemyColor))
      self.units.append(Unit((400, 400), enemyColor))
      self.units.append(Unit((600, 700), enemyColor))
      self.units.append(Unit((300, 900), enemyColor))

      print("initialization successful")


   def create_window(self, width, height) -> pygame.Surface:
      #return pygame.display.set_mode((width, height), pygame.RESIZABLE)
      #return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
      return pygame.display.set_mode((width, height), pygame.FULLSCREEN)


   def cleanup(self):
      print("Cleaning up...")
      pygame.quit()
      print("Done cleaning up")


   def main_loop(self):
      self.player = Unit([200, 200], (9, 9, 255))

      running = True

      timeLastFrame = pygame.time.get_ticks()

      screenCenter = (self.screen.get_width() / 2, self.screen.get_height() / 2)

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

               map_pos = (
                  mouse_pos[0] - screenCenter[0] + self.player.position[0],
                  mouse_pos[1] - screenCenter[1] + self.player.position[1])

               self.player.setTarget(map_pos)
            elif event.type == pygame.QUIT:
               running = False

         for unit in self.units:
            if not unit.moving:
               unit.setTarget((randrange(50, 950), randrange(50, 950)))

         for unit in self.units:
               unit.move(timeElapsed)

         self.player.move(timeElapsed)

         self.render_frame()

         pygame.display.update()


   def render_frame(self):
      self.screen.fill((0, 0, 0))

      focus = self.player.position

      self.world_map.draw(self.screen, focus)

      self.player.draw(self.screen, focus)

      for u in self.units:
         u.draw(self.screen, focus)


AIGame().run()