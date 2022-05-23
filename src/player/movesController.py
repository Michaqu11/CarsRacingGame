import math

import pygame
from math import cos, sin, pi

from src.loadAssets.assets import Assets


class MovesController:
    def __init__(self, game, player):
        self.game = game
        self.player = player

    """def on(self):
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_w]:
            moved = True
            self.drive(1)

        if keys[pygame.K_s]:
            moved = True
            self.drive(0)

        if keys[pygame.K_a]:
            self.rotate(1)

        if keys[pygame.K_d]:
            self.rotate(0)

        if keys[pygame.K_SPACE]:
            self.hand_brake()

        if keys[pygame.K_ESCAPE]:
            moved = True
            self.game.run = False

        if not moved:
            self.reduce()
    """

    def onServer(self, move):

        moved = False

        if move[0]:
            moved = True
            self.drive(1)

        if move[1]:
            moved = True
            self.drive(0)

        if move[2]:
            self.rotate(1)

        if move[3]:
            self.rotate(0)

        if not moved:
            self.reduce()

        return move[4]

    def rotate(self, turn):
        if turn == 1:
            self.player.angle += self.player.turn - self.player.speed/3
        if turn == 0:
            self.player.angle -= self.player.turn - self.player.speed/3

    def drive(self, way):
        if way == 1:
            if self.player.speed > self.player.max_speed/3:
                self.player.speed = min(self.player.speed + self.player.acceleration/5, self.player.max_speed)
            else:
                self.player.speed = min(self.player.speed + self.player.acceleration, self.player.max_speed)
        if way == 0:
            if self.player.speed > 0:
                self.player.speed = max(self.player.speed - self.player.breaks, -(self.player.max_speed/5))
            else:
                self.player.speed = max(self.player.speed - self.player.acceleration, -(self.player.max_speed / 5))
        self.player.move()

    """def hand_brake(self):
        self.player.speed = max(self.player.speed - 2 * self.player.breaks, 0)
        self.player.move()"""

    def reduce(self):
        self.player.speed = max(self.player.speed - self.player.acceleration / 3, 0)
        self.player.move()