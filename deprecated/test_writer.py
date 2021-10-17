import maya.cmds as cmds

cmds.file('C:/Users/16C24E/Desktop/Final Character/0070_weights.mb', o=True, f=True)


def copy_joint_attributes(name,target):
    cmds.setAttr(name+'.jointOrientX',cmds.getAttr(target+'.jointOrientX'))
    cmds.setAttr(name+'.jointOrientY',cmds.getAttr(target+'.jointOrientY'))
    cmds.setAttr(name+'.jointOrientZ',cmds.getAttr(target+'.jointOrientZ'))
    cmds.setAttr(name+'.rotateOrder',cmds.getAttr(target+'.rotateOrder'))
    cmds.setAttr(name+'.translateX',cmds.getAttr(target+'.translateX'))
    cmds.setAttr(name+'.translateY',cmds.getAttr(target+'.translateY'))
    cmds.setAttr(name+'.translateZ',cmds.getAttr(target+'.translateZ'))
    cmds.setAttr(name+'.rotateX',0)
    cmds.setAttr(name+'.rotateY',0)
    cmds.setAttr(name+'.rotateZ',0)


def color_joint(name,rgb):
    cmds.setAttr(name+'.overrideEnabled', 1)
    cmds.setAttr(name+'.overrideRGBColors', 1)
    cmds.setAttr(name+'.overrideColorR', rgb[0])
    cmds.setAttr(name+'.overrideColorG', rgb[1])
    cmds.setAttr(name+'.overrideColorB', rgb[2])
    
def duplicate_joint(target,name,nopar=False):
    
    if nopar==True:
        cmds.select(cl=True)
        
    cmds.joint( p=(0, 0, 0),n=name )
    copy_joint_attributes(name,target)
    return name    
     
def duplicate_joints(joints,new_joints): 
    par = cmds.listRelatives(joints[0], p=True)    
    new_arr = []
    
    for j,n in zip(joints, new_joints): 
        n = duplicate_joint(j,n)
        
        new_arr.append(n)       
    cmds.parent(new_arr[0],par,r=True)
    return new_arr


suf = '_r'
upperarm = ['upperarm'+suf,'upperarm_twist1'+suf,'upperarm_twist2'+suf,'upperarm_twist3'+suf,'lowerarm'+suf]
upperarm_goals = ['armuptwist_upperarm_goal'+suf,'armuptwist_upperarm_twist1_goal'+suf,'armuptwist_upperarm_twist2_goal'+suf,'armuptwist_upperarm_twist3_goal'+suf,'armuptwist_lowerarm_goal'+suf]
lowerarm = ['lowerarm'+suf,'lowerarm_twist1'+suf,'lowerarm_twist2'+suf,'lowerarm_twist3'+suf,'hand'+suf]
lowerarm_goals = ['armdntwist_lowerarm_goal'+suf,'armdntwist_lowerarm_twist1_goal'+suf,'armdntwist_lowerarm_twist2_goal'+suf,'armdntwist_lowerarm_twist3_goal'+suf,'armdntwist_hand_goal'+suf]

#chain_upper = duplicate_joints(upperarm, upperarm_goals)
#chain_lower = duplicate_joints(lowerarm, lowerarm_goals)


num = len(upperarm)
cmds.joint( p=(0, 0, 0),n=upperarm_goals[0] )
copy_joint_attributes(upperarm_goals[0],upperarm[0])
cmds.parent(upperarm_goals[0],'clavicle'+suf,r=True)
color_joint(upperarm[0],[0,0,255])
 
for i in range(num-1):
    cmds.select(cl=True)
    cmds.joint( p=(0, 0, 0),n=upperarm_goals[i+1] )
    cmds.parent(upperarm_goals[i+1],upperarm_goals[0])
    color_joint(upperarm_goals[i+1],[0,0,255])
    copy_joint_attributes(upperarm_goals[i+1],upperarm[i+1])

num = len(upperarm)
cmds.joint( p=(0, 0, 0),n=lowerarm_goals[0] )
copy_joint_attributes(lowerarm_goals[0],lowerarm[0])
cmds.parent(lowerarm_goals[0],'upperarm'+suf,r=True)
color_joint(lowerarm_goals[0],[255,0,0])

for i in range(num-1):
    cmds.select(cl=True)
    cmds.joint( p=(0, 0, 0),n=lowerarm_goals[i+1] )
    cmds.parent(lowerarm_goals[i+1],lowerarm_goals[0])
    color_joint(lowerarm_goals[i+1],[255,0,0])
    copy_joint_attributes(lowerarm_goals[i+1],lowerarm[i+1])    
 
  
note = 'arm_twist_note_start'
cmds.joint(n=note, p=(0,0,0))
cmds.matchTransform(note,'upperarm'+suf)
cmds.parent(note,'upperarm'+suf)
color_joint(note,[255,255,0])
note_start = note

note = 'ww'
cmds.joint(n=note, p=(0,0,0))
cmds.matchTransform(note,'lowerarm'+suf)
cmds.parent(note,'lowerarm'+suf)
color_joint(note,[255,255,0])
note_mid = note

note = 'arm_twist_note_end'
cmds.joint(n=note, p=(0,0,0))
cmds.matchTransform(note,'hand'+suf)
cmds.parent(note,'hand'+suf)
color_joint(note,[255,255,0])
note_end = note

     
loc = cmds.xform('upperarm'+suf,q=True,t=True,a=True,ws=True)
loc2 = cmds.xform('lowerarm'+suf,q=True,t=True,a=True,ws=True)

upper_curve = 'upperarm_twist_curve'+suf
lower_curve = 'lowerarm_twist_curve'+suf

#cmds.curve(n=upper_curve,p=[(loc[0],loc[1],loc[2]),(loc2[0],loc2[1],loc2[2])], d=1)

#loc3 = cmds.xform('hand'+suf,q=True,t=True,a=True,ws=True)
#cmds.curve(n=lower_curve,p=[(loc2[0],loc2[1],loc2[2]),(loc3[0],loc3[1],loc3[2])], d=1)

ikh, effector, upper_curve = cmds.ikHandle(sj=upperarm_goals[0], ee=upperarm_goals[4], solver='ikSplineSolver',ccv=True )
ikh, effector, lower_curve = cmds.ikHandle(sj=lowerarm_goals[0], ee=lowerarm_goals[4], solver='ikSplineSolver',ccv=True )

cmds.skinCluster(note_start, note_mid, upper_curve, name='{0}_scl'.format('FUCK'), tsb=True)
cmds.skinCluster(note_mid, note_end, lower_curve, name='{0}_scl'.format('FUCK2'), tsb=True)
