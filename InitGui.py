from Data import ImportPointFile
from Data import ExportPoints
from Surfaces import CreateSurface
from Surfaces import EditSurface
from Surfaces import Contours
from Section import CreateGuideLines

class GeomaticsCommandGroup:
    def __init__(self, cmdlist, menu, TypeId = None, tooltip = None):
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
        return { 'MenuText': self.menu, 'ToolTip': self.tooltip }

    def IsActive(self):
        if self.TypeId != None:
            if FreeCADGui.Selection.getSelection() != None:
                Selection = FreeCADGui.Selection.getSelection()[-1]
                if Selection.TypeId == self.TypeId:
                    return True
            return False
        return True

class GeomaticsWorkbench ( Gui.Workbench ):

    from Init import ICONPATH
    import os

    "Geomatics Workbench Object"
    MenuText = 'Geomatics'
    ToolTip = 'Geomatic/Survey Engineering Workbench'
    Icon = os.path.join(ICONPATH, 'GeomaticsWorkbench.svg')
		
    def __init__(self):

        self.menu = 1
        self.toolbar = 2
        self.context = 4

        self.command_ui = {

            'Data Tools': {
                'gui': self.menu + self.toolbar,
                'cmd': ['Import Point File',
                        'Export Points',
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
                'gui': self.menu,
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

    EditSurfaceSub = ['Add Triangle','Delete Triangle','Swap Edge','Smooth Surface']
    Gui.addCommand('Surface Editor', GeomaticsCommandGroup(EditSurfaceSub, 'Edit Surface', TypeId = 'Mesh::Feature'))

    DraftDraw = ["Draft_Line","Draft_Wire","Draft_Circle","Draft_Arc","Draft_Ellipse",
                 "Draft_Polygon","Draft_Rectangle", "Draft_Text", "Draft_Dimension",
                 "Draft_BSpline","Draft_Point", "Draft_ShapeString","Draft_Facebinder",
                 "Draft_BezCurve","Draft_Label"
                ]
    Gui.addCommand('Draw Tools', GeomaticsCommandGroup(DraftDraw, 'Draft Draw Tools'))

    DraftEdit = ["Draft_Move", "Draft_Rotate", "Draft_Offset",
                 "Draft_Trimex", "Draft_Join", "Draft_Split", "Draft_Upgrade",
                 "Draft_Downgrade", "Draft_Scale", "Draft_Edit", "Draft_WireToBSpline",
                 "Draft_AddPoint", "Draft_DelPoint", "Draft_Shape2DView", "Draft_Draft2Sketch",
                 "Draft_Array", "Draft_PathArray", "Draft_PointArray", "Draft_Clone",
                 "Draft_Drawing", "Draft_Mirror", "Draft_Stretch"
                ]

    Gui.addCommand('Edit Tools', GeomaticsCommandGroup(DraftEdit, 'Draft Snap Tools'))

    def ContextMenu(self, recipient):
        """
        Right-click menu options
        """
        # "recipient" will be either "view" or "tree"

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
