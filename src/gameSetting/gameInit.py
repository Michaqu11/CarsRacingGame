

class GameInit:

    def __init__(self):
        self.players = []
        self.connections = 0

    def addConnections(self):
        self.connections += 1

    def addPlayer(self, player):
        self.players.append(player)

    def removePlayer(self, player):
        self.players.remove(player)
