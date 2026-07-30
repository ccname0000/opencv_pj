import cv2
import numpy as np
import mediapipe as mp
from utils import get_eye_center

def run_calibration(cap, landmarker, w_screen, h_screen):
    calibration_points = [
    (50, 50),                      # 左上
    (w_screen//2, 50),             # 上中
    (w_screen-50, 50),             # 右上
    (50, h_screen//2),             # 左中
    (w_screen//2, h_screen//2),    # 中心
    (w_screen-50, h_screen//2),    # 右中
    (50, h_screen-50),             # 左下
    (w_screen//2, h_screen-50),    # 下中
    (w_screen-50, h_screen-50)     # 右下
]


    eye_points = []
    current_calib = 0
    mapping_matrix = None

    cv2.namedWindow("Calibration", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Calibration", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while mapping_matrix is None:
        ret, frame = cap.read() # ret = True or False, frame = 影像
        if not ret:
            break
        h, w, _ = frame.shape # _ = 通道數量, h = 高度, w = 寬度
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame) #把frame從opencv轉成mediapipe的格式
        time_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC)) #毫秒時間戳
        result = landmarker.detect_for_video(mp_image, time_ms)

        screen = np.zeros((h_screen, w_screen, 3), dtype=np.uint8) # dtype = 是 8 位元整數 2^8 = 256 所以有0~255

        if result.face_landmarks:
            cx, cy = get_eye_center(result.face_landmarks[0], w, h) #result.face_landmarks[0] = mediapipe偵測到的第一張臉的landmark
            calib_x, calib_y = calibration_points[current_calib] #calibration_points 是校準點的座標, current_calib 是目前校準點的索引
            cv2.circle(screen, (calib_x, calib_y), 20, (0, 0, 255), -1) # 畫出校準點

            if cv2.waitKey(1) & 0xFF == ord(' '):
                eye_points.append([cx, cy]) #把眼睛座標存進 eye_points
                current_calib += 1 # 增加校準點索引
                if current_calib >= len(calibration_points): # 如果校準點索引大於等於校準點數量, 就計算映射矩陣
                    eye_points_np = np.array(eye_points, dtype=np.float32) # 把eye_points轉成numpy array
                    calib_points_np = np.array(calibration_points, dtype=np.float32) 
                    mapping_matrix, _ = cv2.findHomography(eye_points_np, calib_points_np) # 計算映射矩陣 eye是來源, calib是目標 

        cv2.imshow("Calibration", screen) 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    return mapping_matrix
