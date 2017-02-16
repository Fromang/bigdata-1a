

class Traffic:
    def __init__(self, departure, arrival):
        self.departure = departure
        self.arrival = arrival

    def __str__(self):
        return "Traffic(" + self.departure + "," + self.arrival + ")"

    @staticmethod
    def from_line(line):
        words = line.split(';')
        return Traffic(words[0], words[1])

    @staticmethod
    def read_file(filename, process):
        with open(filename) as f:
            for line in f:
                traffic = Traffic.from_line(line)
                process(traffic)
