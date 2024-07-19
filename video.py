import cv2

cap = cv2.VideoCapture("../src/video_sample/전.mp4")

while(cap.isOpened()):
   ret, frame = cap.read()
   if ret == True:
        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,
               cv2.WINDOW_FULLSCREEN)
        cv2.imshow('window',frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
