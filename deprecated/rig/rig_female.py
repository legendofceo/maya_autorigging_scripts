import maya.cmds as cmds
import math

autob_win_y_max = 300
g_axis_left = '_l'
g_axis_right = '_r'

g_group_controls = 'controls'
g_group_face_controls = 'face_controls'

g_right_h8 = '_r'
g_left_h8 = '_l'
g_cbo_name = '_cbo'

g_ctr_rot1 = [255,255,255]
g_ctr_rot2 = [255,150,0]
g_ctr_pos1 = [1,1,1]
g_ctr_pos2 = [1,1,1]
 
class Object(object):
    pass
     
def lerpV3(loc1,loc2,amount):
    
    len = [loc2[0]-loc1[0],loc2[1]-loc1[1],loc2[2]-loc1[2]]
    
    return [(len[0]*amount)+loc1[0],(len[1]*amount)+loc1[1],(len[2]*amount)+loc1[2]]

def hide_node(name):
    cmds.setAttr(name+'Shape.visibility',0)
    
def lerp_nodes(nfrom,nto,amount):  
    print(nfrom)   
    print(nto)
    pos1 = cmds.xform(nfrom,t=True,q=True,r=True) 
    print(pos1)
    pos2 = cmds.xform(nto,t=True,q=True,r=True)
    return lerpV3(pos1,pos2,amount)
                

def connect_xform(target,goal):
    cmds.connectAttr(target+'.translate',goal+'.translate')
    cmds.connectAttr(target+'.rotate',goal+'.rotate')
    cmds.connectAttr(target+'.scale',goal+'.scale')
        
def color_joint(name,rgb):
    cmds.setAttr(name+'.overrideEnabled', 1)
    cmds.setAttr(name+'.overrideRGBColors', 1)
    cmds.setAttr(name+'.overrideColorR', rgb[0])
    cmds.setAttr(name+'.overrideColorG', rgb[1])
    cmds.setAttr(name+'.overrideColorB', rgb[2])
               
def split_joint(name,low,high,num):  
    
    gap = 1.0/(num+1)
    
    twists = []
    cmds.select(low,r=True)
    
    for t in range(num):
        loc = lerpV3(cmds.xform(low,q=1,ws=1,rp=1),cmds.xform(high,q=1,ws=1,rp=1),(t+1)*gap)
        create_autob_joint(name+str(t+1),loc)
        
    cmds.parent(high,name+str(num))
        
def duplicate_joints(joints,new_joints): 
    par = cmds.listRelatives(joints[0], p=True)    
    new_arr = []
    
    for j,n in zip(joints, new_joints): 
        cmds.joint( p=(0, 0, 0),n=n )
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
        
        new_arr.append(n)       
    cmds.parent(new_arr[0],par,r=True)
    return new_arr

def duplicate_chain(chain,prefix,rgb):

    new_chain = []
    for j in chain:
        new_chain.append(prefix+j)
        
    chain = duplicate_joints(chain,new_chain)
    for j in chain:
        set_color(j,[.2,1,.2])
    return chain
    
def set_color(name,rgb):        
    cmds.setAttr(name+'.overrideEnabled', 1)
    cmds.setAttr(name+'.overrideRGBColors', 1)
    cmds.setAttr(name+'.overrideColorR', rgb[0])
    cmds.setAttr(name+'.overrideColorG', rgb[1])
    cmds.setAttr(name+'.overrideColorB', rgb[2])
    cmds.setAttr(name+'.overrideShading', 0) 


def match_position(obj,targ):
    pos = cmds.xform(targ, query=True, translation=True, worldSpace=True )
    cmds.xform(obj, translation=pos, worldSpace=True )
                        
















class assist_base():
    
    def setup(self,
              id = 'error',
              suf = None):
        self.id = id
        if suf==None:            
            self.suf = ''
        else:
            self.suf = suf
                   
        if(suf!=None):
            self.follow = 'c_'+self.id+self.suf                     
        else:
            self.ctr = 'c_'+self.id           

class assist_flesh(assist_base):
    
      
    def __init__(self,
                 id = 'error',
                 suf = None,
                 follow = 'error',
                 parent = None,
                 goal = 'error',
                 power = 4,
                 rgb = [255,0,0],
                 ): 
        self.setup(id,suf)
        self.follow = id+'_follow'+suf
        cmds.joint(name=self.follow)
        cmds.parent(self.follow,parent)
        cmds.matchTransform(self.follow,follow)
        cmds.makeIdentity(self.follow, apply=True, t=1, r=1, s=1) 
        cmds.setAttr(self.follow+'.jointOrientX',cmds.getAttr(follow+'.jointOrientX'))
        cmds.setAttr(self.follow+'.jointOrientY',cmds.getAttr(follow+'.jointOrientY'))
        cmds.setAttr(self.follow+'.jointOrientZ',cmds.getAttr(follow+'.jointOrientZ'))
        self.goal = id+'_goal'+suf
        cmds.joint(name=self.goal)
        cmds.matchTransform(self.goal,goal)
        cmds.makeIdentity(self.goal, apply=True, t=1, r=1, s=1)
        cmds.expression(s=self.follow+".rotateZ = ("+follow+".rotateZ/"+str(power)+")")
        set_color(self.follow,rgb)
        set_color(self.goal,rgb) 

        
class assist_muscle(assist_base):
    
      
    def __init__(self,
                 id = 'error',
                 suf = None,
                 parent = 'error',
                 reactor = None,
                 goal = 'error',
                 power = .1,
                 invert = None,
                 rgb = [255,0,0],
                 ): 
        self.setup(id,suf)
        
 
        self.auto = id+'_auto'+suf
        cmds.joint(name=self.auto)
        cmds.parent(self.auto,parent)
        cmds.matchTransform(self.auto,goal)
        cmds.makeIdentity(self.auto, apply=True, t=1, r=1, s=1)               
        set_color(self.auto,rgb)
        
        self.ramp = id+'_ramp'+suf
        cmds.joint(name=self.ramp)
        cmds.matchTransform(self.ramp,goal)
        cmds.makeIdentity(self.ramp, apply=True, t=1, r=1, s=1)               
        set_color(self.ramp,[255,0,0])
        
        pow = str(power)
        
        if invert!=None:
            
            inv = str(invert)
            cmds.expression(s=self.auto+".scaleX = 1.0 + (("+inv+"-"+reactor+".rotateZ)*"+pow+")")
            cmds.expression(s=self.auto+".scaleY = 1.0 + (("+inv+"-"+reactor+".rotateZ)*"+pow+")")
            cmds.expression(s=self.auto+".scaleZ = 1.0 + (("+inv+"-"+reactor+".rotateZ)*"+pow+")")
        else:
            cmds.expression(s=self.auto+".scaleX = 1.0 + ("+reactor+".rotateZ*"+pow+")*-1")
            cmds.expression(s=self.auto+".scaleY = 1.0 + ("+reactor+".rotateZ*"+pow+")*-1")
            cmds.expression(s=self.auto+".scaleZ = 1.0 + ("+reactor+".rotateZ*"+pow+")*-1")
        cmds.scaleConstraint(self.ramp,goal,mo=True)  
                 
                  




    
class control_base():
    
    #cbo stands for control base object
    
    def parent(self,par):
        cmds.parent(self.cbo,par)
        
    def freeze(self):
        cmds.makeIdentity(self.ctr, apply=True, t=1, r=1, s=1)
        
    def snap_cbo(self,targ):
        cmds.matchTransform(self.cbo,targ)

    def orientConstraint(self,targ,mo=True,w=1.0):
        cmds.orientConstraint(self.ctr,targ,mo=mo,w=w)

    def parentConstraint(self,targ,mo=True,w=1.0):
        cmds.parentConstraint(self.ctr,targ,mo=mo,w=w)
     
    def parentConstraintProxy(self,targ,mo=True,w=1.0):
        cmds.parentConstraint(self.proxy,targ,mo=mo,w=w)
                  
    def lock_rot(self,x,y,z):
        if x == True:
            cmds.setAttr(self.ctr+'.rx', lock=True)
        if y == True:
            cmds.setAttr(self.ctr+'.ry', lock=True)
        if z == True:
            cmds.setAttr(self.ctr+'.rz', lock=True)
     

        
        
    def enable_proxy(self,goal):
        self.proxy = self.id+'_proxy'+self.suf 
        cmds.spaceLocator(name=self.proxy)
        cmds.setAttr(self.proxy+'Shape.visibility',0)
        cmds.makeIdentity(self.proxy, apply=True, t=1, r=1, s=1)
        
        match_position(self.proxy,self.control())
        cmds.parent(self.proxy,goal)
         
        connect_xform(self.ctr,self.proxy)
    
    def control(self):
        return self.ctr
    
    def move_offset_control(self,x,y,z,abs=False,nopivot=False):
        pos = cmds.xform(self.ctr, query=True, translation=True, worldSpace=True )
        cmds.select(self.ctr,r=True)
        if abs!=True:
           cmds.move(x,y,z, r=True)
        else:
           cmds.move(x,y,z)  
           
        if nopivot==False:
            cmds.xform(self.ctr, ws=True, piv=(pos[0], pos[1], pos[2]) )
        self.freeze()
    
    def bind_cbo(self):
        cmds.matchTransform(self.ctr,self.cbo)
        cmds.parent(self.ctr,self.cbo)
        self.freeze()

    def override_rotation_cbo(self,x,y,z):
           
        par = cmds.listRelatives(self.cbo,p=True)
        if par!=None:
            cmds.parent(self.cbo,w=True)
        if x != None:
            cmds.setAttr(self.cbo+'.rotateX', x)
        if y != None:
            cmds.setAttr(self.cbo+'.rotateY', y)
        if z != None:
            cmds.setAttr(self.cbo+'.rotateZ', z)
        if par!=None:
            cmds.parent(self.cbo,par) 
     
    def rotate_cbo(self,x,y,z):
        par = cmds.listRelatives(self.cbo,p=True)
        if par!=None:
            cmds.parent(self.cbo,w=True)
        cmds.select(self.cbo,r=True)
        cmds.rotate(x,y,z,r=True)
        if par!=None:
            cmds.parent(self.cbo,par) 
                 
    def setup(self,
              id = 'error',
              suf = None):
        self.id = id
        if suf==None:            
            self.suf = ''
        else:
            self.suf = suf
            
        self.cbo = self.id+g_cbo_name+self.suf
        cmds.spaceLocator(name=self.cbo)
        #cmds.setAttr(self.cbo+'.overrideEnabled',1)
        cmds.setAttr(self.cbo+'Shape.visibility',0)
        
        if(suf!=None):
            self.ctr = 'c_'+self.id+self.suf                     
        else:
            self.ctr = 'c_'+self.id
                   
class control_torus(control_base):
                   
    def __init__(self,
                 id = 'error',
                 suf = None,
                 rgb = [0,255,0],
                 rad = 2.0,
                 hrad = .005,
                 axis = [0,0,1],
                 spans = 4,
                 ssw = 0,
                 esw = 360,
                 ): 
        self.setup(id,suf)
        cmds.torus(n=self.ctr, r=rad, hr=hrad, axis=axis,spans=spans,ssw=ssw,esw=esw)
        set_color(self.ctr,[rgb[0],rgb[1],rgb[2]]) 
        self.bind_cbo()

class control_sphere(control_base):
                   
    def __init__(self,
                 id = 'error',
                 suf = None,
                 rgb = [0,255,0],
                 rad = 3.0,
                 sx = 10,
                 sy = 10
                 ): 
        self.setup(id,suf)
        cmds.polySphere(n=self.ctr, r=rad, sx=sx, sy=sy)
        set_color(self.ctr,[rgb[0],rgb[1],rgb[2]]) 
        self.bind_cbo()


class control_cube(control_base):
                   
    def __init__(self,
                 id = 'error',
                 suf = None,
                 rgb = [0,255,0],
                 size = [0.5,0.5,0.5],
                 span = [1,1,1]
                 ): 
        self.setup(id,suf)
        cmds.polyCube(n=self.ctr, h=size[0],w=size[1],d=size[2],sw=span[0],sh=span[1],sd=span[2])
        set_color(self.ctr,[rgb[0],rgb[1],rgb[2]]) 
        self.bind_cbo()    
    

class control_cone(control_base):
                   
    def __init__(self,
                 id = 'error',
                 suf = None,
                 rgb = [0,255,0],
                 r = 1,
                 h = 2,
                 sx = 20,
                 sy = 1,
                 sz = 0,
                 axis = [0,1,0],
                 rcp = 0
                 ): 
        self.setup(id,suf)
        cmds.polyCone(n=self.ctr,r=r,h=h,sx=sx,sy=sy,sz=sz,axis=axis,rcp=rcp)
        set_color(self.ctr,[rgb[0],rgb[1],rgb[2]]) 
        self.bind_cbo()         


class control_cylinder(control_base):
                   
    def __init__(self,
                 id = 'error',
                 suf = None,
                 rgb = [0,255,0],
                 r = 1,
                 h = 2,
                 sx = 8,
                 sy = 1,
                 sz = 1,
                 axis = [0,1,0],
                 rcp = 0
                 ): 
        self.setup(id,suf)
        cmds.polyCylinder(n=self.ctr,r=r,h=h,sx=sx,sy=sy,sz=sz,axis=axis,rcp=rcp)
        set_color(self.ctr,[rgb[0],rgb[1],rgb[2]]) 
        self.bind_cbo()         


class control_pyramid(control_base):
                   
    def __init__(self,
                 id = 'error',
                 suf = None,
                 rgb = [0,255,0],
                 w = 1,
                 axis = [0,1,0],
                 ): 
        self.setup(id,suf)
        cmds.polyPyramid(n=self.ctr,w=w,axis=axis)
        set_color(self.ctr,[rgb[0],rgb[1],rgb[2]]) 
        self.bind_cbo()      





def make_controls_face(group_name):
    cmds.group(name=group_name,em=True)
    cmds.parent(group_name,'head')
    cmds.matchTransform(group_name,'head')    
    cmds.makeIdentity(group_name, apply=True, t=1, r=1, s=1)
     
    return          
    make_control_point(
    target='nostril',
    rgb=[255,0,0],
    parent=group_name,
    offset=[0,-1,0]
    )
        
    make_control_point(
    target = 'lip_upper_center',
    rgb = [255,0,0],
    parent = group_name,
    offset = [0,-1,0]
    )
           
    make_control_point(
    target = 'lip_lower_center',
    rgb = [255,0,0],
    parent = group_name,
    offset = [0,-1,0]
    )
        
    make_control_point_multi(
    target = 'lip_lower_outer',
    rgb = [255,0,0],
    parent = group_name,
    offset = [0,-1,0]
    )
        
    make_control_point_multi(
    target = 'lip_lower_corner',
    rgb = [255,0,0],
    parent = group_name,
    offset = [0,-1,0]
    )
        
    make_control_point_multi(
    target = 'lip_upper_outer',
    rgb = [255,0,0],
    parent = group_name,
    offset = [0,-1,0]
    )
        
    make_control_point(
    target = 'brow_center',
    rgb = [255,0,0],
    parent = group_name,
    offset = [0,-1,0]
    )
        
    make_control_point_multi(
    target = 'brow_inner',
    rgb = [255,0,0],
    parent = group_name,
    offset = [0,-1,0]
    )
        
    make_control_point_multi(
    target = 'brow_middle',
    rgb = [255,0,0],
    parent = group_name,
    offset = [0,-1,0]
    )
        
    make_control_point_multi(
    target = 'brow_outer',
    rgb = [255,0,0],
    parent = group_name,
    offset = [0,-1,0]
    )
        
    make_control_point_multi(
    target = 'squint',
    rgb = [255,0,0],
    parent = group_name,
    offset = [0,-1,0]
    )






def make_controls_genex(group_name):
    cmds.group( em=True, name=group_name)
    cmds.matchTransform(group_name,'genf')    
    cmds.makeIdentity(group_name, apply=True, t=1, r=1, s=1)
    
    return
    
    make_control_point(
    target = 'ex_upper',
    rgb = [255,0,0],
    parent = group_name,
    offset = [0,-1,0]
    )
    
    make_control_point_multi(
    target = 'ex_corner',
    rgb = [255,0,0],
    parent = group_name,
    offset = [0,-1,0]
    )
    
    make_control_point(
    target = 'ex_lower',
    rgb = [255,0,0],
    parent = group_name,
    offset = [0,-1,0]
    )

                        
    
 


                   
                      

 
class ik_fk_switch():
    
    def __init__(self):
        self.start_mode = False
     
    def set_start_mode(self,b_ik):
        self.start_mode = b_ik    
          
    def set_controls(self,control,ctr_fk,ctr_ik):
        self.ctr = control
        self.ctr_fk = ctr_fk
        self.ctr_ik = ctr_ik
        
    def set_chains(self,base,fk,ik):
        self.chain_base = base
        self.chain_fk = fk
        self.chain_ik = ik
        
    def exe(self):    
    
        dv = 0.0
        if self.start_mode==True:
            dv = 1.0
            
        cmds.addAttr(self.ctr, ln='kinematics_switch',nn='FK -> IK', keyable=True, r=True, hidden=False, dv=dv, min=0.0, max=1.0)    
        cmds.addAttr(self.ctr, ln='fkvis',nn='FK Visibility', keyable=True, r=True, hidden=False, dv=True)
        cmds.addAttr(self.ctr, ln='ikvis',nn='IK Visibility', keyable=True, r=True, hidden=False, dv=True)  
        cmds.addAttr(self.ctr, ln='ik',nn='IK', keyable=True, r=True, hidden=True, dv=1.0, min=0.0, max=1.0)
        cmds.addAttr(self.ctr, ln='fk',nn='FK', keyable=True, r=True, hidden=True, dv=0.0, min=0.0, max=1.0)
        
        cmds.expression(s=self.ctr+".ik = "+self.ctr+".kinematics_switch")
        cmds.expression(s=self.ctr+".fk = 1 - "+self.ctr+".kinematics_switch")
        
        
        for base,fk,ik in zip(self.chain_base,self.chain_fk,self.chain_ik):
            cmds.orientConstraint(fk, base, mo=True,w=0)
            cmds.orientConstraint(ik, base, mo=True,w=0)
        
            cmds.connectAttr(self.ctr+'.fk',base+'_orientConstraint1.'+fk+'W0' )
            cmds.connectAttr(self.ctr+'.ik',base+'_orientConstraint1.'+ik+'W1' )
      
    
        for ctr in self.ctr_fk:
            cmds.connectAttr(self.ctr+'.fkvis',ctr+'.visibility')
        
        for ctr in self.ctr_ik:
            cmds.connectAttr(self.ctr+'.ikvis',ctr+'.visibility')
        
class rig_base():
    
    def set_id(self,id):
        self.id=id
    
    def set_sym(self,sym,suffix):
        self.sym = sym
        self.symsuf = suffix

    def set_rgb(self,rgb):
        self.rgb = rgb
    
    def dict_rgb(self,key,rgb):
        self.rgb_dict[key] = rgb
            
    def idsym(self):
        return self.id+self.symsuf
    
    def set_joint_rgb(self,r,g,b):
        self.joint_rgb = [r/255,g/255,b/255]
    
    def set_symsufs(self,right,left):
        self.symsuf_right = right
        self.symsuf_left = left
        self.sym_arr = [right,left]
         
    def set_parent(self,parent):
        self.parent = parent
              
    def setup(self):
        self.id = 'error'
        self.sym = None
        self.symsuf = ''
        self.rgb = [0,1,0]
        self.rgb_dict = {}


class rig_clavicle(rig_base):
    
    def __init__(self):
        self.setup()
       
    def exe(self):    
        ssw = 330
        esw = 390
        movex = -3
        if self.sym==1:
            ssw = ssw-180
            esw = esw-180
            movex = movex*-1
            
        c = control_torus(
                id = self.id,
                suf = self.symsuf,
                rgb = self.rgb,
                rad = 9.5,
                hrad = .05,
                axis = [1,0,0],
                ssw=ssw,
                esw=esw    
                )
                
        targ = self.idsym() 
        c.snap_cbo(targ)
        
        c.move_offset_control(movex,0,0)
        
        c.parent(self.parent) 
        c.freeze()
        c.orientConstraint(targ)
    
class rig_arm_fk(rig_base):
 
    def __init__(self):
        self.setup()
          
    def set_arm_names(self,names):
        self.arm_names = names
            
       
    def exe(self):
        
        controls = []
        base_chain = []
        
        for j in self.arm_names:
            base_chain.append(j+self.symsuf)
    
            
        fk_chain = duplicate_chain(base_chain,self.id,[.2,1,.2]) 
    
        controls = []
        #####################################
    
        ssw = 320
        esw = 380
    
        if self.sym==1:
            ssw = ssw-180
            esw = esw-180
    
        c = control_torus(
                id = self.arm_names[0],
                suf = self.symsuf,
                rgb = self.rgb_dict['upperarm'],
                rad = 9.5,
                hrad = .005,
                axis = [1,0,0],
                ssw=ssw,
                esw=esw   
                )                
        c.snap_cbo(base_chain[0])
        c.parent(self.parent)
        c.orientConstraint(fk_chain[0])                
        controls.append(c.control())
        upperarm = c
    
        #####################################
        c = control_torus(
                id = self.arm_names[1],
                suf = self.symsuf,
                rgb = self.rgb_dict['lowerarm'],
                rad = 6.5,
                hrad = .005,
                axis = [1,0,0]  
                )                
        c.snap_cbo(base_chain[1])
        c.orientConstraint(fk_chain[1])
        controls.append(c.control())
        c.parent(upperarm.control())
        lowerarm = c

        #####################################
        c = control_torus(
                id = self.arm_names[2],
                suf = self.symsuf,
                rgb = self.rgb_dict['lowerarm'],
                rad = 5.0,
                hrad = .005,
                axis = [1,0,0]  
                )                
        c.snap_cbo(base_chain[2])
        c.orientConstraint(fk_chain[2])
        controls.append(c.control())
        c.parent(lowerarm.control())
            
        self.base_chain = base_chain
        self.controls = controls
        self.chain = fk_chain        
        
        
class rig_arm_ik(rig_base):
 
    def __init__(self):
        self.setup()
          
    def set_arm_names(self,names):
        self.leg_names = names
            
    def set_control_names(self,arm,elbow):
            self.arm_ctr_name = arm
            self.elbow_ctr_name = elbow
                        
    def exe(self):        
        
        controls = []
        base_chain = []
        
        for j in self.leg_names:
            base_chain.append(j+self.symsuf)
    
            
        ik_chain = duplicate_chain(base_chain,self.id,[.2,1,.2]) 
        
        #####################################
        c = control_torus(
                id = self.arm_ctr_name,
                suf = self.symsuf,
                rgb = self.rgb_dict['arm'],
                rad = 6.0,
                hrad = .005,
                axis = [1,0,0] 
                )                
        
        c.snap_cbo(base_chain[2])
        c.parent(self.parent)
        controls.append(c.control())
      
       
        cmds.setAttr(ik_chain[1]+".preferredAngleZ",-90)
        handle = self.id+'_handle_'+self.symsuf
        
        cmds.ikHandle(sj=ik_chain[0], ee=ik_chain[2], solver='ikRPsolver', n=handle )
        cmds.parent(handle,c.control())
        c.orientConstraint(ik_chain[2])
    
        c = control_sphere(
                id = self.elbow_ctr_name,
                suf = self.symsuf,
                rgb = self.rgb_dict['elbow'],
                rad = 3.0
                )              
    
                 
        c.snap_cbo(base_chain[1])
        c.override_rotation_cbo(0,0,0)
        c.move_offset_control(0, 62, 0,nopivot=True)  
        
        cmds.poleVectorConstraint(c.control(),handle)
        c.parent(self.parent)       
        controls.append(c.control())
        
        self.base_chain = base_chain
        self.controls = controls
        self.chain = ik_chain

    
class rig_fingers(rig_base):
   
    def set_fingers(self,thumb,index,middle,ring,pinky):
        self.fingers = [thumb,index,middle,ring,pinky]
    
    def exe(self):
    
        for j in self.fingers:
           
            fing_arr = []        
            for i in range(3):
            
                if i==0:
                    rad = 1.8
                elif i==1:
                    rad = 1.6
                elif i==2:
                    rad = 1.4
                    
                ix = i+1
                ix_str = str(ix)
                c = control_torus(
                    id = j+ix_str,
                    suf = self.symsuf,
                    rgb = self.rgb,
                    rad = rad,
                    hrad = .04,
                    axis = [1,0,0]
                    )
                fing_arr.append(c)              
                targ_joint = j+ix_str+self.symsuf
                c.snap_cbo(targ_joint)  
                
                if i!=0:
                    c.lock_rot(True,False,True)
                    
                if i == 0:
                    c.parent(self.parent)
                else:
                    c.parent(fing_arr[i-1].control())
                
                c.orientConstraint(targ_joint)      



     
class rig_leg_fk(rig_base):
 
    def __init__(self):
        self.setup()
          
    def set_leg_names(self,names):
        self.leg_names = names
            
       
    def exe(self):
        
        controls = []
        base_chain = []
        
        for j in self.leg_names:
            base_chain.append(j+self.symsuf)
    
            
        fk_chain = duplicate_chain(base_chain,self.id,[.2,1,.2]) 
    
        #####################################
                
        move = -9
        ssw = 20
        esw = 100
        
        if self.sym==1:
            move = 9
            ssw = ssw-180
            esw = esw-180
               
        c = control_torus(
                    id = self.leg_names[0],
                    suf = self.symsuf,
                    rgb = self.rgb_dict['thigh'],
                    rad = 12.0,
                    hrad = .05,
                    axis = [1,0,0],
                    spans=12,
                    ssw=ssw,
                    esw=esw   
                    )             
                       
        c.snap_cbo(base_chain[0])
        c.parent(self.parent)
        c.orientConstraint(fk_chain[0])                
        controls.append(c.control())
        thigh = c
    
    
    
        #####################################
        move = 4
        ssw = 300
        esw = 400
        
        if self.sym==1:
            move = -4
            ssw = ssw-180
            esw = esw-180
                
        c = control_torus(
                    id = self.leg_names[1],
                    suf = self.symsuf,
                    rgb = self.rgb_dict['calf'],
                    rad = 6.5,
                    hrad = .1,
                    axis = [1,0,0],
                    spans=12,
                    ssw=ssw,
                    esw=esw   
                    )                
        c.snap_cbo(base_chain[1])
        c.parent(thigh.control())
        c.orientConstraint(fk_chain[1])                
        controls.append(c.control())
        calf = c
        
        
        
    
        c = control_torus(
                    id = self.leg_names[2],
                    suf = self.symsuf,
                    rgb = self.rgb_dict['foot'],
                    rad = 6.25,
                    hrad = .005,
                    axis = [1,0,0],
                    spans=12,
                    ssw=360,
                    esw=0   
                    )                
        c.snap_cbo(base_chain[2])
        
        if self.sym==0:
            c.override_rotation_cbo(None,-90,None)
        else:
            c.override_rotation_cbo(None,90,None)        
        c.parent(calf.control())
        c.orientConstraint(fk_chain[2])                
        controls.append(c.control())
        foot = c
        
        
        c = control_torus(
                    id = self.leg_names[3],
                    suf = self.symsuf,
                    rgb = self.rgb_dict['ball'],
                    rad = 4.25,
                    hrad = .005,
                    axis = [1,0,0],
                    spans=12,
                    ssw=360,
                    esw=0   
                    )                
        c.snap_cbo(base_chain[3])
        c.parent(foot.control())
        c.orientConstraint(fk_chain[3])                
        controls.append(c.control())
        toe = c
        
        self.base_chain = base_chain
        self.controls = controls
        self.chain = fk_chain

        
        
class rig_leg_ik(rig_base):
 
    def __init__(self):
        self.setup()
          
    def set_leg_names(self,names):
        self.leg_names = names
            
    def set_control_names(self,leg,knee):
            self.leg_ctr_name = leg
            self.knee_ctr_name = knee
                        
    def exe(self):        
        
        controls = []
        base_chain = []
        
        xsym = 1
        if self.sym==1:
            xsym=-1
            
        for j in self.leg_names:
            base_chain.append(j+self.symsuf)
    
            
        ik_chain = duplicate_chain(base_chain,self.id,[.2,1,.2]) 
        

        #####################################
        c = control_torus(
                id = self.leg_ctr_name,
                suf = self.symsuf,
                rgb = self.rgb_dict['leg'],
                rad = 8.5,
                hrad = .05,
                axis = [1,0,0] 
                )                
        c.snap_cbo(base_chain[2])
    
        if self.sym==0:
            c.override_rotation_cbo(None,90,None)
        elif self.sym==1:
            c.override_rotation_cbo(None,-90,None)
        
        controls.append(c.control())
        leg = c.control()
        c.parent(self.parent)
        cmds.setAttr(ik_chain[1]+".preferredAngleY",90)
        
        
        handles = []
        handles.append(self.id+'_'+base_chain[2]+'_handle'+self.symsuf)
        handles.append(self.id+'_'+base_chain[3]+'_handle'+self.symsuf)
        handles.append(self.id+'_'+base_chain[4]+'_handle'+self.symsuf)
        
                
           
        cmds.ikHandle(sj=ik_chain[0], ee=ik_chain[2], n=handles[0], solver='ikRPsolver' )
        cmds.ikHandle(sj=ik_chain[2], ee=ik_chain[3], n=handles[1], solver='ikSCsolver')
        cmds.ikHandle(sj=ik_chain[3], ee=ik_chain[4], n=handles[2], solver='ikSCsolver')
    
        ikfollow_chain = duplicate_chain([base_chain[0],base_chain[1],base_chain[2]],self.id+'_ik_follow',[.2,1,.2]) 
        cmds.setAttr(ikfollow_chain[1]+".preferredAngleY",90)
        ikfollow = self.id+'_ik_follow_handle'+self.symsuf
        cmds.ikHandle(sj=ikfollow_chain[0], ee=ikfollow_chain[2], n=ikfollow, solver='ikSCsolver' ) 
        cmds.parent(ikfollow,leg)
        
        #0 = toe
        #1 = ball
        #2 = wiggle
    
        helpers = []
        helpers.append(self.id+'_helper_toe'+self.symsuf)
        helpers.append(self.id+'_helper_ball'+self.symsuf)
        helpers.append(self.id+'_helper_wiggle'+self.symsuf)
        
        htoe = helpers[0]
        hball = helpers[1]
        hwiggle = helpers[2]
    
        cmds.spaceLocator(n=htoe)
        cmds.matchTransform(htoe,base_chain[3])

        cmds.spaceLocator(n=hball )
        cmds.matchTransform(hball,base_chain[3])

        cmds.spaceLocator(n=hwiggle )
        cmds.matchTransform(hwiggle,base_chain[3])

        cmds.parent(htoe,leg)    
        cmds.parent(handles[1], htoe)
        cmds.parent(hwiggle, htoe)
        cmds.parent(handles[2], hwiggle)    
        cmds.parent(hball, htoe)    
        cmds.parent(handles[0], hball)    
    
        c = control_sphere(
                id = self.knee_ctr_name,
                suf = self.symsuf,
                rgb = self.rgb_dict['knee'],
                rad = 1.5
                )              
        
        c.snap_cbo(base_chain[1]) 
        if self.sym==0:
            c.override_rotation_cbo(None,90,None)
        elif self.sym==1:
            c.override_rotation_cbo(None,-90,None)
            
        
        angle_mes = 'angle_mes'+self.symsuf
        cmds.spaceLocator(n=angle_mes,p=[0,0,0])
        cmds.matchTransform(angle_mes,ik_chain[1])
        cmds.parent(angle_mes,ik_chain[1])
        cmds.setAttr(angle_mes+'.translateZ',-30*xsym)
        
        cmds.matchTransform(c.cbo,angle_mes)
        cmds.delete(angle_mes)  
        
        knee = c.control()
        cmds.poleVectorConstraint(knee,handles[0])
        
        c.parent(ikfollow_chain[0])       
        controls.append(knee)    
    
        
        

        


        c = control_cylinder(
                id = 'toe',
                suf = self.symsuf,
                rgb = self.rgb_dict['toes'],
                h = 1.0,
                r = 0.6,
                )           
          
          

                       
        c.snap_cbo(leg)
        c.parent(leg)
        controls.append(c.control())
        cmds.setAttr(c.control()+'.translateY', -10.5*xsym)
        cmds.makeIdentity(c.control(), apply=True, t=1, r=1, s=1)
        cmds.expression(s=hwiggle+'.rotateY = '+c.control()+'.rotateY' )
                
        c = control_cylinder(
                id = 'tiptoe',
                suf = self.symsuf,
                rgb = self.rgb_dict['tiptoe'],
                h = 1.0,
                r = 0.6,
                )                
        c.snap_cbo(leg)
        c.parent(leg)
        controls.append(c.control())
        cmds.setAttr(c.control()+'.translateY', -9.5*xsym)
        cmds.makeIdentity(c.control(), apply=True, t=1, r=1, s=1)
        cmds.expression(s=hball+'.rotateY = '+c.control()+'.rotateY' )
        tiptoe = c.control()
        
        


        self.base_chain = base_chain
        self.controls = controls
        self.chain = ik_chain
                
        return
        
        c = control_cylinder(
                id = 'squash',
                suf = self.symsuf,
                rgb = self.rgb_dict['leg'],
                h = 1.0,
                r = 0.6,
                axis = [1,0,0]
                )           
                     
        c.snap_cbo(leg)
        controls.append(c.control())
        c.parent(leg)
        cmds.setAttr(c.control()+'.translateY', -9.5)


        cmds.makeIdentity(c.control(), apply=True, t=1, r=1, s=1)
         
        

        
        self.base_chain = base_chain
        self.controls = controls
        self.chain = ik_chain
        
        
                                       
class rig_toes(rig_base):
 
    def __init__(self):
        self.setup()
          
    def set_toes(self,big,long,middle,ring,little):
        self.toes = [big,long,middle,ring,little]
    
    def exe(self):
    
        for j in self.toes:
           
            toes_arr = []        
            for i in range(2):
            
                if i==0:
                    rad = 1.8
                elif i==1:
                    rad = 1.6
                elif i==2:
                    rad = 1.4
                    
                ix = i+1
                ix_str = str(ix)
                c = control_torus(
                    id = j+ix_str,
                    suf = self.symsuf,
                    rgb = self.rgb,
                    rad = rad,
                    hrad = .04,
                    axis = [1,0,0]
                    )
                toes_arr.append(c)              
                targ_joint = j+ix_str+self.symsuf
                c.snap_cbo(targ_joint)  
                
                if i!=0:
                    c.lock_rot(True,True,False)
                    
                if i == 0:
                    c.parent(self.parent)
                else:
                    c.parent(toes_arr[i-1].control())
                
                c.orientConstraint(targ_joint)  
                         
class rig_belly(rig_base):
        
    def __init__(self):
        self.setup()
       
    def exe(self):
        joint = self.id
        c = control_cone(
                id = self.id,
                r = 1,
                rgb = self.rgb,
                axis = [0,0,-1]
                )
        c.snap_cbo(joint)                
        #c.parent(fl.goal)
        c.override_rotation_cbo(None,-90,None)
        c.move_offset_control(0,-12,0)           
        cmds.parentConstraint(c.control(),joint,mo=True) 
        cmds.scaleConstraint(c.control(),joint,mo=True)
        c.parent(self.parent) 
        

class rig_glute(rig_base):
        
    def __init__(self):
        self.setup()
              
    def set_follow_target(self,follow_target):
        self.follow_target = follow_target
    
    def set_goal_target(self,goal_target):
        self.goal_target = goal_target
        
    def set_power(self,power):
        self.power = power
    

    def exe(self):

        follow = self.id+'_follow'+self.symsuf
        cmds.joint(name=follow)
        cmds.parent(follow,self.parent)
        cmds.matchTransform(follow,self.follow_target)
        cmds.makeIdentity(follow, apply=True, t=1, r=1, s=1) 
        cmds.setAttr(follow+'.jointOrientX',cmds.getAttr(self.follow_target+'.jointOrientX'))
        cmds.setAttr(follow+'.jointOrientY',cmds.getAttr(self.follow_target+'.jointOrientY'))
        cmds.setAttr(follow+'.jointOrientZ',cmds.getAttr(self.follow_target+'.jointOrientZ'))
        goal = self.id+'_goal'+self.symsuf
        
        cmds.joint(name=goal)
        cmds.matchTransform(goal,self.goal_target)
        cmds.makeIdentity(goal, apply=True, t=1, r=1, s=1)
        cmds.expression(s=follow+".rotateY = ("+self.follow_target+".rotateY/"+str(self.power)+")")
        cmds.expression(s=follow+".rotateZ = ("+self.follow_target+".rotateZ/"+str(self.power/2.0)+")")
        set_color(follow,self.joint_rgb)
        set_color(goal,self.joint_rgb) 
        
        joint = self.idsym()
        c = control_cone(
                id = self.id,
                suf = self.symsuf,
                rgb = self.rgb,
                r = 1,
                axis = [0,0,1]
                )
                
        c.snap_cbo(joint)                
        c.parent(goal)
        
        
        if self.sym==0:
            c.override_rotation_cbo(180,-90,90)    
        else:
            c.override_rotation_cbo(180,-90,90)
        c.move_offset_control(0,18,0)               

            
        cmds.parentConstraint(c.control(),joint,mo=True) 
        cmds.scaleConstraint(c.control(),joint,mo=True)
            
                    
class rig_ham(rig_base):
        
    def __init__(self):
        self.setup()
       
    def exe(self):
        joint = self.idsym()
        c = control_cone(
                id = self.id,
                suf = self.symsuf,
                r = 1,
                rgb = self.rgb,
                axis = [0,0,1]
                )
        c.snap_cbo(joint)                
        #c.parent(fl.goal)
        
        if self.sym==0:
            c.override_rotation_cbo(180,-90,90)    
        else:
            c.override_rotation_cbo(180,-90,90)
            
        c.move_offset_control(0,15,0)           
        cmds.parentConstraint(c.control(),joint,mo=True) 
        cmds.scaleConstraint(c.control(),joint,mo=True)                                                                                                                                                                                                
        cmds.parent(c.control(),self.parent)

class rig_quad(rig_base):
        
    def __init__(self):
        self.setup()
       
    def exe(self):
        joint = self.idsym()
        c = control_cone(
                id = self.id,
                suf = self.symsuf,
                r = 1,
                rgb = self.rgb,
                axis = [0,0,-1]
                )
        c.snap_cbo(joint)                
        #c.parent(fl.goal)
        
        if self.sym==0:
            c.override_rotation_cbo(0,-90,90)    
        else:
            c.override_rotation_cbo(180,-90,90)
            
        c.move_offset_control(0,-15,0)           
        cmds.parentConstraint(c.control(),joint,mo=True) 
        cmds.scaleConstraint(c.control(),joint,mo=True)
        cmds.parent(c.control(),self.parent)

class rig_breast(rig_base):
        
    def __init__(self):
        self.setup()
       
    def exe(self):
        joint = self.idsym()
        c = control_cone(
                id = self.id,
                suf = self.symsuf,
                r = 1,
                rgb = self.rgb,
                axis = [0,0,-1]
                )
        c.snap_cbo(joint)                

        
        if self.sym==0:
            c.override_rotation_cbo(0,-90,90)    
        else:
            c.override_rotation_cbo(180,-90,90)
            
        c.move_offset_control(0,-15,0)           
        cmds.parentConstraint(c.control(),joint,mo=True) 
        cmds.scaleConstraint(c.control(),joint,mo=True)
        cmds.parent(c.control(),self.parent)
 
class rig_nip(rig_base):
        
    def __init__(self):
        self.setup()
       
    def exe(self):
        joint = self.idsym()
        c = control_cone(
                id = self.id,
                suf = self.symsuf,
                r = 0.5,
                rgb = self.rgb,
                axis = [0,0,-1]
                )
        c.snap_cbo(joint)                
        #c.parent(fl.goal)
        
        if self.sym==0:
            c.override_rotation_cbo(0,-90,90)    
        else:
            c.override_rotation_cbo(180,-90,90)
            
        c.move_offset_control(0,-5,0)           
        cmds.parentConstraint(c.control(),joint,mo=True) 
        cmds.scaleConstraint(c.control(),joint,mo=True)
        cmds.parent(c.control(),self.parent)
                      
class rig_gastro(rig_base):
        
    def __init__(self):
        self.setup()
       
    def exe(self):
        joint = self.idsym()
        c = control_cone(
                id = self.id,
                suf = self.symsuf,
                r = 1,
                rgb = self.rgb,
                axis = [0,0,1]
                )
        c.snap_cbo(joint)                
        #c.parent(fl.goal)
        
        if self.sym==0:
            c.override_rotation_cbo(0,-90,90)    
        else:
            c.override_rotation_cbo(180,-90,90)
            
        c.move_offset_control(0,15,0)           
        cmds.parentConstraint(c.control(),joint,mo=True) 
        cmds.scaleConstraint(c.control(),joint,mo=True)
        cmds.parent(c.control(),self.parent)

class rig_scapula(rig_base):
        
    def __init__(self):
        self.setup() 
       
    def exe(self):
        joint = self.idsym()
        c = control_cone(
                id = self.id,
                suf = self.symsuf,
                r = 1,
                rgb = self.rgb,
                axis = [0,0,1]
                )
        c.snap_cbo(joint)                
        #c.parent(fl.goal)
        
        if self.sym==0:
            c.override_rotation_cbo(0,-90,90)    
        else:
            c.override_rotation_cbo(180,-90,90)
            
        c.move_offset_control(0,15,0)           
        cmds.parentConstraint(c.control(),joint,mo=True) 
        cmds.scaleConstraint(c.control(),joint,mo=True)
        cmds.parent(c.control(),self.parent)
        
class rig_spinae(rig_base):
        
    def __init__(self):
        self.setup()
       
    def exe(self):
        joint = self.idsym()
        c = control_cone(
                id = self.id,
                suf = self.symsuf,
                r = 1,
                rgb = self.rgb,
                axis = [0,0,1]
                )
        c.snap_cbo(joint)                
        #c.parent(fl.goal)
        
        if self.sym==0:
            c.override_rotation_cbo(0,-90,90)    
        else:
            c.override_rotation_cbo(180,-90,90)
            
        c.move_offset_control(0,15,0)           
        cmds.parentConstraint(c.control(),joint,mo=True) 
        cmds.scaleConstraint(c.control(),joint,mo=True)
        c.parent(self.parent) 
        
class rig_lat(rig_base):
        

    def __init__(self):
        self.setup()
               
    def exe(self):
        joint = self.idsym()
        c = control_cone(
                id = self.id,
                suf = self.symsuf,
                r = 1,
                rgb = self.rgb,
                axis = [0,0,1]
                )
        c.snap_cbo(joint)                
        #c.parent(fl.goal)
        
        if self.sym==0:
            c.override_rotation_cbo(0,-90,90)    
        else:
            c.override_rotation_cbo(180,-90,90)
            
        c.move_offset_control(0,15,0)           
        cmds.parentConstraint(c.control(),joint,mo=True) 
        cmds.scaleConstraint(c.control(),joint,mo=True)
        c.parent(self.parent) 
 


class rig_tongue(rig_base):
        

    def __init__(self):
        self.setup()
        
    def set_joint_num(self,num):
        self.joint_num = num
               
    def exe(self):

        first = self.id+'1'
        last = self.id+str(self.joint_num)
        
        ikh, effector, curve = cmds.ikHandle(sj=first, ee=last, solver='ikSplineSolver',ccv=True )
        #cmds.rename(curve_out,curve)
    
        start_joint = self.id+'_start_bond'
        end_joint = self.id+'_end_bond'
        
        cmds.select(cl=True)
        cmds.joint(n=start_joint)
        cmds.matchTransform(start_joint,first)
        cmds.select(cl=True)
        cmds.joint(n=end_joint)
        cmds.matchTransform(end_joint,last)
        
        cmds.skinCluster(start_joint,end_joint,curve, name=self.id+'_scl', tsb=True)
        
         
        curve_info = cmds.arclen(curve, constructionHistory=True)
    

        mdn = cmds.createNode('multiplyDivide', name='{0}Stretch_mdn'.format(self.id))
        cmds.connectAttr('{0}.arcLength'.format(curve_info), '{0}.input1X'.format(mdn))
        cmds.setAttr('{0}.input2X'.format(mdn), cmds.getAttr('{0}.arcLength'.format(curve_info)))
        cmds.setAttr('{0}.operation'.format(mdn), 2)  # Divide
 
        # Connect to joints
        
        joints = ['tongue1','tongue2','tongue3','tongue4','tongue5']
        
        for j in joints[1:]:
            tx = cmds.getAttr('{0}.translateX'.format(j))
            mdl = cmds.createNode('multDoubleLinear', name='{0}Stretch_mdl'.format(j))
            cmds.setAttr('{0}.input1'.format(mdl), tx)
            cmds.connectAttr('{0}.outputX'.format(mdn), '{0}.input2'.format(mdl))
            cmds.connectAttr('{0}.output'.format(mdl), '{0}.translateX'.format(j))
        
        
        cmds.setAttr('{0}.dTwistControlEnable'.format(ikh), True)
        cmds.setAttr('{0}.dWorldUpType'.format(ikh), 4)  # Object up
        cmds.setAttr('{0}.dWorldUpAxis'.format(ikh), 0)  # Positive Y Up
        cmds.setAttr('{0}.dWorldUpVectorX'.format(ikh), 0)
        cmds.setAttr('{0}.dWorldUpVectorY'.format(ikh), 1)
        cmds.setAttr('{0}.dWorldUpVectorZ'.format(ikh), 0)
        cmds.setAttr('{0}.dWorldUpVectorEndX'.format(ikh), 0)
        cmds.setAttr('{0}.dWorldUpVectorEndY'.format(ikh), 1)
        cmds.setAttr('{0}.dWorldUpVectorEndZ'.format(ikh), 0)
        cmds.connectAttr('{0}.worldMatrix[0]'.format(start_joint), '{0}.dWorldUpMatrix'.format(ikh))
        cmds.connectAttr('{0}.worldMatrix[0]'.format(end_joint), '{0}.dWorldUpMatrixEnd'.format(ikh))
        
        cmds.rename(curve,self.id+'_curve')
            
        return
        
        c = control_cone(
                id = self.id+'_start',
                r = 1,
                rgb = [255,255,255],
                axis = [0,0,1]
                )

        c.snap_cbo(start)  
        ctr_start = c.control()
        cmds.pointConstraint(c.control(),'tongue2')
        
        c = control_cone(
                id = self.id+'_end',
                r = 1,
                rgb = [255,255,255],
                axis = [0,0,1]
                )
        c.snap_cbo(end) 
        ctr_end = c.control()
           

        curve = self.id+'_curve'
        ikh, effector, curve_out = cmds.ikHandle(sj=start, ee=end, solver='ikSplineSolver',ccv=True )
        cmds.rename(curve_out,curve)
        
        
        
        cmds.parentConstraint(ctr_start,joint_start,mo=True)
        cmds.parentConstraint(ctr_end,joint_end,mo=True)
        
        print(ctr_start)
        cmds.setAttr('{0}.dTwistControlEnable'.format(ikh), True)
        cmds.setAttr('{0}.dWorldUpType'.format(ikh), 4)  # Object up
        cmds.setAttr('{0}.dWorldUpAxis'.format(ikh), 0)  # Positive Y Up
        cmds.setAttr('{0}.dWorldUpVectorX'.format(ikh), 0)
        cmds.setAttr('{0}.dWorldUpVectorY'.format(ikh), 1)
        cmds.setAttr('{0}.dWorldUpVectorZ'.format(ikh), 0)
        cmds.setAttr('{0}.dWorldUpVectorEndX'.format(ikh), 0)
        cmds.setAttr('{0}.dWorldUpVectorEndY'.format(ikh), 1)
        cmds.setAttr('{0}.dWorldUpVectorEndZ'.format(ikh), 0)
        cmds.connectAttr('{0}.worldMatrix[0]'.format(ctr_start), '{0}.dWorldUpMatrix'.format(ikh))
        cmds.connectAttr('{0}.worldMatrix[0]'.format(ctr_end), '{0}.dWorldUpMatrixEnd'.format(ikh))
            
        
class expression_constraint_2p():
    
    
        def exe(self,ctr,W0,W1,W2,val,pow):
        
        #cmds.expression(s='if('+n+'.translateZ >=0 ){brow1_r_parentConstraint1.brow_rest1_rW0 = 1-('+n+'.translateZ/100.0);}else{brow1_r_parentConstraint1.brow_rest1_rW0 = 1+('+n+'.translateZ/100);}')
        #cmds.expression(s='if('+n+'.translateZ >=0 ){brow1_r_parentConstraint1.brow_up1_rW1 = '+n+'.translateZ/100.0;}else{brow1_r_parentConstraint1.brow_up1_rW1 = 0.0;}')
        #cmds.expression(s='if('+n+'.translateZ <=0 ){brow1_r_parentConstraint1.brow_down1_rW2 = ('+n+'.translateZ/100.0)*-1;}else{brow1_r_parentConstraint1.brow_down1_rW2 = 0.0;}')  
        
            pow = str(pow)
            cmds.expression(s='if('+ctr+'.'+val+' >=0 ){'+W0+' = 1-('+ctr+'.'+val+'/'+pow+');}else{'+W0+' = 1+('+ctr+'.'+val+'/'+pow+');}')
            cmds.expression(s='if('+ctr+'.'+val+' >=0 ){'+W1+' = '+ctr+'.'+val+'/'+pow+';}else{'+W1+' = 0.0;}')
            cmds.expression(s='if('+ctr+'.'+val+' <=0 ){'+W2+' = ('+ctr+'.'+val+'/'+pow+')*-1;}else{'+W2+' = 0.0;}')  
            
class rig_brow(rig_base):
        

    def __init__(self):
        self.setup()
    
    def set_suite(self,suite):
        self.suite = suite
      
    def exe(self):              
           
        xsym = 1
        if self.sym==1:
            xsym = -1
        
        dock = 'dock_'+self.id+self.symsuf
        cmds.spaceLocator(n=dock) 
        hide_node(dock)
        brow_parent = 'head'
        
        for i in range(4):
            v = str(i+1)
            
            
           
            
            c = control_cube(
                id = self.id+v,
                suf = self.symsuf,
                size = [1.0,1.0,1.0],
                rgb = [255,255,255],
                )                
            c.snap_cbo(dock)  
            c.parent(dock)
            cmds.select(c.cbo)
            cmds.move((i*1.2)*-1*xsym,0,0) 
            ctr = c.control()
            
            c = control_cone(
                id = self.id+v+'_micro',
                suf = self.symsuf,
                r = 0.15,
                h = 0.5,
                sx = 8,
                rgb = [255,255,255],
                axis = [0,0,-1]
                )                
            c.snap_cbo(self.id+v+self.symsuf)  
            c.parent(brow_parent)
            c.move_offset_control(0,-1.00,0)  
            
            ctr_micro = c.control()

            
            cmds.parentConstraint(self.id+'_rest'+v+self.symsuf,ctr_micro,w=-0.0)
            cmds.parentConstraint(self.id+'_up'+v+self.symsuf,ctr_micro,w=-0.0)
            cmds.parentConstraint(self.id+'_down'+v+self.symsuf,ctr_micro,w=0)
        
            ex = expression_constraint_2p()
            ex.exe(ctr,
                ctr_micro+'_parentConstraint1.'+self.id+'_rest'+v+self.symsuf+'W0',
                ctr_micro+'_parentConstraint1.'+self.id+'_up'+v+self.symsuf+'W1',
                ctr_micro+'_parentConstraint1.'+self.id+'_down'+v+self.symsuf+'W2','translateZ',
                1.5)
        
        
            cmds.parentConstraint(ctr_micro, self.id+v+self.symsuf)

            hide_node(self.id+'_rest'+v+self.symsuf)
            hide_node(self.id+'_up'+v+self.symsuf)
            hide_node(self.id+'_down'+v+self.symsuf)
        

            
class rig_eyelid(rig_base):
        

    def __init__(self):
        self.setup()
    
    def set_suite(self,suite):
        self.suite = suite

    def set_names(self,upper,lower):
        self.names= [upper,lower]
      
    def exe(self):              
        
        dock = 'dock_'+self.id+self.symsuf
        cmds.spaceLocator(n=dock) 
        hide_node(dock)
        brow_parent = 'head'
        
        c = control_cube(
                    id = self.id+self.symsuf,
                    suf = self.symsuf,
                    size = [1.0,1.0,1.0],
                    rgb = [255,255,255],
                    )  
        c.snap_cbo(dock)  
        c.parent(dock)
        cmds.select(c.cbo)
        ctr = c.control()
        
        for y in range(2):
            
            name = self.id+'_'+self.names[y]
            
            for i in range(3):
                v = str(i+1)                   
                                
                c = control_cone(
                    id = name+v+'_micro',
                    suf = self.symsuf,
                    r = 0.15,
                    h = 0.5,
                    sx = 8,
                    rgb = [255,255,255],
                    axis = [0,0,-1]
                    )                
                c.snap_cbo(name+v+self.symsuf)  
                c.parent(brow_parent)
                c.move_offset_control(0,-1.00,0)  
                
                ctr_micro = c.control()
    
                
                cmds.parentConstraint(name+'_rest'+v+self.symsuf,ctr_micro,w=-0.0)
                cmds.parentConstraint(name+'_open'+v+self.symsuf,ctr_micro,w=-0.0)
                cmds.parentConstraint(name+'_close'+v+self.symsuf,ctr_micro,w=0)
            
                ex = expression_constraint_2p()
                ex.exe(ctr,
                    ctr_micro+'_parentConstraint1.'+name+'_rest'+v+self.symsuf+'W0',
                    ctr_micro+'_parentConstraint1.'+name+'_open'+v+self.symsuf+'W1',
                    ctr_micro+'_parentConstraint1.'+name+'_close'+v+self.symsuf+'W2','translateZ',
                    1.5)
            
            
                cmds.parentConstraint(ctr_micro, name+v+self.symsuf)
    
                hide_node(name+'_rest'+v+self.symsuf)
                hide_node(name+'_open'+v+self.symsuf)
                hide_node(name+'_close'+v+self.symsuf)
            
                     
class rig_genf(rig_base):
        

    def __init__(self):
        self.setup()
    
    def set_suite(self,suite):
        self.suite = suite

    def set_names(self,cli,lab,vay_up,vay_dn,vay_corner):
        self.cli = cli
        self.lab = lab
        self.vay_up = vay_up
        self.vay_dn = vay_dn
        self.vay_corner = vay_corner
      
    def set_hub(self,hub):
        self.hub = hub 
        
    def do_lab(self):
                
        for i in range(2):
            suf = self.sym_arr[i]             
        
            for i in range(4):
                v = str(i+1)
                goal = self.lab+v+suf

                c = control_cube(
                    id = self.lab+v,
                    suf = suf,
                    rgb = self.rgb_dict['lab'],
                    size = [1,1,1],
                    span = [2,2,2] 
                    )                              
                c.snap_cbo(goal)        
                c.parent(self.suite.id)
                c.move_offset_control(0,0,-6,nopivot=True)
                c.enable_proxy(self.hub)
                c.parentConstraintProxy(goal)

     
    def do_vay(self):
        
        for i in range(2):
            suf = self.sym_arr[i]   
            
            goal = self.vay_corner+suf
            c = control_cube(
                id = self.vay_corner+suf,
                suf = suf,
                rgb = self.rgb_dict['vay'],
                size = [1,1,1],
                span = [2,2,2] 
            )                              
            c.snap_cbo(goal)
            c.parent(self.suite.id)
            c.move_offset_control(0,0,-6,nopivot=True)
            c.enable_proxy(self.hub)
            c.parentConstraintProxy(goal)
      
        goal = self.vay_up
        c = control_cube(
                id = self.vay_up,
                suf = suf,
                rgb = self.rgb_dict['vay'],
                size = [1,1,1],
                span = [2,2,2] 
                )                              
        c.snap_cbo(goal)
        c.parent(self.suite.id)
        c.move_offset_control(0,0,-6,nopivot=True)
        c.enable_proxy(self.hub)
        c.parentConstraintProxy(goal)
        
        goal = self.vay_dn
        c = control_cube(
            id = self.vay_dn,
            suf = suf,
            rgb = self.rgb_dict['vay'],
            size = [1,1,1],
            span = [2,2,2]  
        )                  
                    
        c.snap_cbo(goal)
        c.parent(self.suite.id)
        c.move_offset_control(0,0,-6,nopivot=True)
        c.enable_proxy(self.hub)
        c.parentConstraintProxy(goal)
                     
    def exe(self):              
        
        self.do_lab()
        self.do_vay()


class rig_orrifice(rig_base):
        

    def __init__(self):
        self.setup()
    
    def set_names(self,names):
        self.names = names      

    def set_base_position(self,pos):
        cmds.xform(self.base,ws=True,a=True,t=pos)
        
    def exe(self):              
        
        pos = []
        goals = []
        goal_cons = []
        goal_docks = []
        
        for j in self.names:
            pos.append(cmds.xform(j,t=True,q=True,a=True,ws=True))
            cur_goal = j+'_goal'
            cur_goalcon = j+'_goalcon'
            cur_goaldock = j+'_goaldock'
            
            goals.append(cur_goal)
            goal_cons.append(cur_goalcon)
            goal_docks.append(cur_goaldock)
            
            cmds.select(cl=True)
            cmds.joint(n=cur_goal)
            cmds.setAttr(cur_goal+'.radius',0.1)
            cmds.matchTransform(cur_goal,j)
            
            cmds.select(cl=True)
            cmds.joint(n=cur_goalcon)
            cmds.setAttr(cur_goal+'.radius',0.1)
            cmds.matchTransform(cur_goalcon,cur_goal)
            cmds.makeIdentity(cur_goalcon, apply=True, t=1, r=1, s=1)
            cmds.parentConstraint(cur_goal,cur_goalcon,mo=True)
            
            cmds.select(cl=True)
            cmds.joint(n=cur_goaldock)
            cmds.setAttr(cur_goal+'.radius',0.1)
            cmds.matchTransform(cur_goaldock,cur_goalcon)
            cmds.parent(cur_goaldock,cur_goalcon)
             
        pos_total = [0,0,0]
        for p in pos:
            pos_total[0] = pos_total[0]+p[0]
            pos_total[1] = pos_total[1]+p[1]
            pos_total[2] = pos_total[2]+p[2]
             
        num = len(pos)
         
        for i in range(3):
            pos_total[i] = pos_total[i]/num
                      
        goal_c = self.id+'_goal_center'
        cmds.select(cl=True)
        cmds.joint(n=goal_c)
        cmds.setAttr(goal_c+'.radius',0.015)
        cmds.xform(goal_c,t=pos_total,a=True,ws=True)

        for j in goals:
            cmds.parent(j,goal_c)

        base = self.id+'_base'        
        cmds.polyPyramid(n=base,w=3,axis=[0,0,1])
        cmds.rotate(0,0,45)
        cmds.makeIdentity(base, apply=True, t=1, r=1, s=1)
        set_color(base,self.rgb_dict['ex'])
        c = control_torus(
            id = self.id+'_ring',
            rgb = self.rgb_dict['ex'],
            rad = .2,
            hrad = .16,
            spans = 10,
            ) 
        c.snap_cbo(goal_c)
        ring = c.control()        
        co_ring = c
        #c.move_offset_control(0, 0, -3,nopivot=True) 
        
        ctrs = []
        for j in self.names:
            
            cgoal = 'cgoal_'+j
            cmds.spaceLocator(n=cgoal)
            cmds.matchTransform(cgoal,j) 
            hide_node(cgoal)
            cmds.parent(cgoal,ring)
            
            cgoal_constraint = 'goalconstraint_'+j
            cmds.spaceLocator(n=cgoal_constraint) 
            hide_node(cgoal_constraint)
            cmds.pointConstraint(cgoal,cgoal_constraint,mo=False)
            
            
            c = control_cone(
                id = j,
                rgb = self.rgb_dict['ex'],
                r = .4,
                h = .7,
                rcp = True,
                sx = 10,
                sz = 3,
                axis = [0,0,1]
                ) 
            c.snap_cbo(j)
            c.move_offset_control(0, 0, -1,nopivot=True)
            c.parent(cgoal_constraint)
            ctrs.append(c.control())
            
        for g,c in zip(goal_docks,ctrs):
           
            connect_xform(c,g)
            
            
            
        
        cmds.connectAttr(ring+'.scale', goal_c+'.scale')
        
        #c.move_offset_control(0,0,-2)
        #c.parent(g_group_controls)
        #c_root = c.control()   
        
        cmds.xform(co_ring.cbo, a=True,ws=True,t=[0,0,-2])
        co_ring.parent(base)
        
        
        for j,d in zip(self.names,goal_docks):
            cmds.parentConstraint(d,j,mo=True)       
        
        self.base = base
        
        
class rig_suite(rig_base):


    def __init__(self):
        self.setup()
   
            
    def exe(self):          
        cmds.spaceLocator(name=self.id)
        cmds.matchTransform(self.id,self.parent)    
        cmds.makeIdentity(self.id, apply=True, t=1, r=1, s=1)
        cmds.parent(self.id,self.parent)
                    

    
                                  
class female_rig_class():
   

    def __init__(self):
        self.rgb = {}
        
    def set_rgb(self,name,rgb):
        self.rgb[name] = [rgb[0]/255.0,rgb[1]/255.0,rgb[2]/255.0]    
    
    def create_skeleton_assistants(self,add_controls):

        suf_arr = [g_axis_right,g_axis_left]
        
        for i in range(2):
            
            suf = suf_arr[i]

               
            ##################################
            #fl = assist_flesh(
            #                id = 'deltoid',
            #                suf = suf,
            #                follow = 'upperarm'+suf,
            #                parent = 'clavicle'+suf,
            #                goal = 'deltoid'+suf,
            #                power = 6,
            #                rgb = [255,0,0]
            #                ) 
             
            #cmds.parentConstraint(fl.goal,'deltoid'+suf)               
            ##################################
            #assist_flesh(
            #                id = 'pit',
            #                suf = suf,
            #                follow = 'upperarm'+suf,
            #                parent = 'clavicle'+suf,
            #                goal = 'pit'+suf,
            #                power = 6,
            #                rgb = [255,0,0]
            #                )                 
            
            #cmds.parentConstraint(fl.goal,'pit'+suf) 
            
            ##################################
            assist_muscle(
                            id = 'bicep',
                            suf = suf,
                            parent = 'upperarm'+suf,
                            reactor = 'lowerarm'+suf,
                            goal = 'bicep'+suf,
                            power = .003,
                            rgb = [255,0,0]
                            )  
            ##################################
            assist_muscle(
                            id = 'tricep',
                            suf = suf,
                            parent = 'upperarm'+suf,
                            reactor = 'lowerarm'+suf,
                            goal = 'tricep'+suf,
                            power = .1,
                            invert = 110,
                            rgb = [255,0,0]
                            )           
                    
    def exe(self):    

        
        r = rig_scapula()
        r.set_id('scapula')
        r.set_parent('spine5')
        r.set_rgb(self.rgb['scapula'])
        r.set_sym(1,g_axis_right)
        r.exe()
        r.set_sym(1,g_axis_left)
        r.exe()
        
        
        r = rig_breast()
        r.set_id('breast')
        r.set_rgb(self.rgb['breast'])
        r.set_sym(1,g_axis_right)
        r.set_parent('spine4')
        r.exe()
        r.set_sym(1,g_axis_left)
        r.exe()
        
        r = rig_nip()
        r.set_id('nip')
        r.set_rgb(self.rgb['nip'])
        r.set_sym(1,g_axis_right)
        r.set_parent('breast'+g_axis_right)
        r.exe()
        r.set_sym(1,g_axis_left)
        r.set_parent('breast'+g_axis_left)
        r.exe()
         
        r = rig_lat()
        r.set_id('lat')
        r.set_parent('spine5')
        r.set_rgb(self.rgb['lat'])
        r.set_sym(1,g_axis_right)
        r.exe()
        r.set_sym(1,g_axis_left)
        r.exe()
           
  
        r = rig_belly()
        r.set_id('belly')
        r.set_rgb(self.rgb['belly'])
        r.set_parent('spine1') 
        r.exe()
        
        r = rig_spinae()
        r.set_id('spinae')
        r.set_rgb(self.rgb['spinae'])
        r.set_parent('spine1')
        r.set_sym(1,g_axis_right)
        r.exe()
        r.set_sym(1,g_axis_left)
        r.exe()
        
        r = rig_glute()
        r.set_id('glute')
        r.set_parent('pelvis')
        r.set_power(4)
        r.set_rgb(self.rgb['glute'])
        r.set_joint_rgb(255,0,0)
        r.set_sym(0,g_axis_right)
        r.set_follow_target('thigh'+g_axis_right)
        r.set_goal_target('glute'+g_axis_right)
        r.exe()
        r.set_sym(1,g_axis_left)
        r.set_follow_target('thigh'+g_axis_left)
        r.set_goal_target('glute'+g_axis_left)
        r.exe()     
        
        r = rig_ham()
        r.set_id('ham')
        r.set_rgb(self.rgb['ham'])
        r.set_sym(0,g_axis_right)
        r.set_parent('thigh'+g_axis_right)
        r.exe()
        r.set_sym(1,g_axis_left)
        r.set_parent('thigh'+g_axis_left)
        r.exe()
        
        r = rig_quad()
        r.set_id('quad')
        r.set_rgb(self.rgb['quad'])
        r.set_sym(1,g_axis_right)
        r.set_parent('thigh'+g_axis_right)
        r.exe()
        r.set_sym(1,g_axis_left)
        r.set_parent('thigh'+g_axis_left)
        r.exe()
        
        r = rig_gastro()
        r.set_id('gastro_outer')
        r.set_rgb(self.rgb['gastro'])
        r.set_sym(1,g_axis_right)
        r.set_parent('calf_twist1'+g_axis_right)
        r.exe()
        r.set_sym(1,g_axis_left)
        r.set_parent('calf_twist1'+g_axis_left)
        r.exe()
        

        
        cmds.group( em=True, name=g_group_controls)
                  
        self.create_skeleton_assistants(False)
     
     
        ##################################
        c = control_pyramid(
                id = 'root',
                rgb = self.rgb['root'],
                w = 4.2,
                axis = [0,0,-1]
                )
        c.snap_cbo('root')
        c.move_offset_control(0,0,-2)
        c.parent(g_group_controls)
        c_root = c.control()
        
        
        ##################################
        c = control_torus(
                id = 'hip',
                #rgb = [1,.2,.6],
                rgb = self.rgb['hip'],
                rad = 30.0,
                hrad = .025,
                axis = [0,0,1]
                )     
        c.snap_cbo('hip')
        c.parent(c_root)
        c_hip = c.control()
        c.parentConstraint('hip')    
        
        ##################################        
        c = control_torus(
                id = 'pelvis',
                rgb = self.rgb['pelvis'],
                rad = 25.0,
                hrad = .02,
                axis = [0,0,1]
                )     
        c.snap_cbo('pelvis')
        c.override_rotation_cbo(None,0,None)
        c.parent(c_hip)
        c_pelvis = c.control()
        c.orientConstraint('pelvis')  
        
        ##################################
        c = control_torus(
                id = 'abdomen_lower',
                rgb = g_ctr_rot1,
                rad = 20.0,
                hrad = .0005,
                axis = [1,0,0]
                )     
        c.snap_cbo('spine1')
        c.override_rotation_cbo(None,-90,None)
        c.parent(c_hip)
        c_spine1 = c.control()
        c.orientConstraint('spine1')
        c.orientConstraint('spine2',w=0.5)

        ##################################
        c = control_torus(
                id = 'abdomen_upper',
                rgb = g_ctr_rot1,
                rad = 18.0,
                hrad = .0005,
                axis = [1,0,0]
                )     
                
        c.snap_cbo('spine3')
        c.override_rotation_cbo(None,-90,None)
        c.parent(c_spine1)
        c_spine2 = c.control()
        c.orientConstraint('spine3')
        c.orientConstraint('spine2',w=0.5)
        c.orientConstraint('spine4',w=0.5)

        ##################################
        c = control_torus(
                id = 'chest',
                rgb = g_ctr_rot1,
                rad = 12.0,
                hrad = .0005,
                axis = [1,0,0]
                )     
        c_spine3 = c.control()
        c.snap_cbo('spine5')
        c.move_offset_control(0,0,9)
        c.override_rotation_cbo(None,-90,None)
        c.parent(c_spine2)        
        c.orientConstraint('spine5')
        c.orientConstraint('spine4',w=0.5)
        c.orientConstraint('neck1',w=0.3)
        
        
        ##################################
        c = control_torus(
                id = 'neck',
                rgb = g_ctr_rot1,
                rad = 10.0,
                hrad = .0005,
                axis = [1,0,0]
                )     
        c_head = c.control()
        c.snap_cbo('neck1')
        c.move_offset_control(0,0,6)
        c.override_rotation_cbo(None,-90,None)
        c.parent(c_spine3)        
        c.orientConstraint('neck1',w=0.7)
        c.orientConstraint('neck2',w=0.6)        
        c_neck = c.control()
        
        ##################################
        c = control_torus(
                id = 'head',
                rgb = g_ctr_rot1,
                rad = 14.0,
                hrad = .0005,
                axis = [1,0,0]
                )     
        c_head = c.control()
        c.snap_cbo('head')
        c.override_rotation_cbo(0,90,None)
        c.move_offset_control(0,-4,24)
        c.parent(c_neck)        
        c.orientConstraint('head')
        c.orientConstraint('neck2',w=0.4)


        r = rig_fingers()
        r.set_fingers('finger_thumb','finger_index','finger_middle','finger_ring','finger_pinky')
        r.set_rgb(self.rgb['finger'])
        r.set_sym(0,g_axis_right)
        r.set_parent('hand'+g_axis_right)
        r.exe()
        r.set_sym(1,g_axis_left)
        r.set_parent('hand'+g_axis_left)
        r.exe()

        r = rig_toes()
        r.set_toes('toe_big','toe_long','toe_middle','toe_ring','toe_little')
        r.set_rgb(self.rgb['toe'])
        r.set_sym(0,g_axis_right)
        r.set_parent('ball'+g_axis_right)
        r.exe()
        r.set_sym(1,g_axis_left)
        r.set_parent('ball'+g_axis_left)
        r.exe()
        
        r = rig_clavicle()
        r.set_id('clavicle')
        r.set_parent('spine5')
        r.set_rgb(self.rgb['clavicle'])
        r.set_sym(0,g_axis_right)
        r.exe()
        r.set_sym(1,g_axis_left)
        r.exe()
        
        #ARMS
        #############################################################
        arm_ids = ['upperarm','lowerarm','hand'] 
        fk = rig_arm_fk()
        fk.set_id('arm_fk')
        fk.dict_rgb('upperarm',self.rgb['upperarm'])
        fk.dict_rgb('lowerarm',self.rgb['lowerarm'])
        fk.dict_rgb('hand',self.rgb['hand'])      
        fk.set_arm_names(arm_ids)
        fk.set_parent('c_clavicle'+g_axis_right)
        fk.set_sym(0,g_axis_right)            
        fk.exe()
        
        ik = rig_arm_ik()
        ik.set_id('arm_ik')
        ik.set_control_names('arm','elbow')
        ik.set_parent(g_group_controls)
        ik.dict_rgb('arm',self.rgb['arm'])
        ik.dict_rgb('elbow',self.rgb['elbow'])      
        ik.set_arm_names(arm_ids)
        ik.set_sym(0,g_axis_right)            
        ik.exe() 
        
        switch = ik_fk_switch()
        switch.set_start_mode(True)
        switch.set_controls(ik.controls[0],fk.controls,ik.controls)
        switch.set_chains(fk.base_chain,fk.chain,ik.chain)
        switch.exe()
               
               
        fk.set_parent('c_clavicle'+g_axis_left)
        fk.set_sym(1,g_axis_left)            
        fk.exe()
        ik.set_sym(1,g_axis_left)            
        ik.exe() 
        
        switch = ik_fk_switch()
        switch.set_start_mode(True)
        switch.set_controls(ik.controls[0],fk.controls,ik.controls)
        switch.set_chains(fk.base_chain,fk.chain,ik.chain)
        switch.exe()
        
        #LEGS
        #############################################################
        leg_ids = ['thigh','calf','foot','ball','toetip'] 
        fk = rig_leg_fk()
        fk.set_id('leg_fk')
        fk.set_parent('c_pelvis')
        fk.dict_rgb('thigh',self.rgb['thigh'])
        fk.dict_rgb('calf',self.rgb['calf'])
        fk.dict_rgb('foot',self.rgb['foot'])
        fk.dict_rgb('ball',self.rgb['ball'])        
        fk.set_leg_names(leg_ids)
        fk.set_sym(0,g_axis_right)            
        fk.exe()
        
        ik = rig_leg_ik()
        ik.set_id('leg_ik')
        ik.set_control_names('leg','knee')
        ik.set_parent(g_group_controls)
        ik.dict_rgb('leg',self.rgb['leg'])
        ik.dict_rgb('knee',self.rgb['knee'])
        ik.dict_rgb('toes',self.rgb['toes'])
        ik.dict_rgb('tiptoe',self.rgb['tiptoe'])      
        ik.set_leg_names(leg_ids)
        ik.set_sym(0,g_axis_right)            
        ik.exe() 
        
        switch = ik_fk_switch()
        switch.set_start_mode(True)
        switch.set_controls(ik.controls[0],fk.controls,ik.controls)
        switch.set_chains(fk.base_chain,fk.chain,ik.chain)
        switch.exe()
               
        fk.set_sym(1,g_axis_left)            
        fk.exe()
        ik.set_sym(1,g_axis_left)            
        ik.exe()

        switch = ik_fk_switch()
        switch.set_start_mode(True)
        switch.set_controls(ik.controls[0],fk.controls,ik.controls)
        switch.set_chains(fk.base_chain,fk.chain,ik.chain)
        switch.exe()
         
        #FACE
        #############################################################                
        make_controls_face('controls_face')
        
        suite = rig_suite()
        suite.set_id('suite_genf')
        suite.set_parent('genf')
        suite.exe()
        
        r = rig_genf()
        r.set_symsufs(g_axis_right,g_axis_left)
        r.set_names('cli','lab','vay_upper','vay_lower','vay_corner')
        r.set_suite(suite)
        r.set_hub('genf')
        r.dict_rgb('cli',self.rgb['cli'])
        r.dict_rgb('lab',self.rgb['lab'])
        r.dict_rgb('vay',self.rgb['vay'])
        r.exe()
        
        
        r = rig_brow()
        r.set_id('brow')
        r.set_sym(0,g_axis_right)
        r.exe()
        r.set_sym(1,g_axis_left)
        r.exe()
        
        r = rig_tongue()
        r.set_id('tongue')
        r.set_joint_num(5)
        r.exe()
        
        #r = rig_eyelid()
        #r.set_id('eyelid')
        #r.set_names('upper','lower')
        #r.set_sym(0,g_axis_right)
        #r.exe()
        #r.set_sym(1,g_axis_left)
        #r.exe()
        
        #make_controls_genf(
        #         suite = 'suite_genf',
        #         suite_par = 'genf',
        #         names = ['cli','lab','vay_upper','vay_corner','vay_lower'],
        #         cli_rgb = [1,0,0],
        #         lab_rgb = [[1,.3,.2],[1,.31,.21],[1,.3,.2]],
        #         vay_rgb = [[.8,.15,.45],[.8,.13,.43],[.8,.11,.41]])
        
        r = rig_orrifice()
        r.set_id('ex')
        r.set_names(['ex_u','ex_d','ex'+g_axis_right,'ex'+g_axis_left])
        r.dict_rgb('ex',self.rgb['ex'])
        r.exe()
        r.set_base_position([-35,0,70])
      
  
def human_rig_basic(args):
    #this_file = cmds.file(q=True, sn=True)
    #cmds.file('C:/Users/16C24E/Desktop/Final Character/0500_continue.mb', o=True, f=True)
    cmds.file('O:/one/asset/archive/human_female_final.mb', o=True, f=True)
    rig = female_rig_class()
    
    rgb_rot1 = [255,255,255]
    rgb_rot2 = [255,150,0]
        
    rig.set_rgb('root',[255,0,0])
    rig.set_rgb('hip',[255,255,255])
    rig.set_rgb('pelvis',[255,255,180])
    rig.set_rgb('abdomen_lower',rgb_rot1)
    rig.set_rgb('abdomen_upper',rgb_rot1)
    rig.set_rgb('chest',rgb_rot1)
    rig.set_rgb('clavicle',rgb_rot2)
   
    rig.set_rgb('upperarm',rgb_rot1)
    rig.set_rgb('lowerarm',rgb_rot1)
    rig.set_rgb('hand',rgb_rot1)
    rig.set_rgb('arm',rgb_rot1)
    rig.set_rgb('elbow',rgb_rot1)
    
    rig.set_rgb('thigh',rgb_rot1)
    rig.set_rgb('calf',rgb_rot1)
    rig.set_rgb('foot',rgb_rot1)
    rig.set_rgb('ball',rgb_rot1)
    rig.set_rgb('leg',rgb_rot1)
    rig.set_rgb('knee',rgb_rot1)
    rig.set_rgb('toes',[255,255,0])
    rig.set_rgb('tiptoe',[255,0,255])
    
    rig.set_rgb('scapula',[255,40,40])
    rig.set_rgb('breast',[215,100,60])
    rig.set_rgb('nip',[255,40,20])
    
    rig.set_rgb('lat',[255,240,80])
    rig.set_rgb('spinae',[10,220,10])
    rig.set_rgb('belly',[10,220,140])
    rig.set_rgb('glute',[10,180,230])
    rig.set_rgb('quad',[30,120,250])
    rig.set_rgb('ham',[60,80,230])
    rig.set_rgb('gastro',[140,60,230])
    
    rig.set_rgb('cli',[255,0,0])
    rig.set_rgb('lab',[255,75,50])
    rig.set_rgb('vay',[220,20,100])    
    
    rig.set_rgb('ex',[220,220,20]) 
    
    

    rig.set_rgb('clavicle',rgb_rot2)
    rig.set_rgb('finger',rgb_rot1)
    rig.set_rgb('toe',rgb_rot1)
    rig.exe() 


window = cmds.window( 
    title='Human Rigger',  
    width=autob_win_y_max,
    resizeToFitChildren=True) 

scrollLayout = cmds.scrollLayout(
    horizontalScrollBarThickness=16,
    verticalScrollBarThickness=16)
    
cmds.columnLayout(
    columnOffset=['left',0])
 

cmds.button( label='Draft', 
             width = 100,
             command=human_rig_basic )
  

cmds.setParent( '..' )
                                               
cmds.showWindow( window )