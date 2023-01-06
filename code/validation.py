
def is_valid(dictionary):
    """
        Its job is to validate input test files.
    :param dictionary: the data given in form of a dictionary
    :return: True if the test is valid and False otherwise.
    """
    try:
        n_rows = dictionary.get("n_rows")
        n_columns = dictionary.get("n_columns")
        source_coords = dictionary.get("source")
        target_coords = dictionary.get("target")
        obstacles_coords = dictionary.get("obstacles")
        if None in [n_rows, n_columns] or None in source_coords or None in target_coords or None in obstacles_coords:
            raise ValueError
        if [val for val in [n_rows, n_columns, source_coords[0], source_coords[1], target_coords[0], target_coords[1]] + [x[0] for x in obstacles_coords] + [x[1] for x in obstacles_coords] if not isinstance(val, int)]:
            raise TypeError
    except ValueError:
        print("Arguments cannot be None! Run it again.")
        return False
    except TypeError:
        print([val for val in [n_rows, n_columns, source_coords[0], source_coords[1], target_coords[0], target_coords[1]] + [x[0] for x in obstacles_coords] + [x[1] for x in obstacles_coords] if not isinstance(val, int)])
        print("Arguments must be integers! Run it again.")
        return False

    if n_rows < 2:
        return False
    if n_columns < 2:
        return False
    if not (0 <= source_coords[0] < n_rows and 0 <= source_coords[1] < n_columns):
        return False
    if not (0 <= target_coords[0] < n_rows and 0 <= target_coords[1] < n_columns):
        return False
    for obstacle_coords in obstacles_coords:
        if not (0 <= obstacle_coords[0] < n_rows and 0 <= obstacle_coords[1] < n_columns):
            return False
    return True
