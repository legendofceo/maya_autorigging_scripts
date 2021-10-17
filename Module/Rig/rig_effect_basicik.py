import maya.cmds as cmds

class new():
           
    def setup(self,j,handle,solver):
        self.joints = j
        self.handle = handle
        self.solver = solver
        return self
                        
    def go(self):              
        cmds.ikHandle(sj=self.joints[0], ee=self.joints[2], n=self.handle, solver=self.solver )               
        return