import maya.cmds as cmds

def duplicateJointChain(joints,prefix): 
    par = cmds.listRelatives(joints[0], p=True)
    
    newJoints = []
    
    for j in joints: 
        joi = cmds.joint( p=(0, 0, 0),n="NEWJOINT" )
        newName = prefix+j
        cmds.matchTransform(joi,j)
        cmds.rename(joi,newName)
        newJoints.append(newName)       
        
    print(par)
    cmds.parent(newJoints[0],par)
    return newJoints
    
def make_stretch_ik(name,spline_chain,lower_control, upper_control):
    original_chain = spline_chain
    spline_chain = duplicateJointChain(spline_chain, prefix='ikSpine_')
    num = len(spline_chain)
    cmds.select(cl=True)
    ikh, effector, curve = cmds.ikHandle(name='{0}_ikh'.format(name), startJoint=spline_chain[0], endEffector=spline_chain[num-1], solver='ikSplineSolver')
    
    cmds.select(cl=True)
    start_joint = cmds.joint(n='joint_start')
    cmds.select(cl=True)
    end_joint = cmds.joint(n='joint_end')
    cmds.select(cl=True)
    cmds.matchTransform(start_joint,joints[0])
    cmds.matchTransform(end_joint,joints[num-1])
    
    cmds.skinCluster(start_joint, end_joint, curve, name='{0}_scl'.format(name), tsb=True)
    
    
    cmds.parentConstraint(lower_control,start_joint,mo=True)
    cmds.parentConstraint(upper_control,end_joint,mo=True)
    
    # Create stretch network
    curve_info = cmds.arclen(curve, constructionHistory=True)
    

    mdn = cmds.createNode('multiplyDivide', name='{0}Stretch_mdn'.format(name))
    cmds.connectAttr('{0}.arcLength'.format(curve_info), '{0}.input1X'.format(mdn))
    cmds.setAttr('{0}.input2X'.format(mdn), cmds.getAttr('{0}.arcLength'.format(curve_info)))
    cmds.setAttr('{0}.operation'.format(mdn), 2)  # Divide
 
    # Connect to joints
    for joint in spline_chain[1:]:
        tx = cmds.getAttr('{0}.translateZ'.format(joint))
        mdl = cmds.createNode('multDoubleLinear', name='{0}Stretch_mdl'.format(joint))
        cmds.setAttr('{0}.input1'.format(mdl), tx)
        cmds.connectAttr('{0}.outputX'.format(mdn), '{0}.input2'.format(mdl))
        cmds.connectAttr('{0}.output'.format(mdl), '{0}.translateZ'.format(joint))
 
    # Setup advanced twist
    cmds.setAttr('{0}.dTwistControlEnable'.format(ikh), True)
    cmds.setAttr('{0}.dWorldUpType'.format(ikh), 4)  # Object up
    cmds.setAttr('{0}.dWorldUpAxis'.format(ikh), 0)  # Positive Y Up
    cmds.setAttr('{0}.dWorldUpVectorX'.format(ikh), 0)
    cmds.setAttr('{0}.dWorldUpVectorY'.format(ikh), 1)
    cmds.setAttr('{0}.dWorldUpVectorZ'.format(ikh), 0)
    cmds.setAttr('{0}.dWorldUpVectorEndX'.format(ikh), 0)
    cmds.setAttr('{0}.dWorldUpVectorEndY'.format(ikh), 1)
    cmds.setAttr('{0}.dWorldUpVectorEndZ'.format(ikh), 0)
    cmds.connectAttr('{0}.worldMatrix[0]'.format(lower_control), '{0}.dWorldUpMatrix'.format(ikh))
    cmds.connectAttr('{0}.worldMatrix[0]'.format(upper_control), '{0}.dWorldUpMatrixEnd'.format(ikh))
 
    # Constrain original chain back to spline chain

    for ik_joint, joint in zip(spline_chain, original_chain):
        if joint == end_joint:
            cmds.pointConstraint(ik_joint, joint, mo=True)
            cmds.orientConstraint(upper_control, joint, mo=True)
        else:
            cmds.parentConstraint(ik_joint, joint)
    
 
joints = ['joint1','joint2','joint3','joint4']
make_stretch_ik('spine',joints,'c_start','c_end');