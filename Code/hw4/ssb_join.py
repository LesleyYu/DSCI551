import csv


def simple_sort_based_join(product_filename, maker_filename, output_filename):
    """
    Executes a simple sort-based join between two datasets and writes the output to a CSV file.

    :param product_filename: Filename of the sorted product dataset.
    :param maker_filename: Filename of the sorted maker dataset.
    :param output_filename: Filename for the output joined dataset.
    """
    with open(product_filename, "r") as product_file, open(maker_filename, "r") as maker_file, open(output_filename, "w", newline="") as output_file:
        product_reader = csv.reader(product_file)
        maker_reader = csv.reader(maker_file)
        writer = csv.writer(output_file)

        product_row = next(product_reader, None)
        maker_row = next(maker_reader, None)

        while product_row and maker_row:
            if product_row[0] == maker_row[0]:
                writer.writerow(product_row + [maker_row[1]])
                product_row = next(product_reader, None)
                maker_row = next(maker_reader, None)
            elif product_row[0] < maker_row[0]:
                product_row = next(product_reader, None)
            else:
                maker_row = next(maker_reader, None)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python ssb_join.py <product_file.csv> <maker_file.csv> <output_file.csv>")
    else:
        simple_sort_based_join(sys.argv[1], sys.argv[2], sys.argv[3])
