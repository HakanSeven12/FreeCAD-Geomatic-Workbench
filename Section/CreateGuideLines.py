# /**********************************************************************
# *                                                                     *
# * Copyright (c) 2019 Hakan Seven <hakanseven12@gmail.com>             *
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
import math
import FreeCAD
import FreeCADGui
import Draft
from FreeCAD import Vector
from PySide import QtCore, QtGui


class CreateGuideLines:

    def __init__(self):

            # Command to create guide lines for selected alignment.
        self.Path = os.path.dirname(__file__)

        self.resources = {
            'Pixmap': self.Path + '/../Resources/Icons/CreateGuideLines.svg',
            'MenuText': "Create Guide Lines",
            'ToolTip': "Create guide lines for selected alignment"
                    }

        self.IPFui = FreeCADGui.PySideUic.loadUi(
            self.Path + "/CreateGuideLines.ui")
        self.CPGui = FreeCADGui.PySideUic.loadUi(
            self.Path + "/CreateGuideLinesGroup.ui")

        # To Do List
        self.IPFui.CreateB.clicked.connect(self.CreateGuideLines)
        self.IPFui.CancelB.clicked.connect(self.IPFui.close)
        self.IPFui.AddGLGroupB.clicked.connect(self.LoadCGLGui)
        self.CPGui.OkB.clicked.connect(self.CreateNewGroup)
        self.CPGui.CancelB.clicked.connect(self.CPGui.close)
        self.IPFui.AlignmentCB.currentIndexChanged.connect(
            self.ListGuideLinesGroups)
        self.IPFui.FromAlgStartChB.stateChanged.connect(self.ActivateStations)
        self.IPFui.ToAlgEndChB.stateChanged.connect(self.ActivateStations)

    def GetResources(self):
        # Return the command resources dictionary
        return self.resources

    def IsActive(self):
        if FreeCAD.ActiveDocument is None:
            return False
        return True

    def Activated(self):
        try:
            self.GuideLineGroup = FreeCAD.ActiveDocument.Alignments
        except:
            self.GuideLineGroup = FreeCAD.ActiveDocument.addObject(
                "App::DocumentObjectGroup", 'Alignments')
            self.GuideLineGroup.Label = "Alignments"

        try:
            self.GuideLineGroup = FreeCAD.ActiveDocument.GuideLines
        except:
            self.GuideLineGroup = FreeCAD.ActiveDocument.addObject(
                "App::DocumentObjectGroup", 'GuideLines')
            self.GuideLineGroup.Label = "Guide Lines"

        FreeCAD.ActiveDocument.Alignments.addObject(self.GuideLineGroup)

        self.IPFui.setParent(FreeCADGui.getMainWindow())
        self.IPFui.setWindowFlags(QtCore.Qt.Window)
        self.IPFui.show()

        # List Alignments.
        self.IPFui.AlignmentCB.clear()
        alignment_group = FreeCAD.ActiveDocument.Alignments.Group
        self.alignment_list = []

        for Object in alignment_group:
            if Object.TypeId == 'Part::Part2DObjectPython':
                self.alignment_list.append(Object.Name)
                self.IPFui.AlignmentCB.addItem(Object.Label)

        # Check that the Alignments Group has Wire objects
        if len(self.alignment_list) == 0:
            FreeCAD.Console.PrintMessage(
                "Please add a Wire Object to the Alignment Group")
            return

        self.ListGuideLinesGroups()

    def getAlignmentInfos(self):
        alignment_index = self.IPFui.AlignmentCB.currentIndex()

        if alignment_index < 0:
            FreeCAD.Console.PrintMessage(
                "Please add a Wire object to the Alignment Group")
            return None, 0.0, 0.0

        alignment_name = self.alignment_list[alignment_index]

        Alignment = FreeCAD.ActiveDocument.getObject(alignment_name)
        # # At this point the WorkBench make use of an unregistred WB
        # # freecad.trails
        # Start = Alignment.Proxy.model.data['meta']['StartStation']
        # Length = Alignment.Proxy.model.data['meta']['Length']
        # End = Start + Length/1000

        # Workaround to make it work
        Start = 0.0
        Length = Alignment.Length.Value
        End = Start + Length

        return Alignment, Start, End

    def ListGuideLinesGroups(self):

        # List Guide Lines Groups.
        self.IPFui.GLGroupCB.clear()
        GuideLines_group = FreeCAD.ActiveDocument.GuideLines.Group
        self.GLGList = []

        for Object in GuideLines_group:
            if Object.TypeId == 'App::DocumentObjectGroup':
                self.GLGList.append(Object.Name)
                self.IPFui.GLGroupCB.addItem(Object.Label)

        Alignment, Start, End = self.getAlignmentInfos()

        self.IPFui.StartStationLE.setText(str(round(Start, 3)))
        self.IPFui.EndStationLE.setText(str(round(End, 3)))

    def LoadCGLGui(self):

        # Load Create Guide Lines Group UI.
        self.CPGui.setParent(self.IPFui)
        self.CPGui.setWindowFlags(QtCore.Qt.Window)
        self.CPGui.show()

    def CreateNewGroup(self):
        # Create new guide lines group.
        NewGroupName = self.CPGui.GuideLinesGroupNameLE.text()
        NewGroup = FreeCAD.ActiveDocument.addObject(
            "App::DocumentObjectGroup", NewGroupName)
        NewGroup.Label = NewGroupName
        FreeCAD.ActiveDocument.GuideLines.addObject(NewGroup)
        self.IPFui.GLGroupCB.addItem(NewGroupName)
        self.GLGList.append(NewGroup.Name)
        NewGroup.Label = NewGroupName
        self.CPGui.close()

    def ActivateStations(self):
        # When QCheckBox status changed do the following options.
        Alignment, Start, End = self.getAlignmentInfos()
        if self.IPFui.FromAlgStartChB.isChecked():
            self.IPFui.StartStationLE.setEnabled(False)
            self.IPFui.StartStationLE.setText(str(round(Start, 3)))
        else:
            self.IPFui.StartStationLE.setEnabled(True)

        if self.IPFui.ToAlgEndChB.isChecked():
            self.IPFui.EndStationLE.setEnabled(False)
            self.IPFui.EndStationLE.setText(str(round(End, 3)))
        else:
            self.IPFui.EndStationLE.setEnabled(True)

    def GetOrthoVector(self, line, distance, side=''):
        """
        Return the orthogonal vector pointing toward the indicated side at the
        provided position.  Defaults to left-hand side
        """

        _dir = 1.0

        _side = side.lower()

        if _side in ['r', 'rt', 'right']:
            _dir = -1.0

        start = line.Start
        end = line.End

        if (start is None) or (end is None):
            return None, None

        _delta = end.sub(start).normalize()
        _left = Vector(-_delta.y, _delta.x, 0.0)

        _coord = start.add(_delta.multiply(distance))

        return _coord, _left.multiply(_dir)

    def CreateGuideLines(self):
        l = self.IPFui.LeftLengthLE.text()
        r = self.IPFui.RightLengthLE.text()
        FirstStation = self.IPFui.StartStationLE.text()
        LastStation = self.IPFui.EndStationLE.text()
        glg_index = self.IPFui.GLGroupCB.currentIndex()

        if glg_index < 0:
            FreeCAD.Console.PrintMessage(
                "Please add a Guide Line Group")
            return

        GLGIndexName = self.GLGList[glg_index]
        tangent_increment = self.IPFui.TIncrementLE.text()
        CurveSpiralIncrement = self.IPFui.CSIncrementLE.text()

        Alignment, Start, End = self.getAlignmentInfos()

        if Alignment is None :
            FreeCAD.Console.PrintMessage(
                "Please add a Wire object to the Alignment Group")
            return

        Stations = []

        StartStation = Start
        EndStation = End
        if StartStation != 0:
            if self.IPFui.HorGeoPointsChB.isChecked():
                Stations.append(StartStation)

        for i in range(int(float(StartStation)), int(float(EndStation))):
            if i % int(tangent_increment) == 0:
                Stations.append(i)

        Stations.append(round(End, 3))

        Result = []
        for Station in Stations:
            if float(FirstStation) <= Station <= float(LastStation):
                Result.append(Station)
        Result.sort()

        for Station in Result:
            Coord, vec = self.GetOrthoVector(Alignment, Station, "Left")
            LeftEnd = Coord.add(FreeCAD.Vector(vec).multiply(int(l)))
            RightEnd = Coord.add(vec.negative().multiply(int(r)))

            GuideLine = Draft.makeWire([LeftEnd, Coord, RightEnd])
            GuideLine.Label = str(round(Station, 3))
            FreeCAD.ActiveDocument.getObject(GLGIndexName).addObject(GuideLine)
            FreeCAD.ActiveDocument.recompute()


FreeCADGui.addCommand('Create Guide Lines', CreateGuideLines())
