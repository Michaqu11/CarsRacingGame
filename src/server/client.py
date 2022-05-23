from src.config.Config import Config
from src.gameSetting.game import Game
import pygame
import src.server.network as network


def restartMoves():
    keys = pygame.key.get_pressed()
    move = [False, False]
    if keys[pygame.K_r]:
        move[0] = True

    if keys[pygame.K_q]:
        move[1] = True
    return move


def moves():
    keys = pygame.key.get_pressed()
    move = [False, False, False, False, True]

    if keys[pygame.K_w]:
        move[0] = True

    if keys[pygame.K_s]:
        move[1] = True

    if keys[pygame.K_a]:
        move[2] = True

    if keys[pygame.K_d]:
        move[3] = True

    if keys[pygame.K_ESCAPE]:
        move[4] = False

    return move


name = input("Please enter your name: ")

pygame.init()
server = network.Network()
config = Config()

current_id = server.connect(name)
players = server.send("get")

game = Game()
game.screen = pygame.display.set_mode((game.assets.width, game.assets.height))
pygame.display.set_caption("Car Racing")
assets = [(game.assets.track, (0, 0)), (game.assets.start, (502, 160)), (game.assets.borders, (0, 0))]
run = True
game.constDraw()
start = True
win = False
sendEndInfo = True

cur_players = next((x for x in players if x.id == current_id))
while run:

    pygame.time.Clock().tick(config.FPS)

    if start and cur_players.connection == config.playersNumer:
        players = server.send("temp")
        cur_players = next((x for x in players if x.id == current_id))
        start_ticks = pygame.time.get_ticks()
        game.constDraw()
        while True:
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            if seconds > 5:
                break
            game.draw(game.screen, assets, cur_players.lab, cur_players.speed,
                      cur_players.time)
            for p in players:
                game.drawCar(game.loadCar(p.id), p.angle, p.position)
            game.draw_counter(int(seconds))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        game.constDraw()

        data = "time"
        players = server.send(data)
        start = False

    keys = pygame.key.get_pressed()

    data = "move"
    for m in moves():
        data += " " + str(m)

    players = server.send(data)
    if not players:
        break
    cur_players = next((x for x in players if x.id == current_id))
    game.draw(game.screen, assets, cur_players.lab, cur_players.speed, cur_players.time)

    if cur_players.showTimer:
        game.showTimerBonus(cur_players.posTimer)

    for p in players:
        game.drawCar(game.loadCar(p.id), p.angle, p.position)

    if cur_players.win and not start:
        game.drawWinner(cur_players.name)
        keys = restartMoves()
        if keys[0]:
            players = server.send("restart")
            start = True

        if keys[1]:
            run = False
        game.draw_end_game_info()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

server.disconnect()
pygame.quit()
quit()
