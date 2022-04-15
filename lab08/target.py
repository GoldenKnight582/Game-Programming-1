import pygame
import random
import base


class TargetSpawner(base.BasicObject):

    """ Circle that moves and shoots """

    def __init__(self, start_x, start_y, horizontal_speed, vertical_speed):
        super().__init__(start_x, start_y)
        self.color = (100, 100, 100)
        self.horizontal_speed = horizontal_speed
        self.vertical_speed = vertical_speed
        self.spawn_timer = random.uniform(3.0, 4.5)
        self.spawn_buffer = 50

    def update(self, delta_time, play_area, target_list):
        # Cooldown for spawning targets
        self.spawn_timer -= delta_time

        # Move around the play area
        super().update(delta_time)

        if self.spawn_timer <= 0:
            # Check to see if the spawner is close to the edge of the play area
            if self.x >= play_area[0] + self.spawn_buffer or self.x <= play_area[0] + play_area[2] - self.spawn_buffer \
                    or self.y >= play_area[1] + self.spawn_buffer or \
                    self.y <= play_area[1] + play_area[3] - self.spawn_buffer:

                self.spawn_timer = random.uniform(3.0, 4.5)

                new_t = Target(self.x, self.y)
                target_list.append(new_t)

        # If touching boundary, wrap to the other side of the screen
        if self.y + self.radius > play_area[1] + play_area[3]:
            self.y = play_area[1] + self.radius
        if self.y - self.radius < play_area[1]:
            self.y = play_area[1] + play_area[3] - self.radius
        if self.x - self.radius < play_area[0]:
            self.x = play_area[0] + play_area[2] - self.radius
        if self.x + self.radius > play_area[0] + play_area[2]:
            self.x = play_area[0] + self.radius

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.radius, 1)


class Target(base.BasicObject):
    """ A single target """

    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y)
        self.start_radius = 25
        self.radius = 25
        self.horizontal_speed = 30
        self.vertical_speed = 30
        self.health = 5

    def update(self, delta_time, play_area):
        # Move around the play area
        super().update(delta_time)

        # If touching boundary, change direction
        if self.y + self.radius > play_area[1] + play_area[3]:
            self.y = play_area[1] + play_area[3] - self.radius
            self.vertical_speed *= -1
        if self.y - self.radius < play_area[1]:
            self.y = play_area[1] + self.radius
            self.vertical_speed *= -1
        if self.x - self.radius < play_area[0]:
            self.x = play_area[0] + self.radius
            self.horizontal_speed *= -1
        if self.x + self.radius > play_area[0] + play_area[2]:
            self.x = play_area[0] + play_area[2] - self.radius
            self.horizontal_speed *= -1

    def draw(self, surf):
        if self.health > 4:
            pygame.draw.circle(surf, (255, 0, 0), (int(self.x), int(self.y)), self.start_radius)
        if self.health > 3:
            pygame.draw.circle(surf, (255, 255, 255), (int(self.x), int(self.y)), self.start_radius - self.start_radius // 5)
        if self.health > 2:
            pygame.draw.circle(surf, (255, 0, 0), (int(self.x), int(self.y)), self.start_radius - 2 * self.start_radius // 5)
        if self.health > 1:
            pygame.draw.circle(surf, (255, 255, 255), (int(self.x), int(self.y)), self.start_radius - 3 * self.start_radius // 5)
        if self.health > 0:
            pygame.draw.circle(surf, (255, 0, 0), (int(self.x), int(self.y)), self.start_radius - 4 * self.start_radius // 5)