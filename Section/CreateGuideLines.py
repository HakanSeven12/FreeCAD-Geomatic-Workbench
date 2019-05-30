import FreeCAD, FreeCADGui
from PySide import QtCore, QtGui
import Draft
import os

class CreateGuideLines:
    #Command to create guide lines for selected alignment.
    Path = os.path.dirname(__file__)

    Resources = {
        'Pixmap'  : Path + '/../Resources/Icons/CreateSections.svg',
        'MenuText': "Create Guide Lines",
        'ToolTip' : "Create guide lines for selected alignment."
    }

    def __init__(self):
        #Import *.ui file(s)
        self.Path = os.path.dirname(os.path.abspath(__file__))
        self.IPFui = FreeCADGui.PySideUic.loadUi(self.Path + "/CreateGuideLines.ui")
        self.CPGui = FreeCADGui.PySideUic.loadUi(self.Path + "/CreateGuideLinesGroup.ui")

        #To Do List
        self.IPFui.CreateB.clicked.connect(self.CreateGuideLines)
        self.IPFui.CancelB.clicked.connect(self.IPFui.close)
        self.IPFui.AddGLGroupB.clicked.connect(self.LoadCGLGui)
        self.CPGui.OkB.clicked.connect(self.CreateNewGroup)
        self.CPGui.CancelB.clicked.connect(self.CPGui.close)
        self.IPFui.AlignmentCB.currentIndexChanged.connect(self.ListGuideLinesGroups)

    def GetResources(self):
        #Return the command resources dictionary
        return self.Resources

    def Activated(self):
        try:
            self.GuideLineGroup = FreeCAD.ActiveDocument.Guide_Lines
        except:
            self.GuideLineGroup = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",'Guide_Lines')
            self.GuideLineGroup.Label = "Guide Lines"
            FreeCAD.ActiveDocument.Alignments.addObject(self.GuideLineGroup)

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

        self.ListGuideLinesGroups()

    def ListGuideLinesGroups(self):
        #List Guide Lines Groups.
        self.IPFui.GLGroupCB.clear()
        GuideLinesGroup = FreeCAD.ActiveDocument.Guide_Lines.Group
        self.GLGList = []

        for Object in GuideLinesGroup:
            if Object.TypeId == 'App::DocumentObjectGroup':
                self.GLGList.append(Object.Name)
                self.IPFui.GLGroupCB.addItem(Object.Label)

    def LoadCGLGui(self):
        #Load Create Guide Lines Group UI.
        self.CPGui.setParent(self.IPFui)
        self.CPGui.setWindowFlags(QtCore.Qt.Window)
        self.CPGui.show()

    def CreateNewGroup(self):
        #Create new guide lines group.
        NewGroupName = self.CPGui.GuideLinesGroupNameLE.text()
        NewGroup = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",NewGroupName)
        NewGroup.Label = NewGroupName
        FreeCAD.ActiveDocument.Guide_Lines.addObject(NewGroup)
        self.IPFui.GLGroupCB.addItem(NewGroupName)
        self.GLGList.append(NewGroup.Name)
        NewGroup.Label = NewGroupName
        self.CPGui.close()

    def CreateGuideLines(self):
        L = self.IPFui.LeftLengthLE.text()
        R = self.IPFui.RightLengthLE.text()
        AlignmentIndex = self.IPFui.AlignmentCB.currentIndex()
        AlignmentName = self.AlignmentList[AlignmentIndex]
        GLGIndex = self.IPFui.GLGroupCB.currentIndex()
        GLGIndexName = self.GLGList[GLGIndex]
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
            FreeCAD.ActiveDocument.getObject(GLGIndexName).addObject(GuideLine)
            FreeCAD.ActiveDocument.recompute()

FreeCADGui.addCommand('Create Guide Lines',CreateGuideLines())