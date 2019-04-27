import NewProject
import ImportPointFile
import CreateSurface
import EditSurface
import CreateGuideLines
import ExportPoints

class GeomaticsCommandGroup:
    def __init__(self, cmdlist, menu, tooltip = None):
        self.cmdlist = cmdlist
        self.menu = menu
        if tooltip is None:
            self.tooltip = menu
        else:
            self.tooltip = tooltip

    def GetCommands(self):
        return tuple(self.cmdlist)

    def GetResources(self):
        return { 'MenuText': self.menu, 'ToolTip': self.tooltip }

class GeomaticsWorkbench ( Workbench ):
    "Geomatics Workbench Object"
    MenuText = 'Geomatics'
    ToolTip = 'Geomatic/Survey Engineering Workbench'
    Icon = App.__path__[3] + '/Geomatics/Resources/Icons/GeomaticsWorkbench.svg'
		
    def __init__(self):

        self.menu = 1
        self.toolbar = 2
        self.context = 4

        self.command_ui = {

            'Project Tools': {
                'gui': self.toolbar,
                'cmd': ['New Project']
            },
            'Data Tools': {
                'gui': self.menu + self.toolbar,
                'cmd': ['Import Point File',
                        'Export Points',
                       ]
            },

            'Surface Tools': {
                'gui': self.menu + self.toolbar + self.context,
                'cmd': ['Create Surface',
                        'Edit Surface',
                        'Surface Editor'
                       ]
			},
			
            'Section Tools': {
                'gui': self.menu,
                'cmd': ['Create Guide Lines']
            },
        }

    def Initialize(self):
        global GeomaticsCommandGroup

        for _k, _v in self.command_ui.items():

            if _v['gui'] & self.toolbar:
                self.appendToolbar(_k, _v['cmd'])

            if _v['gui'] & self.menu:
                self.appendMenu(_k, _v['cmd'])

    EditSurfaceSub = ['Edit Surface']
    FreeCADGui.addCommand('Surface Editor', GeomaticsCommandGroup(EditSurfaceSub, 'Edit Surface'))

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
