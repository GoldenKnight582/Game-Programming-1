import pygame


class Asteroid:
    def __init__(self, start_x, start_y, world_surf, draw_surf, state, hspeed, vspeed, debug, image):
        self.x = start_x
        self.y = start_y
        self.state = state
        if self.state == "Full":
            self.scale = 0.75
        elif self.state == "Broken":
            self.scale = 0.5
        elif self.state == "Final":
            self.scale = 0.25
        self.horizontal_speed = hspeed
        self.vertical_speed = vspeed
        self.hit = False
        self.world_surf = world_surf
        self.draw_surf = draw_surf
        self.width = 261
        self.height = 239
        self.radius = 95 * self.scale
        self.width_edge = world_surf.get_width()
        self.height_edge = world_surf.get_height()
        self.sprite_sheet = image
        self.sprite_sheet.set_colorkey((5, 5, 5))

        # Asteroid frames
        self.frame0 = pygame.Surface((261, 239))
        self.frame0.set_colorkey((0, 0, 0))
        self.frame0.blit(self.sprite_sheet, (0, 0), (0, 0, 261, 239))
        self.frame0 = pygame.transform.scale(self.frame0, (int(261 * self.scale), int(239 * self.scale)))
        self.frame1 = pygame.Surface((235, 227))
        self.frame1.set_colorkey((0, 0, 0))
        self.frame1.blit(self.sprite_sheet, (0, 0), (338, 1, 235, 227))
        self.frame1 = pygame.transform.scale(self.frame1, (int(235 * self.scale), int(227 * self.scale)))
        self.frame2 = pygame.Surface((242, 213))
        self.frame2.set_colorkey((0, 0, 0))
        self.frame2.blit(self.sprite_sheet, (0, 0), (8, 258, 242, 213))
        self.frame2 = pygame.transform.scale(self.frame2, (int(242 * self.scale), int(213 * self.scale)))
        self.frame3 = pygame.Surface((254, 229))
        self.frame3.set_colorkey((0, 0, 0))
        self.frame3.blit(self.sprite_sheet, (0, 0), (319, 247, 254, 229))
        self.frame3 = pygame.transform.scale(self.frame3, (int(254 * self.scale), int(229 * self.scale)))

        self.cur_frame = 0
        self.anim_timer = 0.5
        self.anim_delay = 0.5

        self.debug = debug

    def update(self, dt):
        # Animation
        self.anim_timer -= dt

        if self.anim_timer <= 0:
            self.anim_timer = self.anim_delay
            if self.cur_frame < 4:
                self.cur_frame += 1
            if self.cur_frame == 4:
                self.cur_frame = 0

        # Movement
        self.x += self.horizontal_speed * dt
        self.y += self.vertical_speed * dt

        # If touching boundary, change direction
        if self.y + self.height // 2 > self.height_edge:
            self.y = self.height_edge - self.height // 2
            self.vertical_speed *= -1
        if self.y - self.height // 2 < 0:
            self.y = self.height // 2
            self.vertical_speed *= -1
        if self.x - self.width // 2 < 0:
            self.x = self.width // 2
            self.horizontal_speed *= -1
        if self.x + self.width // 2 > self.width_edge:
            self.x = self.width_edge - self.width // 2
            self.horizontal_speed *= -1

    def draw(self, screen_x, screen_y):
        if self.cur_frame == 0:
            self.draw_surf.blit(self.frame0, (screen_x - self.frame0.get_width() // 2, screen_y - self.frame0.get_height() // 2))
        elif self.cur_frame == 1:
            self.draw_surf.blit(self.frame1, (screen_x - self.frame1.get_width() // 2, screen_y - self.frame1.get_height() // 2))
        elif self.cur_frame == 2:
            self.draw_surf.blit(self.frame2, (screen_x - self.frame2.get_width() // 2, screen_y - self.frame2.get_height() // 2))
        elif self.cur_frame == 3:
            self.draw_surf.blit(self.frame3, (screen_x - self.frame3.get_width() // 2, screen_y - self.frame3.get_height() // 2))

        if self.debug:
            # Hitbox
            pygame.draw.circle(self.draw_surf, (200, 0, 0), (int(screen_x), int(screen_y)), int(self.radius), 1)


class Explosion:
    def __init__(self, e_x, e_y, image):
        self.explosion_sheet = image
        self.explosion_x = e_x
        self.explosion_y = e_y
        self.explosion_frame = 0
        self.explosion_timer = 0.1
        self.explosion_delay = 0.1

    def update(self, dt):
        self.explosion_timer -= dt

        if self.explosion_timer <= 0:
            self.explosion_timer = self.explosion_delay
            if self.explosion_frame < 13:
                self.explosion_frame += 1

    def draw(self, surf, screen_x, screen_y):
        surf.blit(self.explosion_sheet, (screen_x - 196 // 2, screen_y - 190 // 2), (196 * self.explosion_frame, 0, 196, 190))
