from a import DictionaryTest, ListTest, SortedListTest
from b import PythonMapReduceTest, SparkTest

programs = {
    "list": ListTest,
    "sorted-list": SortedListTest,
    "dict": DictionaryTest,
    "spark": SparkTest,
    "map-reduce": PythonMapReduceTest
}

types = "/".join(programs.keys())
