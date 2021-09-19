import cv2
import time
from datetime import datetime

Stop_recording = False
cap= cv2.VideoCapture(0)
now = datetime.now()
dt_string = now.strftime("%d_%m_%Y %H¦%¦%S")
recording_title = dt_string + '.mp4'
width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
writer= cv2.VideoWriter(recording_title, cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))
while True:
    ret,frame= cap.read()
    writer.write(frame)
    cv2.imshow('frame', frame)
    if Stop_recording == True:
        time.sleep(10)
        break
cap.release()
writer.release()
cv2.destroyAllWindows()