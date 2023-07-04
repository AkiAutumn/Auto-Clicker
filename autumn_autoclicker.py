import time
import os
import json
import pyautogui
import threading
import random
from pynput.mouse import Controller, Button, Listener as mouseListener
from pynput.keyboard import Listener as keyListener, Key, KeyCode
from datetime import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

os.system('color')

clickingLeft = False
clickingRight = False
optionsKeyHeld = False
pressLeftTime = None
pressRightTime = None
optionsScreen = False
MinecraftOnly = False
selected = 0
options = ["MC Only", "Half CPS", "Double CPS (unsafe)", "Quit"]
enabled = [False, False, False, False]
delayRange = [0.01, 0.16]

def clickerLeft():
    while True:
        if clickingLeft and statusLeftclick:
            if MinecraftOnly:
                window_title = pyautogui.getActiveWindowTitle()
                if window_title != None and "Minecraft" in window_title:
                    mouse.click(buttonLeftclick)
            else: mouse.click(buttonLeftclick)
        time.sleep(random.uniform(delayRange[0], delayRange[1]))

def clickerRight():
    while True:
        if clickingRight and statusRightclick:
            if MinecraftOnly:
                window_title = pyautogui.getActiveWindowTitle()
                if window_title != None and "Minecraft" in window_title:
                    mouse.click(buttonRightclick)
            else: mouse.click(buttonRightclick)
        time.sleep(random.uniform(delayRange[0], delayRange[1]))

def on_press(key): 
    global optionsScreen

    key = str(KeyCode.from_char(key).char)[4:].upper()

    if key == toggleKeyLeft:
        global statusLeftclick, clickingLeft
        if mouse_listener.running:
            if statusLeftclick:
                statusLeftclick = False
                clickingLeft = False
            else:
                statusLeftclick = True
        else:
            mouse_listener.start()
            statusLeftclick = True

    if key == toggleKeyRight:
        global statusRightclick, clickingRight
        if mouse_listener.running:
            if statusRightclick:
                statusRightclick = False
                clickingRight = False
            else:
                statusRightclick = True
        else:
            mouse_listener.start()
            statusRightclick = True
    
    if key == optionsKey:
        if optionsScreen:    
                os.system('cls')
                showMainScreen()
                optionsScreen = False
        else:
            optionsScreen = True
            showOptions()

    if optionsScreen:  
        if key == "UP": up()
        elif key == "DOWN": down()
        elif key == "ENTER": enter()

def showOptions():
    global optionsScreen, options, MinecraftOnly, selected, enabled
    os.system('cls')
    print(bcolors.HEADER + "                                   " + "\n" +
                                "  ,    _  -/--/- .  ,__,   __   ,  " + "\n" +
                                "_/_)__(/__/__/__/__/ / (__(_/__/_)_" + "\n" +
                                "                          _/_      " + "\n" +
                                "                         (/        " + "\n" + bcolors.ENDC +
                                "(Press " + bcolors.BOLD + optionsKey + bcolors.ENDC + " to return)\n")

    for i in range(0, len(options)):
        print("{0} {1}{2}".format("> " if selected == i else " ", bcolors.OKGREEN if enabled[i] else bcolors.FAIL, (options[i] + bcolors.ENDC)))

def enter():
    global selected, enabled, delayRange

    if enabled[selected]:
        enabled[selected] = False
    else:  
        enabled[selected] = True

    if selected == 0: #MC Only
        toggleMinecraftOnly()

    if selected == 1: #Half CPS
        if enabled[selected]:
            delayRange[0] = delayRange[0] * 2
            delayRange[1] = delayRange[1] * 2
        else:
            delayRange[0] = delayRange[0] * 0.5
            delayRange[1] = delayRange[1] * 0.5

    if selected == 2: #Double CPS
        if enabled[selected]:
            delayRange[0] = delayRange[0] * 0.5
            delayRange[1] = delayRange[1] * 0.5
        else:
            delayRange[0] = delayRange[0] * 2
            delayRange[1] = delayRange[1] * 2
    if selected == 3: #Terminate
        os.kill(os.getpid(), 9)
    
    showOptions()

def up():
    global selected
    if selected == 0:
        return
    selected -= 1
    showOptions()

def down():
    global selected, options
    if selected == (len(options) - 1):
        return
    selected += 1
    showOptions()

def toggleMinecraftOnly():
    global MinecraftOnly
    if MinecraftOnly: MinecraftOnly = False
    else: MinecraftOnly = True

def on_click(x,y,button,pressed):
    global pressLeft, pressRight, releaseLeft, releaseRight, statusLeftclick, statusRightclick, clickingLeft, clickingRight, pressLeftTime, pressRightTime

    if button == buttonLeftclick:
        if pressed and statusLeftclick:
            if clickingLeft:
                pressLeft += 1
            else:
                clickingLeft = True
                pressLeftTime = datetime.now().timestamp()
        else:
            if clickingLeft:
                releaseLeft += 1
                if releaseLeft > pressLeft:
                    pressLeft,releaseLeft = 0,0
                    clickingLeft = False
                    pressLeftTime = None

    elif button == buttonRightclick:
        if pressed and statusRightclick:
            if clickingRight:
                pressRight += 1
            else:
                clickingRight = True
                pressRightTime = datetime.now().timestamp()
        else:
            if clickingRight:
                releaseRight += 1
                if releaseRight > pressRight:
                    pressRight,releaseRight = 0,0
                    clickingRight = False
                    pressRightTime = None

def updateStats():
    while True:
        time.sleep(0.25)
        if not optionsScreen:
            global statusLeftclick, statusRightclick, pressLeft, pressRight, pressLeftTime
            cpsLeft = "---"

            cpsRight = "---"
            now = datetime.now().timestamp()
            if not pressLeftTime == None:
                duration = now - pressLeftTime
                cpsLeft = round((pressLeft / duration), 2)
                if cpsLeft > 20:
                    cpsLeft = bcolors.WARNING + str(cpsLeft) + bcolors.ENDC
            if not pressRightTime == None:
                duration = now - pressRightTime
                cpsRight = round((pressRight / duration), 2)
                if cpsRight > 20:
                    cpsRight = bcolors.WARNING + str(cpsRight) + bcolors.ENDC
            
            if statusLeftclick: statusLeft = bcolors.OKGREEN + "LMB" + bcolors.ENDC
            else: statusLeft = bcolors.FAIL + "LMB" + bcolors.ENDC
            if statusRightclick: statusRight = bcolors.OKGREEN + "RMB" + bcolors.ENDC
            else: statusRight = bcolors.FAIL + "RMB" + bcolors.ENDC

            print(f"Status [{statusLeft} | {statusRight}]    CPS [{cpsLeft} | {cpsRight}]             ", end="\r")

def showMainScreen():
    os.system('cls')
    print(bcolors.HEADER +  "                                                              _                     " + "\n"
                         +  " __,       -/-      ,____,   ,__,     __,       -/- _,_ __   //  .  __   /,  _   ,_ " + "\n"
                         +  "(_/(__(_/__/__(_/__/ / / (__/ / (_   (_/(__(_/__/__(_/_(_,__(/__/__(_,__/(__(/__/ (_" + "\n"
                         +  "                                                                                    " + bcolors.ENDC)
    print(f"Toggle Leftclick: {bcolors.BOLD}{toggleKeyLeft}{bcolors.ENDC}")
    print(f"Toggle Rightclick: {bcolors.BOLD}{toggleKeyRight}{bcolors.ENDC}")
    print(f"Show Settings: {bcolors.BOLD}{optionsKey}{bcolors.ENDC}\n")

import sys


def query_yes_no(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

if __name__ == '__main__':
    try:
        with open('autumn_autoclicker.json') as config_file:
            data = json.load(config_file)
    except IOError:
        createConfig = query_yes_no("No config file found, do you wish to create one?", default=None)
        if createConfig:
            configData = {'toggleLeftclick':'F6', 'toggleRightclick':'F7', 'toggleOptions':'F8'}
            jsonData = json.dumps(configData, indent=4)
            with open("autumn_autoclicker.json", "w") as outfile:
                outfile.write(jsonData)
    
    try:
        toggleKeyLeft = str(data["toggleLeftclick"]).upper()
    except NameError:
        toggleKeyLeft = "F6"

    try:
        toggleKeyRight = str(data["toggleRightclick"]).upper()
    except NameError:
        toggleKeyRight = "F7"

    try:
        optionsKey = str(data["toggleOptions"]).upper()
    except NameError:
        optionsKey = "F8"

    buttonLeftclick = Button.left
    buttonRightclick = Button.right
    delay = 0.001
    showMainScreen()
    statusLeftclick = False
    statusRightclick = False
    pressLeft,releaseLeft,pressRight,releaseRight = 0,0,0,0
    mouse_listener = mouseListener(on_click=on_click)
    mouse = Controller()
    stat_thread = threading.Thread(target=updateStats)
    stat_thread.start()
    clickLeft_thread = threading.Thread(target=clickerLeft)
    clickRight_thread = threading.Thread(target=clickerRight)
    clickLeft_thread.start()
    clickRight_thread.start()
    with keyListener(on_press=on_press) as key_listener:
        key_listener.join()