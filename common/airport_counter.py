

class AirportCounter:
    def __init__(self, name):
        self.name = name
        self.take_off = 0
        self.landings = 0
        self.movements = 0

    def increase_take_off(self):
        self.take_off += 1
        self.movements += 1

    def increase_landing(self):
        self.landings += 1
        self.movements += 1
