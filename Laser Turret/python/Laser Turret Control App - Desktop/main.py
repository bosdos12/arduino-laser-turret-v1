# Importing modules;
import pygame;
import json
import cv2 as cv
import numpy as np
from PIL import Image as PIL_IMAGE
from tkinter import messagebox
import win32gui
import serial
import time



# App initialisations;
pygame.init()
pygame.font.init()

infoFont = pygame.font.SysFont("Arial", 30)

# Importing functions;
from drawBBoxF                             import drawBBoxF;
from TargetsDataRelated.saveNewTargetF     import saveNewTargetF
from TargetsDataRelated.clickTargetButtonF import clickTargetButtonF
from arduinoWriteF                         import arduinoWriteF


# CONSTANT APP DATA;

# Settings;
with open("appWorkingData.json", "r") as settingsUnReady:
    APPSETTINGS = json.load(settingsUnReady)

print(APPSETTINGS)

# Basic;
WIDTH, HEIGHT = 1280, 720


# Colors;
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)


# CONSTANT PLACE BUTTONS RECTS;
CREATENEWTARGETBUTTONRECT = pygame.Rect(700, 500, 220, 100)



class MainApp():
    def __init__(self):
        # THIS FUNCTION IS JUST FOR DATA/APP INITIALISATIONS;
        # THE MAIN LOOP IS IN mainAppLoopF AND WILL BE CALLED AFTER ALL SETUP BEING DONE IN __INIT__;


        # APP STATE HOLDERS;
        self.ALLTARGETBBOXDATAOBJECTSARRAY        = []
        self.ALLTARGETDATABUTTONSCOORDINATESARRAY = []
        self.currentLockedTarget                  = None
        self.leftButton                           = pygame.Rect(5, 500, 150, 150)
        self.rightButton                          = pygame.Rect(165, 500, 150, 150)
        self.topButton                            = pygame.Rect(325, 500, 150, 150)
        self.downtButton                          = pygame.Rect(485, 500, 150, 150)


        # Initialising the pygame window;
        pygame.display.set_caption("Adaks Laser Turret")
        self.WIN = pygame.display.set_mode((WIDTH,HEIGHT))
        

        # Starting the video camera capture from the desired camera port;
        self.CAMERACAPTURE = cv.VideoCapture(APPSETTINGS["cameraPort"])

        try:
            self.ARDUINOCONNECTION = serial.Serial(port=f'COM{APPSETTINGS["arduinoPort"]}', baudrate=APPSETTINGS['arduinoSerialCommunicationBaudrate'])
            time.sleep(2)
        except:
            messagebox.showerror("Error connecting to Arduino", f"Make sure you have an Arduino connected on PORT: {APPSETTINGS['arduinoPort']} and running on a BAUDRATE OF: {APPSETTINGS['arduinoSerialCommunicationBaudrate']}")





        # Calling the main app loop;
        self.mainAppLoopF()







    def mainAppLoopF(self):
        while True:
            # Event Handlers
            for event in pygame.event.get():
                # Quit event handler;
                if event.type == pygame.QUIT:
                    pygame.quit()

                    # Button event handler;
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePosition = pygame.mouse.get_pos()
                    FULLSCREENMOUSEPOSITION = win32gui.GetCursorInfo()[2]
                    # Checking if the user wants to add a new target;
                    if CREATENEWTARGETBUTTONRECT.collidepoint(mousePosition):
                        saveNewTargetF(self, APPSETTINGS["maxSelectedTargetsCount"])
                    # Checking if the user is clicking a target button;
                    for targetButtonIndex in range(len(self.ALLTARGETDATABUTTONSCOORDINATESARRAY)):
                        if self.ALLTARGETDATABUTTONSCOORDINATESARRAY[targetButtonIndex].collidepoint(mousePosition):
                            clickTargetButtonF(self, targetButtonIndex, FULLSCREENMOUSEPOSITION)

                    # Manual movement buttons;
                    if self.leftButton.collidepoint(mousePosition):
                        print("leftButton")
                        arduinoWriteF(1, self.ARDUINOCONNECTION)
                    if self.rightButton.collidepoint(mousePosition):
                        print("rightButton")
                        arduinoWriteF(2, self.ARDUINOCONNECTION)
                    if self.topButton.collidepoint(mousePosition):
                        print("topButton")
                        arduinoWriteF(3, self.ARDUINOCONNECTION)
                    if self.downtButton.collidepoint(mousePosition):
                        print("downtButton")
                        arduinoWriteF(4, self.ARDUINOCONNECTION)








            # Aiming at the locked target;
            if self.currentLockedTarget != None:
                if self.currentLockedTarget["visible"]:
                    self.trackTheLockedTargetF()
                else:
                    self.currentLockedTarget = None
                    for target in self.ALLTARGETBBOXDATAOBJECTSARRAY:
                        target["isCurrentLockedTarget"] = False
                    print("Locked target lost;")
                
            

            # Updating the video data;
            self.updateVideoOfScreenF()

            # ReRendering the screen;
            self.reRenderScreenF()





    # The function for saving all screen changes;
    def reRenderScreenF(self):
        # Clearing the screen;
        self.WIN.fill(BLACK)

        # Displaying the tracking video;
        pygame.draw.rect(self.WIN, WHITE, (4, 4, 642, 482), 1) # Border Frame;
        imageToDisplayPil = cv.cvtColor(self.CURRENTCAMERAFRAME, cv.COLOR_BGR2RGB)
        imageToDisplayPil = PIL_IMAGE.fromarray(imageToDisplayPil)
        imageToDisplayPil = imageToDisplayPil.tobytes("raw", 'RGB')
        imageToDisplayPil = pygame.image.fromstring(imageToDisplayPil, (640, 480), 'RGB')
        self.WIN.blit(imageToDisplayPil, (5, 5))

        # Displaying the "current targets list";
        pygame.draw.rect(self.WIN, WHITE, (660, 5, 300, 480), 1) # Border Frame;
        self.WIN.blit(infoFont.render(f"Targets: {str(len(self.ALLTARGETBBOXDATAOBJECTSARRAY))}", False, WHITE), (750, 10))

        # Clearing the ALLTARGETDATABUTTONSCOORDINATESARRAY;
        self.ALLTARGETDATABUTTONSCOORDINATESARRAY.clear()
        singleTargetButtonBaseStartPoint = 70
        for singleTargetData in self.ALLTARGETBBOXDATAOBJECTSARRAY:
            singleTargetButtonRect = pygame.Rect(680, singleTargetButtonBaseStartPoint, 260, 50)
            if (singleTargetData["visible"]):
                pygame.draw.rect(self.WIN, GREEN, singleTargetButtonRect, 2)
            else:
                pygame.draw.rect(self.WIN, RED, singleTargetButtonRect, 2)


            # Putting the name of the target in the selector button;
            if singleTargetData["isCurrentLockedTarget"]:
                self.WIN.blit(infoFont.render(singleTargetData["name"], False, WHITE), (685, singleTargetButtonBaseStartPoint+10))
                # Displaying if the target is locked on the selector button;
            else:
                self.WIN.blit(infoFont.render(singleTargetData["name"], False, WHITE), (685, singleTargetButtonBaseStartPoint+10))



            # Adding the current index positions to the self.ALLTARGETDATABUTTONSCOORDINATESARRAY;
            self.ALLTARGETDATABUTTONSCOORDINATESARRAY.append(singleTargetButtonRect)

            singleTargetButtonBaseStartPoint+=55
            





        # Create new target button;
        pygame.draw.rect(self.WIN, GREEN, CREATENEWTARGETBUTTONRECT, 1)
        self.WIN.blit(infoFont.render("New Target", False, WHITE), (CREATENEWTARGETBUTTONRECT[0]+45, int((CREATENEWTARGETBUTTONRECT[1]+(CREATENEWTARGETBUTTONRECT[3]/2))-20)))



        # Manual move target buttons;
        pygame.draw.rect(self.WIN, GREEN, self.leftButton, 1)
        pygame.draw.rect(self.WIN, GREEN, self.rightButton, 1)
        pygame.draw.rect(self.WIN, GREEN, self.topButton, 1)
        pygame.draw.rect(self.WIN, GREEN, self.downtButton, 1)



        # Logs;
        # Border Frame;
        pygame.draw.rect(self.WIN, WHITE, (970, 5, 300, 480), 1)





        # Updating the display;
        pygame.display.update()



    # The function for updating the video data from opencv;
    def updateVideoOfScreenF(self):
        # Getting the current camera frame;
        cameraFrameSuccessfull, self.CURRENTCAMERAFRAME = self.CAMERACAPTURE.read()

        # Checking if camera read successfull;
        if cameraFrameSuccessfull:
            # Camera read successfull;

            # Going through all saved targets, if they are successfully found displaying them on the screen;
            # If not, logging that the item is lost and displaying the item in red color on the "all items" scroller to make it easier to see;
            # Also playing an alarm tone;
            for bboxArrayElement in self.ALLTARGETBBOXDATAOBJECTSARRAY:

                success, bbox = bboxArrayElement["tracker"].update(self.CURRENTCAMERAFRAME)
                bboxArrayElement["bbox"] = bbox

                print(bboxArrayElement)
                print(bbox)


                if success:
                    bboxArrayElement["visible"] = True
                    cv.putText(self.CURRENTCAMERAFRAME, bboxArrayElement["name"], (int(bbox[0]), int(bbox[1]+(bbox[3]/2))), cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    drawBBoxF(self.CURRENTCAMERAFRAME, bbox, bboxArrayElement["visible"])
                    
                    # Checking if this bbox array element is the locked target, if it is, updating the self.currentLockedTarget;
                    if bboxArrayElement["isCurrentLockedTarget"]:
                        self.currentLockedTarget = bboxArrayElement
                else:
                    # Item not found on camera, loggin the event and displaying it in red, also playing an alarm sound;
                    bboxArrayElement["visible"] = False

            # Drawing the crosshair;
            capture_height, capture_width, capture_channels = self.CURRENTCAMERAFRAME.shape
            

            crosshairLength = 25
            # NOTE: THE CROSSHAIR HAS TO BE EXACTLY WHERE THE LASER IS, NOT THE CENTER;
            cv.rectangle(self.CURRENTCAMERAFRAME, (327, 219), (327, (219+crosshairLength)), WHITE, thickness=2)
            cv.rectangle(self.CURRENTCAMERAFRAME, (327, 219), (327, (219-crosshairLength)), WHITE, thickness=2)
            cv.rectangle(self.CURRENTCAMERAFRAME, (327, 219), ((327+crosshairLength), (219)), WHITE, thickness=2)
            cv.rectangle(self.CURRENTCAMERAFRAME, (327, 219), ((327-crosshairLength), (219)), WHITE, thickness=2)

        

            

        else:
            # Camerrra read NOT successfull;
            # Displaying an error message and asking for the user to make sure the camera on the desired port is connected successfully;
            messagebox.showwarning("Camera not found", f"Please make sure that there is a camera connected to PORT: {APPSETTINGS['cameraPort']}")

    # The function for tracking the locked target, only works if a locked target exists and the locked target is currently visible on the screen;
    def trackTheLockedTargetF(self):
        cameraLaserPosition = (327, 219) # This is a system, not an app; Always the same camera and data is used. Its safe to use constants;(EDIT: not. )

        # COMMANDS: | 0 - left | 1 - right | 2 - up | 3 - down |; 

        # X AXIS;
        if int(cameraLaserPosition[0]) < int(self.currentLockedTarget["bbox"][0]):
            print("right")
            arduinoWriteF(1, self.ARDUINOCONNECTION)
        elif int(cameraLaserPosition[0]) > int(self.currentLockedTarget["bbox"][0] + self.currentLockedTarget["bbox"][2]):
            print("left")
            arduinoWriteF(2, self.ARDUINOCONNECTION)

        # Y AXIS;
        if int(cameraLaserPosition[1]) < int(self.currentLockedTarget["bbox"][1]):
            print("down")
            arduinoWriteF(4, self.ARDUINOCONNECTION)
        elif int(cameraLaserPosition[1]) > int(self.currentLockedTarget["bbox"][1] + self.currentLockedTarget["bbox"][3]):
            print("up")
            arduinoWriteF(3, self.ARDUINOCONNECTION)


        # For stopping the camera if it is inside the 






    











if __name__ == "__main__":
    MainApp()
        

