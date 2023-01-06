import random
from datetime import datetime
import sys
import os
import json
import time

# default values for test generator to create tests.
n_test = 10  # number of tests
row_start_range = 50  # start range of selecting number of rows
row_end_range = 500  # end range of selecting number of rows
# -> the number of rows randomly select from range[row_start_range, row_end_range]
column_start_range = 50  # start range of selecting number of columns
column_end_range = 500  # end range of selecting number of columns
# -> the number of columns randomly select from range[column_start_range, column_end_range]
obstacle_percent = 25  # percentage of obstacles we want in the maze

try:
    if len(sys.argv) > 1:  # check whether we have first argument.
        n_test = int(sys.argv[1])
    if len(sys.argv) > 2:  # check whether we have second argument.
        row_start_range = int(sys.argv[2])
    if len(sys.argv) > 3:  # check whether we have third argument.
        row_end_range = int(sys.argv[3])
    if len(sys.argv) > 4:  # check whether we have fourth argument.
        column_start_range = int(sys.argv[4])
    if len(sys.argv) > 5:  # check whether we have fifth argument.
        column_end_range = int(sys.argv[5])
    if len(sys.argv) > 6:  # check whether we have sixth argument.
        obstacle_percent = int(sys.argv[6])
except ValueError:  # check whether the given arguments are integer.
    print("Arguments must be integers! Run it again.")
    exit(0)

invalid = False
if n_test <= 0 or n_test > 100:  # check whether number of tests is between 1 and 100 cause it is the reasonable range.
    print("Number of tests must be between 1 and 100. You can run multiple times if you want more tests. "
          "Please run again with correct values.")
    invalid = True
if row_start_range < 2 or row_end_range < 2:  # check whether the given range for number of rows is reasonable or not.
    invalid = True
    print("Number of rows must be greater than 2, so the range must be (2, 2) at least. "
          "Please run again with correct values.")
if row_start_range > row_end_range:  # check whether the given range is reasonable or not.
    invalid = True
    print("The given range is not valid. start of the range of rows must be less than end of the range! "
          "Please run again with correct values.")
if column_start_range < 2 or column_end_range < 2:  # check whether the given range for number of columns is reasonable or not.
    invalid = True
    print("Number of columns must be greater than 2, so the range must be (2, 2) at least. "
          "Please run again with correct values.")
if column_start_range > column_end_range:  # check whether the given range is reasonable or not.
    invalid = True
    print("The given range is not valid. start of the range of columns must be less than end of the range! "
          "Please run again with correct values.")
if obstacle_percent < 0 or obstacle_percent > 100:  # check whether the given percentage is valid.
    print("Percentage of obstacles must in range 0 and 100! Please run again with correct values.")
    invalid = True

if obstacle_percent > 50:
    print(
        "With over 50% obstacles in the maze the probability of existing a path between start point and target is low.")

if invalid:
    exit(0)

for test_i in range(n_test):
    # Name of test files is datetime of system.
    test_file_name = (str(datetime.now().date()) + "_" + str(datetime.now().time()).replace(':', '') + '.json')
    if os.path.isfile("./tests/" + test_file_name):  # because of the speed of the system the name of two test can be the same. we do not want this to happen.
        time.sleep(1)
        test_file_name = (str(datetime.now().date()) + "_" + str(datetime.now().time()).replace(':', '') + '.json')
    # number of rows, number of columns, source, target, and obstacles determine randomly.
    n_rows = random.randint(row_start_range, row_end_range)
    n_columns = random.randint(column_start_range, column_end_range)
    source = (random.randint(0, n_rows - 1), random.randint(0, n_columns - 1))
    target = None
    while target is None or source == target:
        target = (random.randint(0, n_rows - 1), random.randint(0, n_columns - 1))
    n_obstacles = obstacle_percent * (n_rows * n_columns) // 100
    obstacles = []
    for obstacle_i in range(n_obstacles):
        obstacle = None
        while obstacle is None or obstacle in obstacles + [source, target]:
            obstacle = (random.randint(0, n_rows - 1), random.randint(0, n_columns - 1))
        obstacles.append(obstacle)
    test_data_dictionary = {
        "n_rows": n_rows,
        "n_columns": n_columns,
        "source": source,
        "target": target,
        "obstacles": obstacles
    }
    # we store each test as a json file.
    test_data_json = json.dumps(test_data_dictionary)
    if not os.path.isdir("./tests/"):
        os.mkdir("./tests/")
    with open("./tests/" + test_file_name, "w") as test_file:
        test_file.write(test_data_json)
