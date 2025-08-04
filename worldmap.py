import pygame

class WorldMap:
   width: int
   height: int
   tile_size: int

   def __init__(self, width: int, height: int, tile_size: int):
      self.width = width
      self.height = height
      self.tile_size = tile_size

   def draw(self, screen: pygame.Surface, focus: tuple[int, int]):
      center = (screen.get_width() / 2, screen.get_height() / 2)

      half_tile_size = self.tile_size // 2
      start = (center[0] - focus[0] + half_tile_size, center[1] - focus[1] + half_tile_size)

      for i in range(self.width):
         for j in range(self.height):
            self.__draw_tile(screen, (start[0] + i * self.tile_size, start[1] + j * self.tile_size))


   def __draw_tile(self, screen: pygame.Surface, center: tuple[int, int]):
      start = self.tile_size // 2
      tile_rect = pygame.Rect((center[0] - start, center[1] - start), (self.tile_size, self.tile_size))

      pygame.draw.rect(screen, (0, 255, 0), tile_rect, 2)