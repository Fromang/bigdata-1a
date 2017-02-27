import os
import sys

# Configure the environmental variables
os.environ['SPARK_HOME'] = "C:/opt/spark-2.0.0-bin-hadoop2.7"
os.environ['JAVA_HOME'] = "C:/Program Files/Java/jre1.8.0_111"
os.environ['HADOOP_HOME'] = "C:/opt/hadoop-common-2.2.0-bin-master"

sys.path.append(os.environ['SPARK_HOME'] + "/python")
sys.path.append(os.environ['SPARK_HOME'] + "/python/lib/")
# -------------------------------------


from pyspark import SparkContext
from common import AirportTableFast
from _base import BaseTest


class SparkTest(BaseTest):
    def __init__(self, *args, **kwargs):
        BaseTest.__init__(self, *args, **kwargs)
        self.sc = SparkContext(appName="Big Data")
        self.sc.setLogLevel("WARN")
        self.airports = None

    @staticmethod
    def group_airports(airport_a, airport_b):
        airport_a[1] += airport_b[1]
        airport_a[2] += airport_b[2]
        airport_a[3] += airport_b[3]
        return airport_a

    def execute(self):
        dist_file = self.sc.textFile(self.filename)
        rdd = dist_file.map(lambda line: line.split(';'))
        rdd = rdd.flatMap(
            lambda words: (
                (words[0], [words[0], 1, 0, 1]),
                (words[1], [words[1], 0, 1, 0])
            )
        )
        rdd = rdd.reduceByKey(self.group_airports)
        rdd = rdd.map(lambda kv: kv[1])

        self.airports = rdd.takeOrdered(10, key=lambda airport: -airport[3])

    def print_results(self):
        table = AirportTableFast(self.airports)

        print("Top ten airports:")
        table.draw()

        print("Total airports: " + str(table.total_airports()))

SparkTest.description = """Spark
First Spark try. Seems to be faster"""


class SparkParallelTest(BaseTest):
    def __init__(self, *args, **kwargs):
        BaseTest.__init__(self, *args, **kwargs)
        self.sc = SparkContext(appName="Big Data")
        self.sc.setLogLevel("WARN")
        self.airports = None

    @staticmethod
    def group_airports(airport_a, airport_b):
        airport_a[1] += airport_b[1]
        airport_a[2] += airport_b[2]
        airport_a[3] += airport_b[3]
        return airport_a

    @staticmethod
    def group_landings_departures(airport):
        airport = airport[1]
        airport[0][1] += airport[1][1]
        airport[0][2] += airport[1][2]
        airport[0][3] += airport[1][3]
        return airport[0]

    def execute(self):
        dist_file = self.sc.textFile(self.filename)
        rdd = dist_file.map(lambda line: line.split(';'))

        # Parallel tasks
        rdd1 = rdd.map(lambda words: (words[0], [words[0], 1, 0, 1]), 2).reduceByKey(self.group_airports)
        rdd2 = rdd.map(lambda words: (words[1], [words[1], 0, 1, 1]), 2).reduceByKey(self.group_airports)

        rdd = rdd1.join(rdd2)
        rdd = rdd.map(self.group_landings_departures)

        self.airports = rdd.takeOrdered(10, key=lambda airport: -airport[3])

    def print_results(self):
        table = AirportTableFast(self.airports)

        print("Top ten airports:")
        table.draw()

        print("Total airports: " + str(table.total_airports()))

SparkParallelTest.description = """Spark Parallel
Try to use different maps to increase performance when the computer has more CPUs"""


class PythonMapReduceTest(BaseTest):
    def __init__(self, *args, **kwargs):
        BaseTest.__init__(self, *args, **kwargs)
        self.airports = None

    @staticmethod
    def join_airports(airports, traffic):
        airports.append([traffic[0], 1, 0, 1])
        airports.append([traffic[1], 0, 1, 1])
        return airports

    @staticmethod
    def group_airports(airports, airport):
        if airport[0] in airports:
            airport = airports[airport[0]]
            airport[1] += 1
            airport[2] += 1
            airport[3] += 1
        else:
            airports[airport[0]] = airport

        return airports

    @staticmethod
    def top_ten(top_ten, airport):
        i = 0
        found = False
        for i in range(0, len(top_ten)):
            _airport = top_ten[i]
            if airport[3] > _airport[3]:
                found = True
                break

        if i < 10:
            if found:
                top_ten[i] = airport
            else:
                top_ten.insert(i, airport)

        return top_ten

    def execute(self):
        # Read the file
        with open(self.filename) as f:
            lines_splitted = map(lambda l: l.split(";"), f)

        traffic = map(lambda words: (words[0], words[1]), lines_splitted)
        airports = reduce(self.join_airports, traffic, [])
        reduced_airports = reduce(self.group_airports, airports, dict())
        top_ten = reduce(self.top_ten, reduced_airports.values(), [])
        self.airports = top_ten

    def print_results(self):
        table = AirportTableFast(self.airports)

        print("Top ten airports:")
        table.draw()

        print("Total airports: " + str(table.total_airports()))

PythonMapReduceTest.description = """Python Map Reduce"""

