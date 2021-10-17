import maya.cmds as cmds

g_data_joint_left_h8 = 'left_abbr'
g_data_joint_right_h8 = 'righ_abbr'

g_data_num_spine_h8 = 'num_spine'
g_data_num_neck_h8 = 'num_neck'

g_ph_symx = '<'
g_ph_symx_text = 'C15Z94'

autob_win_y_max = 300
g_group_draft_h8 = 'biped_draft_h8'
g_group_skeleton_h8 = 'biped_skeleton_h8'
g_group_rig_h8 = 'autobiped_rig'

autob_data = 'dataobj#'

g_draft_pelvis_h8 = 'pelvis#'
g_draft_spine_h8 = 'spine^#'
g_draft_neck_h8 = 'neck^#'
g_draft_head_h8 = 'head#'

g_draft_thigh_h8 = 'thigh#'
g_draft_shin_h8 = 'shin#'
g_draft_foot_h8 = 'foot#'
g_draft_toe_h8 = 'toe#'
g_draft_toetip_h8 = 'toetip#'

g_draft_clavicle_h8 = 'clavicle#'
g_draft_upperarm_h8= 'upperarm#'
g_draft_lowerarm_h8 = 'lowerarm#'
g_draft_hand_h8 = 'hand#'

class Object(object):
    pass
     
def lerpV3(loc1,loc2,amount):
    
    len = [loc2[0]-loc1[0],loc2[1]-loc1[1],loc2[2]-loc1[2]]
    
    return [(len[0]*amount)+loc1[0],(len[1]*amount)+loc1[1],(len[2]*amount)+loc1[2]]
        
def split_joint(name,low,high,num):  
    
    gap = 1.0/(num+1)
    
    twists = []
    cmds.select(low,r=True)
    
    for t in range(num):
        loc = lerpV3(cmds.xform(low,q=1,ws=1,rp=1),cmds.xform(high,q=1,ws=1,rp=1),(t+1)*gap)
        create_autob_joint(name+str(t+1),loc)
        
    cmds.parent(high,name+str(num))


class node_h8:
    
    def set_parent(self,target):
        cmds.parent(self.get(),target.get())
    
    def get(self):
        return self.name
        
    def match(self,j):
        cmds.matchTransform(self.get(),j.get()) 
    
    def get_parent(self):
        return joint_h8().be(cmds.listRelatives(self.get(),parent=True,shapes=True)[0])
        
    def select(self):
        cmds.select(cl=True)
        cmds.select(self.get())
        return self
           
    def move(self,pos):
        self.select()
        pos = pos.get_array()
        cmds.move(pos[0], pos[1], pos[2],r=True,os=True,wd=True )
        return self
    
    def rotate(self,pos):
        self.select()
        cmds.rotate(pos.x, pos.y, pos.z,r=True )
        return self
    
    def orient_constraint(self,target):
        cmds.orientConstraint(target.get(), self.get(), mo=True )
        return self
        
    def point_constraint(self,target):
        cmds.pointConstraint(target.get(),self.get(),mo=True)
        return self
    
    def parent_constraint(self,target):
        cmds.parentConstraint(target.get(), self.get(), mo=True) 
        return self
        
    def remove_transform_attrs(self):
        cmds.setAttr(self.name+".tx", keyable=False, channelBox=False)
        cmds.setAttr(self.name+".ty", keyable=False, channelBox=False)
        cmds.setAttr(self.name+".tz", keyable=False, channelBox=False)
        cmds.setAttr(self.name+".rx", keyable=False, channelBox=False)
        cmds.setAttr(self.name+".ry", keyable=False, channelBox=False)
        cmds.setAttr(self.name+".rz", keyable=False, channelBox=False)
        cmds.setAttr(self.name+".sx", keyable=False, channelBox=False)
        cmds.setAttr(self.name+".sy", keyable=False, channelBox=False)
        cmds.setAttr(self.name+".sz", keyable=False, channelBox=False)
        cmds.setAttr(self.name+".v",  keyable=False, channelBox=False)
    
    def add_attr_float(self,ln='Error',nn='Error', keyable=True, r=True, hidden=False, dv=0.0, min=0.0, max=1.0):
        cmds.addAttr(self.get(), longName=ln, nn=nn, keyable=keyable, r=r, hidden=hidden, attributeType='float', dv=dv, min=min, max=max)
        return self
    
    def add_attr_bool(self,ln='Error',nn='Error', keyable=True, r=True, hidden=False, dv=bool):
        cmds.addAttr(self.get(), longName=ln, nn=nn, keyable=keyable, r=r, hidden=hidden, attributeType='bool', dv=0.0)
        return self
    
    def add_attr_int(self,type="byte",ln='Error',nn='Error', keyable=True, r=True, hidden=False, dv=0, min=0, max=100):
        cmds.addAttr(self.get(), longName=ln, nn=nn, keyable=keyable, r=r, hidden=hidden, attributeType=type, dv=dv, min=min, max=max)
        return self
                      
    def freeze(self):
        cmds.makeIdentity( apply=True, t=1, r=1, s=1)
        return self
    
    def new(self,name):
        self.name = name        
        
                
    def __init__(self): 
        self.name=None
 

class proxy_h8(node_h8):
    
    def get(self):
        return self.name
                      
    def new(self,name,r=1.2):
        self.name = name
        cmds.sphere(r=r, n=name)                
        return self
            
    def be(self,name):
        self.name = name
        return self
     
    def spawn_joint(self,name):
        xform = cmds.xform(self.name,q=1,ws=1,rp=1)
        xform = vec3_h8(xform[0],xform[1],xform[2])
        return joint_h8().new(name,xform)
     
    def spawn_joint_symx(self,name):
        xform = cmds.xform(self.name,q=1,ws=1,rp=1)
        xform = vec3_h8(xform[0],xform[1],xform[2])
        return joint_symx_h8().new(name,xform)
 
    def set_color(self,rgb):
        rgb = rgb.get_array()
        cmds.setAttr( self.name+'.overrideEnabled', 1)
        cmds.setAttr( self.name+'.overrideRGBColors', 1)
        cmds.setAttr( self.name+'.overrideColorR', rgb[0])
        cmds.setAttr( self.name+'.overrideColorG', rgb[1])
        cmds.setAttr( self.name+'.overrideColorB', rgb[2])
        
                              
class joint_h8(node_h8):
    
    def get(self):
        return self.name
                      
    def new(self,name,pos):
        self.name = name
        cmds.joint(p=pos.get_array(),n=name)
        return self
            
    def be(self,name):
        self.name = name
        return self
        
    def set_color(self,rgb):
        cmds.setAttr( self.name+'.overrideEnabled', 1)
        cmds.setAttr( self.name+'.overrideRGBColors', 1)
        cmds.setAttr( self.name+'.overrideColorR', rgb.r)
        cmds.setAttr( self.name+'.overrideColorG', rgb.g)
        cmds.setAttr( self.name+'.overrideColorB', rgb.b)
    
class joint_symx_h8(joint_h8):
    
    def get(self):
        return self.name
                      
    def new(self,name,pos):
        self.name = name.replace(g_ph_symx,g_ph_symx_text)
        cmds.joint(p=pos.get_array(),n=self.name)
        return self
            
    def be(self,name):
        self.name = name
        return self
        
    def set_color(self,rgb):
        cmds.setAttr( self.name+'.overrideEnabled', 1)
        cmds.setAttr( self.name+'.overrideRGBColors', 1)
        cmds.setAttr( self.name+'.overrideColorR', rgb[0])
        cmds.setAttr( self.name+'.overrideColorG', rgb[1])
        cmds.setAttr( self.name+'.overrideColorB', rgb[2])
           
class control_h8(node_h8):
    
    def get(self):
        return self.name
     
    def set_color(self,rgb):        
        cmds.setAttr( self.name+'.overrideEnabled', 1)
        cmds.setAttr( self.name+'.overrideRGBColors', 1)
        cmds.setAttr( self.name+'.overrideColorR', rgb.r)
        cmds.setAttr( self.name+'.overrideColorG', rgb.g)
        cmds.setAttr( self.name+'.overrideColorB', rgb.b)
        cmds.setAttr( self.name+'.overrideShading', 0) 
  
                      
    def new(self):
        return self
            
    def be(self,name):
        self.name = name
        return self
        
class ctr_ring_h8(control_h8):
    
    
    def new(self,name,r=1.2, hr=0.05, axis=(0, 0, 0), msw=360,ssw=360, esw=0,s=2,nsp=1):
        
        self.name = name
        cmds.torus( r=r, hr=hr, axis=axis, msw=msw, ssw=ssw, esw=esw, s=s, nsp=nsp, n=self.name )
        return self

    
    def __init__(self):        
        self.name=None
        
class ctr_sphere_h8(control_h8):
      
    def new(self,name,r=2):        
        self.name = name
        cmds.sphere( r=r, n=self.name )
        return self
    
    def __init__(self):        
        self.name=None                      
       
class jchain_h8:
         
    def match(self,j):
        cmds.matchTransform(self.name,j) 
                 
    def __getitem__(self, key):
        return self.joints[key]
    
    def set_color(self,rgb):
        for j in self.joints:
            j.set_color(rgb)
    
    def match(self,targs):
        for i in range(len(self.joints)):
           self.joints[i].match(targs[i])
           
    def orient_constraint(self,arr):        
        for i in range(len(self.joints)):
            self.joints[i].orient_constraint(arr[i])
        return self
     
    def set_parent(self,target):
        self.joints[0].set_parent(target)
    
    def duplicate(self,joints):
        par = cmds.listRelatives(self.joints[0].get(), p=True)
        newJoints = []
    
        for i in range(len(joints)): 
            newJoint = cmds.joint( p=(0, 0, 0),n=joints[i] )
            cmds.matchTransform(newJoint,self.joints[i].get())
            newJoints.append(joint_h8().be(newJoint))
        
        cmds.parent(newJoints[0].get(),par)
        
        return jchain_h8(newJoints)      
    
    def convert_to_ik2(self):
                
        return ik2chain_h8(self.joints)
        
        
         
    def add_toggle_ikfk(self,attr_holder,fk_chain,ik_chain):
        
        self.orient_constraint(fk_chain)
        self.orient_constraint(ik_chain)
        
    
        attr_holder.add_attr_float(ln='kinematics_switch',nn='FK -> IK', keyable=True, r=True, hidden=False, dv=0.0, min=0.0, max=1.0)    
        attr_holder.add_attr_bool(ln='fkvis',nn='FK Visibility', keyable=True, r=True, hidden=False, dv=True)
        attr_holder.add_attr_bool(ln='ikvis',nn='IK Visibility', keyable=True, r=True, hidden=False, dv=True)  
        attr_holder.add_attr_float(ln='ik',nn='IK', keyable=True, r=True, hidden=True, dv=1.0, min=0.0, max=1.0)
        attr_holder.add_attr_float(ln='fk',nn='FK', keyable=True, r=True, hidden=True, dv=0.0, min=0.0, max=1.0)
    
        cmds.expression(s=attr_holder.get()+".ik = "+attr_holder.get()+".kinematics_switch")
        cmds.expression(s=attr_holder.get()+".fk = 1 - "+attr_holder.get()+".kinematics_switch")
    
        for i in range(len(self.joints)):
            cmds.connectAttr(attr_holder.get()+'.fk',self.joints[i].get()+'_orientConstraint1.'+fk_chain[i].get()+'W0' )
            cmds.connectAttr(attr_holder.get()+'.ik',self.joints[i].get()+'_orientConstraint1.'+ik_chain[i].get()+'W1' )
            
        return self        
              
    def __init__(self,joints):        
        self.joints = joints
        
    
class ik2chain_h8(jchain_h8):
    
    def go(self,handle_name):
        cmds.ikHandle(sj=self.joints[0].get(), ee= self.joints[2].get(), n= handle_name )
        self.handle = handle_name
        return self
    
    def handle():
        return self.handle  
     
    def parent_handle(self,targ):
        cmds.parent(self.handle,targ.get())
        return self
    
    def set_preferred_angle(self,rot):
        cmds.setAttr(self.joints[1].get()+".preferredAngleX",rot[0])
        cmds.setAttr(self.joints[1].get()+".preferredAngleY",rot[1])
        cmds.setAttr(self.joints[1].get()+".preferredAngleZ",rot[2])
        return self
      
    def add_pole_vector(self,target):
        cmds.poleVectorConstraint(target.get(),self.handle)
        return self           
        
    def __init__(self,joints):        
        self.joints = joints
        self.handle = None
     
    
    
    
    
    
      
      
class vec3_h8():
      
    def get_array(self):
        return [self.x,self.y,self.z]
        
    def __init__(self,x,y,z):        
        self.x = x
        self.y = y
        self.z = z
              
class str_h8():
    
      
    def get(self):
        return self.str
        
    def rep(self,this,that):
        self.str = self.str.replace(this,that)
        return self           
        
    def __init__(self,str):        
        self.str = str
              

class strfi_h8(str_h8):
               
    def __init__(self,str):        
        self.str = cmds.textField(str,q=True,tx=True)




class int_h8():
    
      
    def get(self):
        return self.int  
        
    def __init__(self,int):        
        self.int = int
              
class intfi_h8(int_h8):
    
              
    def __init__(self,int):        
        self.int = cmds.intField(int,q=True,v=True)
        
        
        
class rgb_h8():
    
    def get_array(self):
        return [self.r,self.g,self.b]
        
    def __init__(self,r,g,b):        
        self.r = r/255
        self.g = g/255
        self.b = b/255
        
                     
class group_h8():

    def get(self):
        return self.name
        
    def restart(self):
        if cmds.objExists(self.name):
            cmds.delete(self.name)            
        cmds.group( em=True, name=self.name)
    
    def add(self,added):
        cmds.parent(added.get(),self.name)
        
    def __init__(self,name):        
        self.name = name 
                              
class autob_rig():
    
      
    def add_joint(self,key,joint):
        self.j[key] = joint
        return self           
    
    def add_control(self,key,control):
        self.c[key] = control
        return self 
        
    def joint(self,key):
        return self.j[key]
    
    def control(self,key):
        return self.c[key]
                
    def __init__(self):        
        self.c = {}
        self.j = {}           
      
 
 
   

class biped_dataobj_h8():
    
    
    def get(self):
        return self.name
    
    def build(self):
        if cmds.objExists(self.name):     
            cmds.delete(self.name)
        p = proxy_h8().new(self.name,3)
        p.move(vec3_h8(0,0,0))
        p.set_color(rgb_h8(255,200,200))
        fi_control_hash
        
        cmds.addAttr(p.get(), longName=g_data_joint_left_h8, nn='Joint Left Suffix', keyable=False, r=True, hidden=False, dataType='string')
        cmds.setAttr(p.get()+'.'+g_data_joint_left_h8,strfi_h8(fi_joint_suffix_left_h8).get(),type='string')
        cmds.addAttr(p.get(), longName=g_data_joint_right_h8, nn='Joint Right Suffix', keyable=False, r=True, hidden=False, dataType='string')
        cmds.setAttr(p.get()+'.'+g_data_joint_right_h8,strfi_h8(fi_joint_suffix_right_h8).get(),type='string')
                
        p.add_attr_int(type='byte',ln=g_data_num_spine_h8,nn='Spine Joints', keyable=False, r=True, hidden=False, dv=intfi_h8(autob_num_spine).get(), min=1, max=255)
        p.add_attr_int(type='byte',ln=g_data_num_neck_h8,nn='Neck Joints', keyable=False, r=True, hidden=False, dv=intfi_h8(autob_num_neck).get(), min=1, max=255)
        #p.remove_transform_attrs()
       
    def get_data(self,type):
       return cmds.getAttr(self.name+'.'+type)
      
              
    def __init__(self):    
        self.name = 'data_object'
        

         
class biped_draft_h8():
  
     
     def get_data():
         d_pre = '_draft'
         n = str_h8(autob_data).rep('#',d_pre)
         p = proxy_h8().be(n.get())
          
     def build(self):
         
         group = group_h8(g_group_draft_h8)
         group.restart()
         
         d_pre = '_draft'
         
         #data
         data = biped_dataobj_h8()
         data.build()
         
         group.add(data)  
                
         #pelvis
         n = str_h8(g_draft_pelvis_h8).rep('#',d_pre)
         p = proxy_h8().new(n.get(),2)
         p.move(vec3_h8(0,0,80.87))
         p.set_color(rgb_h8(0,0,255))
         group.add(p)
         
         #spine
         spine_num = biped_dataobj_h8().get_data(g_data_num_spine_h8)         
         for s in range(spine_num):
           
            n = str_h8(g_draft_spine_h8).rep('#',d_pre).rep('^',str(s+1))
            span = 65.0/spine_num
            rad =  2-((2.0 / spine_num) * s)
            hue =  80-((255 / spine_num) * s)        
            p = proxy_h8().new(n.get(),rad)
            p.move(vec3_h8(0,0,90+(s*span)))
            p.set_color(rgb_h8(255,hue,hue))
            p.freeze()
            group.add(p)
            
         #neck
         neck_num = biped_dataobj_h8().get_data(g_data_num_neck_h8)         
         for s in range(neck_num):
           
            n = str_h8(g_draft_neck_h8).rep('#',d_pre).rep('^',str(s+1))
            span = 10.0/neck_num
            rad =  2-((2.0 / neck_num) * s)
            hue =  .3-((0.4 / neck_num) * s)        
            p = proxy_h8().new(n.get(),rad)
            p.move(vec3_h8(0,0,145+(s*span)))
            p.set_color(rgb_h8(hue,hue,255))
            p.freeze() 
            group.add(p)
         
         #head
         n = str_h8(g_draft_head_h8).rep('#',d_pre)
         p = proxy_h8().new(n.get(),2)
         p.move(vec3_h8(0,-3.09,161.262))
         p.set_color(rgb_h8(140,140,0))
         group.add(p)
         
         #clavicle
         n = str_h8(g_draft_clavicle_h8).rep('#',d_pre)
         p = proxy_h8().new(n.get(),2)
         p.move(vec3_h8(-7.461,0,136.133))
         p.set_color(rgb_h8(255,255,0))
         group.add(p)
         
         #upperarm
         n = str_h8(g_draft_upperarm_h8).rep('#',d_pre)
         p = proxy_h8().new(n.get(),2)
         p.move(vec3_h8(-11.47,0,133.31))
         p.set_color(rgb_h8(255,255,0))
         group.add(p)
         
         #lowerarm
         n = str_h8(g_draft_lowerarm_h8).rep('#',d_pre)
         p = proxy_h8().new(n.get(),2)
         p.move(vec3_h8(-28.452,0,115.808))
         p.set_color(rgb_h8(255,255,0))
         group.add(p)
         
         #Hand
         n = str_h8(g_draft_hand_h8).rep('#',d_pre)
         p = proxy_h8().new(n.get(),2)
         p.move(vec3_h8(-45.15,0,95.69))
         p.set_color(rgb_h8(140,140,0))
         group.add(p)
        
         #Hip
         n = str_h8(g_draft_thigh_h8).rep('#',d_pre)
         p = proxy_h8().new(n.get(),2)
         p.move(vec3_h8(-8.93,0,76.22))
         p.set_color(rgb_h8(0,255,255))
         group.add(p)
         
         #Knee
         n = str_h8(g_draft_shin_h8).rep('#',d_pre)
         p = proxy_h8().new(n.get(),2)
         p.move(vec3_h8(-10.036, 0, 46.531))
         p.set_color(rgb_h8(0,140,140))
         group.add(p)
         
         #Foot
         n = str_h8(g_draft_foot_h8).rep('#',d_pre)
         p = proxy_h8().new(n.get(),2)
         p.move(vec3_h8(-13.00,0,13.48))
         p.set_color(rgb_h8(0,140,140))
         group.add(p)
         
         #Toe
         n = str_h8(g_draft_toe_h8).rep('#',d_pre)
         p = proxy_h8().new(n.get(),2)
         p.move(vec3_h8(-20.556, -5.487, -0.718))
         p.set_color(rgb_h8(140,140,0))
         group.add(p)
         
         #Toetip
         n = str_h8(g_draft_toetip_h8).rep('#',d_pre)
         p = proxy_h8().new(n.get(),2)
         p.move(vec3_h8(-25.73, -13.573, -1.036))
         p.set_color(rgb_h8(140,140,0))
         group.add(p)
     
     def link(self):
         d_pre = '_draft'
                  
         n = str_h8(g_draft_pelvis_h8).rep('#',d_pre)
         self.add_pin('pelvis',proxy_h8().be(n.get()))
         
         num_spine = intfi_h8(autob_num_spine).get()         
         for i in range(num_spine):
             n = str_h8(g_draft_spine_h8).rep('#',d_pre).rep('^',str(i+1))
             p = proxy_h8().be(n.get())
             self.add_pin('spine'+str(i+1), p)
             self.chain_spine.append(p)
             
         num_neck = intfi_h8(autob_num_neck).get()         
         for i in range(num_neck):
             n = str_h8(g_draft_neck_h8).rep('#',d_pre).rep('^',str(i+1))
             p = proxy_h8().be(n.get())
             self.add_pin('neck'+str(i+1), p)
             self.chain_neck.append(p)
             
         n = str_h8(g_draft_head_h8).rep('#',d_pre)
         self.add_pin('head',proxy_h8().be(n.get()))
         
         n = str_h8(g_draft_clavicle_h8).rep('#',d_pre)
         self.add_pin('clavicle',proxy_h8().be(n.get()))
         
         n = str_h8(g_draft_upperarm_h8).rep('#',d_pre)
         self.add_pin('upperarm',proxy_h8().be(n.get()))
         
         n = str_h8(g_draft_lowerarm_h8).rep('#',d_pre)
         self.add_pin('lowerarm',proxy_h8().be(n.get()))
         
         n = str_h8(g_draft_hand_h8).rep('#',d_pre)
         self.add_pin('hand',proxy_h8().be(n.get()))
         
         n = str_h8(g_draft_thigh_h8).rep('#',d_pre)
         self.add_pin('thigh',proxy_h8().be(n.get()))
         
         n = str_h8(g_draft_shin_h8).rep('#',d_pre)
         self.add_pin('shin',proxy_h8().be(n.get()))
         
         n = str_h8(g_draft_foot_h8).rep('#',d_pre)
         self.add_pin('foot',proxy_h8().be(n.get()))
         
         n = str_h8(g_draft_toe_h8).rep('#',d_pre)
         self.add_pin('toe',proxy_h8().be(n.get()))
         
         n = str_h8(g_draft_toetip_h8).rep('#',d_pre)
         self.add_pin('toetip',proxy_h8().be(n.get()))
         
     def pin(self,key):
         return self.proxy[key]
              
     def add_pin(self,key,proxy):        
         self.proxy[key] = proxy
         return self 
             
     def __init__(self):         
         self.proxy = {}
         self.chain_spine = []
         self.chain_neck = []        
         
        
 
class biped_skeleton_h8():
  
     
     def get_hierarchy(self):
        n = strfi_h8(autob_j_root).get()
        list = cmds.listRelatives(n,allDescendents=True)
        listRev = []
        for j in reversed(list):
            listRev.append(j)
        return listRev        
  
       #  new_list = get_joint_hierarchy(get_text_field(autob_j_root))           
       #  i=0
       # for j in new_list:
       # i+=1 
       # xpos = cmds.xform(j,q=1,ws=1,rp=1)[0]          
                   
       # side = cmds.getAttr(j+'.side')
        
       # set_color_joint(j,[255,255,255])   
       # if xpos<0:
       #     cmds.rename(j,j+'_l')

     def mirror_joint(self,j,suf_left):
    
         pos = cmds.xform(j,q=1,ws=1,rp=1) 
         if(pos[0]<0):
            par = joint_h8().be(j).get_parent()
            
            
            cmds.select(cl=True)
            mirrored_pos = vec3_h8(pos[0]*-1,pos[1],pos[2])
            new = joint_h8().new(j.replace(g_ph_symx_text,suf_left),mirrored_pos)
    
            cmds.setAttr(new.get()+'.side',1)
            cmds.setAttr(new.get()+'.type',18)
            cmds.setAttr(new.get()+'.drawLabel',1)
            cmds.setAttr(new.get()+'.otherType',cmds.getAttr(j+'.otherType'),type='string')
        
            parType = cmds.nodeType(par.get(), api=True )
            if parType=="kJoint":
                parx = cmds.xform(par.get(),q=1,ws=1,rp=1)[0]

                if parx<0:         
                    par_axis = par.get().replace(g_ph_symx_text,suf_left)                    
                    cmds.parent(new.get(),par_axis)
                else:              
                    cmds.parent(new.get(),par.get())
            elif parType=="kTransform":
                pass
                #cmds.parent(new,autob_group_output)
        
    
     def mirror(self,suf_right,suf_left):   
            
        list = self.get_hierarchy()
        for j in list:
            self.mirror_joint(j,suf_left)
        list = self.get_hierarchy()  
        for j in list:
            cmds.rename(j,j.replace(g_ph_symx_text,suf_right))
            
     def label_joints(self):
        joints = self.get_hierarchy()
        
        for j in joints:
            label = j.replace(g_ph_symx_text,'')
            cmds.setAttr(j+'.type',18)
            cmds.setAttr(j+'.drawLabel',1)
            cmds.setAttr(j+'.otherType',label,type='string')
            pos = cmds.xform(j,q=1,ws=1,rp=1) 
            x = pos[0]
            
            if(x<0):
                cmds.setAttr(j+'.side',2)
            else:
                cmds.setAttr(j+'.side',0)    
        
     def color_skeleton(self):
         joints = self.get_hierarchy()
        
         for j in joints:
             joint_h8().be(j).set_color(rgb_h8(255,255,255))
               
     def color_joints_outliner_byaxial(self):
        #this doesn't work, something in maya isn't refreshing after making the change
        #only works if you manually set it
        
        joints = self.get_hierarchy()
        
        for j in joints:
            
            pos = cmds.xform(j,q=1,ws=1,rp=1) 
            x = pos[0]
            
            side = cmds.getAttr(j+'.side')
            cmds.setAttr(j+'.useOutlinerColor',True)
            
            if side==0:
                cmds.setAttr(j+'.outlinerColorR',255)
                cmds.setAttr(j+'.outlinerColorG',255)
                cmds.setAttr(j+'.outlinerColorB',255)
            elif side==1:
                cmds.setAttr(j+'.outlinerColorR',255)
                cmds.setAttr(j+'.outlinerColorG',0)
                cmds.setAttr(j+'.outlinerColorB',0)
            elif side==2:
                cmds.setAttr(j+'.outlinerColorR',0)
                cmds.setAttr(j+'.outlinerColorG',255)
                cmds.setAttr(j+'.outlinerColorB',0)
 
                   
     def build_joint(self,key,name,draft):
         return draft.pin(key).spawn_joint_symx(name)
              
     def build_from_draft(self):
                
         group = group_h8(g_group_skeleton_h8)
         group.restart()         
         
         draft = biped_draft_h8()
         draft.link()
          
         suf_left = biped_dataobj_h8().get_data(g_data_joint_left_h8)
         suf_right = biped_dataobj_h8().get_data(g_data_joint_right_h8)
           
                     
         n = strfi_h8(autob_j_root).get()
         pos = vec3_h8(0,0,0)
         joint_h8().new(n,pos)
         
         pelvis = self.build_joint('pelvis',strfi_h8(autob_j_pelvis).get(),draft)
         
         i = 1
         spines = []
         for p in draft.chain_spine:
             n = strfi_h8(autob_j_spine).rep('^',str(i)).get()
             j = p.spawn_joint(n);
             i+=1
             spines.append(j)
        
         i = 1

         for p in draft.chain_neck:
             n = strfi_h8(autob_j_neck).rep('^',str(i)).get()
             p.spawn_joint(n);
             i+=1
         
         self.build_joint('head',strfi_h8(autob_j_head).get(),draft)
          
         spines[len(spines)-1].select()

         self.build_joint('clavicle',strfi_h8(autob_j_clavicle).get(),draft)         
         self.build_joint('upperarm',strfi_h8(autob_j_upperarm).get(),draft)
         self.build_joint('lowerarm',strfi_h8(autob_j_lowerarm).get(),draft)
         self.build_joint('hand',strfi_h8(autob_j_hand).get(),draft)
         
         pelvis.select()    
         self.build_joint('thigh',strfi_h8(autob_j_thigh).get(),draft)         
         self.build_joint('shin',strfi_h8(autob_j_shin).get(),draft)
         self.build_joint('foot',strfi_h8(autob_j_foot).get(),draft)
         self.build_joint('toe',strfi_h8(autob_j_toe).get(),draft)
         self.build_joint('toetip',strfi_h8(autob_j_toetip).get(),draft)
         
         
         
         self.label_joints()
         self.mirror(suf_right,suf_left)
         #broken on maya's end
         #self.color_joints_outliner_byaxial()
         self.color_skeleton()
         
         
         
         #self.mirror()
        #upperarm_num = cmds.intField(autob_num_twist_upperarm,query=True,value=True)     
        #if upperarm_num>0:
        #    split_joint('upperarm_twist',get_clean_id(autob_j_shoulder),get_text_field(autob_j_elbow),upperarm_num)
        
        #lowerarm_num = cmds.intField(autob_num_twist_lowerarm, query=True,value=True)     
        #if upperarm_num>0:
        #    split_joint('lowerarm_twist',get_text_field(autob_j_elbow),get_text_field(autob_j_wrist),lowerarm_num)
        
        #thigh_num = cmds.intField(autob_num_twist_thigh,query=True,value=True)     
        #if upperarm_num>0:
        #    split_joint('thigh_twist',get_text_field(autob_j_hip),get_text_field(autob_j_knee),lowerarm_num)   
     
     def link_joint(self,key,name):
         j = joint_h8().be(name)
         self.add_joint(key,j)
         return j 
     
     def link_range(self,key,name,placeholder,amount):
         for i in range(amount):
             n = str_h8(name).rep(placeholder,str(i+1)).get()                
             self.link_joint(key+str(i+1),n)  
                             
     def link(self):

         print ('Linking Skeleton: Start')
         suf_right = biped_dataobj_h8().get_data(g_data_joint_right_h8)
         suf_left = biped_dataobj_h8().get_data(g_data_joint_left_h8)
         
         self.link_joint('root',strfi_h8(autob_j_root).get())
         self.link_joint('pelvis',strfi_h8(autob_j_pelvis).get())
         
         self.link_range('spine',strfi_h8(autob_j_spine).get(),'^',biped_dataobj_h8().get_data(g_data_num_spine_h8))         
         self.link_range('neck',strfi_h8(autob_j_neck).get(),'^',biped_dataobj_h8().get_data(g_data_num_neck_h8)) 
         
         self.link_joint('clavicle_r',strfi_h8(autob_j_clavicle).rep('<',suf_right).get())
         self.link_joint('clavicle_l',strfi_h8(autob_j_clavicle).rep('<',suf_left).get())      
         
         self.link_joint('upperarm_r',strfi_h8(autob_j_upperarm).rep('<',suf_right).get())
         self.link_joint('upperarm_l',strfi_h8(autob_j_upperarm).rep('<',suf_left).get()) 
         
         self.link_joint('lowerarm_r',strfi_h8(autob_j_lowerarm).rep('<',suf_right).get())
         self.link_joint('lowerarm_l',strfi_h8(autob_j_lowerarm).rep('<',suf_left).get()) 
         
         self.link_joint('hand_r',strfi_h8(autob_j_hand).rep('<',suf_right).get())
         self.link_joint('hand_l',strfi_h8(autob_j_hand).rep('<',suf_left).get()) 
         
         self.link_joint('thigh_r',strfi_h8(autob_j_thigh).rep('<',suf_right).get())
         self.link_joint('thigh_l',strfi_h8(autob_j_thigh).rep('<',suf_left).get()) 
         
         self.link_joint('shin_r',strfi_h8(autob_j_shin).rep('<',suf_right).get())
         self.link_joint('shin_l',strfi_h8(autob_j_shin).rep('<',suf_left).get()) 
         
         self.link_joint('toe_r',strfi_h8(autob_j_toe).rep('<',suf_right).get())
         self.link_joint('toe_l',strfi_h8(autob_j_toe).rep('<',suf_left).get()) 
         
         self.link_joint('toetip_r',strfi_h8(autob_j_toetip).rep('<',suf_right).get())
         self.link_joint('toetip_l',strfi_h8(autob_j_toetip).rep('<',suf_left).get()) 
         
         print ('Linking Skeleton: Complete')
         
     def joint(self,key):
         return self.joints[key]
         
     def add_joint(self,key,proxy):        
         self.joints[key] = proxy    
             
     def __init__(self):        
         self.joints = {}        
         
              
class biped_rig_h8():
        
      
    def build(self):
        
        group = group_h8(g_group_rig_h8)
        group.restart()   
         
        skel = biped_skeleton_h8()
        skel.link()
        
        c_pre = strfi_h8(fi_control_hash).get()
        suf_left = biped_dataobj_h8().get_data(g_data_joint_left_h8)
        suf_right = biped_dataobj_h8().get_data(g_data_joint_right_h8)
         
        #Root
        n = strfi_h8(autob_c_root).rep('#',c_pre)    
        root = ctr_ring_h8().new(n.get(),r=30.0,hr=0.02,msw=360,ssw=-140,esw=-40,s=2,nsp=1)
        root.set_color(rgb_h8(255,100,150))
        root.match(skel.joint('root')) 
        root.freeze()
        self.add_control('root',root)    
        skel.joint('root').parent_constraint(root)
        group.add(root)
                
        #Hip
        n = strfi_h8(autob_c_hip).rep('#',c_pre)    
        hip = ctr_ring_h8().new(n.get(),r=30, hr=0.02,ssw=-140,esw=-40,s=2,nsp=1)
        hip.set_color(rgb_h8(255,100,150))
        hip.match(skel.joint('pelvis')) 
        hip.freeze()
        self.add_control('hip',hip)    
        skel.joint('pelvis').point_constraint(hip)
        hip.set_parent(root)
        
        #Pelvis
        n = strfi_h8(autob_c_pelvis).rep('#',c_pre)    
        pelvis = ctr_ring_h8().new(n.get(),r=25.0, hr=0.005,msw=360,ssw=-140,esw=-40,s=2,nsp=1)
        pelvis.set_color(rgb_h8(255,100,150))
        pelvis.match(skel.joint('pelvis')) 
        pelvis.freeze()
        self.add_control('pelvis',pelvis)    
        skel.joint('pelvis').orient_constraint(self.control('pelvis'))
        pelvis.set_parent(hip)
        
        
          
        #Spine
        
        num_spine = 4
        chain_spine = []   
        chain_new_names = []
        prechain = []


        for i in range(num_spine):
            prechain.append(skel.joint('spine'+str(1+i)))   
        
        spine_chain = jchain_h8(prechain)
          
        chain_new_names = []  
        for i in range(num_spine):                  
            n = str_h8('spine$_@')
            n = n.rep('$','ik')
            n = n.rep('@',strfi_h8(autob_j_spine).get())
            n = n.rep('^',str(i+1))
            chain_new_names.append(n.get())    
                  
        
        chain_ik = spine_chain.duplicate(chain_new_names)
        chain_ik = chain_ik.convert_to_ik2() 
        chain_ik.go('spineik')
        
        chain_new_names = []         
        for i in range(num_spine):                  
            n = str_h8('spine$_@')
            n = n.rep('$','sk')
            n = n.rep('@',strfi_h8(autob_j_spine).get())
            n = n.rep('^',str(i+1))
            chain_new_names.append(n.get())    
        
        chain_sk = spine_chain.duplicate(chain_new_names)
        chain_sk = chain_sk.convert_to_ik2() 
        
        chain_new_names = []         
        for i in range(num_spine):                  
            n = str_h8('spine$_@')
            n = n.rep('$','isk')
            n = n.rep('@',strfi_h8(autob_j_spine).get())
            n = n.rep('^',str(i+1))
            chain_new_names.append(n.get())    
        
        chain_isk = spine_chain.duplicate(chain_new_names)
        
                
        chain_new_names = []         
        for i in range(num_spine):                  
            n = str_h8('spine$_@')
            n = n.rep('$','fik')
            n = n.rep('@',strfi_h8(autob_j_spine).get())
            n = n.rep('^',str(i+1))
            chain_new_names.append(n.get())    
        
        chain_fik = spine_chain.duplicate(chain_new_names)

        
        
        chain_new_names = []         
        for i in range(num_spine):                  
            n = str_h8('spine$_@')
            n = n.rep('$','fk')
            n = n.rep('@',strfi_h8(autob_j_spine).get())
            n = n.rep('^',str(i+1))
            chain_new_names.append(n.get())    
                  
        
        chain_fk = spine_chain.duplicate(chain_new_names)

           
        def biped_arms(ax):
           
            if ax==0:
                axis = suf_right
                key_ax = '_r'
            elif ax==1:
                axis = suf_left
                key_ax = '_l'
            
            

            chain_arm= jchain_h8([skel.joint('upperarm'+key_ax),skel.joint('lowerarm'+key_ax),skel.joint('hand'+key_ax)])            
    
            n = strfi_h8(autob_c_armik).rep('#',c_pre).rep(g_ph_symx,axis) 
            c_armik = ctr_ring_h8().new(n.get(),r=5.4, hr=0.05)
            #c_armik.set_color(rgb_h8(255,0,0))
            c_armik.match(skel.joint('hand'+key_ax)) 
            c_armik.rotate(vec3_h8(0, 90, 0))
            c_armik.freeze()
            
            #c_elbowik = autob_ctr_sphere().new(p.c_elbowik+ax_c,r=1.4)
            #c_elbowik.match(j_elbow)
            #c_elbowik.move([0,32,0])
            
            upperarm = str_h8('arm$_@').rep('$','ik').rep('@',strfi_h8(autob_j_upperarm).get()).rep(g_ph_symx,axis).get()
            lowerarm = str_h8('arm$_@').rep('$','ik').rep('@',strfi_h8(autob_j_lowerarm).get()).rep(g_ph_symx,axis).get()
            hand = str_h8('arm$_@').rep('$','ik').rep('@',strfi_h8(autob_j_hand).get()).rep(g_ph_symx,axis).get()
            chain_ik = chain_arm.duplicate([upperarm,lowerarm,hand])
            chain_ik = chain_ik.convert_to_ik2()                    
            chain_ik.go('ik_arm'+axis)    
            chain_ik.parent_handle(c_armik)
            
            def ezrig_arm_fk(org_joints,new_joints,controls):
                print('ok')
            
            chain_fk = []
            chain_fk.append(str_h8('arm$_@').rep('$','fk').rep('@',strfi_h8(autob_j_upperarm).get()).rep(g_ph_symx,axis))
            chain_fk.append(str_h8('arm$_@').rep('$','fk').rep('@',strfi_h8(autob_j_lowerarm).get()).rep(g_ph_symx,axis))
            chain_fk.append(str_h8('arm$_@').rep('$','fk').rep('@',strfi_h8(autob_j_hand).get()).rep(g_ph_symx,axis))
            chain_fk = arm_chain.duplicate(chain_fk)
             
            ctr_armfk = []
            
            n = strfi_h8(autob_c_upperarm).rep('#',c_pre)    
            upperarm = ctr_ring_h8().new(n.get(),r=30, hr=0.02,ssw=-140,esw=-40,s=2,nsp=1)
            upperarm.set_color(rgb_h8(255,100,150))
            self.add_control('uppperarm'+key_ax,upperarm)  
            armfk_ctr.append(upperarm)
            
            n = strfi_h8(autob_c_lowerarm).rep('#',c_pre)    
            lowerarm = ctr_ring_h8().new(n.get(),r=30, hr=0.02,ssw=-140,esw=-40,s=2,nsp=1)
            lowerarm.set_color(rgb_h8(255,100,150))
            self.add_control('lowerarm'+key_ax,upperarm)  
            armfk_ctr.append(lowerarm)
            
            n = strfi_h8(autob_c_hand).rep('#',c_pre)    
            hand = ctr_ring_h8().new(n.get(),r=30, hr=0.02,ssw=-140,esw=-40,s=2,nsp=1)
            hand.set_color(rgb_h8(255,100,150))
            self.add_control('hand'+key_ax,upperarm)  
            armfk_ctr.append(hand)
        
            ezrig_armfk(chain_arm,chain_fk,ctr_armfk)
            
      
        arm_names = ['upperarm','lowerarm','hand']
        arm_id    = ['upperarm','lowerarm','hand']
        joint_name_layout = '#$_@'
        biped_arms(0)
        biped_arms(1)

    
        
    def control(self,key):
         return self.controls[key]
             
    def add_control(self,key,proxy):        
        self.controls[key] = proxy   
                   
    def __init__(self):        
         self.controls = {}
                    
  
def button_biped_draft_h8(args):    
    draft = biped_draft_h8()
    draft.build()   
           
def button_biped_skeleton_h8(args):            
    skeleton = biped_skeleton_h8()
    skeleton.build_from_draft()
    
def button_biped_rig_h8(args):            
    rig = biped_rig_h8()
    rig.build()   
      
window = cmds.window( 
    title='AutoBiped',  
    width=autob_win_y_max,
    resizeToFitChildren=True) 

scrollLayout = cmds.scrollLayout(
    horizontalScrollBarThickness=16,
    verticalScrollBarThickness=16)
    
cmds.columnLayout(
    columnOffset=['left',0])
 


cmds.frameLayout(label="Draft Skeleton",width=autob_win_y_max, collapsable=True,collapse=False)
cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(autob_win_y_max-16, 40))

cmds.text( label='Place the drafting objects, or reset the drafting objects:' , height=35 )

cmds.button( label='Draft', 
             width = 100,
             command=button_biped_draft_h8 )

cmds.text( label='Create a skeleton from the draft:' , height=35 )

cmds.button( label='Output', 
             width = 100,
             command=button_biped_skeleton_h8 )

                         
cmds.text( label='Customize the features of the skeleton:' , height=35 )

cmds.setParent( '..' ) 

cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(140, 30))
 
cmds.text( label='Control Hash' )
fi_control_hash = cmds.textField(tx='c_')
                                               
cmds.text( label='Spine Joints' )
autob_num_spine = cmds.intField(minValue=3, maxValue=20, step=1, value=4)

cmds.text( label='Neck Joints' )
autob_num_neck = cmds.intField(minValue=1, maxValue=10, step=1, value=2)

cmds.text( label='Left Joint Suffix' )
fi_joint_suffix_left_h8 = cmds.textField(tx='_l')

cmds.text( label='Right Joint Suffix' )
fi_joint_suffix_right_h8 = cmds.textField(tx='_r')

cmds.text( label='Neck Joints' )
autob_num_neck = cmds.intField(minValue=1, maxValue=10, step=1, value=2)


cmds.text( label='Upper Arm Twists' )
autob_num_twist_upperarm = cmds.intField(minValue=1, maxValue=10, step=1, value=2)

cmds.text( label='Lower Arm Twists' )
autob_num_twist_lowerarm = cmds.intField(minValue=1, maxValue=10, step=1, value=2)

cmds.text( label='Thigh Twists' )
autob_num_twist_thigh = cmds.intField(minValue=1, maxValue=10, step=1, value=2)

cmds.setParent( '..' ) 
cmds.setParent( '..' )


cmds.frameLayout(label='Export/Import Settings',width=autob_win_y_max, collapsable=True,collapse=True)
cmds.gridLayout(numberOfColumns=2,cellWidthHeight=(100, 20))

cmds.button( label='Export Settings', 
             width = 100,
             command=button_biped_draft_h8 )
               
cmds.button( label='Import Settings', 
             width = 100,
             command=button_biped_skeleton_h8 )
 
cmds.setParent( '..' ) 
cmds.setParent( '..' )
            
cmds.frameLayout(label="Names",width=autob_win_y_max, collapsable=True,collapse=True)
  



cmds.frameLayout(label="Joint Names",width=autob_win_y_max, collapsable=True,collapse=True)
cmds.gridLayout(numberOfColumns=2,cellWidthHeight=(100, 20))
 
            
cmds.text( label='Root' , height=15 )
autob_j_root = cmds.textField(text='root')

cmds.text( label='Pelvis' , height=15 )
autob_j_pelvis = cmds.textField(text='pelvis')

cmds.text( label='Spine' , height=15 )
autob_j_spine = cmds.textField(text='spine^')

cmds.text( label='Neck' , height=15 )
autob_j_neck = cmds.textField(text='neck^')

cmds.text( label='Head' , height=15 )
autob_j_head = cmds.textField(text='head')

cmds.text( label='Clavicle' , height=15 )
autob_j_clavicle = cmds.textField(text='clavicle<')

cmds.text( label='Upperarm' , height=15 )
autob_j_upperarm = cmds.textField(text='upperarm<')

cmds.text( label='Lowerarm' , height=15 )
autob_j_lowerarm = cmds.textField(text='lowerarm<')

cmds.text( label='Hand' , height=15 )
autob_j_hand = cmds.textField(text='hand<')

cmds.text( label='Thigh' , height=15 )
autob_j_thigh = cmds.textField(text='thigh<')

cmds.text( label='Shin' , height=15 )
autob_j_shin = cmds.textField(text='shin<')

cmds.text( label='Foot' , height=15 )
autob_j_foot = cmds.textField(text='foot<')

cmds.text( label='Toe' , height=15 )
autob_j_toe = cmds.textField(text='toe<')

cmds.text( label='ToeTip' , height=15 )
autob_j_toetip = cmds.textField(text='toetip<')
cmds.setParent( '..' )
cmds.setParent( '..' )
  
  
  
cmds.frameLayout(label="Control Names",width=autob_win_y_max, collapsable=True,collapse=True)
cmds.gridLayout(numberOfColumns=2,cellWidthHeight=(100, 20))
 
            
cmds.text( label='Root' , height=15 )
autob_c_root = cmds.textField(text='#root')

cmds.text( label='Hip' , height=15 )
autob_c_hip = cmds.textField(text='#hip')

cmds.text( label='Pelvis' , height=15 )
autob_c_pelvis = cmds.textField(text='#pelvis')

cmds.text( label='Spine' , height=15 )
autob_c_spine = cmds.textField(text='#spine^')

cmds.text( label='Neck' , height=15 )
autob_c_neck = cmds.textField(text='#neck^')

cmds.text( label='Head' , height=15 )
autob_c_head = cmds.textField(text='#head')

cmds.text( label='clavicle' , height=15 )
autob_c_clavicle = cmds.textField(text='#clavicle<')

cmds.text( label='upperarm (FK)' , height=15 )
autob_c_upperarm = cmds.textField(text='#upperarm<')

cmds.text( label='lowerarm (FK)' , height=15 )
autob_c_lowerarm = cmds.textField(text='#lowerarm<')

cmds.text( label='Wrist (FK)' , height=15 )
autob_c_wrist = cmds.textField(text='#wrist<')

cmds.text( label='Arm (IK)' , height=15 )
autob_c_armik = cmds.textField(text='#armik<')

cmds.text( label='lowerarm (IK)' , height=15 )
autob_c_lowerarmik = cmds.textField(text='#lowerarmik<')

cmds.text( label='armHub' , height=15 )
autob_c_armhub = cmds.textField(text='#armhub<')

cmds.text( label='Thigh' , height=15 )
autob_c_thigh = cmds.textField(text='#thigh<')

cmds.text( label='Calf' , height=15 )
autob_c_calf = cmds.textField(text='#calf<')

cmds.text( label='Foot' , height=15 )
autob_c_foot = cmds.textField(text='#foot<')

cmds.text( label='legik' , height=15 )
autob_c_legik = cmds.textField(text='#legik<')

cmds.text( label='kneeik' , height=15 )
autob_c_kneeik = cmds.textField(text='#kneeik<')

cmds.text( label='leghub' , height=15 )
autob_c_leghub = cmds.textField(text='#leghub<')

cmds.text( label='Toe' , height=15 )
autob_c_toe = cmds.textField(text='#Toe<')

cmds.text( label='ToeTip' , height=15 )
autob_c_toetip = cmds.textField(text='#ToeTip<')
cmds.setParent( '..' )
cmds.setParent( '..' )

 
cmds.frameLayout(label="Aux Names",width=autob_win_y_max, collapsable=True,collapse=True)
cmds.gridLayout(numberOfColumns=2,cellWidthHeight=(100, 20))
cmds.setParent( '..' )
cmds.setParent( '..' )
        
cmds.frameLayout(label="Weight",width=autob_win_y_max, collapsable=True,collapse=True)
cmds.setParent( '..' )
cmds.setParent( '..' )
            
cmds.frameLayout(label="Rig",width=autob_win_y_max, collapsable=True,collapse=True)

cmds.button( label='Create Rig', 
             width = 100,
             command=button_biped_rig_h8 )
cmds.setParent( '..' )
                                               
cmds.showWindow( window )