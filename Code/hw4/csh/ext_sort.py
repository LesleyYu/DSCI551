import csv
import os

def sort_and_write_chunk(chunk, run_id):
    """
    Sorts a chunk of data in-memory by the first column and writes it to a temporary file.
    
    :param chunk: A list of data rows to be sorted.
    :param run_id: Identifier for the run, used for naming the temporary file.
    """
    # Sorts a chunk of data in-memory by the first column (product name)
    chunk.sort(key=lambda row: row[0])
    temp_filename = f"temp_run_{run_id}.csv"
    with open(temp_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(chunk)
    return temp_filename

def merge_runs(run_files, output_filename):
    """
    Merges sorted files (runs) into a single sorted output file.
    
    :param run_files: List of filenames representing sorted runs to be merged.
    :param output_filename: Filename for the merged, sorted output.
    """
    files = [open(run_file, 'r') for run_file in run_files]
    readers = [csv.reader(file) for file in files]

    with open(output_filename, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        rows = [next(reader, None) for reader in readers]
        
        while any(rows):
            # Find the row with the smallest first column (product name)
            min_row = min((row for row in rows if row is not None), key=lambda row: row[0])
            writer.writerow(min_row)
            # Fetch the next row from the reader that provided the last min_row
            for i, row in enumerate(rows):
                if row == min_row:
                    rows[i] = next(readers[i], None)
                    break

    for file in files:
        file.close()
        os.remove(file.name)

def external_sort(input_filename, output_filename):
    """
    the external sort process: chunking, sorting, and merging.
    
    :param input_filename: Name of the file with data to sort.
    :param output_filename: Name of the file where sorted data will be written.
    """
    # Variables for controlling chunk size and naming
    chunk_size = 2  # Each chunk contains 2 rows
    run_id = 0
    run_files = []
    
    with open(input_filename, 'r') as file:
        reader = csv.reader(file)
        chunk = []
        for row in reader:
            chunk.append(row)
            if len(chunk) == chunk_size:
                temp_filename = sort_and_write_chunk(chunk, run_id)
                run_files.append(temp_filename)
                chunk = []
                run_id += 1
        if chunk:
            temp_filename = sort_and_write_chunk(chunk, run_id)
            run_files.append(temp_filename)
    
    merge_runs(run_files, output_filename)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python3 ext_sort.py input.csv output.csv")
    else:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
        external_sort(input_filename, output_filename)
