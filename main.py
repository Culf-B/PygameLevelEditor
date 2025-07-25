import pygame
pygame.init()

import projectManager
import gui

screen = pygame.display.set_mode([1600, 900], pygame.RESIZABLE)
pygame.display.set_caption("Pygame Level Editor")
clock = pygame.time.Clock()
run = True

pm = projectManager.ProjectManager()
gm = gui.Gui(screen, pm)

while run:
    delta = clock.tick(60)
    deltaInSec = delta / 1000
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False

    screen.fill([0, 0, 0])

    gm.draw(events, deltaInSec)

    pygame.display.update()