import pygame
import bullet
import base
import math


class Player(base.BasicObject):

    """ Circle that moves and shoots """

    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y)
        self.start_radius = 45
        self.radius = 45
        self.color = (100, 200, 0)
        self.speed = 100
        self.x_velocity = 0
        self.y_velocity = 0
        self.bullet_list = []              # will hold 0-many drop.Drop object
        self.bullet_timer = 0.1
        self.invuln_timer = 2
        self.invuln = False
        self.health = 9
        self.score = 0
        self.used_keyboard_last = True

    def update(self, delta_time, play_area):
        # Move the player
        diagDistance = (((self.speed * delta_time) ** 2) / 2) ** 0.5
        self.x += (self.x_velocity * self.speed) * delta_time
        self.y += (self.y_velocity * self.speed) * delta_time
        if self.x_velocity == -1 and self.y_velocity != 0 or self.x_velocity == 1 and self.y_velocity != 0:
            self.x += self.x_velocity * int(diagDistance)
            self.y += self.y_velocity * int(diagDistance)

        # Warp the cloud to the left side of the play area if it hits the right
        if self.x + self.radius > play_area[0] + play_area[2]:
            self.x = play_area[0] + play_area[2] - self.radius
        if self.x - self.radius < play_area[0]:
            self.x = play_area[0] + self.radius
        if self.y - self.radius < play_area[1]:
            self.y = play_area[1] + self.radius
        if self.y + self.radius > play_area[1] + play_area[3]:
            self.y = play_area[1] + play_area[3] - self.radius

        # Separation between spawning of new bullets
        self.bullet_timer -= delta_time

        # Update all bullet movement
        for cur_b in self.bullet_list:
            result = cur_b.update(delta_time, play_area)
            if result:
                self.bullet_list.remove(cur_b)
            else:
                cur_b.update(delta_time, play_area)

        # Count down the invulnerability timer
        self.invuln_timer -= delta_time
        # If invulnerability is on and the timer reaches 0, revert to normal
        if self.invuln and self.invuln_timer <= 0:
            self.invuln = False
            self.color = (100, 200, 0)

    def process_input(self, event):
        # Keyboard Input - Movement
        all_keys = pygame.key.get_pressed()
        if all_keys[pygame.K_a]:
            self.x_velocity = -1
            self.used_keyboard_last = True
        elif all_keys[pygame.K_d]:
            self.x_velocity = 1
            self.used_keyboard_last = True
        else:
            self.x_velocity = 0
        if all_keys[pygame.K_w]:
            self.y_velocity = -1
            self.used_keyboard_last = True
        elif all_keys[pygame.K_s]:
            self.y_velocity = 1
            self.used_keyboard_last = True
        else:
            self.y_velocity = 0

        mouse_button = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        # Mouse Input - Shooting
        if self.bullet_timer <= 0 and mouse_button[0]:
            self.used_keyboard_last = True
            self.bullet_timer = 0.15
            click_x = mouse_pos[0]
            click_y = mouse_pos[1]

            # Angle
            adjacent = click_x - self.x
            opposite = click_y - self.y
            angle = math.atan2(opposite, adjacent)

            new_x = self.x + self.radius * math.cos(angle)
            new_y = self.y + self.radius * math.sin(angle)
            new_bullet = bullet.Bullet(new_x, new_y)
            new_bullet.horizontal_speed = new_bullet.speed * math.cos(angle)
            new_bullet.vertical_speed = new_bullet.speed * math.sin(angle)
            self.bullet_list.append(new_bullet)

        # Controller Input
        if pygame.joystick.get_count() > 0:
            gamepad = pygame.joystick.Joystick(0)
        else:
            gamepad = None

        if gamepad:
            # Lef Stick - Movement
            if abs(gamepad.get_axis(0)) > 0.1:
                self.x_velocity = gamepad.get_axis(0)
                self.used_keyboard_last = False
            if abs(gamepad.get_axis(1)) > 0.1:
                self.y_velocity = gamepad.get_axis(1)
                self.used_keyboard_last = False
            # Right Stick w/ Trigger - Shooting  (Either trigger will work.
            # Used triggers to get around stick drift causing shooting when the stick wasn't being moved.)
            if self.bullet_timer <= 0:
                if abs(gamepad.get_axis(3)) and abs(gamepad.get_axis(4)) and abs(gamepad.get_axis(2)) > 0.1:
                    self.used_keyboard_last = False
                    self.bullet_timer = 0.15
                    diff_x = self.x + gamepad.get_axis(4)
                    diff_y = self.y + gamepad.get_axis(3)

                    # Angle
                    adjacent = diff_x - self.x
                    opposite = diff_y - self.y
                    angle = math.atan2(opposite, adjacent)

                    new_x = self.x + self.radius * math.cos(angle)
                    new_y = self.y + self.radius * math.sin(angle)
                    new_bullet = bullet.Bullet(new_x, new_y)
                    new_bullet.horizontal_speed = new_bullet.speed * math.cos(angle)
                    new_bullet.vertical_speed = new_bullet.speed * math.sin(angle)
                    self.bullet_list.append(new_bullet)

    def draw(self, surf):
        super().draw(surf)

        for b in self.bullet_list:
            b.draw(surf)

    def hit_detection(self, target_list):
        for t in target_list:
            distance = self.get_distance(self.x, self.y, t.x, t.y)
            if distance < self.radius + t.radius and not self.invuln:
                self.health -= 1
                self.color = (200, 200, 0)
                self.radius -= (1 / 9) * self.start_radius
                # Reset the timer here on hit
                self.invuln_timer = 2
                self.invuln = True

        for b in self.bullet_list:
            for t in target_list:
                distance = self.get_distance(t.x, t.y, b.x, b.y)
                if distance < t.radius + b.radius:
                    # If the bullet hits, remove it from the list and decrease target health
                    t.health -= 1
                    # Tell the check that the actual radius of the target has decreased
                    t.radius -= (1/5) * t.start_radius
                    self.score += 10
                    self.bullet_list.remove(b)
                # Delete the target if it's health is 0
                if t.health == 0:
                    target_list.remove(t)

        if self.health == 0:
            return True

    def get_distance(self, x1, y1, x2, y2):
        if x2 > x1:
            adjacent = x2 - x1
        elif x1 > x2:
            adjacent = x1 - x2
        if y2 > y1:
            opposite = y2 - y1
        elif y1 > y2:
            opposite = y1 - y2

        distance = (opposite ** 2 + adjacent ** 2) ** 0.5

        return distance
