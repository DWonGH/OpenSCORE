# OpenSCORE
Software for viewing and reporting EEGs according to the SCORE standard.

## Install
1. Download code
```shell script
git clone https://github.com/DWonGH/OpenSCORE.git
cd OpenSCORE
```

2. Setup virtual / conda environment e.g.
```shell script
conda create -y -n openscore python=3.7
conda activate openscore
```

3. Install requirements
```shell script
pip install -r requirements.txt
```

4. Run
```shell script
python main.py
```

## Usage
### Save a score report. 
Edit the report as required, then use the File -> Save/ Save As to save to a new json formatted file describing the report.

### Open a score report
Use File -> open and select a previously recorded report in json format.

### View an EEG in EDFBrowser
First specify the location of the EDF file using the "Recording Conditions" tab -> "Recorded data" field. Then click 
"Open in EDFBrowser" to open the file in a new EDFBrowser window. Close EDFBrowser window when finished.

### Load an EEG recording
I.e. load the contents of an EEG recording session - including the EDF file, and the accompanying txt file containing the 
recordings notes. Use the "File" -> "Load EEG" option and select the directory that contains the recording.
OpenSCORE will auto-populate fields using the edf and txt files where possible.

### Load a sequence of EEG's
To load and analyse a set of EEG recordings, use the "File" -> "Load EEG Sequence" option. First specify a list paths to 
the directories of the recordings in a txt file. Then complete the start session dialog from 
File -> Load EEG Sequence. An output directory will be created with a mirrored structure as the one specified in 
the specified paths txt file. Then, each of the recordings can be browsed by clicking "Next" or "Previous". In this mode,
reports will be saved to the mirror directory automatically when you click "Next" & "Previous" with the edf filename 
(but with a .json extension instead). If a report has been saved in the mirror directory then it will load that,
otherwise it will try to populate fields like in the "Load EEG" option

## Walkthrough "Load EEG sequence"
1. Create a txt file specifying the directories containing the required eeg recordings. The text file should look like:
```
E:\a_path_to_tueg_dataset\data\v2.0.0\edf\eval\abnormal\01_tcp_ar\007\00000768\s003_2012_04_06
E:\a_path_to_tueg_dataset\data\v2.0.0\edf\eval\abnormal\01_tcp_ar\011\00001154\s007_2012_07_25
E:\a_path_to_tueg_dataset\data\v2.0.0\edf\eval\abnormal\01_tcp_ar\012\00001217\s002_2012_09_17
``` 

2. Run OpenSCORE
3. Go to File -> Load EEG Sequence
4. Complete the start session dialog - including the interpreter name, a root directory to save the 
mirror directories to; and the path to the txt file specifying the eeg paths.
5. After clicking OK, there should be a new folder structure in the specified root directory.
6. Open the EDF file in EDFBrowser, and make changes to the score report as required.
7. Click the "Next" button, changes to the score report will be saved to the mirror output directory.


