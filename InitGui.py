# /**********************************************************************
# *                                                                     *
# * Copyright (c) 2019 Hakan Seven <hakanseven12@gmail.com>             *
# *                    BENAHMED DAHO Ali <bidandou@yahoo.fr>            *
# *                                                                     *
# * This program is free software; you can redistribute it and/or modify*
# * it under the terms of the GNU Lesser General Public License (LGPL)  *
# * as published by the Free Software Foundation; either version 2 of   *
# * the License, or (at your option) any later version.                 *
# * for detail see the LICENCE text file.                               *
# *                                                                     *
# * This program is distributed in the hope that it will be useful,     *
# * but WITHOUT ANY WARRANTY; without even the implied warranty of      *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the       *
# * GNU Library General Public License for more details.                *
# *                                                                     *
# * You should have received a copy of the GNU Library General Public   *
# * License along with this program; if not, write to the Free Software *
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307*
# * USA                                                                 *
# *                                                                     *
# ***********************************************************************

import os

import GeoData
from Data import ImportPointFile, ExportPoints
from Surfaces import CreateSurface, EditSurface, Contours
from Section import CreateGuideLines


class GeomaticsCommandGroup:
    def __init__(self, cmdlist, menu, TypeId=None, tooltip=None):
        self.cmdlist = cmdlist
        self.menu = menu
        self.TypeId = TypeId
        if tooltip is None:
            self.tooltip = menu
        else:
            self.tooltip = tooltip

    def GetCommands(self):
        return tuple(self.cmdlist)

    def GetResources(self):
        return {'MenuText': self.menu, 'ToolTip': self.tooltip}

    def IsActive(self):
        if self.TypeId is not None:
            if FreeCADGui.Selection.getSelection() is not None:
                Selection = FreeCADGui.Selection.getSelection()[-1]
                if Selection.TypeId == self.TypeId:
                    return True
            return False
        return True


class GeomaticsWorkbench (Gui.Workbench):
    "Geomatics Workbench Object"
    MenuText = 'Geomatics (Alpha)'
    ToolTip = 'Geomatics/Survey Engineering Workbench'
    Icon = FreeCAD.getUserAppDataDir() + \
      "Mod/FreeCAD-Geomatics-Workbench/Resources/Icons/GeomaticsWorkbench.svg"

    def __init__(self):

        self.menu = 1
        self.toolbar = 2
        self.context = 4

        self.command_ui = {

            'Data Tools': {
                'gui': self.menu + self.toolbar,
                'cmd': ['Import Point File',
                        'Export Points',
                        'GeoData Tools'
                        ]
            },

            'Surface Tools': {
                'gui': self.menu + self.toolbar + self.context,
                'cmd': ['Create Surface',
                        'Surface Editor',
                        'Create Contour'
                        ]
            },

            'Section Tools': {
                'gui': self.menu + self.toolbar,
                'cmd': ['Create Guide Lines']
            },

            'Draft Tools': {
                'gui': self.toolbar,
                'cmd': ['Draw Tools',
                        'Edit Tools',
                        ]
            },
        }

    def Initialize(self):
        global GeomaticsCommandGroup

        for _k, _v in self.command_ui.items():

            if _v['gui'] & self.toolbar:
                self.appendToolbar(_k, _v['cmd'])

            if _v['gui'] & self.menu:
                self.appendMenu(_k, _v['cmd'])

    EditSurfaceSub = ['Add Triangle', 'Delete Triangle', 'Swap Edge', 
                      'Smooth Surface']
    Gui.addCommand('Surface Editor',
                   GeomaticsCommandGroup(EditSurfaceSub,
                                         'Edit selected surface.',
                                         TypeId='Mesh::Feature'))

    DraftDraw = ["Draft_Line", "Draft_Wire", "Draft_Circle", "Draft_Arc",
                 "Draft_Ellipse", "Draft_Polygon", "Draft_Rectangle",
                 "Draft_Text", "Draft_Dimension", "Draft_BSpline",
                 "Draft_Point", "Draft_ShapeString", "Draft_Facebinder",
                 "Draft_BezCurve", "Draft_Label"
                 ]
    Gui.addCommand('Draw Tools',
                   GeomaticsCommandGroup(DraftDraw, 'Draft Draw Tools'))

    DraftEdit = ["Draft_Move", "Draft_Rotate", "Draft_Offset",
                 "Draft_Trimex", "Draft_Join", "Draft_Split", "Draft_Upgrade",
                 "Draft_Downgrade", "Draft_Scale", "Draft_Edit", 
                 "Draft_WireToBSpline", "Draft_AddPoint", "Draft_DelPoint", 
                 "Draft_Shape2DView", "Draft_Draft2Sketch", "Draft_Array", 
                 "Draft_PathArray", "Draft_PointArray", "Draft_Clone",
                 "Draft_Drawing", "Draft_Mirror", "Draft_Stretch"
                 ]

    Gui.addCommand('Edit Tools', 
                   GeomaticsCommandGroup(DraftEdit, 'Draft Snap Tools'))

    GeoData = ['Import OSM Map', 'Import CSV', 'Import GPX', 'Import Heights',
               'Import SRTM', 'Import XYZ', 'Import LatLonZ',  'Import Image', 
               'Import ASTER', 'Import LIDAR', 'Create House', 'Navigator',
               'ElevationGrid', 'Import EMIR',
               ]

    Gui.addCommand('GeoData Tools', 
                   GeomaticsCommandGroup(GeoData, 'GeoData WB Tools'))

    def ContextMenu(self, recipient):
        """
        Right-click menu options
        """
        #  "recipient" will be either "view" or "tree"

        for _k, _v in self.fn.items():
            if _v['gui'] & self.context:
                self.appendContextMenu(_k, _v['cmds'])

    def GetClassName(self):

        return 'Gui::PythonWorkbench'

    def Activated(self):
        """
        Called when switching to this workbench
        """
        pass

    def Deactivated(self):
        """
        Called when switiching away from this workbench
        """
        pass

Gui.addWorkbench(GeomaticsWorkbench())
