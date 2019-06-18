import numpy as np
from PIL import ImageGrab
import cv2
import time
import pyautogui
from multiprocessing import Process

# Gives a few seconds to switch to the emulator
time.sleep(3)


# Moves past "wild ___ appeared!" screen
def encounter():
    time.sleep(1.5)
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')
    time.sleep(1)


# Move cursor to "run" and select it
def flee_battle():
    time.sleep(1)
    pyautogui.keyDown('k')
    pyautogui.keyUp('k')
    pyautogui.keyDown('l')
    pyautogui.keyUp('l')
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')
    time.sleep(1)
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')


# Change to a Pokemon that knows the move Thief, in the second slot
def changepkmn():
    pyautogui.keyDown('l')
    pyautogui.keyUp('l')
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')
    time.sleep(1)
    pyautogui.keyDown('k')
    pyautogui.keyUp('k')
    time.sleep(1)
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')
    check_battle_status()


# Use the move
def use_thief():
    time.sleep(2)
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')
    check_battle_status()
    time.sleep(3)


# This part was tricky because there's a chance the move could have failed.
# There are also certain statuses that require multiple button presses.
# Allows you to press A until you're ready for the next move, which bypasses the text
def check_battle_status():
    time.sleep(3)

    try:
        img = cv2.imread('screenshot.png')[250:275, 10:270]
        cv2.imwrite('status.png', img)
    except TypeError:
        try:
            img = cv2.imread('screenshot.png')[250:275, 10:270]
            cv2.imwrite('status.png', img)
        except TypeError:
            pass

    if open('status.png', 'rb').read() == open('status/success.png', 'rb').read():
        print('EGG STOLEN!!!!!')

    if open('status.png', 'rb').read() == open('status/ready.png', 'rb').read():
        pass
    elif open('status.png', 'rb').read() == open('status/miss.png', 'rb').read():
        check_battle_status()
        use_thief()
    else:
        pyautogui.keyDown('a')
        pyautogui.keyUp('a')
        check_battle_status()


# Grabs the screenshot. Note, if you want to use this code, you should be using the VisualBoyAdvance emulator, set
# video size to 2x, and make sure screenshot.png lines up correctly and you can't see any part of your desktop.
# Otherwise, it won't work.
def opencv():
    while True:
        screen = np.array(ImageGrab.grab(bbox=(8, 51, 328, 338)))
        cv2.imwrite('screenshot.png', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))


# Moves left and up against the wall, checks for pokemon, and calls necessary functions
def movement():
    c = 0
    n = 0
    while True:
        pyautogui.keyDown('i')
        pyautogui.keyUp('i')
        pyautogui.keyDown('j')
        pyautogui.keyUp('j')

        try:
            img = cv2.imread('screenshot.png')[0:112,195:313]
            cv2.imwrite('enemy.png', img)
        except TypeError:
            pass

        if open('pkmn/pidgeotto.png', 'rb').read() == open('enemy.png', 'rb').read():
            encounter()
            flee_battle()

        if open('pkmn/noctowl.png', 'rb').read() == open('enemy.png', 'rb').read():
            n = n + 1
            print('Noctowl Encounters - ' + str(n))
            encounter()
            flee_battle()

        if open('pkmn/skiploom.png', 'rb').read() == open('enemy.png', 'rb').read():
            encounter()
            flee_battle()

        if open('pkmn/chansey.png', 'rb').read() == open('enemy.png', 'rb').read():
            c = c + 1
            print('Chansey Encounters - ' + str(c))
            encounter()
            changepkmn()
            use_thief()
            flee_battle()

        # NPCs will call you and mess up the loop if you don't press A to skip
        if open('call_am.jpg', 'rb').read() == open('enemy.png', 'rb').read():
            pyautogui.keyDown('a')
            pyautogui.keyUp('a')

        if open('call_day.png', 'rb').read() == open('enemy.png', 'rb').read():
            pyautogui.keyDown('a')
            pyautogui.keyUp('a')

        if open('call_night.png', 'rb').read() == open('enemy.png', 'rb').read():
            pyautogui.keyDown('a')
            pyautogui.keyUp('a')


if __name__=='__main__':

    # If you just want to take a screenshot, uncomment this code
    # Helpful for adding new Pokemon or battle status

    '''
    screen = np.array(ImageGrab.grab(bbox=(8, 51, 328, 338)))
    cv2.imwrite('screenshot.png', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    # img = cv2.imread('screenshot.png')[250:275, 10:270] #battle status ONLY NEED ONE OF THESE
    # img = cv2.imread('screenshot.png')[0: 112, 195: 315] #enemy pkmn ONLY NEED ONE OF THESE
    cv2.imwrite('screen.png', img)
    '''

    # Run PyAutoGUI and OpenCV processes
    p1 = Process(target = opencv)
    p1.start()
    p2 = Process(target = movement)
    p2.start()