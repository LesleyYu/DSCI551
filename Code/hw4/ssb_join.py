import csv


def simple_sort_based_join(product_filename, maker_filename, output_filename):
    """
    Executes a simple sort-based join between two datasets and writes the output to a CSV file.

    :param product_filename: Filename of the sorted product dataset.
    :param maker_filename: Filename of the sorted maker dataset.
    :param output_filename: Filename for the output joined dataset.
    """


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python ssb_join.py <product_file.csv> <maker_file.csv> <output_file.csv>")
    else:
        simple_sort_based_join(sys.argv[1], sys.argv[2], sys.argv[3])
