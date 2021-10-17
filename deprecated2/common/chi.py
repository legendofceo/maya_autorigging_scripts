import maya.cmds as cmds
import maya.mel as mel

class chi_h8():
    
    def __init__(self,target_bone):
        self.id = 'chi'
        cmds.polyPlane(n=self.id, w=0.0001,h=0.0001)
        cmds.matchTransform(self.id,target_bone)
        cmds.skinCluster(self.id,target_bone, name=self.id+'_scl')
        mel.eval("polyNormal -normalMode 2 -userNormalMode 0 -ch 1 "+self.id+";")
        
    def delete(self):
        cmds.delete(self.id)
        
    def get(self):
        return self.id