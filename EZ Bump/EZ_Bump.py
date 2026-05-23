import subprocess
import time
import random
import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

ADB_DEVICE = "127.0.0.1:5563"

def log(msg):
    print(f"[EZ Bump] {msg}")

def adb(cmd):
    subprocess.run(f"adb -s {ADB_DEVICE} {cmd}", shell=True)

def tap(x, y):
    adb(f"shell input tap {x} {y}")

def long_press(x, y, duration=1200):
    adb(f"shell input swipe {x} {y} {x} {y} {duration}")

def swipe(x1, y1, x2, y2, duration=300):
    adb(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")

def type_text(text):
    for char in text:
        if char == " ":
            adb("shell input keyevent 62")
        else:
            adb(f'shell input text "{char}"')

        time.sleep(random.uniform(0.05, 0.2))

def find_channel_by_text(channel_name):

    screenshot()

    img = cv2.imread("screen.png")

    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    for i, word in enumerate(data["text"]):

        if channel_name.lower() in word.lower():

            x = data["left"][i] + data["width"][i] // 2
            y = data["top"][i] + data["height"][i] // 2

            log(f"Channel '{channel_name}' found")

            tap(x, y)

            return True

    log("Channel not found")

    return False

def screenshot():
    adb("shell screencap -p /sdcard/screen.png")
    adb("pull /sdcard/screen.png screen.png")

def find_and_click(image_path, threshold=0.8):

    screenshot()

    screen = cv2.imread("screen.png")
    template = cv2.imread(image_path)

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)

    loc = np.where(result >= threshold)

    if len(loc[0]) > 0:
        y, x = loc[0][0], loc[1][0]

        h, w = template.shape[:2]

        center_x = x + w // 2
        center_y = y + h // 2

        tap(center_x, center_y)

        return True

    return False

def find_channel(channel_name):

    for i in range(10):

        if find_channel_by_text(channel_name):
            return True

        log("Scrolling channel list")

        swipe(500, 1600, 500, 300, 600)

        time.sleep(2)

    return False

# COORDINATES

DEFAULT_X, DEFAULT_Y = 75, 130
SERVER1_X, SERVER1_Y = 80, 350
SERVER2_X, SERVER2_Y = 80, 510
CHANNEL_X, CHANNEL_Y = 740, 1180
MSG_BOX_X, MSG_BOX_Y = 750, 1835
SEND_X, SEND_Y = 1000, 1850
BACK_X, BACK_Y = 60, 150

MESSAGE_X, MESSAGE_Y = 770, 1600
DELETE_X, DELETE_Y = 740, 1800
CONFIRM_X, CONFIRM_Y = 525, 1132


MESSAGES = [
    ":fire:",
    ":carrot:",
    "BUMP",
    "up",
    ".",
    ",",
    ":horse:"
]

log("Starting EZ Bump")
log("Make sure the emulator is running and connected to ADB")
time.sleep(5)
log("Starting main loop")

while True:

    # Reset state
    tap(DEFAULT_X, DEFAULT_Y)
    log("Resetting to default state")
    time.sleep(10)

    # -------------  First server! -------------

    # Select server
    tap(SERVER1_X, SERVER1_Y)
    log("Selecting firstserver")
    time.sleep(10)

    # Scroll channel list up
    swipe(500, 100, 500, 1700, 700)
    time.sleep(5)

    # Select channel
    find_channel("Eden")
    time.sleep(10)

    # Click message box
    tap(MSG_BOX_X, MSG_BOX_Y)
    log("Clicking message box")
    time.sleep(10)

    # Type message
    message = random.choice(MESSAGES)
    type_text(message)
    log(f"Typing message: {message}")
    log("Typing message")
    time.sleep(10)

    # Send message
    tap(SEND_X, SEND_Y)
    log("Sending message")
    time.sleep(10)

    # Hold message
    long_press(MESSAGE_X, MESSAGE_Y)
    log("Preparing to delete message")
    time.sleep(10)

    # Scroll menu
    swipe(500, 1700, 500, 100, 700)
    time.sleep(10)

    # Delete
    tap(DELETE_X, DELETE_Y)
    time.sleep(10)

    # Confirm
    tap(CONFIRM_X, CONFIRM_Y)
    time.sleep(10)

    # Back to server list
    tap(BACK_X, BACK_Y)

    # Reset state
    tap(DEFAULT_X, DEFAULT_Y)
    log("Resetting to default state")
    time.sleep(10)

    # ------------  Second server! -------------

    # Select server 2
    tap(SERVER2_X, SERVER2_Y)
    log("Selecting second server")
    time.sleep(10)

    # Scroll channel list up
    swipe(500, 100, 500, 1700, 700)
    time.sleep(5)

    # Select channel
    find_channel("Eden")
    time.sleep(10)

    # Click message box
    tap(MSG_BOX_X, MSG_BOX_Y)
    log("Clicking message box")
    time.sleep(10)

    # Type message
    message = random.choice(MESSAGES)
    type_text(message)
    log(f"Typing message: {message}")
    log("Typing message")
    time.sleep(10)

    # Send message
    tap(SEND_X, SEND_Y)
    log("Sending message")
    time.sleep(10)

    # Hold message
    long_press(MESSAGE_X, MESSAGE_Y)
    time.sleep(10)

    # Scroll menu
    swipe(500, 1500, 500, 100, 700)
    time.sleep(15)

    # Delete
    tap(DELETE_X, DELETE_Y)
    time.sleep(10)

    # Confirm
    tap(CONFIRM_X, CONFIRM_Y)
    time.sleep(10)

    # Back to server list
    tap(BACK_X, BACK_Y)

    # Reset state
    tap(DEFAULT_X, DEFAULT_Y)
    log("Resetting to default state")
    time.sleep(10)


    # -------------  Add more servers if needed! ------------

    # Wait 30 minutes ± random delay
    delay = 2500 + random.randint(-300, 300)
    log(f"Waiting {delay} seconds")

    time.sleep(delay) 