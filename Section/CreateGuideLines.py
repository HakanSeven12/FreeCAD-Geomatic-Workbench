import FreeCAD, FreeCADGui
from PySide import QtCore, QtGui
import Draft
import os

class CreateGuideLines:

    def __init__(self):
        #Import *.ui file(s)
        self.Path = os.path.dirname(os.path.abspath(__file__))
        self.IPFui = FreeCADGui.PySideUic.loadUi(self.Path + "/CreateGuideLines.ui")

        #To Do List
        self.IPFui.CreateB.clicked.connect(self.CreateGuideLines)
        self.IPFui.CancelB.clicked.connect(self.IPFui.close)
        #self.IPFui.CreateGroupChB.stateChanged.connect(self.CreateNewGroup)
        #self.IPFui.AlignmentCB.currentIndexChanged.connect(self.ListGuideLinesGroups)

    def GetResources(self):
        return {'MenuText': 'Create Guide Lines', 'ToolTip': 'Create guide lines for sections.'}

    def Activated(self):
        try:
            self.GuideLineGroup = FreeCAD.ActiveDocument.Guide_Lines
        except:
            self.GuideLineGroup = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",'Guide_Lines')
            self.GuideLineGroup.Label = "Guide Lines"

        self.IPFui.setParent(FreeCADGui.getMainWindow())
        self.IPFui.setWindowFlags(QtCore.Qt.Window)
        self.IPFui.show()

        #List Alignments.
        self.IPFui.AlignmentCB.clear()
        AlignmentGroup = FreeCAD.ActiveDocument.Alignments.Group
        self.AlignmentList = []

        for Object in AlignmentGroup:
            if Object.TypeId == 'Part::Part2DObjectPython':
                self.AlignmentList.append(Object.Name)
                self.IPFui.AlignmentCB.addItem(Object.Label)

    def CreateGuideLines(self):
        L = self.IPFui.LeftLengthLE.text()
        R = self.IPFui.RightLengthLE.text()
        Index = self.IPFui.AlignmentCB.currentIndex()
        AlignmentName = self.AlignmentList[Index]
        Alignment = FreeCAD.ActiveDocument.getObject(AlignmentName)
        TangentIncrement = self.IPFui.TIncrementLE.text()
        CurveSpiralIncrement = self.IPFui.CSIncrementLE.text()
        Pl = Alignment.Placement.Base

        Stations = []
        Start = Alignment.Proxy.model.data['meta']['StartStation']
        Length = Alignment.Proxy.model.data['meta']['Length']
        End = Start + Length/1000

        Geometry = Alignment.Proxy.model.data['geometry']
        for Geo in Geometry:
            StartStation = Geo.get('StartStation')
            EndStation = Geo.get('StartStation')+Geo.get('Length')/1000
            if StartStation != 0: Stations.append(StartStation)

            if Geo.get('Type') == 'Line':
                for i in range(round(float(StartStation)), round(float(EndStation))):
                    if i % int(TangentIncrement) == 0:
                        Stations.append(i)

            elif Geo.get('Type') == 'Curve' or Geo["Type"] == 'Spiral':
                for i in range(round(float(StartStation)), round(float(EndStation))):
                    if i % int(CurveSpiralIncrement) == 0:
                        Stations.append(i)
        Stations.append(round(End,3))
        Stations.sort()

        for Station in Stations:
            Coord, vec = Alignment.Proxy.model.get_orthogonal( Station, "Left")
            LeftEnd = Coord.add(FreeCAD.Vector(vec).multiply(int(L)*1000))
            RightEnd = Coord.add(vec.negative().multiply(int(R)*1000))

            GuideLine = Draft.makeWire([LeftEnd,Coord,RightEnd])
            GuideLine.Placement.move(Pl)
            GuideLine.Label = str(round(Station,3))
            self.GuideLineGroup.addObject(GuideLine)
            FreeCAD.ActiveDocument.recompute()

FreeCADGui.addCommand('Create Guide Lines',CreateGuideLines())