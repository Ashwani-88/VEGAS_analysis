def check_columns(filename, outfile):
    with open(filename, 'r') as file, open(outfile, 'w') as fout:
        for line in file:
            columns = line.strip().split()
            if len(columns) >= 4:  # ensure there are at least 4 columns.
                if not (columns[2] == columns[3] == columns[4] == columns[5]):
                    print(line.strip())
                    cmd = (
                        'combineLaser("'
                        + out_dir + columns[2] + '_flasher.root","'
                        + out_dir + columns[2] + '_flasher.root","'
                        + out_dir + columns[3] + '_flasher.root","'
                        + out_dir + columns[4] + '_flasher.root","'
                        + out_dir + columns[5] + '_flasher.root")'
                    )
                    fout.write(cmd + "\n")
                else:
                    print("All four laser files are the same!!\n")
            else:
                print(f"Invalid line (less than 4 columns): {line.strip()}\n")

# Example usage
filename = "runlist.txt"
outfile = "combineLaser_commands.txt"
out_dir = "/mnt/data/apandey/op313_latest/veritas_latest_results/out/stg1/"
check_columns(filename, outfile)
