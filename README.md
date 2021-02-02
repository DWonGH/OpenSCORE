# OpenSCORE
An EEG reporting tool according to the SCORE standard (work in progress).

<br>
<p align="center">
  <img height="400" src="OpenSCORE.png">
</p>
<br>

Create, save & open existing ```.SCORE``` files whilst analysing the corresponding EEG using EDFBrowser.

## Installation (Windows)

1. Install this repository locally. E.g. Open a PowerShell terminal:
```shell script
git clone https://github.com/DWonGH/OpenSCORE.git
cd OpenSCORE
```

2. OpenSCORE works with python 3.6 and the dependencies described in the ```requirements.txt``` file. It 
is recommended to use a conda virtual environment or virtualenv and install the dependencies with pip. 
E.g. In the PowerShell terminal:
```shell script
conda create -y -n openscore python=3.6
conda activate openscore
pip install -r requirements.txt
```

3. Install EDFBrowser  
OpenSCORE uses a customised version of EDFBrowser to analyze and view the EEG recordings. Go to [the release](https://github.com/d3-worgan/edfbrowser/releases/tag/v2.0)
for OpenSCORE custom EDFBrowser. Download the ```edfbrowser.zip``` file and unzip into the root of the OpenSCORE directory.
There should be a directory in the root of OpenSCORE called ```edbrowser``` with the ```.exe``` and ```.dll``` files inside.

4. To run OpenSCORE, inside the PowerShell terminal:
```shell script
python main.py
```

## Development
The project structure loosely follows the MVC design pattern:
- The views in the ```src/views``` directory are essentially Qt Widgets. 
Files in the views directory should generally only contain code for specifying the 
widgets and layout.
- Once the view/ widget is created, it is tied to a controller which is where we
"connect" the widgets in the view to action code. E.g. tying the push
buttons to handler (hdl) methods.
- The controllers take data from the view and update the data model (or vice
versa). They also control opening dialogs etc. Data is passed between the model and view via
the controller using python dictionaries.
- The models are then used to build the report and can be written or opened
from persisted files.
- The tests follow the same structure as the source code. Each test case needs
to be added to the main test file in the project root.
