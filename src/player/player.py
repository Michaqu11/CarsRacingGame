import math

import pygame

from src.loadAssets.assets import Assets


class Player:

    def __init__(self, game, server, init, config, id, position, max_speed, turn):
        self.server = server
        self.init = init
        self.game = game
        self.config = config
        self.car = None
        self.id = id
        if position is None:
            self.position = self.config.player['position'][str(self.id)]
        else:
            self.position = position
        self.angle = 0
        self.speed = 0
        self.max_speed = max_speed / 2
        self.acceleration = self.config.player['acceleration']
        self.breaks = self.config.player['breaks']
        self.turn = turn / 2
        self.mask = None
        self.create_car()
        self.rect = pygame.transform.rotate(self.car, self.angle).get_rect(
            center=self.car.get_rect(topleft=self.position).center)
        self.rotated_image = None
        self.image = None
        self.lab = 0
        self.onFinish = False
        self.playing = True
        self.time_race = []
        self.bonusTime = 0
        self.m_start = self.s_start = 0

    def restart(self):
        self.position = self.config.player['position'][str(self.id)]
        self.angle = 0
        self.speed = 0
        self.rect = pygame.transform.rotate(self.car, self.angle).get_rect(
            center=self.car.get_rect(topleft=self.position).center)
        self.lab = 0
        self.onFinish = False
        self.playing = True
        self.time_race = []
        self.bonusTime = 0
        self.m_start = self.s_start = 0

    def collide(self, borders, x1=0, y1=0):
        (x, y) = self.position
        borders_mask = pygame.mask.from_surface(borders)
        offset = (int(x - x1), int(y - y1))
        self.mask = pygame.mask.from_surface(self.car)
        overlap = borders_mask.overlap(self.mask, offset)
        return overlap

    def player_collide(self):
        for player in self.game.players:
            if self != player:
                if pygame.Rect.colliderect(player.rect, self.rect):
                    return True, min(player.speed, self.speed)
        return False, 0

    def create_car(self):
        self.car = pygame.image.load('../../assets/car600.' + str(self.id) + '.png')
        self.car = pygame.transform.scale(pygame.image.load('../../assets/car600.' + str(self.id) + '.png'),
                                          (self.car.get_width() * 0.5, self.car.get_height() * 0.5))

    def end_race(self):
        self.playing = False
        print(self.time_race)

    def onServer(self, move):
        moved = False

        if move[0] != 'False':
            moved = True
            self.drive(1)

        if move[1] != 'False':
            moved = True
            self.drive(0)

        if move[2] != 'False':
            self.rotate(1)

        if move[3] != 'False':
            self.rotate(0)

        if not moved:
            self.reduce()

        """if move[4] == 'True':
            return True

        return False"""

    def rotate(self, turn):
        if turn == 1:
            self.angle += self.turn - self.speed / 3
        if turn == 0:
            self.angle -= self.turn - self.speed / 3

    def drive(self, way):
        if way == 1:
            if self.speed < self.max_speed / 3:
                self.speed = min(self.speed + self.acceleration, self.max_speed)
            elif self.speed < self.max_speed / 2:
                self.speed = min(self.speed + self.acceleration / 5, self.max_speed)
            elif self.speed < 2 * self.max_speed / 3:
                self.speed = min(self.speed + self.acceleration / 15, self.max_speed)
            else:
                self.speed = min(self.speed + self.acceleration / 30, self.max_speed)

        if way == 0:
            if self.speed > 0:
                self.speed = max(self.speed - self.breaks, -(self.max_speed / 5))
            else:
                self.speed = max(self.speed - self.acceleration, -(self.max_speed / 5))
        self.move()

    def reduce(self):
        self.speed = max(self.speed - self.acceleration / 6, 0)
        self.move(True)

    def move(self, r=False):

        rad = math.radians(self.angle)
        ver = math.cos(rad) * self.speed
        hor = math.sin(rad) * self.speed
        x = self.position[0]
        y = self.position[1]
        temp_pos = self.position
        self.position = (x - hor, y - ver)

        if self.collide(self.game.assets.borders) is not None:
            if r:
                self.speed = max(self.speed - 2 * self.breaks, 0)
            else:
                self.speed = max(self.speed - 3 * self.breaks, 0.4)

        finish_col = self.collide(self.game.assets.start, 500, 160)

        if self.collide(
                self.game.assets.block_borders) is not None or finish_col is not None and self.onFinish is False:
            self.position = temp_pos

        if self.game.showTimer:
            timer_pos = self.game.positionTimer
            timer_collidate = self.collide(self.game.assets.timeBonus, timer_pos[0], timer_pos[1])
            if timer_collidate and self.game.showTimer:
                self.game.showTimer = False
                self.bonusTime += 5000
                m, s = divmod(int(self.server.time / 1000), 60)
                self.game.countTimer = s + self.game.config.timer['countTimer']

        if finish_col is not None and self.onFinish is False and finish_col[0] != 10:
            self.onFinish = True
            if self.lab != 0:
                m_end, s_end = divmod(int(pygame.time.get_ticks() / 1000), 60)
                m = m_end - self.m_start
                s = s_end - self.s_start
                self.time_race.append('{:01d}:{:02d}'.format(m, s))
                if self.lab == 3:
                    self.end_race()
            self.lab += 1

        elif finish_col is None and self.onFinish:
            self.m_start, self.s_start = divmod(int(pygame.time.get_ticks() / 1000), 60)
            self.onFinish = False
        player_collide = self.player_collide()
        if player_collide[0]:
            self.speed = player_collide[1]
        self.changeRect()

    def changeRect(self):
        self.rotated_image = pygame.transform.rotate(self.car, self.angle)
        new_rect = self.rotated_image.get_rect(
            center=self.car.get_rect(topleft=self.position).center)
        self.rect = new_rect
