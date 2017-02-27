from common import Traffic, AirportCounter, AirportTable
from _base import BaseTest


class BaseTestA(BaseTest):
    def __init__(self, *args, **kwargs):
        BaseTest.__init__(self, *args, **kwargs)

    def test_process(self, traffic):
        self.get_airport(traffic.arrival).increase_take_off()
        self.get_airport(traffic.departure).increase_landing()

    def get_airport(self, airport_name):
        pass

    def get_airport_table(self):
        pass

    def execute(self):
        Traffic.read_file(self.filename, self.test_process)

    def print_results(self):
        table = self.get_airport_table()

        print("Top ten airports:")
        table.draw_top_ten()

        print("Total airports: " + str(table.total_airports()))


class ListTest(BaseTestA):
    def __init__(self, *args, **kwargs):
        BaseTest.__init__(self, *args, **kwargs)
        self.airports = list()

    def get_airport(self, airport_name):
        for airport in self.airports:
            if airport.name == airport_name:
                return airport
        airport = AirportCounter(airport_name)
        self.airports.append(airport)
        return airport

    def get_airport_table(self):
        return AirportTable(self.airports)

ListTest.description = """List (without index)
This is the worst because each time has to find in all the stored airport counters."""


class SortedListTest(BaseTestA):
    def __init__(self, *args, **kwargs):
        BaseTest.__init__(self, *args, **kwargs)
        self.airports = list()

    def get_airport(self, airport_name):
        (index, airport) = self.dichotomic_search(airport_name)
        if airport is None:
            airport = AirportCounter(airport_name)
            self.airports.insert(index, airport)

        return airport

    def dichotomic_search(self, airport_name, first=0, last=None):
        if last is None:
            last = len(self.airports)
            if last == 0:
                return 0, None

        index = (last - first) / 2 + first
        airport = self.airports[index]
        if airport.name == airport_name:
            return index, airport
        elif first == index:
            if airport.name > airport_name:
                return first + 1, None
            else:
                return first, None
        elif airport.name > airport_name:
            return self.dichotomic_search(airport_name, index, last)
        elif airport.name < airport_name:
            return self.dichotomic_search(airport_name, first, index)

    def get_airport_table(self):
        return AirportTable(self.airports)

SortedListTest.description = """Sorted list (equivalent to tree index)
Optimization for the list method.
The airports are sorted by name, then a dichotomic search can be used."""


class DictionaryTest(BaseTestA):
    def __init__(self, *args, **kwargs):
        BaseTest.__init__(self, *args, **kwargs)
        self.airports = dict()

    def get_airport(self, airport_name):
        if airport_name in self.airports:
            return self.airports[airport_name]

        self.airports[airport_name] = AirportCounter(airport_name)
        return self.airports[airport_name]

    def get_airport_table(self):
        return AirportTable(self.airports.values())

DictionaryTest.description = """Dictionary (equivalent to hash index)
This is the fastest method because its very easy to find elements using its index."""
