import maya.cmds as cmds
import maya.mel as mel

def faces(node,tile):
    sel = node
    
    # Change these variables to the range you want
    minV=tile-1
    minU=0
    maxV=tile
    maxU=1
    
    # This is an empty variable to collect UV we want to select
    tmpBuffer = []
    
    if sel :                                        # Proceed if something is selected otherwise warn user
        for i in sel :                              # for each object selected
            uvNum = cmds.polyEvaluate(i, uv=1)        # Find how many UVs in the object
    
            if uvNum :                              # and if there is UV on the object
                for u in range(uvNum) :             # For each UV
                    # Find their position in UV Layout
                    uvPos = cmds.polyEditUV("%s.map[%d]" % (i, u), q=1) 
                    
                    # and if it is sitting in the UV range given above
                    if uvPos[0] > minU and uvPos[0] < maxU and uvPos[1] > minV and uvPos[1] < maxV : 
                        # Store their name in the variable we set earlier
                        tmpBuffer.append("%s.map[%d]" % (i, u)) 
    
        # and if the variable is not empty
        if tmpBuffer : 
            # Select those UV within the range                
            cmds.select(tmpBuffer, r=1) 
    
    else :
        cmds.warning("Nothing Selected....")
      
    verts = cmds.ls(selection=True)  
    return cmds.polyListComponentConversion(verts, fuv=True, tf=True, internal=True )
    
    
    
def trim_and_clean(faces):
    cmds.select(faces,r=True)
    mel.eval("invertSelection;") 
    cmds.delete()