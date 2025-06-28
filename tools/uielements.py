# 2.x version of uiElements.py by Culf

'''
Colorscheme setup:

Index 0 = Text color
Index 1 = Border color
Index 2 = bg color
'''

import pygame

pygame.init()
all_elements = []
groups = []
windows = []

defaultSimpleColorScheme = [
    [0, 0, 0],
    [0, 0, 0],
    [255, 255, 255]
]

defaultColorScheme = {
    "standard": [
        [0, 0, 0],
        [0, 0, 0],
        [255, 255, 255]
    ]
}
defaultButtonColorScheme = {
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

def update_all():
    for element in all_elements:
        element.update()

def update_ungrouped():
    for element in all_elements:
        if len(element.groups) == 0:
            element.update()

def remove_elements(*args):
    for element in args:
        if element in all_elements:
            for e, i in enumerate(all_elements):
                if e == element:
                    # Delete element from all groups
                    for group in element.groups:
                        group.remove_element(element)
                    # Delete element from all elements
                    del all_elements[i]
                    break

class Group:
    def __init__(self):
        self.elements = []
        self.activated = True
        groups.append(self)

    def update(self, events):
        for element in self.elements:
            element.update(events)

    def add_elements(self, *args):
        for element in args:
            self.elements.append(element)
            element.groups.append(self)

    def remove_elements(self, *args):
        for element in args:
            if element in self.elements:
                for e, i in enumerate(self.elements):
                    if e == element:
                        # Delete self from element
                        for g, j in element.groups:
                            if g == self:
                                del element.groups[j]
                        # Delete element from self
                        del self.elements[i]
                        break

    def activate_all(self):
        self.activated = True
        for element in self.elements:
            element.activated = True

    def deactivate_all(self):
        self.activated = False
        for element in self.elements:
            element.activated = False
    
    def isActive(self):
        return self.activated

class Window(Group):
    def __init__(self, screen, rect, colorscheme, scaling = 1, borderwidth = None):
        super().__init__()
        windows.append(self)

        self.screen = screen
        self.borderWidth = borderwidth
        self.colorscheme = colorscheme
        self.rect = rect
        self.surface = pygame.surface.Surface([rect.w, rect.h])
        self.scaling = scaling # When parentsurface is being rescaled, scaling makes it possible to convert a mouse position to the actual rendered size

    def getWidth(self):
        return self.rect.w
    
    def getHeight(self):
        return self.rect.h

    def getSurface(self):
        return self.surface
    
    def update(self, events, scaling = 1):
        if self.activated:
            self.scaling = scaling

            self.clearSurface()

            for element in self.elements:
                element.update(events, self.rect.topleft, self.scaling)

            self.drawBorder()
            self.drawOnScreen()
    
    def clearSurface(self):
        self.surface.fill(self.colorscheme[2])

    def drawBorder(self):
        if self.borderWidth != None:
            pygame.draw.rect(self.surface, self.colorscheme[1], pygame.Rect(0, 0, self.rect.w, self.rect.h), self.borderWidth)
        
    def drawOnScreen(self):
        self.screen.blit(self.surface, [self.rect.x, self.rect.y])

class Element:
    def __init__(self):
        all_elements.append(self)
        self.activated = False
        self.groups = []

    def update(self, events, positionoffset = None, scaling = 1):
        # Bad looking if statement for compatability
        if self.activated:
            # Updated elements supporting extra arguments
            if positionoffset != None or scaling != 1: # Only used when non-default arguments are supplied
                self.eventupdate(events, positionoffset, scaling)
            # Elements that do not support extra arguments
            else:
                self.eventupdate(events)
            self.draw()

    def eventupdate(self, *args):
        return

    def draw(self, *args):
        return

class Button(Element):
    def __init__(self, screen, rect, colorscheme, font, bordersize=2, text="", command=lambda: None, commandArg = None, activated=True):
        super().__init__()

        self.screen = screen
        self.rect = rect
        self.colors = colorscheme
        self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.font = font
        self.bordersize = bordersize
        self.text = text
        self.command = command
        self.commandArg = commandArg
        self.activated = activated
        
        self.click = False
        self.hover = False

    def runcommand(self):
        if self.commandArg == None:
            self.command()
        else:
            self.command(self.commandArg)

    def getColorScheme(self):
        return self.colors
    
    def setColorScheme(self, colors):
        self.colors = colors

    def eventupdate(self, events, positionoffset = [0, 0], scaling = 1):
        self.eventRect = self.rect.copy()
        self.eventRect.x += positionoffset[0]
        self.eventRect.y += positionoffset[1]
        self.eventRect.x *= scaling
        self.eventRect.y *= scaling
        self.eventRect.width *= scaling
        self.eventRect.height *= scaling

        if self.eventRect.collidepoint(pygame.mouse.get_pos()):
            self.hover = True
            if pygame.mouse.get_pressed()[0]:
                self.click = True
            else:
                if self.click:
                    self.click = False
                    self.runcommand()
                    
        else: self.hover, self.click = False, False

    def draw(self):
        # Choose colors
        if self.click:      self.curColors = self.colors["click"]
        elif self.hover:    self.curColors = self.colors["hover"]
        else:               self.curColors = self.colors["standard"]

        # Draw
        self.surface.fill(self.curColors[2]) # BG
        if self.bordersize > 0: pygame.draw.rect(self.surface, self.curColors[1], pygame.Rect(0,0,self.rect.width,self.rect.height),self.bordersize) # Border
        self.rendered_text = self.font.render(self.text, True, self.curColors[0])
        self.surface.blit(self.rendered_text, (self.rect.width//2-self.rendered_text.get_width()//2,self.rect.height//2-self.rendered_text.get_height()//2)) # Text
        self.screen.blit(self.surface, (self.rect.x,self.rect.y))

class Text(Element):
    def __init__(self, screen, rect, colorscheme, font, bordersize=0, text="", allign="CENTER", activated=True):
        super().__init__()

        self.screen = screen
        self.rect = rect
        self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.colorscheme = colorscheme
        self.font = font
        self.bordersize = bordersize
        self.text = text
        self.allign = allign
        self.activated = activated

    def draw(self):
        # Choose colors
        self.curColors = self.colorscheme["standard"]

        # Draw
        self.surface.fill(self.curColors[2]) # BG
        if self.bordersize > 0: pygame.draw.rect(self.surface, self.curColors[1], pygame.Rect(0,0,self.rect.width,self.rect.height),self.bordersize) # Border
        self.rendered_text = self.font.render(self.text, True, self.curColors[0])
        if self.allign == "CENTER":
            self.surface.blit(self.rendered_text, (self.rect.width//2-self.rendered_text.get_width()//2,self.rect.height//2-self.rendered_text.get_height()//2)) # Text
        elif self.allign == "LEFT":
            self.surface.blit(self.rendered_text, (5,self.rect.height//2-self.rendered_text.get_height()//2)) # Text
        elif self.allign == "RIGHT":
            self.surface.blit(self.rendered_text, (self.rect.width-5-self.rendered_text.get_width(),self.rect.height//2-self.rendered_text.get_height()//2))
        self.screen.blit(self.surface, (self.rect.x,self.rect.y))

class Textbox(Element):
    def __init__(self, screen, rect, colorscheme, font, bordersize=2, text="", allign="CENTER", activated=True):
        super().__init__()

        self.screen = screen
        self.rect = rect
        self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.colorscheme = colorscheme
        self.font = font
        self.bordersize = bordersize
        self.text = text.split("\n") if type(text) == type("") else text
        self.allign = allign
        self.activated = activated

    def draw(self):
        # Choose colors
        self.curColors = self.colorscheme["standard"]

        # Draw
        self.surface.fill(self.curColors[2]) # BG
        if self.bordersize > 0: pygame.draw.rect(self.surface, self.curColors[1], pygame.Rect(0,0,self.rect.width,self.rect.height),self.bordersize) # Border
        
        # Render all lines of text
        self.rendered_text = []
        for line in self.text:
            self.rendered_text.append(self.font.render(line, True, self.curColors[0]))

        self.y = 5
        if self.allign == "CENTER":
            for line in self.rendered_text:
                self.surface.blit(line, (self.rect.width//2-line.get_width()//2,self.y)) # Text
                self.y += line.get_height()
        elif self.allign == "LEFT":
            for line in self.rendered_text:
                self.surface.blit(line, (5,self.y)) # Text
                self.y += line.get_height()
        elif self.allign == "RIGHT":
            for line in self.rendered_text:
                self.surface.blit(line, (self.rect.width-5-line.get_width(),self.y))
                self.y += line.get_height()
        self.screen.blit(self.surface, (self.rect.x,self.rect.y))

class Scrolledtext(Element):
    def __init__(self, screen, rect, colorscheme, font, bordersize=2, text="", allign="CENTER", activated=True):
        super().__init__()

        self.screen = screen
        self.rect = rect
        self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.colorscheme = colorscheme
        self.font = font
        self.bordersize = bordersize
        self.text = text.split("\n") if type(text) == type("") else text
        self.lineheight = self.font.render("",True,(0,0,0)).get_height()
        self.allign = allign
        self.contentposition = 0
        self.scrollspeed = 5
        self.activated = activated

        self.scroll, self.scrollstop, self.hover = False, False, False

    def eventupdate(self, *args):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hover = True
            self.pressedkeys = pygame.key.get_pressed()
            self.scroll, self.scrollstop = False, False
            if self.pressedkeys[pygame.K_DOWN]:
                if self.contentposition > 0:
                    self.contentposition -= self.scrollspeed
                if self.contentposition <= 0:
                    self.contentposition = 0
                    self.scrollstop = True
                self.scroll = True
            if self.pressedkeys[pygame.K_UP]:
                self.contentposition += self.scrollspeed
                self.scroll = True
                if self.contentposition > len(self.text)*self.lineheight-self.lineheight+5:
                    self.contentposition = len(self.text)*self.lineheight-self.lineheight+5 
                    self.scrollstop = True
        else:
            self.hover = False

    def draw(self):
        # Choose colors
        if self.scrollstop: self.curColors = self.colorscheme["stop"]
        elif self.scroll: self.curColors = self.colorscheme["scroll"]
        elif self.hover: self.curColors = self.colorscheme["hover"]
        else: self.curColors = self.colorscheme["standard"]

        # Draw
        self.surface.fill(self.curColors[2]) # BG

        # Text
        self.y = self.rect.height-5
        for line in self.text[::-1]:
            self.rendered_text = self.font.render(line, True, self.curColors[0])

            if self.allign == "LEFT": self.x = 5
            elif self.allign == "CENTER": self.x = self.rect.width//2-self.rendered_text.get_width()//2
            else: self.x = self.rect.width - 5 - self.rendered_text.get_width()
            
            self.y -= self.lineheight
            self.surface.blit(self.rendered_text, (self.x, self.y+self.contentposition))

        # Border
        pygame.draw.rect(self.surface, self.curColors[1], pygame.Rect(0,0,self.rect.width,self.rect.height), self.bordersize)


        self.screen.blit(self.surface, (self.rect.x, self.rect.y))

class Input(Element):
    def __init__(self, screen, rect, colorscheme, font, bordersize = 1, text="", allign = "LEFT", activated = True):
        super().__init__()

        self.screen = screen
        self.rect = rect
        self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.colorscheme = colorscheme
        self.font = font
        self.bordersize = bordersize
        self.text = text
        self.allign = allign
        self.activated = activated

        self.click = False
        self.selected = False

    def eventupdate(self, events, positionoffset = [0, 0], scaling = 1):
        self.eventRect = self.rect.copy()
        self.eventRect.x += positionoffset[0]
        self.eventRect.y += positionoffset[1]
        self.eventRect.x *= scaling
        self.eventRect.y *= scaling
        self.eventRect.width *= scaling
        self.eventRect.height *= scaling

        if self.eventRect.collidepoint(pygame.mouse.get_pos()):
            self.hover = True
        else:
            self.hover = False

        if pygame.mouse.get_pressed()[0]:
            self.click = True
        else:
            if self.click:
                if self.hover:
                    self.click = False
                    self.selected = True
                else:
                    self.click = False
                    self.selected = False

        if self.selected:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode

    def draw(self):
        # Choose colors
        if self.selected:
            self.curColors = self.colorscheme["selected"]
        elif self.hover:
            self.curColors = self.colorscheme["hover"]
        else:
            self.curColors = self.colorscheme["standard"]

        # Draw
        self.surface.fill(self.curColors[2]) # BG
        if self.bordersize > 0: pygame.draw.rect(self.surface, self.curColors[1], pygame.Rect(0,0,self.rect.width,self.rect.height),self.bordersize) # Border
        self.rendered_text = self.font.render(self.text, True, self.curColors[0])
        if self.allign == "CENTER":
            self.surface.blit(self.rendered_text, (self.rect.width//2-self.rendered_text.get_width()//2,self.rect.height//2-self.rendered_text.get_height()//2)) # Text
        elif self.allign == "LEFT":
            self.surface.blit(self.rendered_text, (5,self.rect.height//2-self.rendered_text.get_height()//2)) # Text
        elif self.allign == "RIGHT":
            self.surface.blit(self.rendered_text, (self.rect.width-5-self.rendered_text.get_width(),self.rect.height//2-self.rendered_text.get_height()//2))
        self.screen.blit(self.surface, (self.rect.x,self.rect.y))

    def getText(self):
        return self.text

class RenderWindow(Element):
    def __init__(self, screen, rect):
        super().__init__()

        self.screen = screen
        self.rect = rect
        self.surface = pygame.surface.Surface(self.rect.size)
        self.surface.fill([200, 200, 200])
        self.eventUpdateListeners = []
        self.drawListeners = []

    def getSurface(self):
        '''Get the surface RenderWindow draws to its screen'''
        return self.surface
    
    def addEventUpdateListener(self, func):
        '''Add a function that will be called and passed the offsetEventPos every time RenderWindow performs eventupdate'''
        self.eventUpdateListeners.append(func)

    def addDrawListener(self, func):
        '''Add a function that will be called every time draw runs (use this function to update the renderwindow surface before it is redrawn)'''
        self.drawListeners.append(func)

    def eventupdate(self, offsetEventPos):
        for listener in self.eventUpdateListeners:
            listener(offsetEventPos)

    def draw(self):
        for listener in self.drawListeners:
            listener()

        self.screen.blit(self.surface, self.rect.topleft)

class ObjectScrollBox(Element):
    def __init__(self, screen, rect, objectSize, colorscheme, objectColorScheme = defaultColorScheme, objectBorderSize = 5, objects = [], bordersize = 2, activated = True):
        super().__init__()

        self.screen = screen
        self.rect = rect
        self.objectSize = objectSize
        self.surface = pygame.surface.Surface([self.rect.w, self.rect.h])

        self.colorscheme = colorscheme
        self.objectColorScheme = objectColorScheme
        self.bordersize = bordersize
        self.objectBorderSize = objectBorderSize

        self.activated = activated

        self.objects = objects
        for obj in self.objects:
            obj.setup(self.objectSize, self.surface, self.objectColorScheme, objectBorderSize)

        self.hover = False
        self.scroll = False
        self.contentposition = 0
        self.scrollspeed = 15
        self.maxScroll = 0
        self.objectsPrLine = 0

    def eventupdate(self, events, positionoffset = [0, 0], scaling = 1):
        self.tempMpos = [p * (1 / scaling) for p in pygame.mouse.get_pos()]
        self.scroll = False
        self.collisionrect = pygame.Rect(self.rect.x + positionoffset[0], self.rect.y + positionoffset[1], self.rect.w, self.rect.h)
        if self.collisionrect.collidepoint(self.tempMpos):
            self.hover = True

            for event in events:
                if event.type == pygame.MOUSEWHEEL:
                    self.scroll = True
                    self.contentposition -= event.y * self.scrollspeed

                    if self.contentposition < 0:
                        self.contentposition = 0
                    elif self.contentposition > self.maxScroll:
                        self.contentposition = self.maxScroll
                
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    for obj in self.objects:
                        obj.mouseevent([event.pos[0] * (1 / scaling) - self.collisionrect.x, event.pos[1] * (1 / scaling) - self.collisionrect.y])
        else:
            self.hover = False

    def updateContentDimensions(self):
        self.objectsPrLine = (self.rect.w - self.bordersize * 2) // self.objectSize[0]
        self.maxScroll = (len(self.objects) // self.objectsPrLine) * self.objectSize[1]

    def draw(self):
        self.updateContentDimensions()

        # Background
        self.surface.fill(self.colorscheme[2])

        # Content
        self.contentStartX = (self.rect.w - self.objectsPrLine * self.objectSize[1]) / 2
        self.contentStartY = self.bordersize

        for i in range(len(self.objects)):
            self.objects[i].draw([self.contentStartX + (i % self.objectsPrLine) * self.objectSize[0], self.contentStartY + (i // self.objectsPrLine) * self.objectSize[1] - self.contentposition])

        # Border
        pygame.draw.rect(self.surface, self.colorscheme[1], pygame.Rect(0, 0, self.surface.get_width(), self.surface.get_height()), self.bordersize)

        # Export to parent
        self.screen.blit(self.surface, [self.rect.x, self.rect.y])

    def addObjects(self, objects):
        for obj in objects:
            self.objects.append(obj)
            obj.setup(self.objectSize, self.surface, self.objectColorScheme, self.objectBorderSize)

    def getObjects(self):
        return self.objects

class MultiObjectScrollBox(Element):
    def __init__(self, screen, rect, pageSettings = {}, activated = True, colorscheme = defaultSimpleColorScheme, buttonColorScheme = defaultButtonColorScheme, bordersize = 2, font = pygame.font.SysFont("Consolas", 25)):
        super().__init__()

        self.exportSurface = screen
        self.rect = rect
        self.navRect = pygame.Rect(0, 0, self.rect.width, self.rect.height * 0.1)
        self.scrollBoxRect = pygame.Rect(0, self.rect.height * 0.1, self.rect.width, self.rect.height * 0.9)

        self.mainSurface = pygame.surface.Surface(self.rect.size)
        self.navSurface = pygame.surface.Surface(self.navRect.size)
        self.scrollBoxSurface = pygame.surface.Surface(self.scrollBoxRect.size)

        self.colorscheme = colorscheme
        self.buttonColorScheme = buttonColorScheme
        self.bordersize = bordersize
        self.font = font

        self.activated = activated

        # Page setup
        self.pageSettings = pageSettings
        self.pageNames = list(pageSettings)
        self.currentPage = self.pageNames[0]
        self.navButtons = {}
        self.scrollBoxes = {}

        # Nav button for each page
        for i in range(len(self.pageNames)):
            self.navButtons[self.pageNames[i]] = Button(
                self.navSurface,
                pygame.Rect(
                    i * self.navRect.width / len(self.pageNames),
                    0,
                    self.navRect.width / len(self.pageNames),
                    self.navRect.height
                ),
                self.buttonColorScheme,
                self.font,
                text = self.pageNames[i].capitalize(),
                command = self.selectPage,
                commandArg = self.pageNames[i],
                activated = True
            )

        # ObjectScrollBox for each element
        for pagename, pagesettings in self.pageSettings.items():
            self.scrollBoxes[pagename] = ObjectScrollBox(
                self.scrollBoxSurface,
                pygame.Rect(
                    0,
                    0,
                    self.scrollBoxRect.width,
                    self.scrollBoxRect.height
                ),
                pagesettings["objectSize"],
                self.colorscheme,
                pagesettings["objectColorScheme"],
                pagesettings["objectBorderSize"],
                pagesettings["objects"],
                self.bordersize,
                True
            )
    
    def selectPage(self, pageName):
        self.currentPage = pageName

    def eventupdate(self, events, positionoffset = [0, 0], scaling = 1):
        for button in self.navButtons.values():
                
            button.eventupdate(
                events,
                positionoffset = [positionoffset[0] + self.rect.x + self.navRect.x, positionoffset[1] + self.rect.y + self.navRect.y],
                scaling = scaling
            )
        self.scrollBoxes[self.currentPage].eventupdate(
            events,
            positionoffset = [positionoffset[0] + self.rect.x + self.scrollBoxRect.x, positionoffset[1] + self.rect.y + self.scrollBoxRect.y],
            scaling = scaling
        )

    def draw(self):
        tempColorScheme = None
        for button in self.navButtons.values():

            if button.commandArg == self.currentPage:
                tempColorScheme = button.getColorScheme()
                button.setColorScheme({
                    "standard": tempColorScheme["click"],
                    "hover": tempColorScheme["click"],
                    "click": tempColorScheme["click"]
                })

            button.draw()

            if tempColorScheme != None:
                button.setColorScheme(tempColorScheme)
                tempColorScheme = None

        self.scrollBoxes[self.currentPage].draw()

        self.mainSurface.blit(self.navSurface, [self.navRect.x, self.navRect.y])
        self.mainSurface.blit(self.scrollBoxSurface, [self.scrollBoxRect.x, self.scrollBoxRect.y])
        
        pygame.draw.rect(self.mainSurface, self.colorscheme[1], self.rect, self.bordersize)

        self.exportSurface.blit(self.mainSurface, [self.rect.x, self.rect.y])

    def addObjects(self, page, objects):

        if page in self.pageNames:
            self.scrollBoxes[page].addObjects(objects)
        else:
            print(f'Page "{page}" doesn\'t exists!')

    def getObjects(self, page):
        if page in self.pageNames:
            return self.scrollBoxes[page].getObjects()
        else:
            print(f'Page "{page}" doesn\'t exists!')
            return None
        
    def getCurrentPageName(self):
        return self.currentPage

class LineBasedObjectScrollBox(ObjectScrollBox):
    def updateContentDimensions(self):
        self.objectsPrLine = 1
        self.maxScroll = len(self.objects) * self.objectSize[1]

    def draw(self):
        self.updateContentDimensions()

        # Background
        self.surface.fill(self.colorscheme[2])

        # Content
        self.contentStartX = self.bordersize
        self.contentStartY = self.bordersize

        for i in range(len(self.objects)):
            self.objects[i].draw([self.contentStartX, self.contentStartY + (i // self.objectsPrLine) * self.objectSize[1] - self.contentposition])

        # Border
        pygame.draw.rect(self.surface, self.colorscheme[1], pygame.Rect(0, 0, self.surface.get_width(), self.surface.get_height()), self.bordersize)

        # Export to parent
        self.screen.blit(self.surface, [self.rect.x, self.rect.y])

class ScrollCompatibleObject:
    def __init__(self):
        self.setupDone = False
        self.latestPos = [0, 0]
        self.size = [0, 0]
        self.exportSurface = None

    def setup(self, objectSize, parentSurface, colorScheme = defaultColorScheme, borderWidth = 5):
        self.size = objectSize
        self.exportSurface = pygame.surface.Surface(self.size)
        self.parentSurface = parentSurface
        self.setupDone = True

        self.colorScheme = colorScheme
        self.borderWidth = borderWidth

    def mouseevent(self, pos):
        if self.setupDone:
            clickHit = pygame.rect.Rect(self.latestPos, self.size).collidepoint(pos)
            self.clickevent(clickHit)

    def clickevent(self, hit):
        pass

    def draw(self, pos):
        self.latestPos = pos

        if self.setupDone:
            self.updateGraphics()

            self.parentSurface.blit(self.exportSurface, pos)

    def updateGraphics(self):
        self.exportSurface.fill(self.colorScheme["standard"][2])
        pygame.draw.rect(self.exportSurface, self.colorScheme["standard"][1], pygame.Rect(0, 0, self.size[0], self.size[1]), self.borderWidth)

class SelectableScrollObject(ScrollCompatibleObject):
    def __init__(self, text, font):
        super().__init__()
        self.text = text
        self.font = font
        self.selected = False

    def clickevent(self, hit):
        if hit:
            self.selected = True
        else:
            self.selected = False

    def updateGraphics(self):
        if self.selected:
            self.curColors = self.colorScheme["selected"]
        else:
            self.curColors = self.colorScheme["standard"]

        self.exportSurface.fill(self.curColors[2])
        self.renderedText = self.font.render(self.text, True, self.curColors[0])
        self.exportSurface.blit(self.renderedText, [0, self.size[1] // 2 - self.renderedText.get_height() // 2])
        pygame.draw.rect(self.exportSurface, self.curColors[1], pygame.Rect(0, 0, self.size[0], self.size[1]), self.borderWidth)

    def isSelected(self):
        return self.selected

class SelectableSpriteScrollObject(SelectableScrollObject):
    '''
    A selectable scroll object with a sprite as its icon.

    Requirements for sprite:
    - Sprite has to return a surface when its update function is called.
    - Sprites update function takes delta time as its only parameter
    '''
    def __init__(self, sprite):
        self.selected = False
        self.sprite = sprite

    def updateGraphics(self, delta = 0):
        if self.selected:
            self.curColors = self.colorScheme["selected"]
        else:
            self.curColors = self.colorScheme["standard"]

        self.exportSurface.fill(self.curColors[2])
        
        self.exportSurface.blit(self.sprite.update(delta), [0, 0])
        pygame.draw.rect(self.exportSurface, self.curColors[1], pygame.Rect(0, 0, self.size[0], self.size[1]), self.borderWidth)

    def getSprite(self):
        return self.sprite
