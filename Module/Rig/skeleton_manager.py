import maya.cmds as cmds

class skeleton_filterable_joint():

    def __init__(self,id):
        self.id = id
        self.groups = []

    def g(self,groupid):
        self.groups.append(groupid)

class new():

    def __init__(self):
        self.j = []

    def add(self,id):        
        j = skeleton_filterable_joint(id);
        self.j.append(j)
        return j

    def select_all(self):

        for j in self.j:
            cmds.select(j.id,add=True)