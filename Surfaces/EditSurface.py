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
from pivy import coin
import os


class AddTriangle:
    Path = os.path.dirname(__file__)

    resources = {
        'Pixmap': Path + '/../Resources/Icons/EditSurface.svg',
        'MenuText': "Add Triangle",
        'ToolTip': "Add a triangle to selected surface."
    }

    def __init__(self):

        "
        Edit Surface
        "

    def GetResources(self):

        # Return the command resources dictionary
        return self.resources

    def activated(self):
        FreeCADGui.runCommand("Mesh_AddFacet")

FreeCADGui.addCommand('Add Triangle', AddTriangle())


class DeleteTriangle:
    Path = os.path.dirname(__file__)

    resources = {
        'Pixmap': Path + '/../Resources/Icons/EditSurface.svg',
        'MenuText': "Delete Triangle",
        'ToolTip': "Delete triangles from selected surface."
    }

    def __init__(self):
        print("Delete Triangle Added")


    def GetResources(self):
        # Return the command resources dictionary
        return self.resources

    @staticmethod
    def activated():
        FreeCADGui.runCommand("Mesh_RemoveComponents")


FreeCADGui.addCommand('Delete Triangle', DeleteTriangle())

class SwapEdge:
    Path = os.path.dirname(__file__)

    resources = {
        'Pixmap': Path + '/../Resources/Icons/EditSurface.svg',
        'MenuText': "Swap Edge",
        'ToolTip': "Swap Edge of selected surface."
    }

    def __init__(self):
        "
        Swap Edge Added
        "

    def GetResources(self):
        # Return the command resources dictionary
        return self.resources

    def Activated(self):
        self.FaceIndexes = []
        self.MC = FreeCADGui.ActiveDocument.ActiveView.addEventCallbackPivy(
            coin.SoMouseButtonEvent.getClassTypeId(), self.SwapEdge)

    def SwapEdge(self, cb):
        event = cb.getEvent()
        if event.getButton() == coin.SoMouseButtonEvent.BUTTON2 and event.getState() == coin.SoMouseButtonEvent.DOWN:
            FreeCADGui.ActiveDocument.ActiveView.removeEventCallbackPivy(
                coin.SoMouseButtonEvent.getClassTypeId(), self.MC)
        if event.getButton() == coin.SoMouseButtonEvent.BUTTON1 and event.getState() == coin.SoMouseButtonEvent.DOWN:
            pp = cb.getPickedPoint()

            if not pp is None:
                detail = pp.getDetail()

                if detail.isOfType(coin.SoFaceDetail.getClassTypeId()):
                    face_detail = coin.cast(
                        detail, str(detail.getTypeId().getName()))
                    index = face_detail.getFaceIndex()
                    self.face_indexes.append(index)

                    if len(self.face_indexes) == 2:
                        surface = FreeCADGui.Selection.getSelection()[-1]
                        copy_mesh = surface.Mesh.copy()

                        try:
                            CopyMesh.swapEdge(
                                self.FaceIndexes[0], self.FaceIndexes[1])

                        except:
                            pass

FreeCADGui.addCommand('Swap Edge', SwapEdge())


class SmoothSurface:
    Path = os.path.dirname(__file__)

    resources = {
        'Pixmap': Path + '/../Resources/Icons/EditSurface.svg',
        'MenuText': "Smooth Surface",
        'ToolTip': "Smooth selected surface."
    }

    def __init__(self):
        "
        Smooth Surface Added
        "


    def GetResources(self):

        # Return the command resources dictionary
        return self.resources

    @staticmethod
    def activated():
        surface = FreeCADGui.Selection.getSelection()[0]
        surface.Mesh.smooth()

FreeCADGui.addCommand('Smooth Surface', SmoothSurface())

