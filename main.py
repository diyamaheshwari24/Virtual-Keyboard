import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]
]
finalText = ""
keyboard = Controller()

class Button:
    def __init__(self, pos, text, size=[100, 100]):
        self.pos = pos
        self.size = size
        self.text = text

# def drawALL(img, buttonList):
#     for button in buttonList:
#         x, y = button.pos
#         w, h = button.size
#         cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 255), cv2.FILLED)
#         cv2.putText(img, button.text, (x + 30, y + 70),
#                     cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 5)
#     return img
def drawALL(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size

        # Create an overlay to blend transparent button background
        overlay = img.copy()
        cv2.rectangle(overlay, button.pos, (x + w, y + h), (0, 255, 255), cv2.FILLED)

        # Blend overlay with original image, alpha controls transparency
        alpha = 0.6  # 40% transparency
        img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

        # Draw the text fully opaque on top of the button
        cv2.putText(img, button.text, (x + 30, y + 70),
                    cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 5)
    return img



buttonList = []

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([110 * j + 50, i*(100+20)+50], key))



while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    lmList = []

    if hands:
        lmList = hands[0]['lmList']  # Correct way to get landmarks

    img = drawALL(img, buttonList)

    if lmList and len(lmList) > 8:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (255, 255, 255), cv2.FILLED)
                cv2.putText(img, button.text, (x + 30, y + 70),
                            cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 5)
                l, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2], img)

                print(l)
                if l < 30:
                    keyboard.press(button.text)
                    # On click, draw a more opaque (less transparent) rectangle on overlay
                    overlay = img.copy()
                    cv2.rectangle(overlay, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    img = cv2.addWeighted(overlay, 0.8, img, 0.2, 0)  # more opaque pop effect

                    cv2.putText(img, button.text, (x + 30, y + 70),
                                cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 5)
                    finalText += button.text
                    sleep(0.1)

                # if l < 30:
                #     cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                #     cv2.putText(img, button.text, (x + 30, y + 70),
                #                 cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 5)
                #     finalText += button.text
                #     sleep(0.1)

    # Draw text box and text ALWAYS, outside the hand detection block
    cv2.rectangle(img, (50, 400), (600, 500), (255, 255, 255), cv2.FILLED)
    cv2.putText(img, finalText, (60, 425),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
