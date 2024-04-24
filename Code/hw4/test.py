import csv

run_files = ['run_file_0.csv', 'run_file_1.csv', 'run_file_2.csv', 'run_file_3.csv', 'run_file_4.csv', 'run_file_5.csv', 'run_file_6.csv', 'run_file_7.csv'] 

readers = [csv.reader(open(run_file, "r")) for run_file in run_files]

input_buffers = []
output_buffer = []

for reader in readers:
    # read two lines into input buffers
    try:
        for i in range(2):
            row = next(reader, None)
            print("\n\n Row: ", row)
            if row is not None:
                input_buffers.append(row)
            print("\ninput_buffers: ", input_buffers)
    except StopIteration:
        pass
    
    
