class AirportTable:
    def __init__(self, airports):
        self.airports = airports

    def draw(self):
        self._draw_table(self.airports)

    def draw_top_ten(self):
        airports = sorted(self.airports, key=lambda airport: -airport.movements)
        self._draw_table(airports[:10])

    def total_airports(self):
        return len(self.airports)

    @staticmethod
    def _draw_table(airports):
        print("AIRPORT NAME    TOTAL #MOVEMENTS    #TAKE-OFFs    #LANDINGS")
        for i in range(0, len(airports)):
            airport = airports[i]
            line = airport.name + " " * (16 - len(airport.name))
            line += str(airport.movements) + " " * (20 - len(str(airport.movements)))
            line += str(airport.take_off) + " " * (14 - len(str(airport.take_off)))
            line += str(airport.landings)
            print(line)


class AirportTableFast:
    def __init__(self, airports):
        self.airports = airports

    def draw(self):
        self._draw_table(self.airports)

    def total_airports(self):
        return len(self.airports)

    @staticmethod
    def _draw_table(airports):
        print("AIRPORT NAME    TOTAL #MOVEMENTS    #TAKE-OFFs    #LANDINGS")
        for i in range(0, len(airports)):
            airport = airports[i]
            print airport
            print('%-17s %-17i %-17i %-17i' % (airport[0], airport[1], airport[2], airport[3]))
