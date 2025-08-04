import math
import pygame

class Unit:
   position: tuple[int, int]
   color: pygame.Color
   target: tuple[int, int]
   moving: bool

   real_pos: tuple[float, float]

   def __init__(self, position: tuple[int, int], color: pygame.Color):
      self.position = position
      self.color = color
      self.target = [position[0], position[1]]
      self.moving = False
      self.real_pos = [float(position[0]), float(position[1])]

   def draw(self, screen: pygame.Surface, focus: tuple[int, int]):
      center = (screen.get_width() / 2, screen.get_height() / 2)

      pos = (center[0] + self.position[0] - focus[0], center[1] + self.position[1] - focus[1])

      pygame.draw.circle(screen, self.color, pos, 25)

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