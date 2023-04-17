import cv2 as cv
import mediapipe as mp
import pyautogui
import simpleaudio as sa

class VolumeControl:

    def __init__(self):
        pass

    def adjust_volume(self,new_diff,prev_diff=100):
        diff = new_diff - prev_diff
        scaled_diff = diff/300
        if scaled_diff>=0:
            pyautogui.press("volumeup",int(scaled_diff * 60))
        else:
            pyautogui.press("volumedown", int(abs(scaled_diff) * 60))

    def play(self,sound_path):
        mpHands = mp.solutions.hands
        hands = mpHands.Hands(static_image_mode=False,
                              max_num_hands=2,
                              min_detection_confidence=0.5,
                              min_tracking_confidence=0.5)
        y_points = [0,0]
        start_diff = 100
        cap = cv.VideoCapture(0)

        wave_obj = sa.WaveObject.from_wave_file(sound_path)
        play_obj = wave_obj.play()
        while True:
            success, img = cap.read()
            img = cv.rotate(img, cv.ROTATE_180)
            imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    for id, lm in enumerate(handLms.landmark):
                        h, w, c = img.shape
                        if id ==8:
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            y_points[0]=cy
                        if id == 4:
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            y_points[1]=cy
            diff = abs(y_points[0]-y_points[1])

            cv.rectangle(img, (10, 10), (40,290), (0, 0, 255), 5)
            cv.rectangle(img, (13, 290-int(diff)), (37, 290), (0, 255, 255),cv.FILLED)
            cv.putText(img, f"{int((diff/300) * 100)} %", (10, 350), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv.imshow("image", img)
            self.adjust_volume(diff,start_diff)
            start_diff = diff

            if cv.waitKey(1) & 0xFF==ord("q"):
                break

start = VolumeControl()
path = r"path of the wav file."
start.play(path)




