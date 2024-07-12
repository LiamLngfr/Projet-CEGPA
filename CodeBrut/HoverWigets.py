import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QMainWindow
from PyQt5.QtGui import QPixmap, QCursor, QPainter, QTransform
from PyQt5.QtCore import Qt, QTimer, QPoint


class ImageWindow(QWidget):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)  # Centrer l'image
        self.loadAndResizeImage(image_path)
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)
        self.resize(self.image_label.sizeHint())

    def loadAndResizeImage(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
            self.image_label.setFixedSize(pixmap.size())
        else:
            pass

    def enterEvent(self, event):
        # Empêcher la fenêtre de disparaître si la souris est sur l'image
        event.accept()

    def leaveEvent(self, event):
        # Cacher la fenêtre si la souris quitte l'image
        self.hide()
        event.accept()


class HoverWidget(QLabel):
    def __init__(self, text, image_path, parent=None):
        super().__init__(text, parent)
        self.image_path = image_path
        self.image_window = ImageWindow(image_path)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.showImageWindow)

    def enterEvent(self, event):
        self.timer.start(1000)
        event.accept()

    def leaveEvent(self, event):
        self.timer.stop()
        self.checkMouseLeave()
        event.accept()

    def showImageWindow(self):
        # Calculer la position du label dans la fenêtre principale
        label_pos = self.mapToGlobal(self.rect().topLeft())
        parent_pos = self.parent().mapToGlobal(self.parent().rect().topLeft())
        label_y = label_pos.y() - parent_pos.y()  # Position Y relative du label dans la fenêtre principale

        # Vérifier si le label est situé au-dessus d'une certaine hauteur (par exemple, 200 pixels)
        if label_y <= 350:
            # Afficher l'image en dessous du label
            image_window_pos = label_pos + QPoint(0, self.height())
        else:
            # Afficher l'image au-dessus du label (comme actuellement)
            image_window_pos = self.mapToGlobal(self.rect().topLeft() - self.image_window.rect().bottomLeft())

        self.image_window.move(image_window_pos)
        self.image_window.show()

    def checkMouseLeave(self):
        if not self.rect().contains(self.mapFromGlobal(QCursor.pos())):
            if not self.image_window.rect().contains(self.image_window.mapFromGlobal(QCursor.pos())):
                self.image_window.hide()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Exemple d'ajout de plusieurs widgets HoverWidget
        self.hover_widget1 = HoverWidget("Passez la souris ici pour voir l'image",
                                         "Ressources/Limule1.PNG",
                                         self)
        self.hover_widget2 = HoverWidget("Autre widget avec une image différente",
                                         "Ressources/Limule2.PNG",
                                         self)

        self.setWindowTitle('Fenêtre principale avec survol')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
