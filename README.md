# VEGAS_analysis
Steps for analyzing VERITAS data and required scripts.  

Step 1: Make sure you have the following file in the current directory.
runlist_ext.csv  runlist.txt
(can be downloaded from the logen)

Step 2: Copy create_download_scp.py to the directory and run
Python create_download_scp.py
It will create two files run_ids.txt and unique_flashers.txt

Step 3: Check all four laser files are the same and if now then generate script to combine laser files. 
Python check_same_flashers.py

Step 4: cp runlist.txt run_ids.txt unique_flashers.txt /home/apandey/
Because you can submit a job from the main node (home).

Step 5: In the /home/apandey directory. Change working_dir path in stage1.py and stage1_flasher.py to the working directory where you will get analyzed results. Then, 
Python stage1.py
Python stage1_flasher.py

Step 6: copy read_error.sh file to log directory in the working directory.
Change the file name in read_error.sh. And then run it
Bash read_error.sh

It will print any error reported during different stages. 

Stage 7: 

