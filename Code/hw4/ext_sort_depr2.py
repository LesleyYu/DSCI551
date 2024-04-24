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
    # initializations
    merge_pass_count = 1      # start from pass 1 with 1-page runs
    run_id = 0  #

    # Open readers for input runs
    readers = [csv.reader(open(run_file, "r")) for run_file in run_files]
    
    # i = number of merges in current pass
    for i in range(0, len(readers), 2):
        print("\n\ni: ", i)
        print(f"pass: {merge_pass_count}, file id: {i // 2}")

        for j in range(2):    # read 2 files
            while (readers[i+j]):
                # IO buffers initialization
                input_buffers = [[] for _ in range(2)]
                output_buffer = []

                for k in range(2):  # read 2 lines each buffer
                    print("k: ", k)
                    print("row: ", row)

                    row = next(readers[i+j], None)
                    if row is not None:
                        input_buffers[k].append(row)

                    print("input_buffers: ", input_buffers)

                    merge_buffers(input_buffers, output_buffer, merge_pass_count, run_id)
                    
            run_id += 1

        merge_pass_count += 1

    def merge_buffers(input_buffers, output_buffer, merge_pass_count, run_id):
        while
        
        for input_buffer in input_buffers:
            sorted 
        sorted_chunk = sorted(input_buffers, key= lambda row: row[0])   # sort the chunk by the first column
        temp_f = f"run_file_0_{run_id}.csv"
        with open(temp_f, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(sorted_chunk)
        return temp_f
        
            
          
      

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
