#!/usr/bin/python

# import the soccer bot module - this will include math, time, numpy (as np) and vrep python modules
from soccerbot_lib import *
import time
# SET SCENE PARAMETERS
sceneParameters = SceneParameters()

# SET ROBOT PARAMETERS
robotParameters = RobotParameters()
robotParameters.driveType = 'omni'	# specify if using differential or omni drive system

# MAIN SCRIPT
if __name__ == '__main__':

        # Wrap everything in a try except case that catches KeyboardInterrupts.
        # In the exception catch code attempt to Stop the VREP Simulator so don't have to Stop it manually when pressing CTRL+C
        try:
                soccerBotSim = VREP_SoccerBot('127.0.0.1', robotParameters, sceneParameters)
                soccerBotSim.StartSimulator()
                pastBall=[]
                ballFindStartTime = time.time()
                ran = False
                rann = False
                rannn = False
                goalKicked = False
                searchYellow = False
                searchBlue = False

                while True:

                        ballin = soccerBotSim.BallInDribbler()
                        goBlue = True
                        goYellow = False
                        soccerBotSim.SetCameraPose(0, 0.2, 0.5)
                        objectsDetected = soccerBotSim.GetDetectedObjects()
                        soccerBotSim.UpdateObjectPositions()

#-----------------------Face Ball and Move To It----------------------------------------------#

                        if not soccerBotSim.BallInDribbler():
                                soccerBotSim.UpdateObjectPositions()
                                if objectsDetected[0] != None and objectsDetected[0][1]<-0.08:
                                        soccerBotSim.UpdateObjectPositions()
                                        soccerBotSim.SetTargetVelocities(0, 0, -0.10)
                                        print("Turning right to face ball")
                                elif objectsDetected[0] != None and objectsDetected[0][1]>0.08:
                                        soccerBotSim.UpdateObjectPositions()
                                        soccerBotSim.SetTargetVelocities(0, 0, 0.10)
                                        print("Turning left to face ball")
                                elif objectsDetected[0] != None and -0.08<objectsDetected[0][1]<0.08:
                                        soccerBotSim.UpdateObjectPositions()
                                        print("Lined up and moving to the ball")
                                        pastBall.append(objectsDetected[0][0])
                                        soccerBotSim.SetTargetVelocities(0.10, 0, 0)

#-------------------------------Search For Ball----------------------------#

                                elif objectsDetected[0] == None and searchYellow == False and searchBlue == False:
                                        goalKicked = False
                                        soccerBotSim.UpdateObjectPositions()
                                        print("Searching")
                                        soccerBotSim.SetTargetVelocities(0, 0, 0.4)
                                        while not soccerBotSim.BallInDribbler() and objectsDetected[0] == None and len(pastBall) !=0 and pastBall[-1]<0.3 and goalKicked != True:
                                                soccerBotSim.UpdateObjectPositions()
                                                print("CHARGE!!!")
                                                soccerBotSim.SetTargetVelocities(0.15, 0, 0)


                                if objectsDetected[0] == None and not soccerBotSim.BallInDribbler():
                                        ballFindElapsedTime = time.time() - ballFindStartTime
                                        print(ballFindElapsedTime)
                                if ballFindElapsedTime>5 and objectsDetected[2] != None and objectsDetected[2][0]>0.6 and objectsDetected[2][1]<-0.1 and objectsDetected[0] == None:
                                        soccerBotSim.SetTargetVelocities(0.08, 0, -0.08)
                                elif ballFindElapsedTime>5 and objectsDetected[2] != None and objectsDetected[2][0]>0.6 and objectsDetected[2][1]>0.1 and objectsDetected[0] == None:
                                        soccerBotSim.SetTargetVelocities(0, 0, 0.08)
                                elif ballFindElapsedTime>5 and objectsDetected[2] != None and -0.1<objectsDetected[2][1]<0.1 and objectsDetected[2][0]>0.6 and objectsDetected[0] == None:
                                        print(objectsDetected[2][0])
                                        print('moving to search yellow goal area')
                                        soccerBotSim.SetTargetVelocities(0.08, 0, 0)
                                        searchYellow = True

                                if ballFindElapsedTime>5 and objectsDetected[2] != None and objectsDetected[2][0]<=0.6 and not ran:
                                        print('resetting time')
                                        ballFindStartTime = time.time()
                                        ran = True
                                        searchYellow = False

                                if ran == True and objectsDetected[0] == None:
                                        if ballFindElapsedTime>5 and objectsDetected[1] != None and objectsDetected[1][0]>0.6 and objectsDetected[1][1]<-0.1 and objectsDetected[0] == None:
                                            soccerBotSim.SetTargetVelocities(0.08, 0, -0.08)
                                        elif ballFindElapsedTime>5 and objectsDetected[1] != None and objectsDetected[1][0]>0.6 and objectsDetected[1][1]>0.1 and objectsDetected[0] == None:
                                            soccerBotSim.SetTargetVelocities(0, 0, 0.08)
                                        elif ballFindElapsedTime>5 and objectsDetected[1] != None and -0.1<objectsDetected[1][1]<0.1 and objectsDetected[1][0]>0.6 and objectsDetected[0] == None:
                                            print(objectsDetected[1][0])
                                            print('moving to search blue goal area')
                                            soccerBotSim.SetTargetVelocities(0.08, 0, 0)
                                            searchBlue = True
                                if ballFindElapsedTime>5 and objectsDetected[1] != None and objectsDetected[1][0]<=0.6 and not rann and ran == True:
                                        print('resetting time')
                                        ballFindStartTime = time.time()
                                        rann = True
                                        searchYellow = False
                                        searchBlue = False


#-----------------------Object Avoidance------------------------------------#

                        if objectsDetected[3]!=None:
                                print('obstacle!!!!!!!')
                                #print(objectsDetected[3])
                                for object in objectsDetected[3]:
                                        print(object)
                                        if object[0]<=0.4:
                                                if object[1]>=0.01:
                                                        soccerBotSim.SetTargetVelocities(-0.05, -0.10, 0)
                                                elif object[1]<=-0.01:
                                                        soccerBotSim.SetTargetVelocities(-0.05, 0.10, 0)
                                                
                              
                               
                                        
                        

#-----------------------Ball in the dribbler---------------------------------#

                        if soccerBotSim.BallInDribbler():
                                print("I has ball")
                                pastBall = []

#-----------------------Going for Yellow--------------------------------------#

                        if goYellow == True:

                                if soccerBotSim.BallInDribbler() and objectsDetected[2] == None:
                                        soccerBotSim.UpdateObjectPositions()
                                        print("Searching for goal to score")
                                        soccerBotSim.SetTargetVelocities(0, 0, 0.3)

                                if objectsDetected[2] != None and soccerBotSim.BallInDribbler():
                                        print('YGRange: ', objectsDetected[2][0])
                                        print('YGBearing: ' , objectsDetected[2][1])
                                        print("Getting into position")
                                if objectsDetected[2] != None and objectsDetected[2][1]>0.08 and objectsDetected[2][0]> 0.5 and soccerBotSim.BallInDribbler():
                                        soccerBotSim.SetTargetVelocities(0, 0, 0.10)
                                        print('left!')
                                if objectsDetected[2] != None and objectsDetected[2][1]<-0.08 and objectsDetected[2][0]> 0.5 and soccerBotSim.BallInDribbler():
                                        soccerBotSim.SetTargetVelocities(0, 0, -0.10)
                                        print('right!')
                                if objectsDetected[2] != None and -0.08<objectsDetected[2][1]<0.08 and soccerBotSim.BallInDribbler() and objectsDetected[2][0] <0.8:
                                        print("Kicking the ball")
                                        soccerBotSim.SetTargetVelocities(0, 0, 0)
                                        time.sleep(2)
                                        soccerBotSim.KickBall(0.2)
                                        soccerBotSim.UpdateObjectPositions()
                                        pastBall = []
                                        goalKicked = True
                                elif objectsDetected[2] != None and -0.08<objectsDetected[2][1]<0.08 and soccerBotSim.BallInDribbler() and objectsDetected[2][0] >0.8:
                                        soccerBotSim.SetTargetVelocities(0.08, 0, 0)

#-----------------------Going for Yellow--------------------------------------#

                        if goBlue == True:

                                if soccerBotSim.BallInDribbler() and objectsDetected[1] == None:
                                        soccerBotSim.UpdateObjectPositions()
                                        print("Searching for goal to score")
                                        soccerBotSim.SetTargetVelocities(0, 0, 0.15)

                                if objectsDetected[1] != None and soccerBotSim.BallInDribbler():
                                        print('BGRange: ', objectsDetected[1][0])
                                        print('BGBearing: ' , objectsDetected[1][1])
                                        print("Getting into position")
                                if objectsDetected[1] != None and objectsDetected[1][1]>0.08 and objectsDetected[1][0]> 0.5 and soccerBotSim.BallInDribbler():
                                        soccerBotSim.SetTargetVelocities(0, 0, 0.10)
                                        print('left!')
                                if objectsDetected[1] != None and objectsDetected[1][1]<-0.08 and objectsDetected[1][0]> 0.5 and soccerBotSim.BallInDribbler():
                                        soccerBotSim.SetTargetVelocities(0, 0, -0.10)
                                        print('right!')
                                if objectsDetected[1] != None and -0.08<objectsDetected[1][1]<0.08 and soccerBotSim.BallInDribbler() and objectsDetected[1][0] <0.8:
                                        print("Kicking the ball")
                                        soccerBotSim.SetTargetVelocities(0, 0, 0)
                                        time.sleep(2)
                                        soccerBotSim.KickBall(0.2)
                                        soccerBotSim.UpdateObjectPositions()
                                        pastBall = []
                                        goalKicked = True
                                        ballFindStartTime = time.time()
                                elif objectsDetected[1] != None and -0.08<objectsDetected[1][1]<0.08 and soccerBotSim.BallInDribbler() and objectsDetected[1][0] >0.8:
                                        soccerBotSim.SetTargetVelocities(0.08, 0, 0)


        except KeyboardInterrupt as e:
                # attempt to stop simulator so it restarts and don't have to manually press the Stop button in VREP
                soccerBotSim.StopSimulator()
