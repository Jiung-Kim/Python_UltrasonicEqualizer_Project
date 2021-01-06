## https://stackoverflow.com/questions/51488701/python-desktop-fps-displaying-in-label


## Python desktop FPS displaying in label 

import sys
import time
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QPushButton  
from PyQt5.QtCore import QTimer, pyqtSlot  # Import new bits needed
## from main_view import Ui_MainWindow


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        
        super(ApplicationWindow, self).__init__()  #상위 객체 생성 
        
        self.initUI()
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)
        
        # Add in creating and connecting the timer 
        self.timer = QTimer()
        self.timer.setInterval(100)  # 100 milliseconds = 0.1 seconds
        # self.timer.timeout.connect(self.fps_display)  # Connect timeout signal to function
        self.timer.timeout.connect(self.initUI)  # Connect timeout signal to function
        self.timer.start()  # Set the timer running
    
    @pyqtSlot()  # Decorator to tell PyQt this method is a slot that accepts no arguments
    def fps_display(self):
        start_time = time.time()
        counter = 1
        # All the logic()
        time.sleep(1)
        time_now = time.time()
        self.fps = str((counter / (time_now - start_time)))
        # self.initUI.label_fps.setText(fps)
        
        return self.fps
    
    def initUI(self):
        self.statusBar()  # 상태 표시줄 호출 
        self.statusBar().showMessage(self.fps_display())  # 상태표시줄 내용 입력 - 상태표시줄 호출을 먼저 해야한다. 

        ## 이제 만든다. 
        btn = QPushButton('첫 버튼1', self)
        btn.resize(btn.sizeHint())  
        btn.setToolTip('튤팁입니다.,<b>안녕하세요.<b>') # 버튼에 가져다 대면 팁이 조금하게 나온다.  <b>안녕하세요.<b>은 글짜가 강조된다. 
        btn.move(100, 100)  #버튼 위치 움직이기 
        
        # 창 크기 조절하는것 
        self.setGeometry(300, 300, 300, 300) # 창 크기 조절  (내용표시창의의 가로, 내용표시창의 세로, 전체윈도우의 가로, 전체윈도우의 세로 )

        # title 바꾸기 
        self.setWindowTitle('첫번째 학습시간')

        self.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()