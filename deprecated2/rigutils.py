import maya.cmds as cmds

def set_color(id,rgb):        
    cmds.setAttr(id+'.overrideEnabled', 1)
    cmds.setAttr(id+'.overrideRGBColors', 1)
    cmds.setAttr(id+'.overrideColorR', rgb[0])
    cmds.setAttr(id+'.overrideColorG', rgb[1])
    cmds.setAttr(id+'.overrideColorB', rgb[2])
    cmds.setAttr(id+'.overrideShading', 0)

def bind_twist(j,end,div):
    cmds.expression(s=j+'.rotateX='+end+'.rotateX/'+str(div))
def copy_joint_chain(joints,copy_names):
    par = cmds.listRelatives(joints[0], p=True)
    new_joints = []

    for j,n in zip(joints, copy_names): 
        cmds.joint(p=(0, 0, 0),n=n )
        cmds.setAttr(n+'.jointOrientX',cmds.getAttr(j+'.jointOrientX'))
        cmds.setAttr(n+'.jointOrientY',cmds.getAttr(j+'.jointOrientY'))
        cmds.setAttr(n+'.jointOrientZ',cmds.getAttr(j+'.jointOrientZ'))
        cmds.setAttr(n+'.rotateOrder',cmds.getAttr(j+'.rotateOrder'))
        cmds.setAttr(n+'.translateX',cmds.getAttr(j+'.translateX'))
        cmds.setAttr(n+'.translateY',cmds.getAttr(j+'.translateY'))
        cmds.setAttr(n+'.translateZ',cmds.getAttr(j+'.translateZ'))
        cmds.setAttr(n+'.rotateX',0)
        cmds.setAttr(n+'.rotateY',0)
        cmds.setAttr(n+'.rotateZ',0)        
        new_joints.append(n)   
    cmds.parent(new_joints[0],par,r=True)
    return new_joints

def match_joint_orientation(target,goal):
    cmds.setAttr(target+'.jointOrientX',cmds.getAttr(goal+'.jointOrientX'))
    cmds.setAttr(target+'.jointOrientY',cmds.getAttr(goal+'.jointOrientY'))
    cmds.setAttr(target+'.jointOrientZ',cmds.getAttr(goal+'.jointOrientZ'))
    cmds.setAttr(target+'.rotateOrder',cmds.getAttr(goal+'.rotateOrder'))    
    cmds.setAttr(target+'.rotateX',0)
    cmds.setAttr(target+'.rotateY',0)
    cmds.setAttr(target+'.rotateZ',0)  
        
        
def joint_clone(target,j):
    par = cmds.listRelatives(target,p=True)[0]
    cmds.joint(n=j)
    cmds.matchTransform(j,target)
    cmds.parent(j,par)

def helper_clone(target,j):
    par = cmds.listRelatives(target,p=True)[0]
    cmds.spaceLocator(n=j)
    cmds.matchTransform(j,target)
    cmds.parent(j,par)


def set_joints_color(j,rgb):
    for j in chain:
        RIGUTILS.set_color(j,rgb)
    return chain


def connect_xform(target,goal,translate,rotate,scale):

    if translate == True:
    	cmds.connectAttr(target+'.translate',goal+'.translate')
    if rotate == True:
    	cmds.connectAttr(target+'.rotate',goal+'.rotate')
    if scale == True:
    	cmds.connectAttr(target+'.scale',goal+'.scale')

def make_pin(name,target):
        cmds.spaceLocator(name=name)    
        cmds.setAttr(name+'Shape.visibility',0)
        cmds.matchTransform(name,target)
        cmds.parent(name,target)
        return name

def constraint(to,target,pos,rot,scale):
    if pos==True:
        cmds.pointConstraint(to,target,mo=True,w=1.0)
    if rot==True:
        cmds.orientConstraint(to,target,mo=True,w=1.0)
    if scale==True:
        cmds.scaleConstraint(to,target,mo=True,w=1.0)