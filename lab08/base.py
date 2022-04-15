import pygame


class BasicObject:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.radius = 5

    def update(self, delta_time):
        self.x += self.horizontal_speed * delta_time
        self.y += self.vertical_speed * delta_time

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), int(self.radius))
