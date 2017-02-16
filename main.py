#!/usr/bin/python

import sys
import getopt
import time
import psutil
import os
from programs import programs, types


usage = 'test.py -i <inputfile> -m [' + types + ']'
t0 = time.time()


def close_program(times=list()):
    times.append(('total', time.time() - t0))
    print("")
    print("Resources used:")
    print("\t- Time")
    for (time_name, value) in times:
        print("\t\t- The " + time_name + " the program is " + str(value))

    print("")
    info = psutil.Process(os.getpid()).memory_info()
    print("\t- Memory usage " + str(info.vms/1000) + " Kb")
    sys.exit()


def main(argv):
    # Get args
    input_file = ''
    tp = 'dict'
    try:
        opts, args = getopt.getopt(argv, "hi:m:", ["ifile=", "method="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            close_program()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-m", "--method"):
            tp = arg

    # Run the program
    if tp not in programs:
        print("Type not fount.")
        print(usage)
        close_program()

    test_class = programs[tp]
    test = test_class(input_file)
    print("========================================================================================================")
    print(test_class.description)
    print("========================================================================================================")
    print("")
    print("Executing program...")
    t1 = time.time()
    test.execute()
    print("Output:")
    t2 = time.time()
    test.print_results()
    t3 = time.time()

    # Close the program
    close_program([
        ('fetch and print', t3 - t2),
        ('execution', t2 - t1)
    ])

if __name__ == "__main__":
    main(sys.argv[1:])
