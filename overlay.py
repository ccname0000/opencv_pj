from PyQt5 import QtWidgets, QtGui, QtCore
#QtWidgets: 提供了 GUI 元件 QtGui: 提供了繪圖功能 QtCore: 提供了核心功能
class Overlay(QtWidgets.QWidget):
    def __init__(self, w_screen, h_screen):# 初始化 Overlay 類別
        super().__init__() # 繼承父類別的初始化方法
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | # 1. 無邊框 2. 永遠在最上層 3. tool 視窗, 不會出現在任務欄上 
                            QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.Tool) # 沒加這個的話, 視窗會出現在任務欄上, 也會被 Alt+Tab 切換到
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 使視窗背景透明
        self.setGeometry(0, 0, w_screen, h_screen) # 設定視窗大小與位置 剛好等同於全螢幕 setGeometry(初始X座標, 初始Y座標, 寬度, 高度)
        self.gaze_x, self.gaze_y = None, None # 初始化凝視點座標

    def paintEvent(self, event):
        if self.gaze_x is not None:
            painter = QtGui.QPainter(self) # 創建一個 QPainter 對象, 用於在 Overlay 視窗上繪圖
            painter.setRenderHint(QtGui.QPainter.Antialiasing) # 啟用抗鋸齒, 使繪製的圖形邊緣更平滑
            painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0, 180))) # 設定畫刷顏色為半透明綠色 (R, G, B, A)
            painter.setPen(QtCore.Qt.NoPen) # 無邊框, 只繪製填充區域
            painter.drawEllipse(QtCore.QPoint(self.gaze_x, self.gaze_y), 15, 15) # 在凝視點位置繪製一個半徑為 15 的圓形

    def update_gaze(self, x, y): # 更新凝視點座標並觸發重繪
        self.gaze_x, self.gaze_y = x, y
        self.update()

    def keyPressEvent(self, event): 
        if event.key() == QtCore.Qt.Key_Escape or event.key() == QtCore.Qt.Key_Q: # Esc or Q 鍵退出程式
            QtWidgets.QApplication.quit()
