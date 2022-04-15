import pygame
import math
import random


class Spinner:

    def __init__(self, center_x, center_y, surf):
        self.cx = center_x
        self.cy = center_y
        self.surf = surf
        self.start_angle = random.randint(0, 360)
        self.cur_angle = self.start_angle
        self.apex = None
        self.rotation = 0
        self.rotation_speed = 72
        self.rotate_dir = random.randint(1, 2)
        self.dot_list = []
        self.dot_timer = 0.2
        self.dot_delay = 0.2

    def get_relative_point(self, origin_x, origin_y, radians, hypotenuse):
        """
        Find point (px, py) relative to a chosen point.
        :param origin_x: x-value of initial point
        :param origin_y: y-value of initial point
        :param radians: angle of the line between the initial point and second point
        :param hypotenuse: distance between the initial point and second point
        :return:
        """
        opposite = math.sin(radians) * hypotenuse
        adjacent = math.cos(radians) * hypotenuse
        px = int(origin_x + adjacent)
        py = int(origin_y - opposite)

        return px, py

    def update(self, dt):
        # Separation between spawning of dots
        self.dot_timer -= dt

        # Establish the angle for the pointing end of the triangle
        if self.rotate_dir == 1:
            self.cur_angle = self.start_angle + 180 - self.rotation
        elif self.rotate_dir == 2:
            self.cur_angle = self.start_angle + 180 + self.rotation

        # Spinning the Spinner
        self.rotation += self.rotation_speed * dt

    def draw(self):
        """
        Find points relative to the center point in order to draw a triangle
        :return:
        """
        if self.rotate_dir == 1:
            point1 = self.get_relative_point(self.cx, self.cy, math.radians(self.start_angle - 45 - self.rotation), 15)
            point2 = self.get_relative_point(self.cx, self.cy, math.radians(self.start_angle + 45 - self.rotation), 15)
            self.apex = self.get_relative_point(self.cx, self.cy, math.radians(self.cur_angle), 25)
        elif self.rotate_dir == 2:
            point1 = self.get_relative_point(self.cx, self.cy, math.radians(self.start_angle - 45 + self.rotation), 15)
            point2 = self.get_relative_point(self.cx, self.cy, math.radians(self.start_angle + 45 + self.rotation), 15)
            self.apex = self.get_relative_point(self.cx, self.cy, math.radians(self.cur_angle), 25)

        # Triangle
        pygame.draw.polygon(self.surf, (255, 255, 255), (point1, point2, self.apex))
        # Center dot
        pygame.draw.circle(self.surf, (0, 0, 0), (self.cx, self.cy), 2)


class Dot:

    def __init__(self, start_x, start_y, surf):
        # Dot Data
        self.x = start_x
        self.y = start_y
        self.radius = 3
        self.speed = 100
        self.horizontal_speed = 0
        self.vertical_speed = 0
        self.surf = surf
        self.height_edge = self.surf.get_height()
        self.width_edge = self.surf.get_width()
        self.mode = "Dot"

        # Ring Data
        self.rc1 = random.randint(100, 255)
        self.rc2 = random.randint(100, 255)
        self.rc3 = random.randint(100, 255)
        self.ring_color = (self.rc1, self.rc2, self.rc3)
        self.ring_radius = 5
        self.end_x = None
        self.end_y = None

    def update(self, dt):
        # Movement
        if self.mode == "Dot":      # Only move while it's a dot
            self.x += self.horizontal_speed * dt
            self.y += self.vertical_speed * dt

        # Turn into a ring if it hits the edges
        if self.y + self.radius > self.height_edge:
            self.end_x = self.x
            self.end_y = self.height_edge
            self.mode = "Ring"
        elif self.y - self.radius < 0:
            self.end_x = self.x
            self.end_y = 0
            self.mode = "Ring"
        elif self.x - self.radius < 0:
            self.end_x = 0
            self.end_y = self.y
            self.mode = "Ring"
        elif self.x + self.radius > self.width_edge:
            self.end_x = self.width_edge
            self.end_y = self.y
            self.mode = "Ring"

        # Expand the ring and fade out
        if self.mode == "Ring":
            self.ring_radius += 15 * dt
            if self.rc1 > 0:
                self.rc1 -= 100 * dt
            else:
                self.rc1 = 0
            if self.rc2 > 0:
                self.rc2 -= 100 * dt
            else:
                self.rc2 = 0
            if self.rc3 > 0:
                self.rc3 -= 100 * dt
            else:
                self.rc3 = 0
            self.ring_color = (int(self.rc1), int(self.rc2), int(self.rc3))

    def draw(self):
        if self.mode == "Dot":
            pygame.draw.circle(self.surf, (255, 255, 255), (int(self.x), int(self.y)), self.radius)
        elif self.mode == "Ring":
            if self.rc1 >= 0 and self.rc2 >= 0 and self.rc3 >= 0:       # There was a rare problem with one color value somehow coming through as negative sometimes and crashing the program, so this is an extra check against that
                pygame.draw.circle(self.surf, self.ring_color, (int(self.end_x), int(self.end_y)), int(self.ring_radius), 1)
