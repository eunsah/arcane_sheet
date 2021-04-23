import sys
from arc_manager import ARC_Manager
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QWidget

arc_prefix = ['VJ', 'CC', 'LA', 'AR', 'MO', 'ES']
default_text = ('Inconsolata', 12)
default_title = ('Inconsolata', 16)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Arcane Sheet')
        self.resize(700, 400)

def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    # main()
    print ('start main')
    a = ARC_Manager()
    print ('end main')