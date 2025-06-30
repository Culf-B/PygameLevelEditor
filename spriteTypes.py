import pygame
import spritesheet

class BaseType(pygame.sprite.Sprite):
    def __init__(self, spriteData):
        super().__init__()

        self.data = spriteData
        self.properties = self.data["properties"]

        # Path is stored relative in project files but is transformed to abs before sprite object is instantiated
        self.absPath = self.data["absPath"]
        self.rSize = self.data["rSize"] # Real size or size it is resized to before render
        
        # Animated
        self.animated = self.data["animated"]
        if self.animated:
            self.aniFrames = self.properties["animation"]["frames"]
            self.aniDelta = self.properties["animation"]["delta"]
            self.aniCurrentFrame = 0
            self.aniCurrentFrameDelta = 0

        # On spritesheet
        if self.animated:
            self.onSpriteSheet = True
        else:
            self.onSpriteSheet = self.data["onSpriteSheet"]
        
        # Spritesheet properties
        if self.onSpriteSheet:
            # Size on spritesheet
            self.sSize = self.data["sSize"]

            # Position on spritesheet
            self.sPos = self.data["sPos"]

        # Load and resize
        if self.onSpriteSheet:
            self.sRect = pygame.Rect(self.sPos, self.sSize)
            if self.animated:
                self.images = spritesheet.Spritesheet(self.absPath).load_strip(self.sRect, self.aniFrames)
                self.images = [pygame.transform.scale(i, self.rSize) for i in self.images]
            else:
                self.image = pygame.transform.scale(spritesheet.Spritesheet(self.absPath).image_at(self.sRect), self.rSize)
        else:
            self.image = pygame.transform.scale(pygame.image.load(self.absPath).convert_alpha(), self.rSize)
        
        # Rect
        if self.animated:
            self.rect = self.images[0].get_rect()
        else:
            self.rect = self.image.get_rect()

        # Draw options
        self.drawConfigured = False
        self.exportSurface = None
        self.exportPosition = None
        self.exportScale = None

    def setOutput(self, surface, position):
        self.exportSurface = surface
        self.exportPosition = position
        self.drawConfigured = True
    
    def update(self, delta = 0):
        result = None
        if self.animated:
            result = self.updateAnimated(delta)
        else:
            result = self.updateStandard(delta)
        
        if self.drawConfigured:
            self.exportSurface.blit(result, self.exportPosition)
        
        return result

    def updateAnimated(self, delta):
        self.aniCurrentFrameDelta += delta

        # If it is time for a new frame
        if self.aniCurrentFrameDelta >= self.aniDelta:
            tempRatio = self.aniCurrentFrameDelta // self.aniDelta
            self.aniCurrentFrameDelta -= self.aniDelta * tempRatio
            self.aniCurrentFrame += tempRatio

            # If it is time to restat animation
            if self.aniCurrentFrame >= self.aniFrames:
                tempRatio = self.aniCurrentFrame // self.aniFrames
                self.aniCurrentFrame -= self.aniFrames + tempRatio
        
        return self.images[self.aniCurrentFrame]
    
    def updateStandard(self, delta = 0):
        return self.image
    
    def getName(self):
        return self.data["name"]
    
    def getSpriteData(self):
        return self.data

    def instantiateGameObject(self):
        '''
        Quick way to instansiate new game objects of this spriteType without loading assets again
        '''
        return

class Tile(BaseType):
    def __init__(self, spriteData):
        super().__init__(spriteData)

        # Blocking
        if "blocking" in self.properties:
            self.blocking = self.properties["blocking"]
        else:
            self.blocking = False

        # Hitbox (might need to be changed to self.rect since group collisions might use that)
        if self.blocking:
            if "hitbox" in self.properties:
                self.relativeHitbox = pygame.Rect(self.properties["hitbox"])
            else:
                self.relativeHitbox = pygame.Rect(0, 0, self.rSize[0], self.rSize[1])

    def instantiateGameObject(self):
        pass