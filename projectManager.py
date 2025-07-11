import os
import subprocess
import platform
import json
import shutil
import pygame

import spriteTypes

class ProjectManager:
    """
    Manage projects (duh)
    """
    def __init__(self, projectsRelPath = "projects", pathToHere = os.path.abspath(os.path.dirname(__name__))):
        self.projectsRelPath = projectsRelPath
        self.pathToHere = pathToHere
        self.absProjectsPath = os.path.join(self.pathToHere, projectsRelPath)

        if not os.path.exists(self.absProjectsPath):
            os.mkdir(self.absProjectsPath)

        self.currentProjectName = None
        self.currentProject = None
        self.currentProjectPath = None
        self.currentProjectData = None

    def load(self, projectName):
        print(f'Loading project "{projectName}"...')
        self.currentProjectName = projectName
        self.currentProjectPath = os.path.join(self.absProjectsPath, projectName)
        with open(os.path.join(self.currentProjectPath, "project.json"), "r") as f:
            self.currentProjectData = json.load(f)

        self.currentProject = Project(
            self.currentProjectData["sprites"],
            self.currentProjectData["level"],
            self.currentProjectPath
        )

    def save(self):
        print("Saving not implemented!")

    def new(self, projectName):
        """
        Create a new empty project.

        :param projectName: Name of the project to create.
        """
        if self.doesProjectExist(projectName):
            print(f'Project with name "{projectName}" already exists!')
        else:
            self.tempPath = os.path.join(self.absProjectsPath, projectName)
            os.mkdir(self.tempPath)
            os.mkdir(os.path.join(self.tempPath, "assets"))

            with open(os.path.join(self.tempPath, "project.json"), "w") as f:
                json.dump(
                    {
                        "sprites": {},
                        "level": []
                    },
                    f,
                    indent = 2
                )
            self.currentProjectName = projectName
    
    def delete(self, projectName):
        """
        Delete an existing project.

        :param projectName: Name of the project to delete.
        """
        if self.doesProjectExist(projectName):
            shutil.rmtree(os.path.join(self.absProjectsPath, projectName))
        else:
            print(f'Project with name "{projectName}" does not exists!')

    def openInFileexplorer(self, projectName = None):
        """
        Open a project location in the file explorer.

        :param projectName: Name of the project to open.
        """
        if projectName == None:
            if self.projectSelected():
                projectName = self.getSelectedProject()
            else:
                print(f'No project selected!')
                return
            
        if self.doesProjectExist(projectName):
            self.tempPath = os.path.join(self.absProjectsPath, projectName)
            if platform.system() == "Windows": # WINDOWS
                os.startfile(self.tempPath)
            elif platform.system() == "Darwin": # MACOS
                subprocess.run(["open", self.tempPath])
            elif platform.system() == "Linux": # LINUX
                subprocess.run(["xdg-open", self.tempPath])
            else:
                print(f'OS "{platform.system()}" not supported!')
        else:
            print(f'Project with name "{projectName}" not found!')

    def doesProjectExist(self, projectName):
        if os.path.exists(os.path.join(self.absProjectsPath, projectName)):
            return True
        else:
            return False
        
    def projectSelected(self):
        if self.currentProjectName == None:
            return False
        else:
            return True
        
    def getSelectedProject(self):
        return self.currentProjectName
    
    def getSelectedProjectObject(self):
        return self.currentProject
    
    def getProjects(self):
        entries = os.listdir(self.absProjectsPath)
        folders = [entry for entry in entries if os.path.isdir(os.path.join(self.absProjectsPath, entry))]
        return folders

class Project:
    def __init__(self, sprites, level, path):
        self.sprites = pygame.sprite.Group()

        self.path = path

        for name, sprite in sprites.items():
            # Update sprite data
            sprite["name"] = name
            sprite["absPath"] = os.path.join(path, "assets", sprite["path"])

            # Create tiletype object
            if sprite["type"] == "tile":
                newsprite = spriteTypes.Tile(sprite)
                self.sprites.add(newsprite)
                print(f'Loaded sprite with name "{sprite["name"]}"')
            else:
                print(f'Invalid sprite type "{sprite["type"]}"!')

    def initSprite(self, name, spritedata):
        # Update sprite data
        spritedata["name"] = name
        spritedata["absPath"] = os.path.join(self.path, "assets", spritedata["path"])

        # Create tiletype object
        if spritedata["type"] == "tile":
            newsprite = spriteTypes.Tile(spritedata)
            self.sprites.add(newsprite)
            print(f'Loaded sprite with name "{spritedata["name"]}"')
            return 0 # No error
        else:
            print(f'Invalid sprite type "{spritedata["type"]}"!')
            return 1 # Error

    def update(self, delta = 0):
        self.sprites.update(delta)

    def updateSprite(self, sprite, newSpriteData):
        # Init sprite and remove old sprite if no error happens
        self.tempReturnStatus = self.initSprite(sprite.getName(), newSpriteData)
        if self.tempReturnStatus == 0:
            self.sprites.remove(sprite)
        return self.tempReturnStatus


    def getSprites(self):
        return self.sprites

if __name__ == "__main__":
    pygame.init()
    pm = ProjectManager()
