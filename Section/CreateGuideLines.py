import FreeCAD, FreeCADGui
from PySide import QtCore, QtGui
import Draft
import os


class CreateGuideLines:
    # Command to create guide lines for selected alignment.
    Path = os.path.dirname(__file__)

    Resources = {
        'Pixmap': Path + '/../Resources/Icons/create_sections.svg',
        'MenuText': "Create Guide Lines",
        'ToolTip': "Create guide lines for selected alignment."
    }

    def __init__(self):
        # Import *.ui file(s)
        self.Path = os.path.dirname(os.path.abspath(__file__))
        self.IPFui = FreeCADGui.PySideUic.loadUi(self.Path + "/create_guide_lines.ui")
        self.CPGui = FreeCADGui.PySideUic.loadUi(self.Path + "/CreateGuideLinesGroup.ui")

        # todo :
        self.IPFui.CreateB.clicked.connect(self.create_guide_lines)
        self.IPFui.CancelB.clicked.connect(self.IPFui.close)
        self.IPFui.AddGLGroupB.clicked.connect(self.load_cgl_gui)
        self.CPGui.OkB.clicked.connect(self.create_new_group)
        self.CPGui.CancelB.clicked.connect(self.CPGui.close)
        self.IPFui.AlignmentCB.currentIndexChanged.connect(self.list_guide_lines_groups)
        self.IPFui.FromAlgStartChB.stateChanged.connect(self.activate_stations)
        self.IPFui.ToAlgEndChB.stateChanged.connect(self.activate_stations)

    def get_resources(self):
        # Return the command resources dictionary
        return self.Resources

    def activated(self):
        try:
            self.GuideLineGroup = FreeCAD.ActiveDocument.Guide_Lines
        except:
            self.GuideLineGroup = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",'Guide_Lines')
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

        self.list_guide_lines_groups()

    def get_alignment_info(self):
        alignment_index = self.IPFui.AlignmentCB.currentIndex()
        alignment_name = self.alignment_list[alignment_index]

        Alignment = FreeCAD.ActiveDocument.getObject(alignment_name)
        Start = Alignment.Proxy.model.data['meta']['StartStation']
        Length = Alignment.Proxy.model.data['meta']['Length']
        End = Start + Length/1000

        return Alignment, Start, End

    def list_guide_lines_groups(self):
        # List Guide Lines Groups.
        self.IPFui.GLGroupCB.clear()
        guide_lines_group = FreeCAD.ActiveDocument.Guide_Lines.Group
        self.GLGList = []

        for Object in guide_lines_group:
            if Object.TypeId == 'App::DocumentObjectGroup':
                self.GLGList.append(Object.Name)
                self.IPFui.GLGroupCB.addItem(Object.Label)
        alignment, start, end = self.get_alignment_info()

        self.IPFui.StartStationLE.setText(str(round(start, 3)))
        self.IPFui.EndStationLE.setText(str(round(end, 3)))

    def load_cgl_gui(self):
        # Load Create Guide Lines Group UI.
        self.CPGui.setParent(self.IPFui)
        self.CPGui.setWindowFlags(QtCore.Qt.Window)
        self.CPGui.show()

    def create_new_group(self):
        # Create new guide lines group.
        new_group_name = self.CPGui.GuideLinesGroupNameLE.text()
        new_group = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup",new_group_name)
        new_group.Label = new_group_name
        FreeCAD.ActiveDocument.Guide_Lines.addObject(new_group)
        self.IPFui.GLGroupCB.addItem(new_group_name)
        self.GLGList.append(new_group.Name)
        new_group.Label = new_group_name
        self.CPGui.close()

    def activate_stations(self):
        # When QCheckBox status changed do the following options.
        alignment, start, end = self.get_alignment_info()
        if self.IPFui.FromAlgStartChB.isChecked():
            self.IPFui.StartStationLE.setEnabled(False)
            self.IPFui.StartStationLE.setText(str(round(start,3)))
        else:
            self.IPFui.StartStationLE.setEnabled(True)

        if self.IPFui.ToAlgEndChB.isChecked():
            self.IPFui.EndStationLE.setEnabled(False)
            self.IPFui.EndStationLE.setText(str(round(end, 3)))
        else:
            self.IPFui.EndStationLE.setEnabled(True)

    def create_guide_lines(self):
        l = self.IPFui.LeftLengthLE.text()
        r = self.IPFui.RightLengthLE.text()
        first_station = self.IPFui.StartStationLE.text()
        last_station = self.IPFui.EndStationLE.text()
        glg_index = self.IPFui.GLGroupCB.currentIndex()
        glg_index_name = self.GLGList[glg_index]
        tangent_increment = self.IPFui.TIncrementLE.text()
        curve_spiral_increment = self.IPFui.CSIncrementLE.text()

        alignment, start, end = self.get_alignment_info()
        pl = alignment.Placement.Base

        stations = []
        geometry = alignment.Proxy.model.data['geometry']
        for Geo in geometry:
            start_station = Geo.get('StartStation')
            end_station = Geo.get('StartStation')+Geo.get('Length')/1000
            if start_station != 0:
                if self.IPFui.HorGeoPointsChB.isChecked():
                    stations.append(start_station)

            if Geo.get('Type') == 'Line':
                for i in range(round(float(start_station)), round(float(end_station))):
                    if i % int(tangent_increment) == 0:
                        stations.append(i)

            elif Geo.get('Type') == 'Curve' or Geo["Type"] == 'Spiral':
                for i in range(round(float(start_station)), round(float(end_station))):
                    if i % int(curve_spiral_increment) == 0:
                        stations.append(i)
        stations.append(round(end,3))

        result = []
        for Station in stations:
            if float(first_station) <= Station <= float(last_station):
                result.append(Station)
        result.sort()

        for Station in result:
            coord, vec = alignment.Proxy.model.get_orthogonal( Station, "Left")
            left_end = coord.add(FreeCAD.Vector(vec).multiply(int(l)*1000))
            right_end = coord.add(vec.negative().multiply(int(r)*1000))

            guide_line = Draft.makeWire([left_end,coord,right_end])
            guide_line.Placement.move(pl)
            guide_line.Label = str(round(Station,3))
            FreeCAD.ActiveDocument.getObject(glg_index_name).addObject(guide_line)
            FreeCAD.ActiveDocument.recompute()


FreeCADGui.addCommand('Create Guide Lines',CreateGuideLines())