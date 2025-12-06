import subprocess
import concurrent.futures

working_dir='/mnt/data/apandey/op313_latest/veritas_latest_results'
data_dir='/mnt/data/vbf'


def submit_slurm_job(obs_id,laser):
    """
    Submits a SLURM job for a given observation ID.
    """
    # Define the SLURM job script or command
    slurm_script = f"""#!/bin/bash
#SBATCH --job-name=obs_{obs_id}
#SBATCH --output=obs_{obs_id}.out
#SBATCH --error=obs_{obs_id}.err
#SBATCH --ntasks=1

start_time=$(date +%s)  # Capture the start time

# Your command to process the observation ID

echo "Processing stage2 for observation ID: {obs_id}"
cp -v {working_dir}/out/stg1/{obs_id}_stg1.root {working_dir}/out/stg2/{obs_id}_stg2.root >> {working_dir}/log/{obs_id}_stg2.log

vaStage2 -Stage2_CalibratedEventCleaning=RING1 -Stage2_WriteCalibratedEvents=1 {data_dir}/{obs_id}.cvbf {working_dir}/out/stg2/{obs_id}_stg2.root {working_dir}/out/stg1/{laser}_flasher.root >> {working_dir}/log/{obs_id}_stg2.log 2>&1

end_time=$(date +%s)  # Capture the end time

echo "Total elapsed time =$((end_time - start_time))"
"""

    # Write the SLURM script to a temporary file
    script_filename = f"slurm_job_{obs_id}_stg2.sh"
    with open(script_filename, "w") as f:
        f.write(slurm_script)

    # Submit the SLURM job
    command = ["sbatch", script_filename]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Print the result of the submission
    if result.returncode == 0:
        print(f"Successfully submitted job for obs_id: {obs_id}")
    else:
        print(f"Failed to submit job for obs_id: {obs_id}. Error: {result.stderr}")

def read_obs_ids(filename):
    """
    Reads observation IDs from the first column of a file.
    """
    obs_ids = []
    flashers = []
    with open(filename, "r") as f:
        for line in f:
            obs_id = line.strip().split()[1]  # Assuming the first column contains the obs_id
            flasher = line.strip().split()[2] # Select flasher 2. for flasher 1 index will be 2.
            obs_ids.append(obs_id)
            flashers.append(flasher)
    return obs_ids,flashers

def main():
    # File containing observation IDs
    filename = "runlist.txt"

    # Read run IDs and corresponding flashers from the file
    obs_ids,flashers = read_obs_ids(filename)
    
    max_jobs = 25 # Define the maximum number of jobs to be run in parallel. 

    # Submit jobs in parallel using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_jobs) as executor:
        futures = [executor.submit(submit_slurm_job, obs_ids[i],flashers[i]) for i in range(len(obs_ids))]

        # Wait for all futures to complete
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    main()
