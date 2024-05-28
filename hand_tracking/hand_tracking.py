import mediapipe as mp
import cv2


img = cv2.imread('/home/ckg/Documents/python_projects/python_projects/hand_tracking/image.jpeg')

rgb_img =cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

mp_hands =mp.solutions.hands
mp_drawing =mp.solutions.drawing_utils

hands = mp_hands.Hands(static_image_mode =True,max_num_hands = 2)

result = hands.process(rgb_img)
print(result.multi_handedness)

print(result.multi_hand_landmarks)


if result.multi_hand_landmarks:
    for hand_no, hand_land_marks in enumerate(result.multi_hand_landmarks):

        mp_drawing.draw_landmarks(
                                    image=img,
                                    landmark_list=hand_land_marks,
                                    connections=mp_hands.HAND_CONNECTIONS
                                )


cv2.imshow('hand_tracking',img)
cv2.waitKey()
cv2.destroyAllWindows()