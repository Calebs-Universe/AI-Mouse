import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_img)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            lm = handLms.landmark
            index_tip = lm[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_pip = lm[mp_hands.HandLandmark.INDEX_FINGER_PIP]
            middle_tip = lm[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            middle_pip = lm[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]

            # Finger states
            index_up = index_tip.y < index_pip.y
            middle_up = middle_tip.y < middle_pip.y

            if index_up and not middle_up:
                x = int(index_tip.x * screen_width)
                y = int(index_tip.y * screen_height)
                pyautogui.moveTo(x, y)
            elif index_up and middle_up:
                pyautogui.click()

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Virtual Mouse", img)
    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
