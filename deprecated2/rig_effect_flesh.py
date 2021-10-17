import maya.cmds as cmds

import rig_gizmo as RIG_GIZMOS
reload(RIG_GIZMOS)

import rigutils as RIGUTILS
reload(RIGUTILS)

class fatty_area():
           
    def go(self,joi,influence,helper,piv,goal,weight):              


        RIGUTILS.helper_clone(joi,helper)
        RIGUTILS.helper_clone(joi,piv)
        cmds.orientConstraint(helper,piv,mo=True,w=weight)
        cmds.orientConstraint(influence,piv,mo=True,w=1.0-weight)
        cmds.spaceLocator(n=goal)
        cmds.matchTransform(goal,joi)
        cmds.parent(goal,piv)

        self.joint = joi
        self.helper = helper
        self.piv = piv
        self.goal = goal

        return self