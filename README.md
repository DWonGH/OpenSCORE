# OpenSCORE
An EEG reporting tool according to the SCORE standard.

- Create score reports
- Load and edit existing score reports
- Link EDF files to score reports
- Open the corresponding EDF files in EDFBrowser
- Initialise a score report using and EDF and existing
record description.
- Load multiple EDF files for multiple analysis.
- Option for recording eye tracking data with tobii

## Installation

1. Download code
```shell script
git clone https://github.com/DWonGH/OpenSCORE.git
cd OpenSCORE
```

2. Setup virtual / conda environment e.g.
```shell script
conda create -y -n openscore python=3.6
conda activate openscore
```

3. Install requirements
```shell script
pip install -r requirements.txt
```

4. Install EDFBrowser
Go to https://github.com/d3-worgan/edfbrowser/releases/tag/v1.0
Download the zip file and unzip into the root of this project directory.
There should now be a directory called 'release' in the root of the project directory.
Inside is the EDFBrowser application.

5. Install Eye Tracker Manager

4. Run
```shell script
python main.py
```



## Development
- Loosely follows the MVC design pattern
- Data is passed between the model and view using dictionaries.
- User interaction code is separated into controller files
- The controller then manages the updating and passing data between model and view.
- Data is persisted using json files.
- It was important to separate the MVC code especially when changing between reports
- MainWindowController is root controller for application and loads the main model and view
- Unit tests created following same directory structure as source code.

