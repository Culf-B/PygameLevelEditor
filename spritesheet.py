import pygame
pygame.init()

import catcher

class Spritesheet:
    '''A class to handle loading images from a spritesheet'''
    # Slightly modified code from https://www.reddit.com/r/pygame/comments/lervbm/comment/joz32eq
    @catcher.catchFatal
    def __init__(self, path):
        '''Load spritesheet at the specified path'''

        self.spritesheet = pygame.image.load(path).convert_alpha()

    def image_at(self, rect):
        """Load a specific image from a specific rectangle."""
        image = pygame.Surface(rect.size).convert_alpha()
        image.blit(self.spritesheet, (0, 0), rect)
        return image

    def images_at(self, rects):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect) for rect in rects]

    def load_strip(self, rect, image_count):
        """Load a whole strip of images, and return them as a list."""
        tups = [rect.move(x * rect.width)
                for x in range(image_count)]
        return self.images_at(tups)