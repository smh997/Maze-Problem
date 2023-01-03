import random
from datetime import datetime
import sys
import os
import json
import time

n_test = 10
row_start_range = 50
row_end_range = 500
column_start_range = 50
column_end_range = 500
obstacle_percent = 25

try:
    if len(sys.argv) > 1:
        n_test = int(sys.argv[1])
    if len(sys.argv) > 2:
        row_start_range = int(sys.argv[2])
    if len(sys.argv) > 3:
        row_end_range = int(sys.argv[3])
    if len(sys.argv) > 4:
        column_start_range = int(sys.argv[4])
    if len(sys.argv) > 5:
        column_end_range = int(sys.argv[5])
    if len(sys.argv) > 6:
        obstacle_percent = int(sys.argv[6])
except ValueError:
    print("Arguments must be integers! Run it again.")
    exit(0)

invalid = False
if n_test <= 0 or n_test > 100:
    print("Number of tests must be between 1 and 100. You can run multiple times if you want more tests. "
          "Please run again with correct values.")
    invalid = True
if row_start_range < 2 or row_end_range < 2:
    print("Number of rows must be greater than 2, so the range must be (2, 2) at least. "
          "Please run again with correct values.")
if row_start_range > row_end_range:
    print("The given range is not valid. start of the range of rows must be less than end of the range! "
          "Please run again with correct values.")
if column_start_range < 2 or column_end_range < 2:
    print("Number of columns must be greater than 2, so the range must be (2, 2) at least. "
          "Please run again with correct values.")
if column_start_range > column_end_range:
    print("The given range is not valid. start of the range of columns must be less than end of the range! "
          "Please run again with correct values.")
if obstacle_percent < 0 or obstacle_percent > 100:
    print("Percentage of obstacles must in range 0 and 100! Please run again with correct values.")
    invalid = True

if obstacle_percent > 50:
    print(
        "With over 50% obstacles in the maze the probability of existing a path between start point and target is low.")

if invalid:
    exit(0)

for test_i in range(n_test):
    test_file_name = (str(datetime.now().date()) + "_" + str(datetime.now().time()).replace(':', '') + '.json')
    if os.path.isfile("./tests/" + test_file_name):
        time.sleep(1)
        test_file_name = (str(datetime.now().date()) + "_" + str(datetime.now().time()).replace(':', '') + '.json')
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
    test_data_json = json.dumps(test_data_dictionary)
    if not os.path.isdir("./tests/"):
        os.mkdir("./tests/")
    with open("./tests/" + test_file_name, "w") as test_file:
        test_file.write(test_data_json)