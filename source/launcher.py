import sqhUniversal.currentProject as cp
import sqhUniversal.pathmap as pathmap
import os
import maya.cmds as cmd

def launchPlaybetter():
    pPath = "production\_misc_data\scripts\playBetter.py"
    name = cp.load_current_project_name_from_file()
    m = pathmap.PipeMap()
    path = m.generate_path([m.storage_projects, name])
    filePath = os.path.normpath(os.path.join(path, pPath))
    execfile(filePath)
    
launchPlaybetter()