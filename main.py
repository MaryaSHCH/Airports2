
import sys
from PyQt5.QtWidgets import QApplication
from controller import AirportController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = AirportController()
    controller.run()
    sys.exit(app.exec_())

