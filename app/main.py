
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QMessageBox
from PySide6.QtGui import QCursor, QPixmap, QPalette, QBrush, QShortcut, QKeySequence
from PySide6.QtCore import Qt
import sys

bg_image = r"C:\Users\gsnis\Projects-2025\My-Personal-Command-Center\assets\blackboard_bg.png"
window_coord = (800, 600)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('My Personal Command Center')
        self.setGeometry(100, 100, window_coord[0], window_coord[1]) # set position and size
        
        #self.setWindowFlags(Qt.FramelessWindowHint) # remove the title bar
       
        # Cursor customization
        pixmap_g_cursor = QPixmap("assets/cursor_g_white.png").scaled(40,40)
        cursor_1 = QCursor(pixmap_g_cursor, -1, -1)
        self.setCursor(cursor_1)
        
        # App key shortcuts
        shortcut_1 = QShortcut(QKeySequence("Ctrl+F"), self)
        shortcut_1.activated.connect(self.toggle_fullscreen)
        
        # Set the background image
        bg_image = QPixmap("assets/blackboard_bg.png").scaled(800,600)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(bg_image.scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )))
        self.setPalette(palette)
        
        
        container = QWidget()
        
        # testing label
        test_label = QLabel("My Personal Command Center")
        test_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(test_label)

    
    # function for app exit
    def keyPressEvent(self, event):
        
        if event.key() == Qt.Key_Escape:
            QApplication.quit()      
        else:
            super().keyPressEvent(event)
            
    # toggle between fullscreen and normal window
    def toggle_fullscreen(self):
        if self.isFullScreen:
            self.showNormal()
        else:
            self.showFullScreen()
        self.isFullScreen = not self.isFullScreen
        
    # Reset the window size
    def resizeEvent(self, event):
        pass

           
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())