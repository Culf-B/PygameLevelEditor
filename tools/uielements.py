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
        for element in self.elements:
            element.activated = True

    def deactivate_all(self):
        for element in self.elements:
            element.activated = False

class Element:
    def __init__(self):
        all_elements.append(self)
        self.activated = False
        self.groups = []

    def update(self, events):
        if self.activated:
            self.eventupdate(events)
            self.draw()

    def eventupdate(self, *args):
        return

    def draw(self, *args):
        return

class Button(Element):
    def __init__(self, screen, rect, colorscheme, font, bordersize=2, text="", command=lambda: None, activated=True):
        super().__init__()

        self.screen = screen
        self.rect = rect
        self.colors = colorscheme
        self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32)
        self.font = font
        self.bordersize = bordersize
        self.text = text
        self.command = command
        self.activated = activated
        
        self.click = False
        self.hover = False

    def runcommand(self):
        self.command()

    def eventupdate(self, offsetEventPos = [0, 0]):
        self.eventRect = self.rect.copy()
        self.eventRect.x += offsetEventPos[0]
        self.eventRect.y += offsetEventPos[1]
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
    def __init__(self, screen, rect, objectSize, colorscheme, objects = [], bordersize = 2, activated = True):
        super().__init__()

        self.screen = screen
        self.rect = rect
        self.objectSize = objectSize
        self.surface = pygame.surface.Surface([self.rect.w, self.rect.h])

        self.colorscheme = colorscheme
        self.bordersize = bordersize
        
        self.activated = activated

        self.objects = objects
        for obj in self.objects:
            obj.setup(self.objectSize, self.surface)

        self.hover = False
        self.scroll = False
        self.contentposition = 0
        self.scrollspeed = 5
        self.maxScroll = 0
        self.objectsPrLine = 0

    def eventupdate(self, events):
        self.tempMpos = pygame.mouse.get_pos()
        self.scroll = False
        if self.rect.collidepoint(self.tempMpos):
            self.hover = True

            for event in events:
                if event.type == pygame.MOUSEWHEEL: # idk this no work this mentions sdl 2: https://pyga.me/docs/ref/event.html
                    self.scroll = True
                    self.contentposition += event.y * self.scrollspeed

                    if self.contentposition < 0:
                        self.contentposition = 0
                    elif self.contentposition > self.maxScroll:
                        self.contentposition = self.maxScroll
                
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    for obj in self.objects:
                        obj.mouseevent([event.pos[0] - self.rect.x, event.pos[1] - self.rect.y])
        else:
            self.hover = False

    def updateContentDimensions(self):
        self.objectsPrLine = (self.rect.w - self.bordersize * 2) // self.objectSize[0]
        self.maxScroll = (len(self.objects) // self.objectsPrLine) * self.objectSize[1]

    def draw(self):
        self.updateContentDimensions()

        # Background
        self.surface.fill(self.colorscheme[2])

        # Border
        pygame.draw.rect(self.surface, self.colorscheme[1], pygame.Rect(0, 0, self.surface.get_width(), self.surface.get_height()), self.bordersize)

        # Content
        self.contentStartX = (self.rect.w - self.objectsPrLine * self.objectSize[1]) / 2

        for i in range(len(self.objects)):
            self.objects[i].draw([(i % self.objectsPrLine) * self.objectSize[0], (i // self.objectsPrLine) * self.objectSize[1]])

        # Export to parent
        self.screen.blit(self.surface, [self.rect.x, self.rect.y])

    def addObjects(self, *args):
        for obj in args:
            self.objects.append(obj)
            obj.setup(self.objectSize, self.surface)

class ScrollCompatibleObject:
    def __init__(self):
        self.setupDone = False
        self.latestPos = [0, 0]
        self.size = [0, 0]
        self.exportSurface = None

    def setup(self, objectSize, parentSurface):
        self.size = objectSize
        self.exportSurface = pygame.surface.Surface(self.size)
        self.parentSurface = parentSurface
        self.setupDone = True

    def mouseevent(self, pos):
        if self.setupDone:
            if pygame.rect.Rect(self.latestPos, self.size).collidepoint(pos):
                self.clickevent()

    def clickevent(self):
        print("Mouseclick!")

    def draw(self, pos):
        self.latestPos = pos

        if self.setupDone:
            self.updateGraphics()

            self.parentSurface.blit(self.exportSurface, pos)

    def updateGraphics(self):
        self.exportSurface.fill([255, 255, 255])