# FreeCAD Geomatics Workbench
This workbench is being developed to provide functionality specific to Geomatics/Survey engineering.

## Functions
* Import Point Files  
* Export Points  
* Create Surface  
* Edit Surface  
* Create Contours  
* Create Guide Lines  
* Create Sections (WIP)

## Requirements
* FreeCAD >= v0.19  
* python >= v3.6  
* scipy >= v1.2.1

## Installation

### Manual Installation
There are two methods to install manually:  
* **First Method:** Download the ZIP file of this repo from Github and extract into the `~/.FreeCAD/Mod/` directory.  

* **Second Method:** *(preferred)* Using `git clone` you clone the repo in to `~/.FreeCAD/Mod/` directory.  
  `cd ~/.FreeCAD/Mod; git clone https://github.com/HakanSeven12/FreeCAD-Geomatics-Workbench`  
  **Note:** to stay up to date with the development of this repo:  
  `cd ~/.FreeCAD/Mod/FreeCAD-Geomatics-Workbench; git fetch`

* Go to **Edit** :arrow_forward: **Preferences** :arrow_forward: **General** :arrow_forward: **Units**  
  * Set `Number of decimals = 6`.  

* Go to **Edit** :arrow_forward: **Preferences** :arrow_forward: **General** :arrow_forward: **Document**  
  * Check `Allow duplicate object labels in one document`.  

* Restart FreeCAD

## Feedback 
Discuss this Workbench on the FreeCAD forum thread dedicated to this topic: 
[Geomatics Workbench](https://forum.freecadweb.org/viewtopic.php?f=8&t=34371).

## Developer 
Hakan Seven with inspiration and help from the FreeCAD community.

## Screenshots

![IPF](https://user-images.githubusercontent.com/3831435/57193645-0d1e6380-6f46-11e9-8f5a-8f9a5c66435b.png)
![EP](https://user-images.githubusercontent.com/3831435/57193646-0d1e6380-6f46-11e9-94d4-4f57023e2791.png)
![CS](https://user-images.githubusercontent.com/3831435/57193647-0db6fa00-6f46-11e9-92bf-0709ddb9cffb.png)
![ES](https://user-images.githubusercontent.com/3831435/57193648-0db6fa00-6f46-11e9-985d-d9376269be28.png)
![CC](https://user-images.githubusercontent.com/3831435/58474068-e3c2b300-8152-11e9-8681-d4fe065150ec.png)
![CGL](https://user-images.githubusercontent.com/3831435/58638005-76eb1c80-82fc-11e9-83bd-49dbb06d9202.png)

## License
Copyright (c) 2019 Hakan Seven <hakanseven12@gmail.com>

This program is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License (LGPL) as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version. For detail see the LICENCE text file.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Library General Public License for more details.

License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
