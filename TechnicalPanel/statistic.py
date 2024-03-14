import math
from Variable import Ball
from Variable import Robot
import socket
import vision_detection_pb2 as vd
from math import atan2, sqrt, pi
from itertools import groupby #用于去除列表中局部连续的重复元素，只留一个
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest_addr = ('',41001)
udp_socket.bind(dest_addr)
vd = vd.Vision_DetectionFrame()
BLUE = 1
YELLOW = 0

#用于去除列表中局部连续的重复元素，只留一个
def remove_consecutive_duplicates(lst):
    return [key for key, group in groupby(lst)]

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
        self.ball = Ball(0, 0, 0, 0)
        self.ourHoldingNum = -1
        self.theirHoldingNum = -1
        self.holdingThreshold = 1500 #判断控球的阈值距离，为需要调整的参数***************************************************
        self.ourHoldingRate = 0
        self.theirHoldingRate = 0
        self.totalTime = 0
        self.groundWidth = 6000
        self.groundHeight = 4500
        self.ballHoldingNum = -1
        self.lastHoldingNum = -1
        self.holdingFpsThreshold = 5 #连续几帧judgeHolding为同一辆车，视为该车处于控球状态

        #射门相关的数据
        self.gateWidth = 900 #判断是射门的球的范围，为需要调整的参数，以下也均需要修改
        self.gateHeight = 300
        self.restrictedAreaWidth = 1800
        self.restrictedAreaHeight = 1800
        self.shootAngleThreshold = 1
        self.shootVelocityThreshold = 100

        #传球相关的数据
        self.ourPassingNum = 0
        self.theirPassingNum = 0
        self.ourTotalPassingNum = 0
        self.theirTotalPassingNum = 0
        self.ourLastHoldingNum = -1
        self.theirLastHoldingNum = -1
        self.ourPassSuccessRate = 0
        self.theirPassSuccessRate = 0
        self.ballStates = []
        self.ballHoldingList = [] #存储每一帧拿球队员的号码， 蓝色号小，黄色号大，从1~16(self.totalRobotNum)，不控球用-1表示

        #输出计时器
        self.printInterval = 300 #打印信息的时间间隔
        self.time = 0

        #传球失误即丢失球权的数据
        self.ourLosingPossessionNum = 0
        self.theirLosingPossessionNum = 0
        #初始化机器人
        for i in range(self.robotNum):
            self.blueRobots.append(Robot(0, 0, 0, 0, 0, False, BLUE))
            self.yellowRobots.append(Robot(0, 0, 0, 0, 0, False, YELLOW))

    #更新视觉信息
    def update(self, vision):
        for i in range(self.robotNum):
            blueRobot = vision.robots_blue[i]
            yellowRobot = vision.robots_yellow[i]
            self.blueRobots[i].update(blueRobot.x, blueRobot.y, blueRobot.orientation, blueRobot.vel_x, blueRobot.vel_y, blueRobot.valid)
            self.yellowRobots[i].update(yellowRobot.x, yellowRobot.y, yellowRobot.orientation, yellowRobot.vel_x, yellowRobot.vel_y, yellowRobot.valid)
        self.ball.update(vision.balls.x, vision.balls.y, vision.balls.vel_x, vision.balls.vel_y)
        self.totalTime += 1

    #判断当前帧控球的车辆
    def judgeHoldingNum(self):
        for i in range(self.robotNum):
            blue = self.blueRobots[i]
            yellow = self.yellowRobots[i]
            ourDir = blue.orientation
            theirDir = yellow.orientation
            ballToThem = atan2(self.ball.y - blue.y, self.ball.x - blue.x)
            ballToUs = atan2(self.ball.y - yellow.y, self.ball.x - yellow.x)
            ourDis = sqrt((blue.x - self.ball.x)**2 + (blue.y - self.ball.y)**2)
            theirDis = sqrt((yellow.x - self.ball.x) ** 2 + (yellow.y - self.ball.y) ** 2)
            if blue.valid and ourDis < self.holdingThreshold and abs(ballToUs - ourDir) < 1.5: #角度阈值1.5可能需要修改
                self.ballIsHold = True
                self.ourHolding = True
                self.theirHolding = False
                self.ourHoldingNum = i
                self.theirHoldingNum = -1
                print("our holding!!!!!!!!!!!!!!!!!!!!!!!")
            if yellow.valid and theirDis < self.holdingThreshold and abs(ballToThem - theirDir) < 1.5:
                self.ballIsHold = True
                self.ourHolding = False
                self.theirHolding = True
                self.theirHoldingNum = i
                self.ourHoldingNum = -1
                print("their holding!!!!!!!!!!!!!!!!!!!!")

    # 确认控球的车号，将我方车辆映射到1 ~ 8，对方车辆映射到9 ~ 16
    def confirmHoldingNum(self):
        holdingNum = -1
        if self.ourHoldingNum > 0:
            holdingNum = self.ourHoldingNum
        elif self.theirHoldingNum > 0:
            holdingNum = self.theirHoldingNum + 8
        return holdingNum

    # 连续一定帧数某辆车满足judgeHolding，被判断为处于控球状态，根据长度添加控球时间
    def confirmHolding(self):
        if len(self.ballHoldingList) > 0:
            last = self.ballHoldingList[0]
        list = []
        if len(self.ballHoldingList) >= 90:
            for p in self.ballHoldingList:
                if p == -1:
                    continue
                elif p > 0:
                    if p == last:
                        list.append(p)
                    elif p != last:
                        if len(list) >= self.holdingFpsThreshold:
                            if list[0] <= 8:
                                self.ourHoldingTime += len(list)
                            elif list[0] > 8:
                                self.theirHoldingTime += len(list)
                        list.clear()
                last = p

    #一定时间清空持球车辆的顺序集合
    def updateHoldingList(self):
        if len(self.ballHoldingList) < 100:
            self.ballHoldingList.append(self.confirmHoldingNum())
        elif len(self.ballHoldingList) >= 100:
            self.ballHoldingList.clear()

    #球是否在禁区里面
    def inRestrictedZone(self):
        if abs(self.ball.x) < self.restrictedAreaWidth and abs(self.ball.y) > self.groundWidth - self.restrictedAreaHeight:
            return True

    #在我方禁区
    def inOurRestrictedZone(self):
        return (self.ball.x < 0) and self.inRestrictedZone()

    #在对方禁区
    def intheirRestrictedZone(self):
        return (self.ball.x > 0) and self.inRestrictedZone()

    #获取移除-1的控球集合,同时去除控球集合中局部连续的重复元素，只留一个
    def getRemovingNoholdingAndRepeatingNumList(self):
        holdingList = self.ballHoldingList
        reduceCount = 0 #记录移除-1的次数
        if len(holdingList) > 0:
            for i in range(len(holdingList)):
                if holdingList[i - reduceCount] == -1:
                    holdingList.remove(-1)
                    reduceCount += 1
        return remove_consecutive_duplicates(holdingList)

    #判断是出现成功传球与传球失误导致丢失球权
    def judgePassAndLosingPossesseion(self):
        stateList = self.getRemovingNoholdingAndRepeatingNumList()
        if len(stateList) > 0:
            for i in range (len(stateList) - 1):
                #我方传球成功
                if abs(stateList[i + 1] - stateList[i]) < 8 and abs(stateList[i + 1] - stateList[i]) > 0 and stateList[i] <=8:
                    self.ourPassingNum += 1
                #我方传球失误
                elif abs(stateList[i + 1] - stateList[i]) >= 8 and stateList[i] <= 8:
                    self.ourLosingPossessionNum += 1
                #对方传球成功
                elif abs(stateList[i + 1] - stateList[i]) < 8 and abs(stateList[i + 1] - stateList[i]) > 0 and stateList[i] > 8:
                    self.theirPassingNum += 1
                #对方传球失误
                elif abs(stateList[i + 1] - stateList[i]) >= 8 and stateList[i] > 8:
                    self.theirLosingPossessionNum += 1

    #判断是否出现射门，通过球是否在禁区内、球速度方向是否朝向球门方向、球速是否大于一定阈值来判断是否为射门
    def judgeShooting(self):
        ballDir = atan2(self.ball.vy, self.ball.vx)
        ballVelocity = sqrt(self.ball.vx**2 + self.ball.vy**2)
        if self.intheirRestrictedZone() and ballDir <= math.pi / 4 and ballDir >= -math.pi / 4 and ballVelocity >= self.shootVelocityThreshold:
            self.ourShootNum += 1
        if self.inOurRestrictedZone() and ((ballDir <= math.pi and ballDir >= 0.75 * math.pi) or (ballDir <= -0.75 * math.pi and ballDir >= -math.pi)) and ballVelocity >= self.shootVelocityThreshold:
            self.theirShootNum += 1

    #生成控球率、传球成功率信息
    def generateInfo(self):
        if self.ourHoldingTime + self.theirHoldingTime > 0:
            self.ourHoldingRate = self.ourHoldingTime / (self.ourHoldingTime + self.theirHoldingTime)
            self.theirHoldingRate = self.theirHoldingTime / (self.ourHoldingTime + self.theirHoldingTime)
        if (self.ourPassingNum + self.ourLosingPossessionNum) > 0:
            self.ourPassSuccessRate = self.ourPassingNum / (self.ourPassingNum + self.ourLosingPossessionNum)
        if (self.theirPassingNum + self.theirLosingPossessionNum) > 0:
            self.theirPassSuccessRate = self.theirPassingNum / (self.theirPassingNum + self.theirLosingPossessionNum)

    #核心函数，启动统计的运行
    def runningStatistic(self):
        self.judgeHoldingNum() #判断更新每一帧控球的车号
        self.confirmHoldingNum() #确认控球的车号，将我方车辆映射到1~8，对方车辆映射到9~16
        self.updateHoldingList() #每隔一段时间更新控球的车号集合
        self.confirmHolding() #根据控球帧数生成并添加控球时间
        self.judgePassAndLosingPossesseion() #判断是否出现成功传球与传球失误导致丢失球权
        self.judgeShooting() #判断是否出现射门
        self.generateInfo() #生成控球率、传球成功率信息
        self.printInfo() #每隔一段时间，打印信息

    #每隔一段时间，打印信息
    def printInfo(self):
        self.time += 1
        if self.time >= self.printInterval:
            print("己方控球率： ", self.ourHoldingRate)
            print("对方控球率： ", self.theirHoldingRate)
            print("己方射门次数： ", self.ourShootNum)
            print("对方射门次数： ", self.theirShootNum)
            print("己方传球次数： ", self.ourPassingNum)
            print("对方传球次数： ", self.theirPassingNum)
            print("己方丢球次数： ", self.ourLosingPossessionNum)
            print("对方丢球次数： ", self.theirLosingPossessionNum)
            print("己方传球成功率： ", self.ourPassSuccessRate)
            print("对方传球成功率： ", self.theirPassSuccessRate)
            self.time = 0

if __name__ == "__main__":
    JackData = DataStatistic()
    while True:
        # receive data from server
        recv_data = udp_socket.recvfrom(4096)
        vd.ParseFromString(recv_data[0])
        JackData.update(vd)  # 每一帧数据更新
        JackData.runningStatistic()




