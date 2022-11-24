# smi-parser
Simple SMI parser for the Caroolive Dashcam App

The [Caroolive Dashcam App](https://github.com/Pokevian/caroolive-app) records videos as mp4's, as well as metrics during a trip as subtitle files (.smi) for the video which was created.  
The data stored in the base64 encoded sections includes timestamps, GPS data, as well as car diagnostic data.

This script (and standalone executable) parses the SMI files to decode the GPS data and add it into the SMI file (saves the file with a .smi2 extension, so as not to overwrite). It will also
generate a KML from the trip data in the SMI to identify the route taken, and the start/end dates.

Standalone executable generated using: `pyinstaller -F --icon=sedan.ico smi-parser.py`
Icon for standalone executable sourced from [here](https://www.flaticon.com/free-icon/sedan_2736906).

# Usage
`smi-parser.exe -i <smi_file>`  
`smi-parser.py -i <smi_file>`  
