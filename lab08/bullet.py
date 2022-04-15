import pygame
import base


class Bullet(base.BasicObject):

    """ A single shot """

    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y)
        self.start_x = start_x
        self.start_y = start_y
        self.color = (255, 255, 255)
        self.speed = 150
        self.horizontal_speed = None
        self.vertical_speed = None

    def update(self, dt, play_area):
        # Movement
        super().update(dt)

        # Boundary check
        if self.y + self.radius > play_area[1] + play_area[3]:
            oob = True  # Out of bounds
        elif self.y - self.radius < play_area[1]:
            oob = True
        elif self.x - self.radius < play_area[0]:
            oob = True
        elif self.x + self.radius > play_area[0] + play_area[2]:
            oob = True
        else:
            oob = False
        return oob

    def draw(self, surf):
        super().draw(surf)