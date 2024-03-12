import math
from variable import Ball
from variable import Robot
import socket
import vision_detection_pb2 as vd
from math import atan2, sqrt

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest_addr = ('',41001)
udp_socket.bind(dest_addr)
vd = vd.Vision_DetectionFrame()
BLUE = 1
YELLOW = 0

class DataStatistic:
    def __init__(self):
        #控球相关的数据
        self.theirHolding = False
        self.ourHolding = False
        self.ballIsHold = False
        self.ourHoldingTime = 0
        self.theirHoldingTime = 0
        self.noHoldingTime = 0
        self.ourShootNum = 0
        self.theirShootNum = 0
        self.robotNum = 8
        self.totalRobotNum = 16
        self.blueRobots = []
        self.yellowRobots = []
        self.ball = Ball(0, 0, 0, 0, 0)
        self.ourHoldingNum = -1
        self.theirHoldingNum = -1
        self.holdingThreshold = 150 #判断控球的阈值距离，为需要调整的参数
        self.ourHoldingRate = 0
        self.theirHoldingRate = 0
        self.totalTime = 0
        self.groundWidth = 6000
        self.groundHeight = 4500
        self.ballHoldingNum = -1
        self.lastHoldingNum = -1

        #射门相关的数据
        self.gateWidth = 900 #判断是射门的球的范围，为需要调整的参数，以下也均需要修改
        self.gateHeight = 300
        self.restrictedAreaWidth = 1800
        self.restrictedAreaHeight = 1800
        self.shootAngleThreshold = 1
        self.shootVelocityThreshold = 50

        #传球相关的数据
        self.ourPassingNum = 0
        self.theirPassingNum = 0
        self.ourTotalPassingNum = 0
        self.theirTotalPassingNum = 0
        self.ourLastHoldingNum = -1
        self.theirLastHoldingNum = -1
        self.ballStates = []
        self.stateLength = 10
        self.ballHoldingList = [] #存储每一帧拿球队员的号码， 蓝色号小，黄色号大，从1~16(self.totalRobotNum)，不控球用-1表示
        #传球失误即丢失球权的数据
        self.ourLosingPossessionNum = 0
        self.theirLosingPossessionNum = 0




        for i in range(self.robotNum):
            self.blueRobots.append(Robot(0, 0, 0, 0, 0, False, BLUE))
            self.yellowRobots.append(Robot(0, 0, 0, 0, 0, False, YELLOW))

    def update(self, vision):
        for i in range(self.robotNum):
            blueRobot = vision.robots_blue[i]
            yellowRobot = vision.robots_yellow[i]
            self.blueRobots[i].update(blueRobot.x, blueRobot.y, blueRobot.orientation, blueRobot.vel_x, blueRobot.vel_y, blueRobot.valid)
            self.yellowRobots[i].update(yellowRobot.x, yellowRobot.y, yellowRobot.orientation, yellowRobot.vel_x, yellowRobot.vel_y, yellowRobot.valid)
        self.ball.update(vision.balls.x, vision.balls.y, vision.balls.orientation, vision.balls.vel_x, vision.balls.vel_y)
        self.totalTime += 1

    #(1)判断控球的函数
    def judgeHolding(self):
        for i in range(self.robotNum):
            blue = self.blueRobots[i]
            yellow = self.yellowRobots[i]
            ourDir = blue.orientation
            theirDir = yellow.orientation
            ballToThem = atan2(self.ball.y - blue.y, self.ball.x - blue.x)
            ballToUs = atan2(self.ball.y - yellow.y, self.ball.x - yellow.x)
            ourDis = sqrt((blue.x - self.ball.x)**2 + (blue.y - self.ball.y)**2)
            theirDis = sqrt((yellow.x - self.ball.x) ** 2 + (yellow.y - self.ball.y) ** 2)
            if blue.valid and ourDis < self.holdingThreshold and abs(ballToUs - ourDir) < 1: #角度阈值1可能需要修改
                self.ballIsHold = True
                self.ourHolding = True
                self.theirHolding = False
                self.ourHoldingTime += 1
                self.ourHoldingNum = i
                self.theirHoldingNum = -1
            if yellow.valid and theirDis < self.holdingThreshold and abs(ballToThem - theirDir) < 1:
                self.ballIsHold = True
                self.ourHolding = False
                self.theirHolding = True
                self.theirHoldingTime += 1
                self.theirHoldingNum = i
                self.ourHoldingNum = -1

            if self.ourHoldingNum > 0:
                self.ballHoldingList.append(self.ourHoldingNum)
            elif self.theirHoldingNum > 0:
                self.ballHoldingList.append((self.theirHoldingNum + 8))
            else:
                self.ballHoldingList.append(-1)

    #一定时间清空持球车辆的顺序集合
    def stateClearing(self):
        self.ballHoldingList.clear()

    def inRestrictedZone(self):
        if abs(self.ball.x) < self.restrictedAreaWidth and abs(self.ball.y) > self.groundWidth - self.restrictedAreaHeight:
            return True

    def inOurRestrictedZone(self):
        return (self.ball.x < 0) and self.inRestrictedZone()

    def intheirRestrictedZone(self):
        return (self.ball.x > 0) and self.inRestrictedZone()

    #(2)判断是否出现射门的函数
    #通过球是否在禁区内、球速度方向是否朝向球门方向、球速是否大于一定阈值来判断是否为射门
    def judgeShooting(self):
        ballDir = atan2(self.ball.vy, self.ball.vx)
        ballVelocity = sqrt(self.ball.vx**2 + self.ball.vy**2)
        velocityThreshold = 200 #球速达到一定值判断为射门的阈值， 为需要调节的参数
        if self.intheirRestrictedZone() and ballDir <= math.pi / 4 and ballDir >= -math.pi / 4 and ballVelocity >= velocityThreshold:
            self.ourShootNum += 1
        if self.inOurRestrictedZone() and ((ballDir <= math.pi and ballDir >= 0.75 * math.pi) or (ballDir <= -0.75 * math.pi and ballDir >= -math.pi)) and ballVelocity >= velocityThreshold:
            self.theirShootNum += 1

#############################################################################
    #(3)判断统计是否成功传球或丢失球权，用持球的车号的状态变换来表示传球或者丢失球权
    def judgePassingAndLossingPossesion(self):
        ballDir = atan2(self.ball.vy, self.ball.vx)
        listLength = len(self.ballHoldingList)
        for i in range(listLength):
            currentHoldingNum = self.ballHoldingList[i]
            if self.ballHoldingList[i] > 0:
               self.lastHoldingNum = self.ballHoldingList[i]
            if currentHoldingNum > 0:
                if currentHoldingNum == self.lastHoldingNum:
                    continue
                if self.lastHoldingNum <= 8:
                    if abs(currentHoldingNum - self.lastHoldingNum) < 8:
                        self.ourPassingNum += 1
                    elif abs(currentHoldingNum - self.lastHoldingNum) >= 8:
                        self.ourLosingPossessionNum += 1
                elif self.lastHoldingNum > 8:
                    if abs(currentHoldingNum - self.lastHoldingNum) < 8:
                        self.theirPassingNum += 1
                    elif abs(currentHoldingNum - self.lastHoldingNum) >= 8:
                        self.theirLosingPossessionNum += 1



    def getHoldingRate(self):
        self.ourHoldingRate = self.ourHoldingTime / (self.ourHoldingTime + self.noHoldingTime)
        self.theirHoldingRate = self.theirHoldingTime / (self.ourHoldingTime + self.noHoldingTime)
        self.noHoldingTime = self.totalTime - self.ourHoldingTime - self.theirHoldingTime
        return self.ourHoldingRate, self.theirHoldingRate


if __name__ == "__main__":
    JackData = DataStatistic()
    totalTime = 0
    matchBreak = False
    while True:
        # 每一帧计算的数据统计顺序
        # 更新控球状态序列信息
        #判断哪方控球
            #处于控球状态， 则统计控球时间
            #判断是否发生了传球或者传球失误导致丢失球权
            #不处于控球状态，遍历相邻的控球车辆， 同时根据当前球的速度与位置判断是否发生了传球或射门


        # receive data from server
        recv_data = udp_socket.recvfrom(4096)
        vd.ParseFromString(recv_data[0])
        JackData.update(vd)
        JackData.judgeHolding()
        if matchBreak:
            JackData.getHoldingRate()
            break







