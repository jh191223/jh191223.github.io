import os
import sys
import time
import cv2
import winsound
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QAction, QImage, QKeySequence, QPixmap
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox,
                               QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget, QSpinBox)

class Thread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.trained_file = None
        self.status = True
        self.cap = None
        self.alarm_time = 5  # 기본 알람 시간 (초)
        self.elapsed_time = 0  # 경과 시간
        self.alarm_triggered = False  # 알람이 울렸는지 여부를 추적
        self.person_detected = False  # 사람이 감지되었는지 여부를 추적

    def set_file(self, fname):
        self.trained_file = os.path.join(cv2.data.haarcascades, fname)

    def start_recording(self, filename):
        """녹화 시작"""
        self.is_recording = True
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 'XVID' 코덱 사용
        self.video_writer = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    def stop_recording(self):
        """녹화 중지"""
        self.is_recording = False
        if self.video_writer:
            self.video_writer.release()

    def set_alarm_time(self, time_seconds):
        """알람 시간을 설정하는 메서드"""
        self.alarm_time = time_seconds
        self.alarm_triggered = False  # 알람 시간 변경 시 알람 상태 초기화

    def run(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while self.status:
            cascade = cv2.CascadeClassifier(self.trained_file)
            ret, frame = self.cap.read()
            if not ret:
                continue

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detections = cascade.detectMultiScale(gray_frame, scaleFactor=1.1,
                                                  minNeighbors=5, minSize=(30, 30))

            if len(detections) > 0:
                self.person_detected = True  # 사람이 감지됨
            else:
                self.person_detected = False  # 사람이 감지되지 않음

            # 사람이 감지되었을 때만 경과 시간 증가
            if self.person_detected:
                self.elapsed_time += 1  # 1초씩 증가한다고 가정

                # 알람 시간에 도달하면 알람 울리기
                if self.elapsed_time >= self.alarm_time and not self.alarm_triggered:
                    self.trigger_alarm()
                    self.alarm_triggered = True  # 알람이 울렸으므로 알람 상태 변경
                    self.elapsed_time = 0  # 알람 후 시간 초기화
            else:
                # 사람이 감지되지 않으면 경과 시간 초기화
                self.elapsed_time = 0
                self.alarm_triggered = False  # 알람 초기화

            # 영상 처리
            for (x, y, w, h) in detections:
                pos_ori = (x, y)
                pos_end = (x + w, y + h)
                color = (0, 255, 0)
                cv2.rectangle(frame, pos_ori, pos_end, color, 2)

            color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = color_frame.shape
            img = QImage(color_frame.data, w, h, ch * w, QImage.Format.Format_RGB888)
            scaled_img = img.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)

            self.updateFrame.emit(scaled_img)
        sys.exit(-1)

    def trigger_alarm(self):
        """알람을 울리는 메서드"""
        print("알람!! 사람이 감지되었습니다.")
        winsound.Beep(1000, 1000)  # 1000Hz 주파수, 1초 동안 울리기


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Patterns detection with Video Recording")
        self.setGeometry(0, 0, 800, 500)

        # 알람 시간 설정 UI 추가
        self.alarm_time_label = QLabel("알람 시간 (초):", self)
        self.alarm_time_label.setFixedSize(100, 30)
        self.alarm_time_spinbox = QSpinBox(self)
        self.alarm_time_spinbox.setRange(1, 60)  # 1초에서 60초까지 설정
        self.alarm_time_spinbox.setValue(5)  # 기본값 5초
        self.alarm_time_spinbox.setFixedSize(80, 30)

        # 알람 시간 UI 배치
        alarm_layout = QHBoxLayout()
        alarm_layout.addWidget(self.alarm_time_label)
        alarm_layout.addWidget(self.alarm_time_spinbox)

        # Create a label for the display camera
        self.label = QLabel(self)
        self.label.setFixedSize(640, 480)

        # Thread in charge of updating the image
        self.th = Thread(self)
        self.th.finished.connect(self.close)
        self.th.updateFrame.connect(self.setImage)

        # Model group
        self.group_model = QGroupBox("Trained model")
        self.group_model.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        model_layout = QHBoxLayout()

        self.combobox = QComboBox()
        for xml_file in os.listdir(cv2.data.haarcascades):
            if xml_file.endswith(".xml"):
                self.combobox.addItem(xml_file)

        model_layout.addWidget(QLabel("File:"), 10)
        model_layout.addWidget(self.combobox, 90)
        self.group_model.setLayout(model_layout)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        self.button1 = QPushButton("Start")
        self.button2 = QPushButton("Stop/Close")
        self.button3 = QPushButton("Start Recording")
        self.button4 = QPushButton("Stop Recording")
        self.button1.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.button2.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.button3.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.button4.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        buttons_layout.addWidget(self.button2)
        buttons_layout.addWidget(self.button1)
        buttons_layout.addWidget(self.button3)
        buttons_layout.addWidget(self.button4)

        right_layout = QHBoxLayout()
        right_layout.addWidget(self.group_model, 1)
        right_layout.addLayout(buttons_layout, 1)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(alarm_layout)
        layout.addLayout(right_layout)

        # Central widget
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connections
        self.button1.clicked.connect(self.start)
        self.button2.clicked.connect(self.kill_thread)
        self.button3.clicked.connect(self.start_recording)
        self.button4.clicked.connect(self.stop_recording)
        self.button2.setEnabled(False)
        self.button3.setEnabled(True)
        self.button4.setEnabled(False)
        self.combobox.currentTextChanged.connect(self.set_model)
        self.alarm_time_spinbox.valueChanged.connect(self.update_alarm_time)

    def update_alarm_time(self):
        """알람 시간 변경 시 호출되는 슬롯"""
        self.th.set_alarm_time(self.alarm_time_spinbox.value())

    def set_model(self, text):
        self.th.set_file(text)

    def kill_thread(self):
        print("Finishing...")
        self.button2.setEnabled(False)
        self.button1.setEnabled(True)
        self.th.cap.release()
        cv2.destroyAllWindows()
        self.status = False
        self.th.terminate()
        time.sleep(1)

    def start(self):
        print("Starting...")
        self.button2.setEnabled(True)
        self.button1.setEnabled(False)
        self.th.set_file(self.combobox.currentText())
        self.th.start()

    def start_recording(self):
        print(f"알람 시간: {self.th.alarm_time}초")
        self.button3.setEnabled(False)
        self.button4.setEnabled(True)
        self.th.start_recording(r'C:\Users\dolch\Desktop\네클캠\mini_project\OpenCV_Face_Detection\녹화\output.avi')

    def stop_recording(self):
        print("Recording stopped...")
        self.button3.setEnabled(True)
        self.button4.setEnabled(False)
        self.th.stop_recording()

    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))


if __name__ == "__main__":
    app = QApplication()
    w = Window()
    w.show()
    sys.exit(app.exec())
