

class AirportCounter:
    def __init__(self, name, take_off=0, landings=0):
        self.name = name
        self.take_off = take_off
        self.landings = landings
        self.movements = take_off + landings

    def increase_take_off(self):
        self.take_off += 1
        self.movements += 1

    def increase_landing(self):
        self.landings += 1
        self.movements += 1

    def __str__(self):
        return "AirportCounter(name=" + self.name + ", movements=" + self.movements + ")"

    def add(self, other):
        self.take_off += other.take_off
        self.landings += other.landings
        self.movements += other.movements
        return self
