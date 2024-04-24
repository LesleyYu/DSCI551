import csv
import os

def sort_and_write_chunk(chunk, run_id):
    """
    Sorts a chunk of data in-memory by the first column and writes it to a temporary file.
    
    :param chunk: A list of data rows to be sorted.
    :param run_id: Identifier for the run, used for naming the temporary file.
    """
    sorted_chunk = sorted(chunk, key= lambda row: row[0])   # sort the chunk by the first column
    temp_f = f"run_file_0_{run_id}.csv"
    with open(temp_f, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(sorted_chunk)
    return temp_f


def merge_runs(run_files, output_filename):
    """
    Merges sorted files (runs) into a single sorted output file using external sorting.
    :param run_files: List of filenames representing sorted runs to be merged.
    :param output_filename: Filename for the merged, sorted output.
    """
    def merge_buffers(input_buffers, output_file):
        """
        Recursive function to merge input buffers and write to output file.
        """
        # Base case: If all input buffers are empty, return
        if all(not buf for buf in input_buffers):
            return

        # Find the input buffer with the smallest row
        min_buffer_id = None
        min_row = None
        for i, buf in enumerate(input_buffers):
            if buf:
                row = buf[0]
                if min_row is None or row[0] < min_row[0]:
                    min_buffer_id = i
                    min_row = row

        # Write the smallest row to the output file
        writer.writerow(input_buffers[min_buffer_id].pop(0))

        # Refill the input buffer from the corresponding run
        try:
            next_row = next(readers[min_buffer_id])
            input_buffers[min_buffer_id].append(next_row)
        except StopIteration:
            # This run is exhausted, skip it
            pass

        merge_pass += 1     # next pass, with (2^merge_pass)-page runs

        # Recursive call to merge remaining buffers
        merge_buffers(input_buffers, output_file)

    # initializations
    merge_pass_count = 1      # start from pass 1 with 1-page runs
    run_id = 0  # 

    # Open readers for input runs
    readers = [csv.reader(open(run_file, "r")) for run_file in run_files]

    # Merge two input buffers
    for reader in readers:
        input_buffers = []
        output_buffer = []
        # read two lines into input buffers
        try:
            for i in range(2):  # two input buffers in total
                row = next(reader, None)
                if row is not None:
                    input_buffers[i].append(row)
                print("input_buffers: ", input_buffers)
        except StopIteration:
            pass

        merge_buffers(input_buffers, output_buffer)

        # write into run_files
        temp_f = f"run_file_{merge_pass_count}_{run_id}.csv"
        with open(temp_f, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(output_buffer)
        run_id += 1

    # Close input files
    for reader in readers:
        reader.close()

def external_sort(input_filename, output_filename):
    """
    the external sort process: chunking, sorting, and merging.
    
    :param input_filename: Name of the file with data to sort.
    :param output_filename: Name of the file where sorted data will be written.
    """
    runs = []   # initialize all runs
    with open(input_filename, "r") as f:
        reader = csv.reader(f)
        chunk = []      # initialize chunk
        run_id = 0      # id of runs starting from 0
        for row in reader:
            chunk.append(row)
            if len(chunk) == 2:
                run_file = sort_and_write_chunk(chunk, run_id)
                runs.append(run_file)   # store sorted run into 'runs'
                # print("run files: ", chunk ,'\n')
                chunk = []              # clear current chunk
                run_id += 1             # incre id for next run
    
    # the blocks in last run chunk
    if chunk:
        run_file = sort_and_write_chunk(chunk, run_id)
        # print("run files: ", chunk ,'\n')
        runs.append(run_file)

    merge_runs(runs, output_filename)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python3 ext_sort.py input.csv output.csv")
    else:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
        external_sort(input_filename, output_filename)
