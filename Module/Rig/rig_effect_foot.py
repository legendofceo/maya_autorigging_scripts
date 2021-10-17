import maya.cmds as cmds

import rig_gizmo as RIG_GIZMOS
reload(RIG_GIZMOS)

import rigutils as RIGUTILS
reload(RIGUTILS)

class new():
 
    def go(self, joints, handle_foot_id, handle_toe_id, helper_toe_base, helper_toe, helper_ball, helper_wiggle, control_leg, handle_leg):

        self.handle_foot = handle_foot_id
        self.handle_toe = handle_toe_id

        cmds.ikHandle(sj=joints[0], ee=joints[1], n=self.handle_foot, solver='ikSCsolver')
        cmds.ikHandle(sj=joints[1], ee=joints[2], n=self.handle_toe, solver='ikSCsolver')
        
        #0 = toe
        #1 = ball
        #2 = wiggle
    
        #helpers.append(self.id+'_helper_toe'+self.symsuf)
        #helpers.append(self.id+'_helper_ball'+self.symsuf)
        #helpers.append(self.id+'_helper_wiggle'+self.symsuf)
        
        self.helper_toe_base = helper_toe_base
        self.helper_toe = helper_toe
        self.helper_ball = helper_ball
        self.helper_wiggle = helper_wiggle
    
        cmds.spaceLocator(n=self.helper_toe_base)
        cmds.matchTransform(self.helper_toe_base,joints[1])

        cmds.spaceLocator(n=self.helper_toe)
        cmds.matchTransform(self.helper_toe,joints[1])
        cmds.parent(helper_toe,helper_toe_base)

        cmds.spaceLocator(n=self.helper_ball )
        cmds.matchTransform(self.helper_ball,joints[1])

        cmds.spaceLocator(n=self.helper_wiggle )
        cmds.matchTransform(self.helper_wiggle, joints[1])


        cmds.parent(self.helper_toe_base,control_leg)    
        cmds.parent(self.handle_foot, self.helper_toe)
        cmds.parent(self.helper_wiggle, self.helper_toe)
        cmds.parent(self.handle_toe, self.helper_wiggle)    
        cmds.parent(self.helper_ball, self.helper_toe)    
        cmds.parent(handle_leg, self.helper_ball)