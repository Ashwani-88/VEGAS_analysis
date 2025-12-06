import numpy as np
import os
import pandas as pd

database_path="/mnt/data/vbf"
#database_path="/mnt/data/apandey/op313_jan25"
no_stream=1

def genCommand(date,fname):
    return 'bbftp -u bbftp -p '+str(no_stream)+' -S -V -e "mget /veritas/data/d'+date+'/'+fname+'" gamma1.astro.ucla.edu\n'

def is_file_in_list(file_name, file_list):
    return file_name in file_list

#def create_script(filename):

if __name__=="__main__":
    
    #create_script(runlist)

    df = pd.read_csv("runlist.txt", sep="\t", dtype=str, header=None)
    
    df.columns = ['date', 'runid', 'flasher1', 'flasher2', 'flasher3', 'flasher4']
     
    # Combine all flahser lists and make a unique flasher list.

    unique_flashers = pd.unique(df[['flasher1', 'flasher2', 'flasher3','flasher4']].values.ravel())

    runid = df["runid"]

    # Write runids and unique flashers in text files. 
    runid.to_csv('run_ids.txt', index=False, header=False)
    uniq_flash = pd.DataFrame(unique_flashers)
    uniq_flash.to_csv('unique_flashers.txt', index=False, header=False)

    # Combine all runids and unique flashers. 

    combined_ids = runid.tolist() + unique_flashers.tolist()
    
    # Check for the available data in the database. 

    available_runlist = np.unique(os.listdir(database_path))
    
    # Find new ids to be downloaded. 
    new_ids = []
    print (combined_ids)
    for i in combined_ids:
        filename = i+'.cvbf'
        
        if is_file_in_list(filename,available_runlist):
            print ("File " +filename +' is already available. No need to download again.')
        else:
            new_ids.append(i)
    
    results = {}
            
    # Search for date corresponding to each new id. 
    for obs_id in new_ids:
        date = df.loc[
        (df['runid'] == obs_id) |
        (df['flasher1'] == obs_id) |
        (df['flasher2'] == obs_id) |
        (df['flasher3'] == obs_id) |
        (df['flasher4'] == obs_id),
        'date'
    ].values
    
        results[obs_id] = date.tolist()
    
    if len(new_ids)>0:
        fo = open('scp_download_data.sh','w')
        for obs_id, date_list in results.items():
            command = genCommand(date_list[0],obs_id+'.cvbf')
            fo.writelines(command)
        
        fo.close()

    else:
        print(f"All data already availabe!!!") 
    
