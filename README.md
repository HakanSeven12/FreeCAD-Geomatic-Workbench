# GEOMATICS WORKBENCH WAS MERGED WITH TRAILS WORKBENCH THIS REPOSITORY DEVELOPMENT WAS STOPPED. NEW REPOSITORY: https://github.com/HakanSeven12/freecad.trails

# FreeCAD Geomatics Workbench
This workbench is being developed to provide functionality specific to Geomatics/Survey engineering.

## Functions
* Import Point Files  
* Export Points  
* GeoDataWB Tools
* Create Surface  
* Edit Surface  
* Create Contours  
* Create Guide Lines  (only for line segments)
* Create Sections (WIP, need version >= 0.19)

## Requirements
* FreeCAD 0.18  
* Python 3.6  
### For Surface creation 
* numpy
### For GeoDataWB 
* cv2
* gdal
* gdalconst
* requests (urllib3, chardet, certifi, idna)

## Installation
* Open **Tools** :arrow_forward: **Addon Manager**.

* Select **Geomatics** and click `Install/update selected`.  

* Go to **Edit** :arrow_forward: **Preferences** :arrow_forward: **General** :arrow_forward: **Document**  
  * Check `Allow duplicate object labels in one document`.  

* Restart FreeCAD.

## Feedback 
Discuss this Workbench on the FreeCAD forum thread dedicated to this topic: 
[Geomatics Workbench](https://forum.freecadweb.org/viewtopic.php?f=8&t=34371).

Or submit/comment issues on [github issues tracker](https://github.com/HakanSeven12/FreeCAD-Geomatics-Workbench/issues)

## Developer 
Hakan Seven with inspiration and help from the FreeCAD community.

## Long term vision 
For a long term vision and a list of desired features see the [TODO file](https://github.com/HakanSeven12/FreeCAD-Geomatics-Workbench/blob/master/TODO.md)

## Usage & Screenshots
![IPF](https://user-images.githubusercontent.com/3831435/59975941-f9e35800-95c6-11e9-9afc-05f5a5d0bf2d.gif)
![EP](https://user-images.githubusercontent.com/3831435/59975942-f9e35800-95c6-11e9-995d-4263f34f6f87.gif)
![CS](https://user-images.githubusercontent.com/3831435/59975943-f9e35800-95c6-11e9-99d3-65282669817b.gif)
![ES](https://user-images.githubusercontent.com/3831435/59975944-fa7bee80-95c6-11e9-8b47-a2f583fa25a6.gif)
![CC](https://user-images.githubusercontent.com/3831435/59975946-fa7bee80-95c6-11e9-8e2f-7bdffac13d01.gif)
![CGL](https://user-images.githubusercontent.com/3831435/58638005-76eb1c80-82fc-11e9-83bd-49dbb06d9202.png)
![GeoData](https://user-images.githubusercontent.com/3831435/59973802-212d2b80-95ad-11e9-919f-8cf3f75cb375.png)
![OSM](https://user-images.githubusercontent.com/3831435/59843173-ad96de80-9360-11e9-9c6a-153449516a7f.png)
![Surface](https://user-images.githubusercontent.com/3831435/59920075-fff40000-9431-11e9-8411-b13032364f28.gif)

## License
Copyright (c) 2019 Hakan Seven <hakanseven12@gmail.com>

This program is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License (LGPL) as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version. For detail see the LICENCE text file.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Library General Public License for more details.

License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
