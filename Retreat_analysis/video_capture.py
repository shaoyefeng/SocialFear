import numpy as np
import cv2

input_video = r"F:\fictrac-debug.avi"
output_video = r"F:\fictrac-debug-cap.avi"
#要截取的片段的起止时间，单位s
start_time, end_time = 50, 500
cap = cv2.VideoCapture(input_video)

# 定义编解码器，创建VideoWriter 对象
fourcc = cv2.VideoWriter_fourcc('I', '4', '2', '0')
#进行视频定位播放
fps = cap.get(5)
cap.set(cv2.CAP_PROP_POS_FRAMES, start_time)
out = cv2.VideoWriter(output_video, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) >= end_time:
            break
        out.write(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()


