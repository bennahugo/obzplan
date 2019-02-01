# obzplan
Simple tool for visualizing observations
(C) Benjamin Hugo, South African Radio Astronomy Observatory under GNU GPLv3

# install
In a new virtual environment run to install from PyPI
```
pip3 install obzplan
```
Remember to add -e and obzplan/ if you have cloned the repo locally

Note: you probably need to install tkinter for python3 if you haven't done so yet:
```
apt-get install python3-tk
```
# Usage
```
positional arguments:
  src                   Sources to plot

optional arguments:
  -h, --help            show this help message and exit
  --lat LAT             Observer Latitude
  --long LONG           Observer Longitude
  --elev ELEV           Observer Elevation
  -s START, --start START
                        Observation start time local
  -e END, --end END     Observation end time local
  --elev-cutoff ELEV_CUTOFF
                        Elevation cutoff
  --add-to-catalog ADD_TO_CATALOG [ADD_TO_CATALOG ...]
                        Add source to catalog (format e.g.
                        name,f|J,00:00:00.00000,-90:00:00:00000,0.0)
  --solar-separation SOLAR_SEPARATION
                        Minimum solar separation
  --lunar-separation LUNAR_SEPARATION
                        Minimum lunar separation
  --plot-styles PLOT_STYLES [PLOT_STYLES ...]
                        Plot style
  --marker-size MARKER_SIZE
                        Marker size
  --satelite-separation SATELITE_SEPARATION
                        Minimum satelite separation
```
