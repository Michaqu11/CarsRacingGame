class ClientInfo:
    def __init__(self, config, id, position, angle,speed ,max_speed, acceleration, breaks, turn, lab, rect, time, showTimer, posTimer, win, name, con):
        self.config = config
        self.id = id
        self.position = position
        self.angle = angle
        self.speed = speed
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.breaks = breaks
        self.turn = turn
        self.lab = lab
        self.rect = rect
        self.time = time
        self.showTimer = showTimer
        self.posTimer = posTimer
        self.win = win
        self.name = name
        self.connection = con


    def updateValues(self, id, position, angle,speed ,max_speed, acceleration, breaks, turn, lab, rect, time, showTimer, posTimer, win, name, con):
        self.id = id
        self.position = position
        self.angle = angle
        self.speed = speed
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.breaks = breaks
        self.turn = turn
        self.lab = lab
        self.rect = rect
        self.time = time
        self.showTimer = showTimer
        self.posTimer = posTimer
        self.win = win
        self.name = name
        self.connection = con
