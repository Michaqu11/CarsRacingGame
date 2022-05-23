from datetime import datetime
from random import randint

import pygame
import time

from src.config.Config import Config
from src.loadAssets.assets import Assets
from src.player.movesController import MovesController
from src.player.player import Player


class DrawMap:

    FPS = 100
    run = True
    time = pygame.time.Clock()
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self):
        self.players = []
        self.assets = Assets()
        self.config = Config()
        self.cur_player = None
        self.maxlab = 3
        pygame.font.init()
        self.font = pygame.font.Font('../../assets/fonts/Dodgv2.ttf', 18)
        self.font2 = pygame.font.Font('../../assets/fonts/911v2.ttf', 15)
        self.font3 = pygame.font.Font('../../assets/fonts/Dodgv2.ttf', 8)
        self.img = self.font.render('Cars Racing', False, self.BLACK)
        self.labinfo = self.font3.render('Labs', False, self.WHITE)
        self.speedinfo = self.font3.render('km/h', False, self.WHITE)
        self.timeinfo = self.font3.render('Time', False, self.WHITE)
        self.countTimer = self.config.timer['countTimer']
        self.showTimer = False
        self.positionTimer = None
        self.clock = pygame.time.Clock()
        #self.game()


    def loadCar(self, id):
        car = pygame.image.load('../../assets/car600.' + str(id) + '.png')
        car = pygame.transform.scale(pygame.image.load('../../assets/car600.' + str(id) + '.png'), (car.get_width() * 0.5, car.get_height() * 0.5))
        return car

    def constDraw(self):
        self.screen.blit(self.assets.grass, (0, 0))
        self.screen.blit(self.img, (40, 360))

    def draw(self, screen, assets):
        for img, pos in assets:
            screen.blit(img, pos)
        for player in self.players:
            player.draw()
        #self.draw_dashBoard()

    def draw_dashBoard(self):
        self.screen.blit(self.assets.dashboard, (10, 400))
        lab_number = 1
        if self.cur_player.player.lab > 0:
            lab_number = self.cur_player.player.lab

        lab = self.font2.render(str(lab_number) + '/' + str(self.maxlab), False, self.WHITE)
        self.screen.blit(self.labinfo, (38, 468))
        self.screen.blit(lab, (35, 450))
        speed = self.font2.render(str("{0:03}".format(int(self.cur_player.player.speed * 100))), False, self.WHITE)
        self.screen.blit(speed, (115, 455))
        m, s = divmod(int(pygame.time.get_ticks() / 1000), 60)

        if int(s) == self.countTimer and self.showTimer == False:
            self.showTimer = True
            self.positionTimer = self.config.timer['positon'][randint(0, 2)]

        if self.showTimer:
            self.showTimerBonus()

        s = s - self.cur_player.player.bonusTime
        clock = self.font2.render('{:01d}:{:02d}'.format(m, s), False, self.WHITE)
        self.screen.blit(self.timeinfo, (200, 450))
        self.screen.blit(clock, (192, 455))

    def showTimerBonus(self):
        self.screen.blit(self.assets.timeBonus, self.positionTimer)
        pass

    def firstDraw(self):
        self.assetsToDraw = [(self.assets.track, (0, 0)), (self.assets.start, (502, 160)), (self.assets.borders, (0, 0))]
        self.constDraw()

    def drawCar(self, car, angle, position):
        rotated_image = pygame.transform.rotate(car, angle)
        new_rect = rotated_image.get_rect(
            center=car.get_rect(topleft=position).center)
        self.rect = new_rect
        self.screen.blit(rotated_image, new_rect.topleft)

    def drawAll(self):
        self.draw(self.screen, self.assetsToDraw)

    def game(self):
        self.screen = pygame.display.set_mode((self.assets.width, self.assets.height))
        pygame.display.set_caption("Racing Game")
        assets = [(self.assets.track, (0, 0)), (self.assets.start, (502, 160)), (self.assets.borders, (0, 0))]
        self.constDraw()
        self.draw(self.screen, assets)
        pygame.display.update()

