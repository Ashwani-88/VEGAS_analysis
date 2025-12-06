import subprocess
import concurrent.futures

def submit_slurm_job(obs_id):
    """
    Submits a SLURM job for a given observation ID.
    """
    # Define the SLURM job script or command
    slurm_script = f"""#!/bin/bash
#SBATCH --job-name=obs_{obs_id}
#SBATCH --output=obs_{obs_id}_stage4.out
#SBATCH --error=obs_{obs_id}_stage4.err
#SBATCH --ntasks=1

# Your command to process the observation ID
echo "Processing observation ID: {obs_id}"

cp -v /mnt/data/apandey/op313_latest/veritas/out/stg2/{obs_id}_stg2.root /mnt/data/apandey/op313_latest/veritas/out/stg4/{obs_id}_soft_0p5off_ITMgeo_stg4.root >> /mnt/data/apandey/op313_latest/veritas/log/{obs_id}_soft_0p5off_ITMgeo_stg4.log

vaStage4 -DistanceUpper=0/1.43 -SizeLower=0/400 -NTubesMin=0/5 -table=/mnt/data/IRFs/v6/lt_2324w_CARE162d12_v259rc0v2p1GT_05off_Z0-60_d1p43_4nsb.root -ITM_MSW_Upper=1.1 -ITM_MSL_Upper=1.3 -ITM_NpeMin=3 -ITM_NpeMax=300  -M3D_Algorithm=ImageTemplateModel -ITM_templateList=/mnt/data/IRFs/v6/TemplateList_CARE_V6_ATM61_seas2324w.txt  /mnt/data/apandey/op313_latest/veritas/out/stg4/{obs_id}_soft_0p5off_ITMgeo_stg4.root >> /mnt/data/apandey/op313_latest/veritas/log/{obs_id}_soft_0p5off_ITMgeo_stg4.log 2>&1

echo "Done processing stage4 for {obs_id}"
"""

    # Write the SLURM script to a temporary file
    script_filename = f"slurm_job_{obs_id}_stage4.sh"
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
    filename = "run_ids.txt"

    # Read observation IDs from the file
    obs_ids = read_obs_ids(filename)
    max_jobs = 25
    # Submit jobs in parallel using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_jobs) as executor:
        futures = [executor.submit(submit_slurm_job, obs_id) for obs_id in obs_ids]

        # Wait for all futures to complete
        concurrent.futures.wait(futures)
    
if __name__ == "__main__":
    main()
