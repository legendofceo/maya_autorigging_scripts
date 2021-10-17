import maya.cmds as cmds

import sys
sys.path.append(r'O:\one\tools\maya\common')

import common_test 
reload(common_test)

common_test.fuck()

#chi = 'chi'
#cmds.polyPlane(n=chi, w=0.00001,h=0.00001)
#cmds.matchTransform(chi,'hip')
#cmds.skinCluster(chi,'hip', name=chi+'_scl')

#print(os.environ['MAYA_SCRIPT_PATH'])