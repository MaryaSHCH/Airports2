from view import AirportView

class AirportController:
    def __init__(self):
        self.view = AirportView()

    def run(self):
        self.view.show()
