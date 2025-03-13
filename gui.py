import pygame
pygame.init()

from tools.uielements import *

class Gui:
    def __init__(self, parentSurface):
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

        # --- Render window ---
        self.gMainRender = Group(eventOffset = [0, 0])

        # Render window element setup
        self.gMainRender.add_elements(
            RenderWindow(
                self.renderSurface,
                pygame.Rect(0, 0, self.renderRes[0] * self.wMainCoeffs[0], self.renderRes[1] * self.wMainCoeffs[1])
            )
        )

        # --- Right sidebar ---
        # Different groups for different sidebar options
        self.gRightImporter = Group() # UI for importing new tiles
        self.gRightOptions = Group() # UI for configuring selected tile

        # --- Bottombar ---
        # Different groups for different bottombar options
        self.gBottomTools = Group() # Overview and selection of tools such as delete, place and brushes
        self.gBottomTiles = Group() # Overview and selection of tiles

        # --- Activate default groups ---
        self.gMainRender.activate_all()

    def draw(self):
        self.renderSurface.fill([255, 255, 255])

        # Update all grouped elements
        for group in groups:
            group.update()

        self.parentSurface.blit(self.renderSurface, [0, 0])




def _guiTest():
    screen = pygame.display.set_mode([1600, 900])
    pygame.display.set_caption("GUI Test")
    clock = pygame.time.Clock()
    run = True

    gui = Gui(screen)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill([255, 255, 255])

        gui.draw()

        clock.tick(60)
        pygame.display.update()

# Testing
if __name__ == "__main__":
    _guiTest()