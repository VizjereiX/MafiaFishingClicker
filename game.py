import win32api as wapi
import pyautogui
from PIL import ImageGrab, ImageOps

import time
import os
from datetime import datetime

# settings
pyautogui.PAUSE = 0.01
MARGIN = 10
LEVEL = 15


def determineGaugeMargins(img):
    rightMargin = -1
    leftMargin  = 100
    for i in range(420, 200, -1):
        if img.getpixel((i, 28)) > 50:
            rightMargin = i
            break

    for i in range(rightMargin, 100, -1):
        if img.getpixel((i, 28)) < 50:
            leftMargin = i
            break
    return (leftMargin, rightMargin)

def singleGame():
    #do first click
    time.sleep(0.5)
    pyautogui.click(1000, 900)

    #wait until gauge is shown
    waitForGauge()

    #start pulling
    pyautogui.moveTo(1000, 900)
    pyautogui.mouseDown()
    time.sleep(0.3)

    leftMargin, rightMargin = determineGaugeMargins(getGaugeImg())
    
    #play
    pulling = True

    while True:
        # check if it is end of the round or we are forcing quit
        if getBtnImg().getpixel((25,160)) < 100 or wapi.GetAsyncKeyState(ord("Q")):
            return

        # get gauge image
        img  = getGaugeImg()

        # pulling phase
        if (pulling):
            # gauge is full - we need to stop pulling
            if img.getpixel((rightMargin + MARGIN, LEVEL)) > 50:
                pulling = False
                pyautogui.mouseUp()
        else:
            #gauge is empty - start pulling
            if img.getpixel((leftMargin - MARGIN, LEVEL)) < 50:
                pulling = True 
                pyautogui.moveTo(1000, 900)
                pyautogui.mouseDown()
        
        # sleep to prevent too fast clicks
        time.sleep(0.01) 

def waitForGauge():
    while True:
        btnImg = getBtnImg()
        if btnImg.getpixel((25,160)) > 100:
            return
        time.sleep(0.01)       

def getBtnImg():
    return ImageOps.grayscale(ImageGrab.grab((900, 850, 1090, 1030)))
        
def getGaugeImg():
    return ImageOps.grayscale(ImageGrab.grab((800, 780, 1240, 820)))

def mainLoop():
    print("Usage: ")
    print("\tF: set numer of retries [default: 1]")
    print("\tA: start a game F-times")
    print("\tX: quit")
    print("\nDuring game: Q to abort")
    retries = 1
    wd = os.getcwd()
    while True:
        if wapi.GetAsyncKeyState(ord("A")):

            # prepare screenshots directory
            dir = os.path.join(wd, "ss", datetime.now().strftime("%Y%m%d%H%M%S"))
            os.makedirs(dir)
            os.chdir(dir)
            
            
            for i in range(0, retries):
                print("Playing single stage")
                singleGame()
                time.sleep(5)
                path = str(i) + ".jpg"
                print("Saving screenshot: " + path)
                ImageGrab.grab().save(path)
                print("Clicking outside a board")
                pyautogui.moveTo(1000, 900)
                pyautogui.click()
                time.sleep(5)
                pyautogui.moveTo(1000, 400)
                print("End of loop")
        if wapi.GetAsyncKeyState(ord("F")):
                while True:
                    try:
                        inp = int(input("Define numer of games [1-100]: "))
                        if inp >=1 and inp <=100:
                            retries = inp
                            break
                    except:
                        print("That's not a valid option!")

        if wapi.GetAsyncKeyState(ord("X")):
            break


mainLoop()