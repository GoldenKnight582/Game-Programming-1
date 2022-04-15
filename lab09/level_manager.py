import pygame
import math
import random
import player
import asteroid


class LevelManager():

    """ Object that handles game state """

    def __init__(self, win):
        # Position / Drawing Variables
        self.win = win
        self.screen_dim = (win.get_width(), win.get_height())
        self.world_dim = (2000, 2000)
        self.world_surface = pygame.Surface(self.world_dim)
        self.player_pos = [self.world_dim[0] // 2, self.world_dim[1] // 2]
        self.update_camera()
        self.player_screen_pos = self.convert_world_position_to_screen(self.player_pos[0], self.player_pos[1])
        self.stars_drawn = 0
        self.mouse_pos = (0, 0)
        # Structural Variables
        self.state = "Title"
        self.clock = pygame.time.Clock()
        self.delta_time = 0.0
        self.total_time = 0.0
        self.debug = False
        self.score = 0
        # Title Screen Data Initialization
        self.title = pygame.font.Font("Font//PressStart2P-Regular.ttf", 45)
        self.header = pygame.font.Font("Font//PressStart2P-Regular.ttf", 24)
        self.normal = pygame.font.Font("Font//PressStart2P-Regular.ttf", 10)
        self.start_rect = None
        self.start_hover = False
        self.quit_rect = None
        self.quit_hover = False
        # Object Initialization
        self.player = None
        self.asteroid_number = 5
        self.asteroids = []
        self.explosions = []
        # Sprites
        self.sprites = {"player": pygame.image.load("Images//player.png"), "asteroid": pygame.image.load("Images//asteroid_sheet1.png"), "explosion": pygame.image.load("Images//explosion_sheet.png").convert_alpha()}
        # Music and SFX
        pygame.mixer.music.load("Sound\\Title.ogg")
        pygame.mixer.music.play(-1)
        self.sfx = {"explosion": pygame.mixer.Sound("Sound\\Explosion.ogg"), "shot": pygame.mixer.Sound("Sound\\Shot.ogg"), "thruster": pygame.mixer.Sound("Sound\\Thruster.ogg"), "damage": pygame.mixer.Sound("Sound\\Player_Hit.ogg")}
        self.sfx["shot"].set_volume(0.4)
        self.sfx["explosion"].set_volume(0.4)
        self.sfx["thruster"].set_volume(0.1)
        self.sfx["damage"].set_volume(0.4)

    def update(self):
        self.delta_time = self.clock.tick() / 1000
        self.total_time += self.delta_time

        # Title Screen Updates
        if self.state == "Title" or self.state == "Resume":
            mouse_pos = pygame.mouse.get_pos()
            if self.start_rect:
                if self.start_rect[0] - 5 < mouse_pos[0] < self.start_rect[0] + self.start_rect[2] + 5 and \
                        self.start_rect[1] - 5 < mouse_pos[1] < self.start_rect[1] + self.start_rect[3] + 5:
                    self.start_hover = True
                else:
                    self.start_hover = False
            if self.quit_rect:
                if self.quit_rect[0] - 5 < mouse_pos[0] < self.quit_rect[0] + self.quit_rect[2] + 5 and \
                        self.quit_rect[1] - 5 < mouse_pos[1] < self.quit_rect[1] + self.quit_rect[3] + 5:
                    self.quit_hover = True
                else:
                    self.quit_hover = False

        # Game Updates
        if self.state == "Level 1":
            self.player_screen_pos = self.convert_world_position_to_screen(self.player.x, self.player.y)
            mouse_world_pos = self.convert_screen_position_to_world(self.mouse_pos)
            self.player_pos = self.player.update(self.delta_time, mouse_world_pos)
            for a in self.asteroids:
                a.update(self.delta_time)
            for e in self.explosions:
                e.update(self.delta_time)
                if e.explosion_frame >= 13:
                    self.explosions.remove(e)
            self.hit_detection()
            if self.player.shield == 0:
                self.state = "Title"
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Sound\\Title.ogg")
                pygame.mixer.music.play(-1)
            # Debug Toggles
            self.player.debug = self.debug
            for a in self.asteroids:
                a.debug = self.debug

    def update_camera(self):
        cam_x = self.player_pos[0] - self.screen_dim[0] / 2
        cam_y = self.player_pos[1] - self.screen_dim[1] / 2
        if cam_x < 0:
            cam_x = 0
        if cam_x > self.world_dim[0] - self.screen_dim[0]:
            cam_x = self.world_dim[0] - self.screen_dim[0]
        if cam_y < 0:
            cam_y = 0
        if cam_y > self.world_dim[1] - self.screen_dim[1]:
            cam_y = self.world_dim[1] - self.screen_dim[1]

        self.camera_pos = (cam_x, cam_y)

    def handle_input(self):
        event = pygame.event.poll()

        # Game Input
        if self.state == "Level 1":
            self.mouse_pos = self.player.input(event, self.win, self.sfx["shot"], self.sfx["thruster"])
            self.update_camera()

        # Quitting
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state == "Title" or self.state == "Resume":
                    return True
                # Return to title screen
                else:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Sound\\Title.ogg")
                    pygame.mixer.music.play(-1)
                    self.state = "Resume"
            if event.key == pygame.K_F1:
                if self.state == "Level 1":
                    if not self.debug:
                        self.debug = True
                    elif self.debug:
                        self.debug = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.start_hover:
                if self.state == "Title" or self.state == "Resume":
                    self.level_1_init()
            if event.button == 1 and self.quit_hover:
                return True

    def hit_detection(self):
        for a in self.asteroids:
            distance = self.get_distance(a.x, a.y, self.player.x, self.player.y)
            if distance < a.radius + self.player.radius:
                self.player.horizontal_speed *= -1
                self.player.vertical_speed *= -1
                self.sfx["damage"].play()
                if self.player.invuln_timer <= 0:
                    self.player.hit = True
                    self.player.shield -= 10
                break
        for b in self.player.bullet_list:
            for a in self.asteroids:
                distance = self.get_distance(a.x, a.y, b.x, b.y)
                if distance < a.radius + b.radius:
                    # If the bullet hits, remove it from the list and decrease target health
                    a.hit = True
                    self.player.bullet_list.remove(b)
                # Delete the target if it's health is 0
                if a.hit:
                    if a.state == "Full":
                        self.score += 100
                        self.asteroids.append(asteroid.Asteroid(a.x - 10, a.y, self.world_surface, self.win, "Broken", random.randint(-30, 30), random.randint(-50, 50), self.debug, self.sprites["asteroid"]))
                        self.asteroids.append(asteroid.Asteroid(a.x, a.y + 10, self.world_surface, self.win, "Broken", random.randint(-30, 30), random.randint(-50, 50), self.debug, self.sprites["asteroid"]))
                        self.explosions.append(asteroid.Explosion(a.x, a.y, self.sprites["explosion"]))
                        self.sfx["explosion"].play()
                        self.asteroids.remove(a)
                        break
                    elif a.state == "Broken":
                        self.score += 150
                        self.asteroids.append(asteroid.Asteroid(a.x - 10, a.y, self.world_surface, self.win, "Final", random.randint(-30, -15), random.randint(-50, -15), self.debug, self.sprites["asteroid"]))
                        self.asteroids.append(asteroid.Asteroid(a.x + 10, a.y, self.world_surface, self.win, "Final", random.randint(15, 30), random.randint(15, 50), self.debug, self.sprites["asteroid"]))
                        self.asteroids.append(asteroid.Asteroid(a.x + 10, a.y - 10, self.world_surface, self.win, "Final", random.randint(15, 30), random.randint(-50, -15), self.debug, self.sprites["asteroid"]))
                        self.explosions.append(asteroid.Explosion(a.x, a.y, self.sprites["explosion"]))
                        self.sfx["explosion"].play()
                        self.asteroids.remove(a)
                        break
                    elif a.state == "Final":
                        self.score += 200
                        self.explosions.append(asteroid.Explosion(a.x, a.y, self.sprites["explosion"]))
                        self.sfx["explosion"].play()
                        self.asteroids.remove(a)
                        break

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

    def convert_screen_position_to_world(self, screen_pos):
        world_x = screen_pos[0] + self.camera_pos[0]
        world_y = screen_pos[1] + self.camera_pos[1]
        world_x = int(world_x)
        world_y = int(world_y)

        return (world_x, world_y)

    def convert_world_position_to_screen(self, world_x, world_y):
        screen_x = world_x - self.camera_pos[0]
        screen_y = world_y - self.camera_pos[1]
        screen_x = int(screen_x)
        screen_y = int(screen_y)

        return (screen_x, screen_y)

    def draw_shield_gradient(self, surf):
        for i in range(self.player.shield):
            percent = (i / 100) / 2
            color_int = int(255 * percent)
            blue_int = int(115 + 115 * percent)
            color = (color_int, color_int, blue_int)
            pygame.draw.line(surf, color, (899+i, 35), (899+i, 20))

    def draw_ammo_gradient(self, surf):
        for i in range(self.player.ammo * 7):
            percent = (i / 100) / 2
            color_int = int(255 * percent)
            red_int = int(115 + 115 * percent)
            color = (red_int, color_int, color_int)
            pygame.draw.line(surf, color, (899+i, 73), (899+i, 58))

    def draw(self):
        self.win.fill((0, 0, 0))
        if self.state == "Title" or self.state == "Resume":
            self.draw_title_screen(self.start_hover, self.quit_hover)
        elif self.state == "Level 1":
            self.draw_level_1()
        pygame.display.flip()

    def draw_title_screen(self, start_highlight=False, quit_highlight=False):
        bg_color = (255, 0, 150)
        title_color = 32 * (math.sin(2 * self.total_time)) + 96
        self.win.fill(bg_color)
        temp = self.title.render("Debris Demolition Co.", False, (title_color, title_color, title_color), bg_color)
        self.win.blit(temp, (self.screen_dim[0] // 2 - temp.get_width() // 2, self.screen_dim[1] // 3 - temp.get_height() // 2))
        temp = self.normal.render("By: Tyler Cobb", False, (75, 75, 75), bg_color)
        self.win.blit(temp, (self.screen_dim[0] - temp.get_width() - 10, self.screen_dim[1] * 0.38))
        temp = self.normal.render("Explosion Animation: https://opengameart.org/content/simple-explosion-bleeds-game-art", False, (150, 150, 150), bg_color)
        self.win.blit(temp, (0, self.screen_dim[1] * 0.82))
        temp = self.normal.render("Spaceship Image: https://opengameart.org/content/spaceship-tutorial-o", False, (150, 150, 150), bg_color)
        self.win.blit(temp, (0, self.screen_dim[1] * 0.85))
        temp = self.normal.render("Font: https://fonts.google.com/specimen/Press+Start+2P#standard-styles", False, (150, 150, 150), bg_color)
        self.win.blit(temp, (0, self.screen_dim[1] * 0.88))
        temp = self.normal.render("Animated Asteroid: https://opengameart.org/content/four-asteroids-in-four-variants", False, (150, 150, 150), bg_color)
        self.win.blit(temp, (0, self.screen_dim[1] * 0.91))
        temp = self.normal.render("Music: https://opengameart.org/content/cc0-music", False, (150, 150, 150), bg_color)
        self.win.blit(temp, (0, self.screen_dim[1] * 0.94))
        temp = self.normal.render("SFX: https://www.kenney.nl/assets/sci-fi-sounds", False, (150, 150, 150), bg_color)
        self.win.blit(temp, (0, self.screen_dim[1] * 0.97))

        if not start_highlight:
            if self.state == "Title":
                temp = self.header.render("Start Game", False, (255, 255, 0), bg_color)
            elif self.state == "Resume":
                temp = self.header.render("Resume Game", False, (255, 255, 0), bg_color)
        else:
            if self.state == "Title":
                temp = self.header.render("Start Game", False, (150, 0, 255), bg_color)
            elif self.state == "Resume":
                temp = self.header.render("Resume Game", False, (150, 0, 255), bg_color)
        self.start_rect = temp.get_rect()
        self.start_rect[0] = self.screen_dim[0] // 2 - temp.get_width() // 2
        self.start_rect[1] = int(self.screen_dim[1] * 0.55)
        self.win.blit(temp, (self.screen_dim[0] // 2 - temp.get_width() // 2, int(self.screen_dim[1] * 0.55)))
        if not quit_highlight:
            temp = self.header.render("Quit Game", False, (255, 255, 0), bg_color)
        else:
            temp = self.header.render("Quit Game", False, (150, 0, 255), bg_color)
        self.quit_rect = temp.get_rect()
        self.quit_rect[0] = self.screen_dim[0] // 2 - temp.get_width() // 2
        self.quit_rect[1] = int(self.screen_dim[1] * 0.61)
        self.win.blit(temp, (self.screen_dim[0] // 2 - temp.get_width() // 2, int(self.screen_dim[1] * 0.61)))

    def draw_level_1(self):
        self.win.blit(self.world_surface, (0, 0), (self.camera_pos[0], self.camera_pos[1], self.screen_dim[0], self.screen_dim[1]))
        while self.stars_drawn < 150:
            color_choice = random.randint(1, 3)
            radius = random.randint(3, 10)
            if color_choice == 1:
                pygame.draw.circle(self.world_surface, (20, 20, 15), (random.randint(0 + radius, self.world_dim[0] - radius), random.randint(0 + radius, self.world_dim[1] - radius)), radius)
            if color_choice == 2:
                pygame.draw.circle(self.world_surface, (15, 20, 20), (random.randint(0 + radius, self.world_dim[0] - radius), random.randint(0 + radius, self.world_dim[1] - radius)), radius)
            if color_choice == 3:
                pygame.draw.circle(self.world_surface, (20, 15, 20), (random.randint(0 + radius, self.world_dim[0] - radius), random.randint(0 + radius, self.world_dim[1] - radius)), radius)
            self.stars_drawn += 1
        player_screen_pos = self.convert_world_position_to_screen(self.player_pos[0], self.player_pos[1])
        self.player.draw(self.win, player_screen_pos)
        for b in self.player.bullet_list:
            screen_x, screen_y = self.convert_world_position_to_screen(b.x, b.y)
            b.draw(screen_x, screen_y)
        for a in self.asteroids:
            asteroid_screen_x, asteroid_screen_y = self.convert_world_position_to_screen(a.x, a.y)
            a.draw(asteroid_screen_x, asteroid_screen_y)
        for e in self.explosions:
            explosion_screen_x, explosion_screen_y = self.convert_world_position_to_screen(e.explosion_x, e.explosion_y)
            e.draw(self.win, explosion_screen_x, explosion_screen_y)
        temp = self.header.render(str(self.score), False, (255, 255, 255), (0, 0, 0))
        self.win.blit(temp, (self.win.get_width() // 2 - temp.get_width() // 2, 0))
        temp = self.normal.render("Shields", False, (170, 170, 255), (0, 0, 0))
        self.win.blit(temp, (900, 0 + temp.get_height() // 2))
        temp = self.normal.render("Ammo", False, (255, 170, 170), (0, 0, 0))
        self.win.blit(temp, (900, 50 - temp.get_height() // 2))
        self.draw_shield_gradient(self.win)
        self.draw_ammo_gradient(self.win)

    def level_1_init(self):
        self.score = 0
        pygame.mixer.music.stop()
        pygame.mixer.music.load("Sound\\Level.ogg")
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)
        self.player_pos = [self.world_dim[0] // 2, self.world_dim[1] // 2]
        self.update_camera()
        self.player_screen_pos = self.convert_world_position_to_screen(self.player_pos[0], self.player_pos[1])
        self.player = player.Player(self.player_pos[0], self.player_pos[1], self.world_surface, self.debug, self.sprites["player"])
        self.player.shield = 100
        self.asteroids = []
        for i in range(self.asteroid_number):
            new_asteroid = asteroid.Asteroid(random.randint(0, self.world_dim[0]), random.randint(0, self.world_dim[1]), self.world_surface, self.win, "Full", random.randint(-20, 20), random.randint(-20, 20), self.debug, self.sprites["asteroid"])
            if self.player.hit:
                new_asteroid = asteroid.Asteroid(random.randint(0, self.world_dim[0]), random.randint(0, self.world_dim[1]), self.world_surface, self.win, "Full", random.randint(-20, 20), random.randint(-20, 20), self.debug, self.sprites["asteroid"])
            self.asteroids.append(new_asteroid)
        self.state = "Level 1"

