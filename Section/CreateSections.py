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

import FreeCAD
import FreeCADGui
from PySide import QtCore, QtGui
import MeshPart
import Draft
import os


class CreateGuideLines:
    # Command to create sections for every selected surfaces.
    Path = os.path.dirname(__file__)

    Resources = {
        'Pixmap': Path + '/../Resources/Icons/CreateSections.svg',
        'MenuText': "Export Points",
        'ToolTip': "Export points to point file."
    }

    def __init__(self):
        # Import *.ui file(s)
        self.IPFui = FreeCADGui.PySideUic.loadUi(
            self.Path + "/CreateSections.ui")

        # To Do List
        self.IPFui.CreateB.clicked.connect(self.CreateSections)
        self.IPFui.CancelB.clicked.connect(self.IPFui.close)

    def GetResources(self):
        # Return the command resources dictionary
        return self.Resources

    def activated(self):
        self.IPFui.setParent(FreeCADGui.getMainWindow())
        self.IPFui.setWindowFlags(QtCore.Qt.Window)
        self.IPFui.show()

    def CreateSections(self):
        GuideLinesGroup = FreeCAD.ActiveDocument.Test.Group
        SectionGroup = FreeCAD.ActiveDocument.Group
        CopyMesh = FreeCAD.ActiveDocument.Surface.Mesh.copy()
        Base = CopyMesh.Placement.Base
        CopyMesh.Placement.move(Base.negative())

        for Wire in GuideLinesGroup:
            CopyShape = Wire.Shape.copy()
            CopyShape.Placement.move(Base.negative())

            Param1 = MeshPart.findSectionParameters(
                CopyShape.Edge1, CopyMesh, FreeCAD.Vector(0, 0, 1))
            Param1.insert(0, CopyShape.Edge1.FirstParameter+1)
            Param1.append(CopyShape.Edge1.LastParameter-1)

            Param2 = MeshPart.findSectionParameters(
                CopyShape.Edge2, CopyMesh, FreeCAD.Vector(0, 0, 1))
            Param2.insert(0, CopyShape.Edge2.FirstParameter+1)
            Param2.append(CopyShape.Edge2.LastParameter-1)

            Points1 = [CopyShape.Edge1.valueAt(i) for i in Param1]
            Points2 = [CopyShape.Edge2.valueAt(i) for i in Param2]

            Section = MeshPart.projectPointsOnMesh(
                Points1+Points2, CopyMesh, FreeCAD.Vector(0, 0, 1))
            Pwire = Draft.makeWire(Section)
            Pwire.Placement.move(Base)
            SectionGroup.addObject(Pwire)

        FreeCAD.ActiveDocument.recompute()


FreeCADGui.addCommand('Create Guide Lines', CreateGuideLines())
