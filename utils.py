def get_eye_center(landmarks, w, h):
    left_eye = landmarks[468]
    right_eye = landmarks[473]
    lx, ly = int(left_eye.x * w), int(left_eye.y * h)
    rx, ry = int(right_eye.x * w), int(right_eye.y * h)
    return (lx + rx) // 2, (ly + ry) // 2

def smooth(prev_x, prev_y, gaze_x, gaze_y, alpha=0.2):
    if prev_x is None:
        return gaze_x, gaze_y
    smooth_x = int(alpha * gaze_x + (1 - alpha) * prev_x)
    smooth_y = int(alpha * gaze_y + (1 - alpha) * prev_y)
    return smooth_x, smooth_y
