from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QColorDialog
from PyQt5.QtGui import QColor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Color Picker Example")
        self.setGeometry(100, 100, 300, 200)

        self.color_button = QPushButton("Color Picker", self)
        self.color_button.setGeometry(50, 50, 200, 50)
        self.color_button.clicked.connect(self.show_color_picker)

        self.Color = None

    def show_color_picker(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.Color = color.name() # Или можно сохранить объект QColor целиком, если нужно хранить больше информации о цвете
            print("Выбранный цвет:", self.Color)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()