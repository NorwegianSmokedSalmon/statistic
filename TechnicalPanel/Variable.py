import pygame as pg
import socket
import vision_detection_pb2 as vd


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

    def draw(self, screen):
        color = (0, 0, 255) if self.team else (255, 255, 0)
        pg.draw.circle(screen, color, (self.x, self.y), self.radius)


class Ball:
    def __init__(self, x, y, velX, velY):
        self.x = x
        self.y = y
        self.vx = velX
        self.vy = velY
        self.radius = 5

    def update(self, x, y, velX, velY):
        self.x = x
        self.y = y
        self.vx = velX
        self.vy = velY

    def draw(self, screen):
        color = (255, 0, 0)
        pg.draw.circle(screen, color, (self.x, self.y), self.radius)

# field params
HEIGHT = 1080
WIDTH = 1920
PITCH_WIDTH = 9000
PITCH_HEIGHT = 12000

# robot params
TOTAL_ROBOT_NUM = 16
BLUE = True
YELLOW = False
robots_blue = []
robots_yellow = []

# game loop
if __name__ == '__main__':
    # initialize socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    dest_addr = ('', 41001)

    udp_socket.bind(dest_addr)

    vd = vd.Vision_DetectionFrame()


    # initialize pygame
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Robocup")

    # initialize robots
    for i in range(TOTAL_ROBOT_NUM):
        robots_blue.append(Robot(0, 0, 0, 0, 0, False, BLUE))
        robots_yellow.append(Robot(0, 0, 0, 0, 0, False, YELLOW))

    # initialize ball
    ball = Ball(0, 0, 0, 0, 0)


    while True:
        # receive data from server
        recv_data = udp_socket.recvfrom(4096)
        vd.ParseFromString(recv_data[0])


        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        screen.fill((255, 255, 255))

        def transform(x,y):
            # transform coordinates from 9000*12000 to screen
            x = x / PITCH_WIDTH * WIDTH + WIDTH / 2
            y = y / PITCH_HEIGHT * HEIGHT + HEIGHT / 2
            return x, y

        for idx in range(TOTAL_ROBOT_NUM):
            robot_blue = vd.robots_blue[idx]
            robot_yellow = vd.robots_yellow[idx]

            x_blue, y_blue = transform(robot_blue.x, robot_blue.y)
            x_yellow, y_yellow = transform(robot_yellow.x, robot_yellow.y)
            robots_blue[idx].update(x_blue, y_blue, robot_blue.orientation, robot_blue.vel_x, robot_blue.vel_y, robot_blue.valid)
            robots_yellow[idx].update(x_yellow, y_yellow, robot_yellow.orientation, robot_yellow.vel_x, robot_yellow.vel_y, robot_yellow.valid)
            if robot_blue.valid:
                robots_blue[idx].draw(screen)
            if robot_yellow.valid:
                robots_yellow[idx].draw(screen)

        ball.x, ball.y = transform(vd.balls.x, vd.balls.y)
        ball.draw(screen)

        pg.display.update()
        clock.tick(60)