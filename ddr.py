import pygame
import sys
from pygame.cursors import load_xbm
from pygame.locals import *
from math import *
WHITE=(255,255,255)
BLACK=(0,0,0,0)
RED=(255,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
GRAY=(0,120,120)
desX=500;desY=700
pygame.init()
WIN=pygame.display.set_mode((800,800))
WIN.fill(BLACK)
bot=pygame.Rect(30,30,50,30)
clk=pygame.time.Clock()
VR=0
VL=0
class diffDrive:
    def __init__(self):
        self.pose=[30,30]
        self.theta=-pi/2
        self.vel=[0,0]
        self.dt=0.1
        self.l=30
    def move(self):
        self.controller()
        v=(self.vel[0]+self.vel[1])/2
        w=(-self.vel[1]+self.vel[0])/self.l
        self.theta+=w*self.dt
        self.pose[0]=self.pose[0]+v*cos(self.theta)
        self.pose[1]=self.pose[1]+v*sin(self.theta)
    def controller(self):
        if abs(atan2((desY-self.pose[1]),(desX-self.pose[0]))-self.theta)<pi/60:
            self.vel=[10,10]
        else:
            err=atan2((desY-self.pose[1]),(desX-self.pose[0]))-self.theta
            w=2*err
            self.vel=[15*w,-15*w]
ddr=diffDrive()
if __name__=='__main__':
    while True:
        clk.tick(10)
        # x,y=pygame.mouse.get_pos()  
        # if pygame.mouse.get_pressed():    
        #     if y>0 and y<10:
        #         ddr.vel[0]=(float(x)-400)/8
        #     elif y>10 and y<20:
        #         ddr.vel[1]=(float(x)-400)/8
        #     elif y>50:
        #         ddr.pose=[x,y]
        #         ddr.theta=0
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        if pygame.mouse.get_pressed():
            desX,desY=pygame.mouse.get_pos()
        ddr.move()
        X=floor(ddr.pose[0]-(6*cos(ddr.theta)))
        Y=floor(ddr.pose[1]-(6*sin(ddr.theta)))
        X1=floor(ddr.pose[0]+(6*cos(ddr.theta)))
        Y1=floor(ddr.pose[1]+(6*sin(ddr.theta)))
        front_X=floor(X-(15*sin(ddr.theta)))
        front_Y=floor(Y+(15*cos(ddr.theta)))
        front_X1=floor(X+(15*sin(ddr.theta)))
        front_Y1=floor(Y-(15*cos(ddr.theta)))
        back_X=floor(X1-(15*sin(ddr.theta)))
        back_Y=floor(Y1+(15*cos(ddr.theta)))
        back_X1=floor(X1+(15*sin(ddr.theta)))
        back_Y1=floor(Y1-(15*cos(ddr.theta)))     
        WIN.fill(BLACK)
        pygame.draw.line(WIN,RED,(0,5),(floor(ddr.vel[0]*8+400),5),10)
        pygame.draw.line(WIN,GREEN,(0,15),(floor(ddr.vel[1]*8+400),15),10)
        pygame.draw.circle(WIN,GRAY, (floor(ddr.pose[0]),floor(ddr.pose[1])), 14)
        pygame.draw.line(WIN,WHITE,(front_X,front_Y),(back_X,back_Y),3)
        pygame.draw.line(WIN,WHITE,(front_X1,front_Y1),(back_X1,back_Y1),3)
        pygame.display.flip()