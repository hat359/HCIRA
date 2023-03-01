#Authors - Harsh Athavale & Abdul Samadh Azath

from tkinter import Canvas, Button, Label, Text, PhotoImage 
from constants import * # importing from constants.py
from copy import deepcopy
from recognizer import Recognizer
from database import Database
from time import strftime, sleep
import json
import os
from shutil import rmtree
from xml.dom import minidom
import os

class Board:
    def __init__(self, root, mode):
        self.root = root
        self.mode = mode
        if self.mode == 'recognition':
            self.createCanvas()
            self.createClearButton()
            self.createPredictionLabels()
            self.points = []
            self.recognizer = Recognizer()
            self.startPointX = 0
            self.startPointY = 0
        elif self.mode == 'collection':
            self.currentWorkingDirectory = os.getcwd()
            print(self.currentWorkingDirectory)
            self.userAdded = False
            self.readyToStore = False
            self.gestureList = GESTURE_LIST
            self.currentUser = ''
            self.userDrawCount = 0
            self.gestureIndex = 0
            self.currentUserId = 'sampleUser'
            self.currentGesture = 'sampleGesture'
            self.points = []
            self.startPointX = 0
            self.startPointY = 0
            self.createCanvas()
            self.createClearButton()
            # # To be added
            # 1. DB module to store user points with user id in a json - Done
            self.db = Database()
            # 2. Show sample drawing on top right
            # 3. Add button to submit user input - Done
            self.createSubmitButton()
            # 4. Add label to show prompt to be drawn - Done
            self.createPromptLabel()
            self.setPromptLabel('Please enter userId',1)
            # 5. Add logic to show prompt and store points - Inprogress
            # 6. Add text box to get user ID and any other user data
            self.createUserIdTextBox()
            self.createGestureImageLabel()
            # 7. Convert json(database.json) to xml
    
    # def collectFromUser(self, userId):
    #     # Delete any existing user with same userId in DB and start fresh
    #     self.db.addUser(userId)
    #     for iteration in range(10):
    #         shuffle(self.gestureList)
    #         for gesture in self.gestureList:
    #             self.setPromptLabel('Please draw a {}'.format(gesture))

    
    def createCanvas(self):
        self.board = Canvas(self.root, width=BOARD_WIDTH, height=BOARD_HEIGHT, bg=BOARD_BG)
        self.setMouseBindings()
        self.board.pack()

    def createUserIdTextBox(self):
        self.userIdTextBox = Text(self.root, width=TEXT_BOX_WITDH, height=TEXT_BOX_HEIGHT)
        self.userIdTextBox.pack(side='top')

    def createClearButton(self):
        self.clearButton = Button(self.root, text=CLEAR_BUTTON_TEXT)
        self.clearButton.configure(command=self.onClearButtonClick)
        self.clearButton.pack(side = 'left')

    def createSubmitButton(self):
        self.submitButton = Button(self.root, text=SUBMIT_BUTTON_TEXT)
        self.submitButton.configure(command=self.onSubmitButtonClick)
        self.submitButton.pack(side = 'left')
    
    def createGestureImageLabel(self):
        self.gestureImageLabel = Label(self.root)

    def createPredictionLabels(self):
        self.predictedGestureLabel = Label(self.root)
        self.confidenceLabel = Label(self.root)
        self.timelabel = Label(self.root)
        # Create bindings for predicted gesture label and confidence label
        self.predictedGestureLabel.pack()
        self.confidenceLabel.pack()
        self.timelabel.pack()
    
    def setGestureImageLabel(self, img):
        self.gestureImageLabel.configure(image = img)
        self.gestureImageLabel.image = img
        self.gestureImageLabel.pack(side='right')

    def clearGestureImageLabel(self):
        self.gestureImageLabel.destroy()
    
    def setPredictionLabels(self, recognizedGesture, score, time):
        self.predictedGestureLabel.configure(text="Predicted Gesture = "  + str(recognizedGesture))
        self.confidenceLabel.configure(text="Confidence = "  + str(round(score,2))) 
        self.timelabel.configure(text="Time = "  + str(round(time*1000,2)) + " ms" )

    def clearPredictionLables(self):
        self.predictedGestureLabel.configure(text="")
        self.timelabel.configure(text="")
        self.confidenceLabel.configure(text="")
    
    def createPromptLabel(self):
        self.promptLabel1 = Label(self.root)
        self.promptLabel1.pack()

        self.promptLabel2 = Label(self.root)
        self.promptLabel2.pack()
    
    def setPromptLabel(self,message, id):
        if id == 1:
            self.promptLabel1.configure(text=message)
        else:
            self.promptLabel2.configure(text=message)

    def loadImage(self, gestureName):
        return PhotoImage(file = "{}\gestures\{}.gif".format(self.currentWorkingDirectory,gestureName))

    def setMouseBindings(self):
        # Creating bindings for board (draw handles mouse down and drag events)
        self.board.bind(MOUSE_CLICK,self.getLastCoordinates)
        self.board.bind(MOUSE_DRAG_MODE, self.draw)
        if self.mode == 'recognition':
            self.board.bind(MOUSE_UP_MODE, self.mouseUp)
        
    # Handler for clear button click
    def onClearButtonClick(self):
        self.points.clear() 
        # Clears everything on the canvas
        self.board.delete(BOARD_DELETE_MODE)
        print(LOG_BOARD_CLEARED)
    
    def onSubmitButtonClick(self):
        if not self.userAdded:
            userId = self.userIdTextBox.get(1.0, "end-1c")
            self.currentUser = userId
            self.db.addUser(userId)
            self.setPromptLabel('Welcome {}!'.format(userId), 1)
            self.userAdded = True
        if self.readyToStore:
            gestureIndex = (self.gestureIndex - 1)%len(self.gestureList)
            self.db.addGesture(self.currentUser, self.gestureList[gestureIndex], deepcopy(self.points))
            self.points.clear()
            self.board.delete(BOARD_DELETE_MODE)
        if self.userDrawCount < 5:
            gestureName = self.gestureList[self.gestureIndex]
            self.setPromptLabel('Please draw a {}'.format(gestureName), 2)
            self.setGestureImageLabel(self.loadImage(gestureName))
            self.userDrawCount += 1
            self.gestureIndex = (self.gestureIndex + 1)%len(self.gestureList)
            self.readyToStore = True
        else:
            self.setPromptLabel('Saving your contribution!', 1)
            self.setPromptLabel('Thank you for participating, {}!'.format(self.currentUser), 2)
            self.clearGestureImageLabel()
            self.root.update()
            sleep(2)
            self.setPromptLabel('', 2)
            self.createXMLUserLogs()
            self.userDrawCount = 0
            self.gestureIndex = 0
            self.setPromptLabel('Please enter user ID and click Submit to Start!', 1)
            self.userAdded = False
            self.readyToStore = False

    def getLastCoordinates(self,event):
        self.startPointX,self.startPointY=event.x,event.y

    # Draws when mouse drag or screen touch event occurs
    def draw(self, event):
        self.board.create_line((self.startPointX, self.startPointY, event.x, event.y),fill=BLUE,width=5)
        self.points.append([event.x,event.y])
        self.startPointX, self.startPointY = event.x,event.y

    # Draws different states of user input (resampled,rotated,scaled)
    def reDraw(self, points, color,fxn):
        if fxn == "resample":
            for i in range(len(points)):
                x1, y1, x2, y2 = points[i][0]-2, points[i][1]-2, points[i][0]+2, points[i][1]+2
                self.board.create_oval(x1+200, y1, x2+200, y2, fill=color, outline=color)

        if fxn == "rotated":
            for i in range(len(points)):
                x1, y1, x2, y2 = points[i][0]-2, points[i][1]-2, points[i][0]+2, points[i][1]+2
                self.board.create_oval(x1+400, y1+100, x2+400, y2+100, fill=color, outline=color)
        
        if fxn == "scaled":
             for i in range(len(points)):
                x1, y1, x2, y2 = points[i][0]-2, points[i][1]-2, points[i][0]+2, points[i][1]+2
                self.board.create_oval(x1+400, y1, x2+400, y2, fill=color, outline=color)

    # Mouse up event handler
    def mouseUp(self, event):
        resampledPoints = self.recognizer.resample(deepcopy(self.points), SAMPLING_POINTS)
        # self.reDraw(resampledPoints, RED,"resample")
        rotatedPoints = self.recognizer.rotate(resampledPoints)
        # self.reDraw(rotatedPoints, ORANGE,"rotated")
        scaledPoints = self.recognizer.scale(rotatedPoints, SCALE_FACTOR)
        translatedPoints = self.recognizer.translate(scaledPoints, ORIGIN)
        # self.reDraw(translatedPoints, GREEN,"scaled")
        recognizedGesture, score, time , _= self.recognizer.recognizeGesture(translatedPoints)
        self.setPredictionLabels(recognizedGesture, score, time)
        print(LOG_DRAWING_FINISHED)
    
    def createXMLUserLogs(self):
        file = open('database.json')
        user_data = json.load(file)
        file.close()
        
        root = os.getcwd()
        log_directory_name = 'xml_collected_logs'
        log_directory_path = os.path.join(root, log_directory_name)
        if os.path.isdir(log_directory_path):
            rmtree(log_directory_path)
        os.makedirs(log_directory_path)

        for user in user_data:
            # print(user)
            user_path = os.path.join(log_directory_path, user)
            os.makedirs(user_path)
            for gesture in user_data[user]:
                # print(gesture)
                # print(len(user_data[user][gesture]))
                for i in range(0,len(user_data[user][gesture])):
                    pointList = user_data[user][gesture][i]
                    # print(user, gesture, len(pointList))
                    root = minidom.Document()
                    gestureChild = root.createElement('Gesture')
                    gestureChild.setAttribute('User', str(user))
                    gestureChild.setAttribute('Gesture', '{}{}'.format(gesture,i+1))
                    gestureChild.setAttribute('Number', str(i+1))
                    gestureChild.setAttribute('NumPts', str(len(pointList)))
                    gestureChild.setAttribute('Date', strftime("%d-%m-%Y"))
                    gestureChild.setAttribute('Time', strftime("%H:%M:%S"))
                    root.appendChild(gestureChild)
                    for point in pointList:
                        pointChild = root.createElement('Point')
                        pointChild.setAttribute('X', str(point[0]))
                        pointChild.setAttribute('Y', str(point[1]))
                        gestureChild.appendChild(pointChild)
                        gestureRootString = root.toprettyxml(indent= "\t")
                        file_name = '{}{}.xml'.format(gesture,i+1)
                        file_path = os.path.join(user_path, file_name)
                        with open(file_path, "w") as file:
                            file.write(gestureRootString) 
