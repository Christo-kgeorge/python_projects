import cv2
import mediapipe as mp


mp_hands =mp.solutions.hands
mp_drawing =mp.solutions.drawing_utils

hands = mp_hands.Hands()

video =cv2.VideoCapture('/home/ckg/Documents/python_projects/python_projects/hand_tracking/Magic hands 🪄.mp4')

while True:
    success, frame =video.read()
    frame=cv2.resize(frame,(500,700))
    # grey_img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results =hands.process(frame)

    print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for hand_no, hand_land_marks in enumerate(results.multi_hand_landmarks):

            mp_drawing.draw_landmarks(
                                    image=frame,
                                    landmark_list=hand_land_marks,
                                    connections=mp_hands.HAND_CONNECTIONS
                                )

    cv2.imshow('web cam hand tracking',frame)
    if cv2.waitKey(1)& 0xFF==27:
        break
video.release()
cv2.destroyAllWindows()