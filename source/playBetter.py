import os
import subprocess
import maya.cmds as cmd
import maya.mel
import getpass
from shutil import copy2

class playBetterWindow(object):   

    def get_project_name(self):
	    return "copain"    
	    
    def get_project_path(self):
    	return os.path.realpath("Z:\marza\proj")	
    	
    def __init__(self):
        self.pLabel = 'This is not an animation file'
        self.enAB = False
        self.name = 'playBetter'
        self.windowSize = [185, 175]

        if (os.path.abspath(cmd.file(q=True, sn=True)).split(os.sep)[-3] == 'anim'):
            self.pLabel = 'PlayBetter'
            self.enAB = True

        if cmd.window(self.name, exists = True):
        	cmd.deleteUI(self.name)

        window = cmd.window(self.name, title = self.name, s = 0, mnb = 0, mxb = 0, widthHeight=(self.windowSize[0], self.windowSize[1]))
        options = ["playblast", "playImages","convertToMovie","playMovie", "copyToDailies"]
        imgType = ['png','jpg','gif','tga']
        movType = ['mp4','mov','avi','wmv']
        thisproj = self.get_project_name()
        projs = [thisproj]
        for one in os.listdir(self.get_project_path()):
            if one is not thisproj:
                projs.append(one)
        cmd.columnLayout("mainColumn", adjustableColumn=True, bgc= [0.2, 0.2, 0.2] )
        cmd.rowColumnLayout("projLayout", nc = 2, bgc= [0.2, 0.2, 0.2], parent = 'mainColumn')
        cmd.rowColumnLayout("mainRows", nc = 2, bgc= [0.2, 0.2, 0.2], parent = 'mainColumn')
        cmd.columnLayout("buttonColumn", adjustableColumn=True, bgc= [0.2, 0.2, 0.2], parent = 'mainRows' )
        projButton = cmd.optionMenu('project', l = 'project:', parent = 'projLayout', en = self.enAB)

        for one in projs:
            cmd.menuItem(label = one)

        cmd.columnLayout("dropColumn", adjustableColumn=True, bgc= [0.2, 0.2, 0.2], parent = 'mainRows' )

        for one in options:
            check = 1
            if one in ["playImages", "playMovie"]: 
                check = 0             
            cmd.checkBox(one, l = one, parent = "buttonColumn", v = check, en = self.enAB)
        cmd.optionMenu('imgType', l='', parent = 'dropColumn', en = self.enAB)

        for one in imgType:
            cmd.menuItem( label= one)

        cmd.text(l='')
        cmd.optionMenu('movType', l='', parent = 'dropColumn', en = self.enAB)

        for one in movType:
            cmd.menuItem( label= one )
        cmd.text('message', l='', parent = 'mainColumn')
        cmd.button( label=self.pLabel, parent = "mainColumn", command = self.playBetterGUI, en = self.enAB)
        cmd.button( label='Close', parent = "mainColumn", command=('cmd.deleteUI(\"' + window + '\", window=True)') )
        cmd.showWindow( self.name )
        gMainWindow = maya.mel.eval('$tmpVar=$gMainWindow')
        cmd.window( self.name, edit=True, widthHeight=(self.windowSize[0], self.windowSize[1]) ) 	
        
    def alert(self, color = 'green', guiElement = 'playBetter|mainColumn', message =''):
        colors = {
        'red':[1.0,0.0,0.0],
        'orange':[0.8,0.4,0.0],
        'green':[0.0,1.0,0.0],
        'blue':[0.0,0.0,1.0],
        'grey': [0.2,0.2,0.2]}
        newColor = colors.setdefault(color, [0.2,0.2,0.2])
        cmd.columnLayout(guiElement, e=True, bgc= (newColor[0],newColor[1],newColor[2]))
        cmd.text(guiElement+'|message', e=True, l= (message))
        cmd.refresh()  
        
    def playBetterGUI(self, *args, **kwds):
    	vals = [0,0,0,0,0]
    	ops = ["playblast", "playImages","convertToMovie","playMovie", "copyToDailies"]
    	drops = ['imgType','movType']
    	window = 'playBetter'
    	dropVals = []
    	for one in drops:
    		dropMenu = '%s|%s|%s' %(window, 'mainColumn|mainRows|dropColumn', one)
    		dropVals.append(cmd.optionMenu(dropMenu, q=True, v=True))  
    	for one in range (0,5):
    		go = one+1
    		checkbox = '%s|%s|%s' %(window, 'mainColumn|mainRows|buttonColumn', ops[one])
    		if (cmd.checkBox(checkbox, q = True, v = True)):
    			self.alert(color= 'orange', message = ('Please Wait, doing '+ops[one]))  
    			self.playBetter(go, imgType  = dropVals[0], movType = dropVals[1])
    	self.alert(color= 'grey', message = '') 
    	
    def playBetter(self, go = 0, scale=100.0, imgCommand = 'nul', movCommand = 'nul', imgFilePath = 'nul', firstImg = 'nul', lastImg = 'nul', imgType='png', movType = 'mp4'): 
        fpsDict = {'ntsc': 30, 'film': 24, 'pal': 25}
        fps = fpsDict[cmd.currentUnit(q = True, t = True)]
        width = cmd.getAttr('defaultResolution.width')
        height = cmd.getAttr('defaultResolution.height')
        curPath = cmd.file(q=True, sn=True)
        get = self.get_project_path()
        proj = self.get_project_name()
        dirs = os.path.abspath(curPath).split(os.sep)
        root = os.path.realpath(os.path.join(dirs[0],dirs[1]))
        seq = dirs[-7]
        shot = dirs[-6]
        fileName = dirs[-1]
        fileBase = os.path.splitext(fileName)[0]
        curFile = os.path.splitext(curPath)[0]
        version = curFile.split('_')[-1]
        dailies = os.path.realpath(os.path.join (get, proj, 'movie','check',getpass.getuser()))
        movPath = os.path.realpath(os.path.join (get, proj, 'shot', seq, shot, 'movies', str(version)))
        imgPath = os.path.realpath(os.path.join (get, proj, 'shot', seq, shot, 'images', str(version)))
        for path in (movPath, imgPath, dailies):
            if not os.path.isdir(path): 
                print "Creating dir " + path
                os.makedirs(path)
        movFile = os.path.join (movPath, fileName.replace('.ma', '.%s' % movType))  
        curMov = fileBase.replace(version, ('cur.'+movType))
        playMov = 'ffplay '+movFile
        if go==1:
            #turn off nurbs curves - replace with store and restore
            panels= []
            getPanels = cmd.getPanel(all=True)
            for panel in getPanels:
                if panel.startswith('model'):
                    cmd.modelEditor(panel, e=True, nc=False)
            cmd.select(clear = True)
            pb = cmd.playblast(v=0,format='image', filename=os.path.join(imgPath, fileBase), sqt=0, os=True, fp=4, p=scale, c=imgType, wh=[width, height])
        imageFiles = []
        
        for file in sorted(os.listdir(imgPath)):
        	if file.endswith(imgType):
        		imageFiles.append(file)
        if len(imageFiles):
            imgFilePath = os.path.join (imgPath,fileBase+'.%04d.'+imgType)
            movCommand = 'ffmpeg -y -i %s -r %s -s %sx%s %s' % (imgFilePath, str(fps), width, height, movFile)
            imgCommand = 'djv_view '+os.path.join(imgPath, imageFiles[0])+' -playback_speed '+ str(fps)
           
            if go==2:
                try:
                    subprocess.Popen(imgCommand, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True )
                except:        
                    alert(color= 'red', message = ('djv_view problem'))             
            if go==3:
                print movCommand
                try:
                    subprocess.call(movCommand, shell = True)
                    print movFile
                except subprocess.CalledProcessError as e:
                    raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))    
                    alert(color= 'red', message = 'problem')        
            elif go==4:
                subprocess.Popen(playMov, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True )
            elif go==5:
                if os.path.isfile(movFile): 
                    copy2(movFile, dailies)
                    copy2(movFile, os.path.join(dailies, curMov))
                    print movFile
                    print (os.path.join(dailies, curMov))
                    #copyfile(movFile, cur) 
                         
        if not go:
            for all in curPath, curFile, movPath, movFile, imgPath, movCommand, imgCommand, playMov, dailies:
                print all
                