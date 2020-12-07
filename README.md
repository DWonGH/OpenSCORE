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
Record information as specified in the UI. Use the file -> save to save to a new json formatted file describing the report.

To view an EDF in EDF browser, use the recording conditions tab -> recorded data option to specify the location
of an EDF file, then click "Open in EDFBrowser" button in the toolbar.

To open an eeg recording where there is an EDF file and previously made txt file with recording information, use the
File -> Load EEG option. Then select a directory which contains the files. The txt file will be automatically loaded in
to openscore as well as the path for the EDF file to open with EDFBrowser (i.e. "Load EEG" will attempt to 
populate as many fields of the score report as possible)

Sets of recordings can be loaded to be analysed sequentially using the File -> Load EEG Sequence option. First
specify a list paths to the directories of the recordings in a txt file. Then complete the start session dialog from 
File -> Load EEG Sequence. An output directory will be created with a mirrored structure as the one specified in 
the specified paths txt file. Then, each of the recordings can be browsed by clicking "Next" or "Previous". In this mode,
reports will be saved to the mirror directory automatically when you click "Next" & "Previous" with the edf filename 
(but with a .json extension instead). If a report has been saved in the mirror directory then it will load that,
otherwise it will try to populate fields like in the "Load EEG" option

## Walkthrough
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
6. Open the EDF file in EDFBrowser, and make changes to the score report.
7. Click the "Next" button, changes to the score report can be saved and will be saved to the mirror output directory.


