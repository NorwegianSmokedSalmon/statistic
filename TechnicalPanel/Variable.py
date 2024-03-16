class Robot:
    def __init__(self, x, y, orientation, velX, velY, valid, team):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.vx = velX
        self.vy = velY
        self.valid = valid
        self.team = team
        self.radius = 10

    def update(self, x, y, orientation, velX, velY, valid):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.vx = velX
        self.vy = velY
        self.valid = valid

class Ball:
    def __init__(self, x, y, velX, velY):
        self.x = x
        self.y = y
        self.vx = velX
        self.vy = velY
        self.radius = 5

    def update(self, x, y,  velX, velY):
        self.x = x
        self.y = y
        self.vx = velX
        self.vy = velY
