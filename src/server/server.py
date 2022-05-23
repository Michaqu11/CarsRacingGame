import time
from random import randint
from timeit import default_timer as timer
import socket
from _thread import *
import _pickle as pickle

import pygame

from src.config.Config import Config
from src.gameSetting.game import Game
from src.gameSetting.gameInit import GameInit
from src.player.player import Player
from src.server.clientInfo import ClientInfo


class server:
    def __init__(self):
        self.start = timer()
        self.game = Game()
        self.S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.HOST_NAME = socket.gethostname()
        self.SERVER_IP = socket.gethostbyname(self.HOST_NAME)
        self.init = GameInit()
        self.config = Config()
        self.time = 0
        self.win = False
        self.winner = None
        self.playersId = [1, 2, 3, 4]
        self.fun()
    # try to connect to server
    def fun(self):
        try:
            self.S.bind((self.SERVER_IP, 420))
        except socket.error as e:
            print(str(e))
            print("[SERVER] Server could not start")
            quit()

        self.S.listen()  # listen for connections

        print(f"[SERVER] Server Started with local ip {self.SERVER_IP}")

        print("waiting for connection")

        while True:

            host, addr = self.S.accept()
            print("[CONNECTION] Connected to:", addr)

            self.init.connections += 1
            if self.init.connections <= self.config.playersNumer:
                start_new_thread(self.threaded_client, (host, self.playersId.pop(0)))
                print()

    def threaded_client(self, conn, _id):
        data = conn.recv(16)
        name = data.decode("utf-8")
        print("[LOG]", name, "connected to the server.")
        player = Player(self.game, self, self.init, self.config, _id, None, self.config.player['speed'],
                        self.config.player['turn'])

        self.game.players.append(player)
        clientsList = ClientInfo(self.config, player.id, player.position, player.angle, player.speed, player.max_speed,
                                 player.acceleration, player.breaks, player.turn, player.lab, player.rect, 0,
                                 self.game.showTimer, self.game.positionTimer, self.win, self.winner,
                                 self.init.connections)
        self.init.addPlayer(clientsList)
        start_time = time.time()
        conn.send(str.encode(str(_id)))
        restart = False
        run = True
        while run:
            data = conn.recv(1024)

            if not data:
                break
            self.time = (pygame.time.get_ticks() - start_time)
            data = data.decode("utf-8")
            # look for specific commands from received data
            if data.split(" ")[0] == "move":
                m, s = divmod(int(self.time / 1000), 60)
                if int(s) == self.game.countTimer and not self.game.showTimer:
                    self.game.showTimer = True
                    self.game.positionTimer = self.config.timer['positon'][randint(0, 2)]
                    # self.game.positionTimer = self.config.timer['positon'][0]

                split_data = data.split(" ")
                key = []
                for i in range(1, len(split_data)):
                    key.append(split_data[i])

                if key[4] == 'False':
                    run = False


                if self.init.connections == self.config.playersNumer:

                    player.onServer(key)
                    #run = player.onServer(key)

                    if player.lab == self.config.labs:
                        self.win = True
                        self.winner = name
                        self.init.connections = 0

                    if restart:
                        self.win = False
                        self.winner = None
                        restart = False
                    clientsList.updateValues(player.id, player.position, player.angle, player.speed, player.max_speed,
                                             player.acceleration, player.breaks, player.turn, player.lab,
                                             player.rect, self.time - player.bonusTime, self.game.showTimer,
                                             self.game.positionTimer, self.win, self.winner, self.init.connections)
                else:
                    clientsList.updateValues(player.id, player.position, player.angle, player.speed, player.max_speed,
                                             player.acceleration, player.breaks, player.turn, player.lab,
                                             player.rect, 0, False,
                                             None, self.win, self.winner, self.init.connections)

            elif data.split(" ")[0] == "time":
                start_time = pygame.time.get_ticks()
                self.time = (pygame.time.get_ticks() - start_time)
                clientsList.updateValues(player.id, player.position, player.angle, player.speed, player.max_speed,
                                         player.acceleration, player.breaks, player.turn, player.lab, player.rect,
                                         self.time - player.bonusTime, self.game.showTimer, self.game.positionTimer,
                                         self.win, self.winner, self.init.connections)

            elif data.split(" ")[0] == "restart":
                restart = True
                player.restart()
                start_time = pygame.time.get_ticks()
                self.game.countTimer = self.config.timer['countTimer']
                self.game.showTimer = False
                self.game.positionTimer = None
                self.time = 0
                self.init.connections += 1
                clientsList.updateValues(player.id, player.position, player.angle, player.speed, player.max_speed,
                                         player.acceleration, player.breaks, player.turn, player.lab, player.rect,
                                         self.time - player.bonusTime, self.game.showTimer, self.game.positionTimer,
                                         self.win, self.winner, self.init.connections)

            else:
                clientsList.updateValues(player.id, player.position, player.angle, player.speed, player.max_speed,
                                         player.acceleration, player.breaks, player.turn, player.lab, player.rect,
                                         0, self.game.showTimer, self.game.positionTimer, self.win, self.winner,
                                         self.init.connections)


            conn.send(pickle.dumps(self.init.players))
            time.sleep(0.001)

        # When user disconnects
        print("[DISCONNECT] Name:", name, ", Client Id:", _id, "disconnected")
        self.playersId.append(_id)
        self.playersId.sort()
        self.init.connections -= 1

        if clientsList in self.init.players:
            self.init.removePlayer(clientsList)  # remove client information from players list
            self.game.players.remove(player)
        conn.close()  # close connection


server()
