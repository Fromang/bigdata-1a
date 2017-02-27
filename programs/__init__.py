from a import DictionaryTest, ListTest, SortedListTest
from b import PythonMapReduceTest, SparkTest, SparkParallelTest

programs = {
    "list": ListTest,
    "sorted-list": SortedListTest,
    "dict": DictionaryTest,
    "spark": SparkTest,
    "spark-parallel": SparkParallelTest,
    "map-reduce": PythonMapReduceTest
}

types = "/".join(programs.keys())
