# VEGAS_analysis
Steps for analyzing VERITAS data and required scripts.  

Step 1: Make sure you have the following files in the current directory.
runlist.csv  runlist.txt
(can be downloaded from the logen: https://veritasm.sao.arizona.edu/DQM/loggen.html)

Step 2: Copy create_download_scp.py to the directory and run
Python create_download_scp.py
It will create two files run_ids.txt and unique_flashers.txt

Step 3: Use extendRunlist.py to get the timecuts and other information. 
python extendRunlist.py runlist.csv   # This will give runlist_extended.csv file. 

Step 4: Check that all four laser files are the same, and if not, then generate a script to combine the laser files. Change out_dir name in the check_same_flashers.py file !!<br>
Python check_same_flashers.py
<br> Check 'combineLaser_commands.txt' if there is any command written in it, then combine the flashers (see steps given below). 

Step 5: cp runlist.txt run_ids.txt unique_flashers.txt /home/apandey/
Because you can submit a job from the main node (home).

Step 6: In the /home/apandey directory. Change working_dir path in stage1.py and stage1_flasher.py to the working directory where you will get analyzed results. Then, 
Python stage1.py
Python stage1_flasher.py

Step 7: copy read_error.sh file to log directory in the working directory.
Change the file name in read_error.sh. And then run it
bash read_error.sh

It will print any errors reported during different stages. 

Stage 7: 

