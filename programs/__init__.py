from programs import DictionaryTest, ListTest, SortedListTest

programs = {
    "list": ListTest,
    "sorted-list": SortedListTest,
    "dict": DictionaryTest,
}

types = "/".join(programs.keys())
