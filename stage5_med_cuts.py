import subprocess
import concurrent.futures

working_dir='/mnt/data/apandey/op313_latest/crab_data/med_cuts/'

def submit_slurm_job(obs_id):
    """
    Submits a SLURM job for a given observation ID.
    """
    # Define the SLURM job script or command
    slurm_script = f"""#!/bin/bash
#SBATCH --job-name=obs_{obs_id}
#SBATCH --output=obs_{obs_id}_stage5.out
#SBATCH --error=obs_{obs_id}_stage5.err
#SBATCH --ntasks=1

# Your command to process the observation ID, use -ES_CutTimes=0/172 for any timecuts.
echo "Processing observation ID: {obs_id}"

vaStage5 -Method=stereo -MeanScaledWidthLower=0.05 -MeanScaledWidthUpper=1.1 -MeanScaledLengthLower=0.05 -MeanScaledLengthUpper=1.3 -MaxHeightLower=7 -inputFile={working_dir}/out/stg4/{obs_id}_soft_0p5off_ITMgeo_stg4.root -outputFile={working_dir}/out/stg5/{obs_id}_soft_0p5off_ITMgeo_stg5.root >> {working_dir}/log/{obs_id}_soft_0p5off_ITMgeo_stg5.log 2>&1

echo "Done processing stage 5 for {obs_id}"
"""

    # Write the SLURM script to a temporary file
    script_filename = f"slurm_job_{obs_id}_stage5.sh"
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
    with open(filename, "r") as f:
        for line in f:
            obs_id = line.strip().split()[0]  # Assuming the first column contains the obs_id
            obs_ids.append(obs_id)
    return obs_ids

def main():
    # File containing observation IDs
    filename = "run_ids_notimecuts.txt"

    # Read observation IDs from the file
    obs_ids = read_obs_ids(filename)
    max_jobs = 25
    for obs_id in obs_ids:
        submit_slurm_job(obs_id)
    
    # Submit jobs in parallel using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_jobs) as executor:
        futures = [executor.submit(submit_slurm_job, obs_id) for obs_id in obs_ids]

        # Wait for all futures to complete
        concurrent.futures.wait(futures)
    
if __name__ == "__main__":
    main()
