import pygame
import math


class Player:

    """ Player object """

    def __init__(self, center_x, center_y, world_surf, debug, image):
        # Movement variables
        self.x = center_x
        self.y = center_y
        self.world_surf = world_surf
        self.screen_pos = None
        self.radius = 46
        self.speed = 90
        self.horizontal_speed = 0
        self.vertical_speed = 0
        self.accel_x = 0
        self.accel_y = 0
        self.accelerating = False
        self.ship_orientation = 0
        # Shooting variables
        self.nose_x, self.nose_y = (0, 0)
        self.snose_x, self.snose_y = (0, 0)
        self.bullet_list = []
        self.bullet_timer = 0.33
        self.bullet_delay = 0.33
        # Image Initialization
        self.image = image
        self.scaled_image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.4), int(self.image.get_height() * 0.4)))
        # Other
        self.shield = None
        self.hit = False
        self.invuln_timer = 0
        self.invuln_delay = 3
        self.ammo = 15
        self.ammo_regen_timer = None
        self.ammo_regen_delay = 2
        self.debug = debug

    def update(self, dt, mouse_pos):
        self.bullet_timer -= dt
        self.invuln_timer -= dt
        if self.ammo_regen_timer:
            self.ammo_regen_timer -= dt

        # Invulnerability if hit
        if self.hit:
            self.invuln_timer = self.invuln_delay
            self.hit = False

        # Ammo Regen
        if self.ammo_regen_timer:
            if self.ammo_regen_timer <= 0:
                self.ammo += 1
                self.ammo_regen_timer = self.ammo_regen_delay

        # Player Movement
        self.ship_orientation = self.get_ship_orientation(mouse_pos)
        self.nose_x, self.nose_y, self.snose_x, self.snose_y = self.get_relative_point(self.ship_orientation, self.radius)
        if self.accelerating:
            self.horizontal_speed += self.accel_x * dt
            self.vertical_speed += self.accel_y * dt
        self.x += self.horizontal_speed * dt
        self.y += -self.vertical_speed * dt

        # Bounds (bounce off edge of world)
        if self.y + self.radius > self.world_surf.get_height():
            self.y = self.world_surf.get_height() - self.radius
            self.vertical_speed *= -1
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vertical_speed *= -1
        if self.x - self.radius < 0:
            self.x = self.radius
            self.horizontal_speed *= -1
        if self.x + self.radius > self.world_surf.get_width():
            self.x = self.world_surf.get_width() - self.radius
            self.horizontal_speed *= -1

        # Bullet Movement
        for cur_b in self.bullet_list:
            result = cur_b.update(dt)
            if result:
                self.bullet_list.remove(cur_b)
            else:
                cur_b.update(dt)

        return self.x, self.y

    def input(self, event, surf, shot_effect, thrust_effect):
        # --Movement--
        # Player turns towards mouse
        mouse_pos = pygame.mouse.get_pos()
        # If the player presses W, fire thrusters and create velocity in the direction they are facing
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                # If the ship isn't moving, give it an initial push. Otherwise, acceleration
                # should take the lead to make gradual changes in direction.
                if self.horizontal_speed == 0 and self.vertical_speed == 0:
                    self.horizontal_speed = self.speed * math.cos(self.ship_orientation)
                    self.vertical_speed = self.speed * math.sin(self.ship_orientation)
        keys = pygame.key.get_pressed()
        # If the player is holding down W, accelerate the velocity
        if keys[pygame.K_w]:
            self.accelerating = True
            self.accel_x = self.speed * math.cos(self.ship_orientation)
            self.accel_y = self.speed * math.sin(self.ship_orientation)
            thrust_effect.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.accelerating = False
                thrust_effect.stop()

        # --Shooting--
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.ammo:
                    if self.bullet_timer <= 0:
                        start_x = self.nose_x
                        start_y = self.nose_y
                        new_bullet = Bullet(start_x, start_y, surf, self.world_surf)
                        new_bullet.horizontal_speed = new_bullet.speed * math.cos(self.ship_orientation)
                        new_bullet.vertical_speed = -new_bullet.speed * math.sin(self.ship_orientation)
                        self.bullet_list.append(new_bullet)
                        shot_effect.play()
                        self.bullet_timer = self.bullet_delay
                        self.ammo -= 1
                        self.ammo_regen_timer = self.ammo_regen_delay

        return mouse_pos

    def draw(self, surf, screen_pos):
        self.screen_pos = screen_pos
        # Rotating the player image
        player_rotated = pygame.transform.rotate(self.scaled_image, math.degrees(self.ship_orientation) - 90)
        # Drawing player image (centered on position)
        surf.blit(player_rotated, (int(screen_pos[0] - player_rotated.get_width() / 2), int(screen_pos[1] - player_rotated.get_height() / 2)))

        if self.debug:
            # Show player position
            pygame.draw.circle(surf, (255, 255, 255), (int(screen_pos[0]), int(screen_pos[1])), 5)
            # Show nose position
            pygame.draw.circle(surf, (255, 255, 255), (int(self.snose_x), int(self.snose_y)), 5)
            # Hitbox
            pygame.draw.circle(surf, (0, 200, 0), (int(screen_pos[0]), int(screen_pos[1])), self.radius, 1)

    def get_ship_orientation(self, mouse_pos):
        """
        Takes the mouse position and determines the way the ship is facing
        :param mouse_pos: Position of the mouse on the screen
        :return:
        """
        adjacent = mouse_pos[0] - self.x
        opposite = -1 * (mouse_pos[1] - self.y)     # Account for inverted y-axis
        angle = math.atan2(opposite, adjacent)

        return angle

    def get_relative_point(self, radians, hypotenuse):
        """
        Gets a point which is hypotenuse pixels from the origin point at an angle or radians.
        :param origin_x:
        :param origin_y:
        :param radians:
        :param hypotenuse:
        :return:
        """
        # World coordinates
        opposite = hypotenuse * math.sin(radians)
        opposite = -opposite
        adjacent = hypotenuse * math.cos(radians)

        px = self.x + adjacent
        py = self.y + opposite
        px = int(px)
        py = int(py)

        # Screen coordinates
        opposite = hypotenuse * math.sin(radians)
        opposite = -opposite
        adjacent = hypotenuse * math.cos(radians)

        sx = int(self.screen_pos[0] + adjacent)
        sy = int(self.screen_pos[1] + opposite)

        return px, py, sx, sy


class Bullet:

    def __init__(self, start_x, start_y, surf, world_surf):
        self.x = start_x
        self.y = start_y
        self.radius = 5
        self.color = (255, 255, 0)
        self.speed = 200
        self.horizontal_speed = 0
        self.vertical_speed = 0
        self.surf = surf
        self.width_edge = world_surf.get_width()
        self.height_edge = world_surf.get_height()

    def update(self, dt):
        # Movement
        self.x += self.horizontal_speed * dt
        self.y += self.vertical_speed * dt

        # Boundary check
        if self.y + self.radius > self.height_edge:
            oob = True  # Out of bounds
        elif self.y - self.radius < 0:
            oob = True
        elif self.x - self.radius < 0:
            oob = True
        elif self.x + self.radius > self.width_edge:
            oob = True
        else:
            oob = False
        return oob

    def draw(self, screen_x, screen_y):
        pygame.draw.circle(self.surf, self.color, (int(screen_x), int(screen_y)), int(self.radius))