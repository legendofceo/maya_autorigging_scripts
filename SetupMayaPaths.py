import maya.cmds as cmds

GVAR_ONEPATH = 'O:\\sword\\'

import sys
sys.path.append(r''+GVAR_ONEPATH+'Scripts\\Maya\\Module\\Common\\')
sys.path.append(r''+GVAR_ONEPATH+'Scripts\\Maya\\Module\\Rig\\')
sys.path.append(r''+GVAR_ONEPATH+'Scripts\\Maya\\Module\\Tools\\')

print("WORKED")

def onMayaDroppedPythonFile(args):

	print("InitializingPaths")

