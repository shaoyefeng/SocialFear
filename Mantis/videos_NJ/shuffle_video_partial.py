import random
import cv2
import sys
import json
import numpy as np

ann = json.load(open(r"D:\exp\SoAL_git\dataset\annotations\person_keypoints_mantis-180.json"))["annotations"]
fr_kpt_d = {}
for a in ann:
    kpt = np.reshape(a["keypoints"], (-1, 3))
    fr_kpt_d[a["id"]] = kpt[6:12, :2]

input_name = r"mantis\c.avi"
cap = cv2.VideoCapture(input_name)
total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
video_w, video_h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
ret, img = cap.read()
output_video = cv2.VideoWriter(input_name.replace(".avi", "_rand_leg.avi"), cv2.VideoWriter_fourcc(*"MJPG"), fps, (video_w, video_h))

for seq in range(0, total_frame):
    ret, img = cap.read()
    if not ret:
        break
    img = img[:, :, 0]

    frame1 = seq//10*10
    frame2 = frame1 + 10
    d1 = seq - frame1
    r = d1/10
    kpt_legs1 = fr_kpt_d[frame1]
    if fr_kpt_d.get(frame2) is None:
        kpts = kpt_legs1
    else:
        kpt_legs2 = fr_kpt_d[frame2]
        kpts = kpt_legs1*(1-r) + kpt_legs2*r

    mask = np.zeros((video_h, video_w), dtype=np.uint8)
    # ell1 = cv2.fitEllipse(np.array([kpt_leg1[0], kpt_leg1[0], kpt_leg1[1], kpt_leg1[1], kpt_leg1[2]]))
    # cv2.ellipse(mask, np.array(ell1[0], dtype=int), np.array(ell1[1], dtype=int), np.rad2deg(ell1[2]), 0, 360, 255, -1)
    # for k in kpt_leg2:
    #     cv2.circle(mask, np.array(k, dtype=int), 10, 128, -1)
    for seg in ([0, 1], [1, 2], [3, 4], [4, 5]):
        a = kpts[seg[0]]+kpts[seg[1]]
        b = kpts[seg[0]]-kpts[seg[1]]
        cv2.ellipse(mask, np.array(a/2, dtype=int),
                    (10, int(np.sqrt(sum(b**2))/2)),
                    -np.rad2deg(np.arctan2(*b)), 0, 360, 255, -1)
    # cv2.imshow("mask", mask)

    f = img.flatten()
    s = mask.flatten()
    idx = s > 0
    f_sub = f[idx]

    random.seed(8)
    random.shuffle(f_sub)
    f[idx] = f_sub
    img = np.reshape(f, (video_h, video_w))
    # cv2.imshow("img", img)
    # cv2.waitKey(200)
    output_video.write(cv2.cvtColor(img, cv2.COLOR_GRAY2BGR))

