#***************************************************************************
#*   (c) Hakan Seven (hakanseven12@gmail.com) 2019                         *
#*                                                                         *
#*   This file is part of the FreeCAD CAx development system.              *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   FreeCAD is distributed in the hope that it will be useful,            *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Lesser General Public License for more details.                   *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with FreeCAD; if not, write to the Free Software        *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *                                                  *
#***************************************************************************/



class GeomaticWorkbench ( Workbench ):
    "Geomatic workbench object"
    def __init__(self):
        #self.__class__.Icon = FreeCAD.getHomePath() + "Mod/Geomatic/Resources/icons/GeomaticWorkbench.svg"
        self.__class__.MenuText = "Geomatic"
        self.__class__.ToolTip = "Geomatic"

    def Initialize(self): #This function is executed when FreeCAD starts
        import ImportPointFile
        import CreateSurface
        import EditSurface
        import CreateGuideLines

        #Create Point Toolbar
        list = ['Import Point File']
        self.appendToolbar("Point Tools",list)

        #Create Surface Toolbar
        list = ['Create Surface','Edit Surface']
        self.appendToolbar("Surface Tools",list)

        #Create Section Toolbar
        list = ['Create Guide Lines']
        self.appendToolbar("Section Tools",list)

        #Create Menu
        #menu = ["Test &Commands","TestToolsGui"]
        #list = ["Std_TestQM","Std_TestReloadQM","Test_Test","Test_TestAll","Test_TestDoc","Test_TestBase"]
        #self.appendCommandbar("TestToolsGui",list)
        #self.appendMenu(menu,list)

    def Activated(self):
        #This function is executed when the workbench is activated

        #Create Point Groups
        try:
            App.ActiveDocument.Point_Groups
        except:
            PointGroups = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",'Point_Groups')
            PointGroups.Label = "Point Groups"

        try:
            App.ActiveDocument.All_Points
        except:
            SubGroup = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",'All_Points')
            SubGroup.Label = "All Points"
            FreeCAD.ActiveDocument.Point_Groups.addObject(SubGroup)

        #Create Surfaces Group
        try:
            App.ActiveDocument.Surfaces
        except:
            FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",'Surfaces')

        #Create Alignments Group
        try:
            App.ActiveDocument.Alignments
        except:
            FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",'Alignments')

        return

Gui.addWorkbench(GeomaticWorkbench())

