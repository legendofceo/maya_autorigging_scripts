import maya.cmds as cmds

class new():
 
    def go(self,hub,chain_base,chain_fk,chain_ik,ctr_fk,ctr_ik):
        dv = 1.0
            
        cmds.addAttr(hub, ln='kinematics_switch',nn='FK -> IK', keyable=True, r=True, hidden=False, dv=dv, min=0.0, max=1.0)    
        cmds.addAttr(hub, ln='fkvis',nn='FK Visibility', keyable=True, r=True, hidden=False, dv=True)
        cmds.addAttr(hub, ln='ikvis',nn='IK Visibility', keyable=True, r=True, hidden=False, dv=True)  
        cmds.addAttr(hub, ln='ik',nn='IK', keyable=True, r=True, hidden=True, dv=1.0, min=0.0, max=1.0)
        cmds.addAttr(hub, ln='fk',nn='FK', keyable=True, r=True, hidden=True, dv=0.0, min=0.0, max=1.0)
        
        cmds.expression(s=hub+".ik = "+hub+".kinematics_switch")
        cmds.expression(s=hub+".fk = 1 - "+hub+".kinematics_switch")
        
        
        for base,fk,ik in zip(chain_base,chain_fk,chain_ik):
            cmds.orientConstraint(fk, base, mo=True,w=0)
            cmds.orientConstraint(ik, base, mo=True,w=0)
        
            cmds.connectAttr(hub+'.fk',base+'_orientConstraint1.'+fk+'W0' )
            cmds.connectAttr(hub+'.ik',base+'_orientConstraint1.'+ik+'W1' )
      
    
        for ctr in ctr_fk:
            cmds.connectAttr(hub+'.fkvis',ctr+'.visibility')
        
        for ctr in ctr_ik:
            cmds.connectAttr(hub+'.ikvis',ctr+'.visibility')