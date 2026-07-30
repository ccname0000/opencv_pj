import cv2
import numpy as np
import mediapipe as mp
from utils import get_eye_center, smooth

def run_tracker(cap, landmarker, mapping_matrix, overlay, w_screen, h_screen):
    prev_x, prev_y = None, None

    def update():
        nonlocal prev_x, prev_y
        ret, frame = cap.read()
        if not ret:
            return
        h, w, _ = frame.shape
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        result = landmarker.detect_for_video(mp_image, int(cap.get(cv2.CAP_PROP_POS_MSEC)))
        if result.face_landmarks:
            cx, cy = get_eye_center(result.face_landmarks[0], w, h)
            pt = np.array([[[cx, cy]]], dtype=np.float32)
            mapped = cv2.perspectiveTransform(pt, mapping_matrix)
            gaze_x, gaze_y = int(mapped[0][0][0]), int(mapped[0][0][1])
            smooth_x, smooth_y = smooth(prev_x, prev_y, gaze_x, gaze_y)
            prev_x, prev_y = smooth_x, smooth_y
            overlay.update_gaze(smooth_x, smooth_y)

    return update
