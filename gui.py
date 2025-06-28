import pygame
pygame.init()

from tools.uielements import *

class Gui:
    def __init__(self, parentSurface, projectManager):
        # --- References ---
        # References to objects that handles the functionality
        self.projectManager = projectManager

        # --- Surface setup ---
        # If resolution of parentsurface and renderres is not the same,
        # the rendered surface will be scaled to fit, 
        # leaving black boxes in the sides or bottom and top.
        self.renderRes = [1600, 900] # Resolution the GUI is rendered in
        self.parentSurface = parentSurface # Surface the GUI has to be displayed on
        self.renderSurface = pygame.surface.Surface(self.renderRes) # Surface the GUI is rendered to
        # Coefficiants multiplied to the renderRes to determine size of the different windows / bars:
        self.wMainCoeffs = [0.7, 0.7]
        self.wRightCoeffs = [0.3, 0.7]
        self.wBottomCoeffs = [1, 0.3]

        # Temporary memory
        self.currentInfoSprite = None

        # Color schemes
        self.standardLabelColorScheme = {
            "standard": [
                [0, 0, 0],
                [0, 0, 0],
                [255, 255, 255]
            ]
        }
        self.standardInputColorScheme = {
            "standard": [
                [0, 0, 0],  # Text color
                [0, 0, 0],        # Border color
                [200, 200, 200]   # Background color
            ],
            "hover": [
                [0, 0, 0],  # Text color (white)
                [100, 100, 100],     # Border color
                [220, 220, 220]   # Background color
            ],
            "selected": [
                [0, 0, 0],  # Text color
                [100, 100, 255],  # Border color
                [255, 255, 255]   # Background color
            ]
        }
        self.standardButtonColorScheme = {
            "standard": [
                [0, 0, 0],  # Text color
                [0, 0, 0],        # Border color
                [200, 200, 200]   # Background color
            ],
            "hover": [
                [0, 0, 0],  # Text color (white)
                [50, 50, 50],     # Border color
                [150, 150, 150]   # Background color
            ],
            "click": [
                [0, 0, 0],  # Text color
                [100, 100, 100],  # Border color
                [100, 100, 100]   # Background color
            ]
        }
        self.standardScrolledSelectorObjectColorScheme = {
            "standard": [
                [0, 0, 0],  # Text color
                [0, 0, 0],        # Border color
                [255, 255, 255]   # Background color
            ],
            "selected": [
                [0, 0, 0],  # Text color
                [200, 200, 255],  # Border color
                [100, 100, 255]   # Background color
            ]
        }
        self.standardFont = pygame.font.SysFont("Consolas", 25)

        self.scalingRatio = 1

        # --- Window Rects ---
        self.rMain = pygame.Rect(0, 0, self.renderRes[0] * self.wMainCoeffs[0], self.renderRes[1] * self.wMainCoeffs[1])
        self.rRight = pygame.Rect(self.renderRes[0] * (1 - self.wRightCoeffs[0]), 0, self.renderRes[0] * self.wRightCoeffs[0], self.renderRes[1] * self.wRightCoeffs[1])
        self.rBottom = pygame.Rect(0, self.renderRes[1] * (1 - self.wBottomCoeffs[1]), self.renderRes[0] * self.wBottomCoeffs[0], self.renderRes[1] * self.wBottomCoeffs[1])

        # --- Render window ---
        self.wMainRender = Window(
            self.renderSurface,
            self.rMain,
            [
                [0, 0, 0],
                [0, 0, 0],
                [100, 100, 100]
            ],
            2
        )

        # Render window element setup

        # --- Right sidebar ---
        # Different sidebar windows
        self.wRightProjectManager = Window(
            self.renderSurface,
            self.rRight,
            [
                [0, 0, 0],
                [0, 0, 0],
                [255, 255, 255]
            ],
            1
        ) # UI for accessing projectManager

        self.wRight_projectStatusText = Text(
            self.wRightProjectManager.getSurface(),
            pygame.Rect(0, 0, self.rRight.width, self.rRight.height * 0.1),
            self.standardLabelColorScheme,
            self.standardFont,
            bordersize = 1
        )

        # Project Management objects
        self.wRight_ProjectManagementGroup = Group()

        self.wRight_saveProjectButton = Button(
            self.wRightProjectManager.getSurface(),
            pygame.Rect(0, self.rRight.height * 0.1, self.rRight.width * 0.5, self.rRight.height * 0.08),
            self.standardButtonColorScheme,
            self.standardFont,
            text = "Save",
            command = self.projectManager.save
        )

        self.wRight_exploreProjectButton = Button(
            self.wRightProjectManager.getSurface(),
            pygame.Rect(self.rRight.width * 0.5, self.rRight.height * 0.1, self.rRight.width * 0.5, self.rRight.height * 0.08),
            self.standardButtonColorScheme,
            self.standardFont,
            text = "Explore",
            command = self.projectManager.openInFileexplorer
        )
        

        self.wRight_ProjectManagementGroup.add_elements(
            self.wRight_saveProjectButton,
            self.wRight_exploreProjectButton
        )

        # Load / create project objects
        self.wRight_LoadingGroup = Group()

        self.wRight_CreateLabel = Text(
            self.wRightProjectManager.getSurface(),
            pygame.Rect(0, self.rRight.height * 0.1, self.rRight.width, self.rRight.height * 0.08),
            self.standardLabelColorScheme,
            self.standardFont,
            text = "New project"
        )

        self.wRight_CreateInput = Input(
            self.wRightProjectManager.getSurface(),
            pygame.Rect(0, self.rRight.height * 0.18, self.rRight.width * 0.7, self.rRight.height * 0.08),
            self.standardInputColorScheme,
            self.standardFont
        )

        self.wRight_CreateButton = Button(
            self.wRightProjectManager.getSurface(),
            pygame.Rect(self.rRight.width * 0.7, self.rRight.height * 0.18, self.rRight.width * 0.3, self.rRight.height * 0.08),
            self.standardButtonColorScheme,
            self.standardFont,
            text = "Create",
            command = self.createNewProject
        )

        self.wRight_LoadLabel = Text(
            self.wRightProjectManager.getSurface(),
            pygame.Rect(0, self.rRight.height * 0.26, self.rRight.width, self.rRight.height * 0.08),
            self.standardLabelColorScheme,
            self.standardFont,
            text = "Load project"
        )

        self.wRight_ProjectSelector = LineBasedObjectScrollBox(
            self.wRightProjectManager.getSurface(),
            pygame.Rect(0, self.rRight.height * 0.34, self.rRight.width, self.rRight.height * 0.58),
            [self.rRight.width, self.rRight.height * 0.08],
            colorscheme = [[0,0,0], [0,0,0], [255, 255, 255]],
            objectColorScheme = self.standardScrolledSelectorObjectColorScheme,
            objectBorderSize = 1,
            objects = [SelectableScrollObject(projectname, self.standardFont) for projectname in self.projectManager.getProjects()]
        )

        self.wRight_LoadButton = Button(
            self.wRightProjectManager.getSurface(),
            pygame.Rect(0, self.rRight.height * 0.92, self.rRight.width, self.rRight.height * 0.08),
            self.standardButtonColorScheme,
            self.standardFont,
            text = "Load selected",
            command = self.loadSelectedProject
        )

        self.wRight_LoadingGroup.add_elements(
            self.wRight_CreateLabel,
            self.wRight_CreateInput,
            self.wRight_CreateButton,
            self.wRight_LoadLabel,
            self.wRight_ProjectSelector,
            self.wRight_LoadButton
        )

        self.wRightProjectManager.add_elements(
            self.wRight_projectStatusText,
            self.wRight_saveProjectButton,
            self.wRight_exploreProjectButton,
            self.wRight_CreateLabel,
            self.wRight_CreateInput,
            self.wRight_CreateButton,
            self.wRight_LoadLabel,
            self.wRight_ProjectSelector,
            self.wRight_LoadButton
        )

        self.wRightOptions = Window(
            self.renderSurface,
            self.rRight,
            [
                [0, 0, 0],
                [0, 0, 0],
                [255, 255, 255]
            ],
            1
        ) # UI for configuring selected tile

        # --- Bottombar ---
        # Different groups for different bottombar options
        self.wBottomTools = Window(
            self.renderSurface,
            self.rBottom,
            [
                [0, 0, 0],
                [0, 0, 0],
                [255, 255, 255]
            ],
            1
        ) # Overview and selection of tools such as delete, place and brushes
        
        self.wBottomSprites = Window(
            self.renderSurface,
            self.rBottom,
            [
                [0, 0, 0],
                [0, 0, 0],
                [255, 255, 255]
            ],
            1
        ) # Overview and selection of tiles

        self.bottomMultiBox = MultiObjectScrollBox(
            self.wBottomSprites.getSurface(),
            pygame.Rect(0, 0, self.wBottomSprites.getWidth(), self.wBottomSprites.getHeight()),
            {
                "all sprites": {
                    "objectSize": [50, 50],
                    "objectColorScheme": self.standardScrolledSelectorObjectColorScheme,
                    "objectBorderSize": 2,
                    "objects": []
                },
                "test": {
                    "objectSize": [50, 50],
                    "objectColorScheme": self.standardScrolledSelectorObjectColorScheme,
                    "objectBorderSize": 1,
                    "objects": []
                }
            }
        )


        self.wBottomSprites.add_elements(
            self.bottomMultiBox
        )

        # --- Activate default groups ---
        self.wMainRender.activate_all()
        self.wBottomSprites.activate_all()
        self.wRightProjectManager.activate_all()

        # --- Deactivate non-default groups ---
        self.wRightOptions.deactivate_all()
        self.wBottomTools.deactivate_all()

    def createNewProject(self):
        self.projectManager.new(self.wRight_CreateInput.getText())

    def loadSelectedProject(self):
        objects = self.wRight_ProjectSelector.getObjects()
        for obj in objects:
            if obj.selected:
                self.projectManager.load(obj.text)
                
                # Place sprites in sprite scrollbox
                self.bottomMultiBox.addObjects("all sprites", [
                    SelectableSpriteScrollObject(sprite) for sprite in self.projectManager.getSelectedProjectObject().getSprites()
                ])

                return
        print("No project selected!")

    def addSpriteType(self, name, sprites):
        pass

    def draw(self, events):
        # Check for selections in bottomMultiBox
        self.currentInfoSprite = None
        for obj in self.bottomMultiBox.getObjects(self.bottomMultiBox.getCurrentPageName()):
            if obj.isSelected():
                self.currentInfoSprite = obj.getSprite()
                break

        # Update activated windows
        if self.currentInfoSprite == None:
            self.wRightOptions.deactivate_all()
            self.wRightProjectManager.activate_all()
        else:
            self.wRightOptions.activate_all()
            self.wRightProjectManager.deactivate_all()

        # Update contents of wRightProjectManager
        if self.wRightProjectManager.activated:
            self.wRight_projectStatusText.text = f'Project: {self.projectManager.getSelectedProject()}'
            if self.projectManager.projectSelected():
                self.wRight_ProjectManagementGroup.activate_all()
                self.wRight_LoadingGroup.deactivate_all()
            else:
                self.wRight_ProjectManagementGroup.deactivate_all()
                self.wRight_LoadingGroup.activate_all()

        # Clear screen
        self.renderSurface.fill([255, 255, 255])

        # Update all grouped elements
        for window in windows:
            window.update(events, scaling = self.scalingRatio)

        self.renderToParentRatio = [
            self.parentSurface.get_width() / self.renderRes[0],
            self.parentSurface.get_height() / self.renderRes[1]
        ]
        self.scalingRatio = min(self.renderToParentRatio)

        self.parentSurface.blit(
            pygame.transform.scale(
                self.renderSurface,
                [self.renderRes[0] * self.scalingRatio, self.renderRes[1] * self.scalingRatio]
            ),
            [0, 0]
        )

def _guiTest():
    screen = pygame.display.set_mode([1600, 900], pygame.RESIZABLE)
    pygame.display.set_caption("GUI Test")
    clock = pygame.time.Clock()
    run = True

    gui = Gui(screen)

    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        screen.fill([0, 0, 0])

        gui.draw(events)

        clock.tick(60)
        pygame.display.update()

# Testing
if __name__ == "__main__":
    _guiTest()