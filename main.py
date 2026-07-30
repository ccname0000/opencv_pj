import sys
import cv2
import mediapipe as mp
from PyQt5 import QtWidgets, QtCore
from calibration import run_calibration
from overlay import Overlay
from tracker import run_tracker

# Mediapipe setup
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="face_landmarker.task"),
    running_mode=VisionRunningMode.VIDEO,
    num_faces=1
)
landmarker = FaceLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

# 建立 QApplication 並動態偵測螢幕解析度
app = QtWidgets.QApplication(sys.argv)
screen = app.primaryScreen()
size = screen.size()
w_screen, h_screen = size.width(), size.height()
print(f"Detected screen resolution: {w_screen}x{h_screen}")

# 校正
mapping_matrix = run_calibration(cap, landmarker, w_screen, h_screen)

# Overlay
overlay = Overlay(w_screen, h_screen)
overlay.showFullScreen()

# Tracker
update = run_tracker(cap, landmarker, mapping_matrix, overlay, w_screen, h_screen)
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(30)

sys.exit(app.exec_())
