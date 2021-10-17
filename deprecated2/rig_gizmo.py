import maya.cmds as cmds


def set_color(id,rgb):        
        cmds.setAttr(id+'.overrideEnabled', 1)
        cmds.setAttr(id+'.overrideRGBColors', 1)
        cmds.setAttr(id+'.overrideColorR', rgb[0])
        cmds.setAttr(id+'.overrideColorG', rgb[1])
        cmds.setAttr(id+'.overrideColorB', rgb[2])
        cmds.setAttr(id+'.overrideShading', 0)



class gizmo():
    
    def set_parent(self,par):
        cmds.parent(self.space,par)
        return self

    def add_additive(self):
        self.additive = "additive_"+self.id
        cmds.spaceLocator(name=self.additive)    
        cmds.setAttr(self.additive+'Shape.visibility',0)
        par = cmds.listRelatives(self.id,p=True)[0]
        cmds.matchTransform(self.additive,self.id)
        cmds.parent(self.additive,par)
        cmds.parent(self.id,self.additive)
        return self

    def create_subspace_switch(self,helper,goal,switch_ln,switch_nn):
        cmds.spaceLocator(name=helper) 
        cmds.setAttr(helper+'Shape.visibility',0)
        cmds.matchTransform(helper,self.id)
        cmds.parent(helper,self.space)

        cmds.spaceLocator(name=goal) 
        cmds.setAttr(goal+'Shape.visibility',0)
        cmds.matchTransform(goal,self.id)
        cmds.parent(self.id,goal)
        cmds.parent(goal,self.space)
        cmds.parentConstraint(self.space,goal,mo=True,w=1.0)
        cmds.parentConstraint(helper,goal,mo=True,w=0.0)
        cmds.scaleConstraint(self.space,goal,mo=True,w=1.0)
        cmds.scaleConstraint(helper,goal,mo=True,w=0.0)

        cmds.addAttr(self.id, ln=switch_ln,nn=switch_nn, keyable=True, r=True, hidden=False, dv=1.0, min=0.0, max=1.0) 
        cmds.expression(s=goal+'_parentConstraint1.'+self.space+'W0 = 1.0 - '+self.id+'.'+switch_ln)
        cmds.expression(s=goal+'_scaleConstraint1.'+self.space+'W0 = 1.0 - '+self.id+'.'+switch_ln)
        cmds.expression(s=goal+'_parentConstraint1.'+helper+'W1 = '+self.id+'.'+switch_ln)
        cmds.expression(s=goal+'_scaleConstraint1.'+helper+'W1 = '+self.id+'.'+switch_ln)
        return self

    def freeze(self):
        cmds.makeIdentity(self.id, apply=True, t=1, r=1, s=1)
        
    def setup(self, id):
        self.id = id
        self.space = "space_"+self.id
        cmds.spaceLocator(name=self.space)    
        cmds.setAttr(self.space+'Shape.visibility',0)
        return self
    
    def attach_to_space(self,gizmo):
        cmds.matchTransform(gizmo,self.space)
        cmds.parent(gizmo,self.space)
        self.freeze()
        return self

    def match_to(self,goal):
        cmds.matchTransform(self.space,goal);
        return self

    def set_space_rotation(self,x,y,z):
          
        par = cmds.listRelatives(self.space,p=True)
        if par!=None:
            cmds.parent(self.space,w=True)
        if x != None:
            cmds.setAttr(self.space+'.rotateX', x)
        if y != None:
            cmds.setAttr(self.space+'.rotateY', y)
        if z != None:
            cmds.setAttr(self.space+'.rotateZ', z)
        if par!=None:
            cmds.parent(self.space,par,a=True) 
        self.freeze()
        return self

    def move_control_local(self,x,y,z,abs=False,movepivot=False):
        pos = cmds.xform(self.id, query=True, translation=True, worldSpace=True )
        if x != None:
            cmds.setAttr(self.id+'.translateX', cmds.getAttr(self.id+'.translateX')+x)
        if y != None:
            cmds.setAttr(self.id+'.translateY', cmds.getAttr(self.id+'.translateY')+y)
        if z != None:
            cmds.setAttr(self.id+'.translateZ', cmds.getAttr(self.id+'.translateZ')+z) 
           
        if movepivot==False:
            cmds.xform(self.id, ws=True, piv=(pos[0], pos[1], pos[2]) )
        self.freeze()
        return self

    def set_channel_enabled(self,translate=False,rotate=False,scale=False):
        
        if translate==False:
            cmds.setAttr(self.id+".tx",keyable=False,channelBox=False) 
            cmds.setAttr(self.id+".ty",keyable=False,channelBox=False)
            cmds.setAttr(self.id+".tz",keyable=False,channelBox=False) 
            cmds.transformLimits(self.id, tx=(0, 0), ty=(0, 0), tz=(0, 0), etx=(True, True), ety=(True, True), etz=(True, True ))

        if rotate==False:
            cmds.setAttr(self.id+".rx",keyable=False,channelBox=False) 
            cmds.setAttr(self.id+".ry",keyable=False,channelBox=False)
            cmds.setAttr(self.id+".rz",keyable=False,channelBox=False)
            cmds.transformLimits(self.id, rx=(0, 0), ry=(0, 0), rz=(0, 0), erx=(True, True), ery=(True, True), erz=(True, True ))

        if scale==False:
            cmds.setAttr(self.id+".sx",keyable=False,channelBox=False) 
            cmds.setAttr(self.id+".sy",keyable=False,channelBox=False)
            cmds.setAttr(self.id+".sz",keyable=False,channelBox=False)  
            cmds.transformLimits(self.id, sx=(1, 1), sy=(1, 1), sz=(1, 1), esx=(True, True), esy=(True, True), esz=(True, True ))
        return self

    def set_channel_rotation_enabled(self,x=False,y=False,z=False):
        
        if x==False:
            cmds.setAttr(self.id+".rx",keyable=False,channelBox=False) 
        if y==False:
            cmds.setAttr(self.id+".ry",keyable=False,channelBox=False) 
        if z==False:
            cmds.setAttr(self.id+".rz",keyable=False,channelBox=False) 
        return self

    def socket_control(self,socket,root,helper_root,helper_result):
        self.socket_target = socket
        par = cmds.listRelatives(socket,p=True)[0]
        cmds.spaceLocator(n=helper_result)
        cmds.spaceLocator(n=helper_root)
        cmds.parent(helper_root,root)
        cmds.matchTransform(helper_result,socket)
        cmds.parent(helper_result,par)
        cmds.parentConstraint(par,helper_result,mo=True,w=1.0)
        cmds.parentConstraint(helper_root,helper_result,mo=False,w=0.0)

        self.match_to(socket)
        self.set_parent(helper_result)

        cmds.addAttr(self.id, ln='socket_switch',nn='Parent -> Root', keyable=True, r=True, hidden=False, dv=1.0, min=0.0, max=1.0)    
        cmds.addAttr(self.id, ln='parent_goal',nn='ParentGoal', keyable=True, r=True, hidden=True, dv=1.0, min=0.0, max=1.0)
        cmds.addAttr(self.id, ln='root_goal',nn='RootGoal', keyable=True, r=True, hidden=True, dv=0.0, min=0.0, max=1.0)

        cmds.connectAttr(self.id+'.parent_goal',helper_result+'_parentConstraint1.'+str(par)+'W0' )
        cmds.connectAttr(self.id+'.root_goal',helper_result+'_parentConstraint1.'+helper_root+'W1' )

        cmds.expression(s=self.id+".parent_goal = "+self.id+".socket_switch")
        cmds.expression(s=self.id+".root_goal = 1 - "+self.id+".socket_switch")

        return self

    def constraint(self,target,pos,rot,scale):
        if pos==True:
            cmds.pointConstraint(self.id,target,mo=True,w=1.0)
        if rot==True:
            cmds.orientConstraint(self.id,target,mo=True,w=1.0)
        if scale==True:
            cmds.scaleConstraint(self.id,target,mo=True,w=1.0)
        return self

    def wire(self,target,pos,rot,scale):
        if pos==True:
            cmds.connectAttr(self.id+'.translate',target+'.translate')
        if rot==True:
            cmds.connectAttr(self.id+'.rotate',target+'.rotate')
        if scale==True:
            cmds.connectAttr(self.id+'.scale',target+'.scale')
        return self


class hoop(gizmo):
                   
    def __init__(self, id, rgb=[0,255,0],rad=2.0,hrad=.005,axis=[0,0,1],spans=4,sections=8,ssw=0,esw=360,degree=3):
        self.setup(id)
        cmds.torus(n=self.id, r=rad, hr=hrad, axis=axis,spans=spans,ssw=ssw,esw=esw, sections=sections,degree=degree)
        set_color(self.id,rgb) 
        self.attach_to_space(self.id)

class pyramid(gizmo):
                   
    def __init__(self, id, rgb=[0,255,0],width=1,axis=[0,1,0]):
        self.setup(id)
        cmds.polyPyramid(n=self.id,w=width,axis=axis)
        set_color(self.id,rgb) 
        self.attach_to_space(self.id) 

class pyramid_shaded(gizmo):
                   
    def __init__(self, id, mat,width=1,axis=[0,1,0]):
        self.setup(id)
        cmds.polyPyramid(n=self.id,w=width,axis=axis)
        cmds.sets(self.id, e=True, forceElement=mat)
        self.attach_to_space(self.id) 

class sphere(gizmo):
                   
    def __init__(self,id,rgb = [0,255,0],rad = 3.0,sx = 5,sy = 5): 
        self.setup(id)
        cmds.polySphere(n=self.id, r=rad, sx=sx, sy=sy)
        set_color(self.id,rgb) 
        self.attach_to_space(self.id) 

class sphere_shaded(gizmo):
                   
    def __init__(self,id,mat,rad = 3.0,sx = 6,sy = 6): 
        self.setup(id)
        cmds.polySphere(n=self.id, r=rad, sx=sx, sy=sy)
        cmds.setAttr(self.id+'.overrideEnabled', 1)
        cmds.sets(self.id, e=True, forceElement=mat)
        self.attach_to_space(self.id) 

class cone(gizmo):
                   
    def __init__(self,id,rgb = [0,255,0],rad = 1,height = 2,sx = 20,sy = 1,sz = 0,axis = [0,1,0],rcp = 0): 
        self.setup(id)
        cmds.polyCone(n=self.id,r=rad,h=height,sx=sx,sy=sy,sz=sz,axis=axis,rcp=rcp)
        set_color(self.id,rgb) 
        self.attach_to_space(self.id)       

class cylinder(gizmo):
                   
    def __init__(self,id,rgb = [0,255,0],rad = 1,height = 2,sx = 8,sy = 1,sz = 1,axis = [0,1,0],rcp = 0): 
        self.setup(id)
        cmds.polyCylinder(n=self.id,r=rad,h=height,sx=sx,sy=sy,sz=sz,axis=axis,rcp=rcp)
        set_color(self.id,rgb)
        self.attach_to_space(self.id)   

class cube(gizmo):
                   
    def __init__(self, id, rgb = [0,255,0], size = [0.5,0.5,0.5], span = [1,1,1]): 
        self.setup(id)
        cmds.polyCube(n=self.id, w=size[0],h=size[1],d=size[2],sw=span[0],sh=span[1],sd=span[2])
        set_color(self.id,rgb)
        self.attach_to_space(self.id)    

class cube_shaded(gizmo):
                   
    def __init__(self, id, mat, size = [0.5,0.5,0.5], span = [1,1,1]): 
        self.setup(id)
        cmds.polyCube(n=self.id, w=size[0],h=size[1],d=size[2],sw=span[0],sh=span[1],sd=span[2])
        cmds.setAttr(self.id+'.overrideEnabled', 1)
        cmds.sets(self.id, e=True, forceElement=mat)
        self.attach_to_space(self.id)  

class cross(gizmo):

    def __init__(self, id, rgb = [0,255,0], size = 10.0, thick=2.0): 
        self.setup(id)
        a = cmds.polyCube(h=size,w=thick,d=thick)
        b = cmds.polyCube(h=size,w=thick,d=thick,axis=[1,0,0])
        c = cmds.polyCube(h=size,w=thick,d=thick,axis=[0,0,1])
        cmds.polyCBoolOp(a[0],b[0],c[0], op=1, n=self.id )
        cmds.bakePartialHistory(self.id,prePostDeformers=True )
        set_color(self.id,rgb)
        self.attach_to_space(self.id)  