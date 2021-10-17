import maya.cmds as cmds

autob_win_y_max = 300
autob_group_draft = 'autobiped_draft'
autob_group_output = 'autobiped_output'
autob_group_rig = 'autobiped_rig'

autob_suf_proxy = '_draft'

autob_pelvis = 'pelvis'+autob_suf_proxy
autob_spine = 'spine^'+autob_suf_proxy
autob_neck = 'neck^'+autob_suf_proxy
autob_head = 'head'+autob_suf_proxy

autob_hip = 'hip'+autob_suf_proxy
autob_knee = 'knee'+autob_suf_proxy
autob_foot = 'foot'+autob_suf_proxy
autob_toe = 'toe'+autob_suf_proxy
autob_toetip = 'toetip'+autob_suf_proxy

autob_collar = 'collar'+autob_suf_proxy
autob_shoulder = 'shoulder'+autob_suf_proxy
autob_elbow = 'elbow'+autob_suf_proxy
autob_hand = 'hand'+autob_suf_proxy

class Object(object):
    pass
    
def set_color_joint(j,RGB):
    cmds.setAttr( j+'.overrideEnabled', 1)
    cmds.setAttr( j+'.overrideRGBColors', 1)
    cmds.setAttr( j+'.overrideColorR', RGB[0])
    cmds.setAttr( j+'.overrideColorG', RGB[1])
    cmds.setAttr( j+'.overrideColorB', RGB[2])
    
def set_color_nurbs(j,RGB):
    cmds.setAttr( j+'.overrideEnabled', 1)
    cmds.setAttr( j+'.overrideRGBColors', 1)
    cmds.setAttr( j+'.overrideColorR', RGB[0])
    cmds.setAttr( j+'.overrideColorG', RGB[1])
    cmds.setAttr( j+'.overrideColorB', RGB[2])
    cmds.setAttr(j+'.overrideShading', 0)
  
def restart_group(name):
    if cmds.objExists(name):
        cmds.delete(name)            
    cmds.group( em=True, name=name)
      
def getParent(node):
    return cmds.listRelatives(node,parent=True,shapes=True)[0]
     
def get_joint_hierarchy(j):
    list = cmds.listRelatives(j,allDescendents=True)
    listRev = []
    listRev.append(j)
    for j in reversed(list):
        listRev.append(j)
    return listRev
     
def get_text_field(name):
    return cmds.textField(name,q=True,tx=True)
    
def get_clean_id(name):
    name = cmds.textField(name,q=True,tx=True)
    return name.replace('$','')
    
def lerpV3(loc1,loc2,amount):
    
    len = [loc2[0]-loc1[0],loc2[1]-loc1[1],loc2[2]-loc1[2]]
    
    return [(len[0]*amount)+loc1[0],(len[1]*amount)+loc1[1],(len[2]*amount)+loc1[2]]
        
def autob_proxy(name,radius,pos,rgb,group):
    cmds.sphere(r=radius, n=name)        
    set_color_nurbs(name,rgb)
    cmds.move(pos[0],pos[1],pos[2])
    cmds.parent(name,group)



def create_autob_joint(name,pos):
    
    j = cmds.joint( p=(pos[0],pos[1],pos[2]), n=name)
    
    xpos = cmds.xform(j,q=1,ws=1,rp=1)[0]
    
    if xpos<0:
        cmds.setAttr( j+'.side', 1)
    else:
        cmds.setAttr( j+'.side', 0)
         
    cmds.setAttr( j+'.drawLabel', 1 )
    
    cmds.setAttr( j+'.type', 18)
    cmds.setAttr( j+'.otherType', name, type='string')
       
    return j
    




 
      
 
def joint_from_proxy(name,proxy):
        
    create_autob_joint(name,cmds.xform(proxy,q=1,ws=1,rp=1) )

def mirror_joint(j):
    
    pos = cmds.xform(j,q=1,ws=1,rp=1) 
    if(pos[0]<0):
        par = getParent(j) 
        cmds.select(cl=True)
        mirrored_pos = [pos[0]*-1,pos[1],pos[2]]
        new = create_autob_joint(j+'_r',mirrored_pos)
        cmds.setAttr(new+'.otherType',j,type='string')
        
        cmds.setAttr(new+'.side',2)
    
        parType = cmds.nodeType(par, api=True )
        if parType=="kJoint":
            parx = cmds.xform(par,q=1,ws=1,rp=1)[0]
            
            print(j)
            if parx<0:          
                cmds.parent(new,par+'_r')
            else:              
                cmds.parent(new,par)
        elif parType=="kTransform":
            cmds.parent(new,autob_group_output)
    
    
def mirror_skeleton():   
            
    list = get_joint_hierarchy(get_text_field(autob_j_root))
    for j in list:
        mirror_joint(j)  
        
        
    new_list = get_joint_hierarchy(get_text_field(autob_j_root))           
    i=0
    for j in new_list:
        i+=1 
        xpos = cmds.xform(j,q=1,ws=1,rp=1)[0]          
                   
        side = cmds.getAttr(j+'.side')
        
        set_color_joint(j,[255,255,255])   
        if xpos<0:
            cmds.rename(j,j+'_l')
            
                     

def split_joint(name,low,high,num):  
    
    gap = 1.0/(num+1)
    
    twists = []
    cmds.select(low,r=True)
    
    for t in range(num):
        loc = lerpV3(cmds.xform(low,q=1,ws=1,rp=1),cmds.xform(high,q=1,ws=1,rp=1),(t+1)*gap)
        create_autob_joint(name+str(t+1),loc)
        
    cmds.parent(high,name+str(num))
    
    print("OK")
    
def autob_draft(args):
    
    restart_group(autob_group_draft)
    
    autob_proxy(autob_pelvis,2,[0,0,80.87],[0,0,1],autob_group_draft)
    
    spine_num = cmds.intField(autob_num_spine,query=True,value=True)     
    for s in range(spine_num):
        name = autob_spine.replace('^',str(s+1))
        span = 65.0/spine_num
        rad =  2-((2.0 / spine_num) * s)
        hue =  .3-((0.4 / spine_num) * s)        
        autob_proxy(name,rad,[0, 0, 90+(s*span)],[1,hue,hue],autob_group_draft)  
     
    neck_num = cmds.intField(autob_num_spine,query=True,value=True)     
    for s in range(spine_num):
        name = autob_neck.replace('^',str(s+1))
        span = 10.0/spine_num
        rad =  2-((2.0 / spine_num) * s)
        hue =  .3-((0.4 / spine_num) * s)        
        autob_proxy(name,rad,[0, 0, 145+(s*span)],[hue,hue,1],autob_group_draft) 
      
      
    autob_proxy(autob_head,2,[0, -3.09, 161.262],[.6,.6,0],autob_group_draft)
    
    autob_proxy(autob_collar,2,[-7.461,0,136.133],[1,1,0],autob_group_draft)
    autob_proxy(autob_shoulder,2,[-11.47,0,133.31],[1,1,0],autob_group_draft)
    autob_proxy(autob_elbow,2,[-28.452,0,115.808],[1,1,0],autob_group_draft)
    autob_proxy(autob_hand,2,[-45.15, 0, 95.69],[.6,.6,0],autob_group_draft)  
                 
    autob_proxy(autob_hip,2,[-8.93, 0, 76.22],[0,1,1],autob_group_draft)  
    autob_proxy(autob_knee,2,[-10.036, 0, 46.531],[0,.6,.6],autob_group_draft)
    autob_proxy(autob_foot,2,[-13.00, 0, 13.48],[0,.6,.6],autob_group_draft)

    autob_proxy(autob_toe,2,[-20.556, -5.487, -0.718],[.6,.6,0],autob_group_draft)
    autob_proxy(autob_toetip,2,[-25.73, -13.573, -1.036],[.6,.6,0],autob_group_draft)
 
    

           
def autob_output(args):        
        
    restart_group(autob_group_output)      
      
    create_autob_joint(get_text_field(autob_j_root),[0,0,0])
     
    joint_from_proxy(get_text_field(autob_j_pelvis),autob_pelvis)
    
    spine_num = cmds.intField(autob_num_spine,query=True,value=True) 
    
    for s in range(spine_num):
        name = get_text_field(autob_j_spine) + str(s+1)
        proxy_name = autob_spine.replace('^',str(s+1))
        joint_from_proxy(name,proxy_name)
    
    neck_num = cmds.intField(autob_num_neck,query=True,value=True)   
    for s in range(neck_num):
        name = get_text_field(autob_j_neck) + str(s+1)
        proxy_name = autob_neck.replace('^',str(s+1))
        joint_from_proxy(name,proxy_name)
     
    joint_from_proxy(get_text_field(autob_j_head),autob_head)
     
    cmds.select(get_text_field(autob_j_spine) + str(spine_num), replace=True) 
    joint_from_proxy(get_text_field(autob_j_collar),autob_collar)
    joint_from_proxy(get_text_field(autob_j_shoulder),autob_shoulder)
    joint_from_proxy(get_text_field(autob_j_elbow),autob_elbow)
    joint_from_proxy(get_text_field(autob_j_wrist),autob_hand)
       
    cmds.select(get_text_field(autob_j_pelvis), replace=True)    
    
    joint_from_proxy(get_text_field(autob_j_hip),autob_hip)
    joint_from_proxy(get_text_field(autob_j_knee),autob_knee)
    joint_from_proxy(get_text_field(autob_j_foot),autob_foot)
    joint_from_proxy(get_text_field(autob_j_toe),autob_toe)
    joint_from_proxy(get_text_field(autob_j_toetip),autob_toetip)
    
    upperarm_num = cmds.intField(autob_num_twist_upperarm,query=True,value=True)     
    if upperarm_num>0:
        split_joint('upperarm_twist',get_clean_id(autob_j_shoulder),get_text_field(autob_j_elbow),upperarm_num)
    
    lowerarm_num = cmds.intField(autob_num_twist_lowerarm, query=True,value=True)     
    if upperarm_num>0:
        split_joint('lowerarm_twist',get_text_field(autob_j_elbow),get_text_field(autob_j_wrist),lowerarm_num)
    
    thigh_num = cmds.intField(autob_num_twist_thigh,query=True,value=True)     
    if upperarm_num>0:
        split_joint('thigh_twist',get_text_field(autob_j_hip),get_text_field(autob_j_knee),lowerarm_num)
            
    mirror_skeleton()
    
    
  
def remove_transform_attrs(name):
    cmds.setAttr(name+".tx", keyable=False, channelBox=False)
    cmds.setAttr(name+".ty", keyable=False, channelBox=False)
    cmds.setAttr(name+".tz", keyable=False, channelBox=False)
    cmds.setAttr(name+".rx", keyable=False, channelBox=False)
    cmds.setAttr(name+".ry", keyable=False, channelBox=False)
    cmds.setAttr(name+".rz", keyable=False, channelBox=False)
    cmds.setAttr(name+".sx", keyable=False, channelBox=False)
    cmds.setAttr(name+".sy", keyable=False, channelBox=False)
    cmds.setAttr(name+".sz", keyable=False, channelBox=False)
    cmds.setAttr(name+".v",  keyable=False, channelBox=False)
     
def duplicate_chain(joints,names): 

    newJoints = []    
    i=0
    for j in joints: 
        newJoint = cmds.joint( p=(0, 0, 0),n=names[i] )
        cmds.matchTransform(newJoint,j)
        newJoints.append(newJoint)       
        i+=1
        
    return newJoints
    
   
     
def set_color_control(name,rgb):

    cmds.sets(name, rm="initialShadingGroup")
    cmds.setAttr(name+".overrideEnabled", 1)
    cmds.setAttr(name+".overrideShading", 0)
    cmds.setAttr(name+".overrideRGBColors", 1)
    cmds.setAttr(name+".overrideColorR", rgb[0])
    cmds.setAttr(name+".overrideColorG", rgb[1])
    cmds.setAttr(name+".overrideColorB", rgb[2])











class autob_node:
    
    def set_parent(self,target):
        cmds.parent(self.get(),target.get())
    
    def get(self):
        return self.name
        
    def match(self,j):
        cmds.matchTransform(self.get(),j.get()) 
    
    def get_parent(self):
        return joint().be(cmds.listRelatives(self.get(),parent=True,shapes=True)[0])
        
    def select(self):
        cmds.select(cl=True)
        cmds.select(self.get())
        return self
           
    def move(self,pos):
        self.select()
        cmds.move(pos[0], pos[1], pos[2],r=True,os=True,wd=True )
        return self
    
    def rotate(self,pos):
        self.select()
        cmds.rotate(pos[0], pos[1], pos[2],r=True )
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
        cmds.addAttr(self.get(), longName=ln, nn=nn, keyable=keyable, r=r, hidden=hidden, attributeType='float', dv=0.0, min=0.0, max=1.0)
        return self
    
    def add_attr_bool(self,ln='Error',nn='Error', keyable=True, r=True, hidden=False, dv=bool):
        cmds.addAttr(self.get(), longName=ln, nn=nn, keyable=keyable, r=r, hidden=hidden, attributeType='bool', dv=0.0)
        return self
                   
    def freeze(self):
        cmds.makeIdentity( apply=True, t=1, r=1, s=1)
        return self
                
    def __init__(self):        
        self.name=None
                       
class autob_joint(autob_node):
    
    def get(self):
        return self.name
                      
    def new(self,name,pos=(0,0,0)):
        self.name = name
        cmds.joint(p=pos,n=name)
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
    
    
class autob_control(autob_node):
    
    def get(self):
        return self.name
     
    def set_color(self,rgb):
        cmds.setAttr( self.name+'.overrideEnabled', 1)
        cmds.setAttr( self.name+'.overrideRGBColors', 1)
        cmds.setAttr( self.name+'.overrideColorR', rgb[0])
        cmds.setAttr( self.name+'.overrideColorG', rgb[1])
        cmds.setAttr( self.name+'.overrideColorB', rgb[2])
        cmds.setAttr( self.name+'.overrideShading', 0) 
  
                      
    def new(self):
        return self
            
    def be(self,name):
        self.name = name
        return self
        
    def __init__(self):        
        self.name=None
 
class autob_ctr_ring(autob_control):
    
    
    def new(self,name,r=1.2, hr=0.05, axis=(0, 0, 0), msw=360,ssw=360, esw=0,s=2,nsp=1):
        
        self.name = name
        cmds.torus( r=r, hr=hr, axis=axis, msw=msw, ssw=ssw, esw=esw, s=s, nsp=nsp, n=self.name )
        return self

    
    def __init__(self):        
        self.name=None
        
class autob_ctr_sphere(autob_control):
      
    def new(self,name,r=2):        
        self.name = name
        cmds.sphere( r=r, n=self.name )
        return self
    
    def __init__(self):        
        self.name=None                      
       
class autob_jchain:
         
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
        
    
class autob_ik2(jchain):
    
    def go(self,handle_name):
        cmds.ikHandle(sj=self.joints[0].get(), ee= self.joints[2].get(), n= handle_name )
        self.handle = handle_name
        return self
    
    def handle():
        return self.handle  
     
    def parent_handle(self,targ):
        print(targ.get())
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
      
def autob_buildrig(args):
    
    restart_group(autob_group_rig)
    
    rig = autob_rig()
    rig.add_joint('root',autob_joint().be(get_text_field(autob_j_root)))
    rig.add_joint('pelvis',autob_joint().be(get_text_field(autob_j_pelvis)))
    
    
  
    c_pre = 'c_'
    
    
    
    c_root = autob_ctr_ring().new(get_text_field(autob_c_root),r=30.0,hr=0.02,msw=360,ssw=-140,esw=-40,s=2,nsp=1)
    c_root.set_color([255,0,0])
    c_root.match(rig.joint('root')) 
    c_root.freeze()
    rig.add_control('root',c_root)    
    rig.joint('root').parent_constraint(rig.control('root'))


    c_hip = autob_ctr_ring().new(get_text_field(autob_c_hip),r=30, hr=0.02,ssw=-140,esw=-40,s=2,nsp=1)
    c_hip.set_color([255,0,255])
    c_hip.match(rig.joint('pelvis')) 
    c_hip.freeze() 
    rig.add_control('hip',c_hip)
    rig.joint('pelvis').point_constraint(c_hip)
    
    #Pelvis
    c_pelvis = autob_ctr_ring().new(get_text_field(autob_c_pelvis),r=25.0, hr=0.005,msw=360,ssw=-140,esw=-40,s=2,nsp=1)
    c_pelvis.set_color([0,255,0])
    c_pelvis.match(rig.joint('pelvis')) 
    c_pelvis.freeze()
    rig.add_control('pelvis',c_pelvis)
    rig.joint('pelvis').orient_constraint(c_pelvis)
    c_pelvis.set_parent(rig.control('hip'))

    return
    
    jnt_root = P8A.jnt.root
    jnt_hip = P8A.jnt.hip
    jnt_pelvis = P8A.jnt.pelvis
    
    cmds.torus(r=30, msw=360,ssw=-140,esw=-40,s=2,nsp=1,hr=0.02, n=ctr_root)
    cmds.matchTransform(ctr_root,jnt_root)
    cmds.rotate(0, 90, 0, r=True)
    registerControl(ctr_root, P8A.rgb.posrot)
    cmds.makeIdentity( apply=True, t=1, r=1, s=1)
    cmds.parentConstraint(ctr_root, jnt_root, mo=True) 
    
    cmds.torus(r=30,msw=360,ssw=-140,esw=-40,s=2,nsp=1,hr=0.02, n=ctr_hip)
    cmds.matchTransform(ctr_hip,jnt_hip)
    cmds.rotate(0, 90, 0, r=True)
    registerControl(ctr_hip, P8A.rgb.posrot)
    cmds.makeIdentity( apply=True, t=1, r=1, s=1)
    cmds.pointConstraint(ctr_hip, jnt_hip, mo=True) 
     
    cmds.torus(r=25, msw=360,ssw=-140,esw=-40,s=2,nsp=1,hr=0.005, n=ctr_pelvis)
    cmds.matchTransform(ctr_pelvis,jnt_pelvis)
    cmds.rotate(0, 90, 0, r=True)
    registerControl(ctr_pelvis, P8A.rgb.rot1)
    cmds.makeIdentity( apply=True, t=1, r=1, s=1)
    cmds.orientConstraint(ctr_pelvis, jnt_pelvis, mo=True) 
    
    
    
    #rig biped arms
    props = Object() 

    props.axis_c = [get_text_field(autob_suffix_left),get_text_field(autob_suffix_right)]
    props.axis_j = [get_text_field(autob_suffix_left),get_text_field(autob_suffix_right)]
    
    props.j_collar = get_text_field(autob_j_collar)
    props.j_shoulder = get_text_field(autob_j_shoulder)
    props.j_elbow = get_text_field(autob_j_elbow)
    props.j_wrist = get_text_field(autob_j_wrist)
    
    props.c_collar = c_pre+get_text_field(autob_c_collar)
    props.c_shoulder = c_pre+get_text_field(autob_c_shoulder)
    props.c_elbow = c_pre+get_text_field(autob_c_elbow)
    props.c_wrist = c_pre+get_text_field(autob_c_wrist)
    props.c_elbowik = c_pre+get_text_field(autob_c_elbowik)
    props.c_armik = c_pre+get_text_field(autob_c_armik)
    props.c_armhub = c_pre+get_text_field(autob_c_armhub)
    
    props.crgb_collar = [255,255,255]
    props.crgb_shoulder = [255,255,255] 
    props.crgb_elbow = [255,255,255]
    props.crgb_wrist = [255,255,255]
    props.crgb_armik = [255,255,255]
    
    props.chain = 'arm$_@<'
     
    props.twist = '@_twist^<'
       
    autob_ik_arm(props,0)
    autob_ik_arm(props,1)
    
    #rig biped legs
     
    props = Object() 

    props.axis_c = [get_text_field(autob_suffix_left),get_text_field(autob_suffix_right)]
    props.axis_j = [get_text_field(autob_suffix_left),get_text_field(autob_suffix_right)]
    
    props.j_hip = get_text_field(autob_j_hip)
    props.j_knee = get_text_field(autob_j_knee)
    props.j_foot = get_text_field(autob_j_foot)
    props.j_toe = get_text_field(autob_j_toe)
    props.j_toetip = get_text_field(autob_j_toetip)
    
    props.c_hip = c_pre+get_text_field(autob_c_hip)
    props.c_knee = c_pre+get_text_field(autob_c_knee)
    props.c_ankle = c_pre+get_text_field(autob_c_ankle)
    props.c_legik = c_pre+get_text_field(autob_c_legik)
    props.c_kneeik = c_pre+get_text_field(autob_c_kneeik)
    props.c_leghub = c_pre+get_text_field(autob_c_leghub)

    
    props.crgb_hip = [255,255,255]
    props.crgb_knee = [255,255,255] 
    props.crgb_ankle = [255,255,255]
    props.crgb_legik = [255,255,255]
    props.crgb_kneeik = [255,255,255]
    props.crgb_leghub = [255,255,255]
        
    props.chain = 'leg$_@<'
     
    props.twist = '@_twist^<'
    
    props.i_leg = 'ik_leg'
    props.i_foot = 'ik_foot'
    props.i_toe = 'ik_toe'
       
    props.h_toe = 'h_toe'
    props.h_ball = 'h_ball'
    props.h_wiggle = 'h_wiggle'
    
    
    props.c_parent = c_pre+get_text_field(autob_c_pelvis)
    
    #autob_ik_biped_leg(props,0)
    #autob_ik_biped_leg(props,1)
 

    


    
def autob_ik_arm(p,axis):    
      
    #DEFINE AXIS      
    ax_c = p.axis_c[axis]
    ax_j = p.axis_j[axis]          
    
    #REGISTER JOINTS
    j_collar = autob_joint().be(p.j_collar+ax_j)
    j_shoulder = autob_joint().be(p.j_shoulder+ax_j)   
    j_elbow = autob_joint().be(p.j_elbow+ax_j)
    j_wrist = autob_joint().be(p.j_wrist+ax_j)
    
    joints = autob_jchain([j_shoulder,j_elbow,j_wrist]) 
    
    
    #CREATE CONTROLS
    c_collar = autob_ctr_sphere().new(p.c_collar+ax_c,r=1.5)
    c_collar.match(j_collar)
    c_collar.set_color(p.crgb_shoulder)
    c_collar.move([0,0,10])
    j_collar.orient_constraint(c_collar)
    
    c_shoulder = autob_ctr_ring().new(p.c_shoulder+ax_c,r=7.5, hr=0.005, axis=(1, 0, 0), ssw=-230, esw=-130)
    c_shoulder.match(j_shoulder)
    c_shoulder.set_color(p.crgb_shoulder)
       
    c_elbow = autob_ctr_ring().new(p.c_elbow+ax_c,r=7.5, hr=0.005, axis=(1, 0, 0), ssw=-140, esw=-40) 
    c_elbow.match(j_elbow)
    c_elbow.set_color(p.crgb_elbow)
    
    c_wrist = autob_ctr_ring().new(p.c_wrist+ax_c,r=4.25, hr=0.005, axis=(1, 0, 0), ssw=360, esw=0) 
    c_wrist.match(j_wrist)
    c_wrist.set_color(p.crgb_wrist)
    
    c_shoulder.set_parent(c_collar)    
    c_elbow.set_parent(c_shoulder)
    c_wrist.set_parent(c_elbow)
    
    c_armhub = autob_ctr_sphere().new(p.c_armhub+ax_c,r=1.4)
    c_armhub.set_color([255,0,0])
    c_armhub.match(j_wrist)
    if(axis==0):
        c_armhub.move([-5, 0, 5])
    else:
        c_armhub.move([5, 0, 5])
    #c_armhub.freeze()
     
    c_armhub.parent_constraint(j_wrist)
            
    c_armhub.remove_transform_attrs()
    
    

    #CREATE IK
    c_armik = autob_ctr_ring().new(p.c_armik+ax_c,r=5.4, hr=0.05)
    c_armik.set_color([255,0,0])
    c_armik.match(j_wrist) 
    c_armik.rotate([0, 90, 0])
    c_armik.freeze()
    
    c_elbowik = autob_ctr_sphere().new(p.c_elbowik+ax_c,r=1.4)
    c_elbowik.match(j_elbow)
    c_elbowik.move([0,32,0])



    ik_shoulder = autob_joint().new(p.chain.replace('@',p.j_shoulder).replace('$','ik').replace('<',ax_c))
    ik_elbow = autob_joint().new(p.chain.replace('@',p.j_elbow).replace('$','ik').replace('<',ax_c))
    ik_hand = autob_joint().new(p.chain.replace('@',p.j_wrist).replace('$','ik').replace('<',ax_c))
    ik_arm = autob_ik2([ik_shoulder,ik_elbow,ik_hand])    
    ik_arm.match(joints)
    ik_arm.set_color([255,255,0])
    ik_arm.set_parent(j_shoulder.get_parent())
    if (axis==0):
        ik_arm.set_preferred_angle([0,0,-90])
    else:
        ik_arm.set_preferred_angle([0,0,90])
          
    ik_arm.go('ik_arm'+ax_c)    
    ik_arm.parent_handle(c_armik)
            
    fk_shoulder = autob_joint().new(p.chain.replace('@',p.j_shoulder).replace('$','fk').replace('<',ax_c))
    fk_elbow = autob_joint().new(p.chain.replace('@',p.j_elbow).replace('$','fk').replace('<',ax_c))
    fk_hand = autob_joint().new(p.chain.replace('@',p.j_wrist).replace('$','fk').replace('<',ax_c))    
    fk_arm = jchain([fk_shoulder,fk_elbow,fk_hand])
    fk_arm.match(joints)
    fk_arm.set_color([0,255,0])  
    fk_arm.set_parent(j_shoulder.get_parent())        
    fk_arm.orient_constraint([c_shoulder,c_elbow,c_wrist])

    #j_upperarm_twist = p.twist.replace('@',j_shoulder).replace('<',ax_c)
    #j_lowerarm_twist = p.twist.replace('@',j_elbow).replace('<',ax_c)
    
    joints.add_toggle_ikfk(c_armhub,fk_arm,ik_arm)  
    
    ik_arm.add_pole_vector(c_elbowik)
    c_elbowik.set_parent(c_armik)
    
    
    return
    
    
    mel.eval('source channelBoxCommand; CBdeleteConnection "'+jnt_upperarm+'.rx"')
    mel.eval('source channelBoxCommand; CBdeleteConnection "'+jnt_upperarm_twist+'.rx"')
    
    cmds.expression(s = jnt_upperarm+'.rx = '+P8A.suf.armmx+jnt_upperarm+'.rx / 2')
    cmds.expression(s = jnt_upperarm_twist+'.rx = ('+P8A.suf.armmx+jnt_forearm+'.rx / 1.5) - ('+P8A.suf.armmx+jnt_upperarm+'.rx / 2)')
    
    #SETUP TWIST BONES
    cmds.orientConstraint(ctr_hand, P8A.suf.armik+jnt_hand, mo=True)
    cmds.orientConstraint(P8A.suf.armmx+jnt_hand, jnt_hand, mo=True)
    cmds.orientConstraint(P8A.suf.armmx+jnt_forearm, jnt_forearm, mo=True)
    cmds.orientConstraint(P8A.suf.armmx+jnt_upperarm, jnt_upperarm, mo=True,skip="x")
        
    #mel.eval("CBdeleteConnection '"+p__.joints[0]+side+".rx';") 
    #cmds.disconnectAttr("PairBlend7.outRotateX", "upperarm_l.rotateX")  
    #cmds.expression(s = p__.joints[0]+side+'.rx = '+p__.joints[1]+side+'.rx / 2')
    
    
    #MAKE CLAVICLE    

    cmds.torus( r=6, hr=0.005, axis=(1, 0, 0), ssw=-210, esw=-150, s=4, n=ctr_clavicle )
    registerControl(ctr_clavicle,P8A.rgb.rot2)
    cmds.matchTransform(ctr_clavicle,jnt_clavicle)
    
    
    if(axis==0):
        cmds.move(7, 0, 0,r=True,os=True,wd=True )
    else:
        cmds.move(-7, 0, 0,r=True,os=True,wd=True )
        
    piv = cmds.xform(jnt_clavicle, q=True, ws=True, rp=True)
    cmds.xform(ctr_clavicle, ws=True, piv=(piv[0], piv[1], piv[2]) )

    cmds.makeIdentity( apply=True, t=1, r=1, s=1)
    cmds.orientConstraint(ctr_clavicle,jnt_clavicle)

      
    #BIND UP CONNECTIONS
    
    cmds.connectAttr(ctr_fkik+'.ikvis',ctr_hand+'.visibility')
    cmds.connectAttr(ctr_fkik+'.fkvis',ctr_arm1_fk+'.visibility')
    cmds.connectAttr(ctr_fkik+'.fkvis',ctr_arm2_fk+'.visibility')
    cmds.connectAttr(ctr_fkik+'.fkvis',ctr_hand_fk+'.visibility')

    
def autob_ik_biped_leg(p,axis):
    
    ax_c = p.axis_c[axis]
    ax_j = p.axis_j[axis]          
        
    j_hip = p.j_hip+ax_c
    j_knee = p.j_knee+ax_c   
    j_foot = p.j_foot+ax_c
    j_toe = p.j_toe+ax_c
    j_toetip = p.j_toetip+ax_c
    
    c_hip = p.c_hip+ax_c
    c_knee = p.c_knee+ax_c   
    c_ankle = p.c_ankle+ax_c

    c_legik = p.c_legik+ax_c
    c_kneeik = p.c_kneeik+ax_c
    c_leghub = p.c_leghub+ax_c
        
    joints_leg = [j_hip,j_knee,j_foot]  
    joints_foot = [j_foot,j_toe,j_toetip]
    
    i_leg = p.i_leg
    i_foot = p.i_foot
    i_toe = p.i_toe
    
    h_toe = p.h_toe
    h_ball = p.h_ball
    h_wiggle = p.h_wiggle
    
    fk_hip = p.chain.replace('@',p.j_hip).replace('$','fk').replace('<',ax_c)
    fk_knee = p.chain.replace('@',p.j_knee).replace('$','fk').replace('<',ax_c)
    fk_ankle = p.chain.replace('@',p.j_foot).replace('$','fk').replace('<',ax_c)    
    arr_fk = [fk_hip,fk_knee,fk_ankle] 
    
    ik_hip = p.chain.replace('@',p.j_hip).replace('$','ik').replace('<',ax_c)
    ik_knee = p.chain.replace('@',p.j_knee).replace('$','ik').replace('<',ax_c)
    ik_ankle = p.chain.replace('@',p.j_foot).replace('$','ik').replace('<',ax_c)    
    arr_ik = [ik_hip,ik_knee,ik_ankle] 


    c_par = p.c_parent
        
    foot_size = 50
          
    #CREATE CHAINS
    
    #DUPLICATE ARM CHAINS (FK, IK)
    duplicate_chain(joints_leg, arr_fk)
    duplicate_chain(joints_leg, arr_ik)
            
    #CREATE IK/FK CONTROL NODE
    
    cmds.polySphere( n=c_leghub, r=2, sx=5, sy=5)
    cmds.matchTransform(c_leghub,j_foot)
    set_color_control(c_leghub,p.crgb_leghub)
    
    cmds.move(0, -14, 5,r=True,os=True,wd=True )
    
    cmds.parentConstraint(j_foot,c_leghub,mo=True)
    remove_transform_attrs(c_leghub)

    cmds.addAttr(c_leghub, longName='ik', nn='IK', keyable=True, r=True, hidden=False, attributeType='float', dv=1.0, min=0.0, max=1.0)
    cmds.addAttr(c_leghub, longName='fk', nn='FK', keyable=True, r=True, hidden=False, attributeType='float', dv=0.0, min=0.0, max=1.0)
    cmds.addAttr(c_leghub, longName='kinematics_switch', nn='FK -> IK', keyable=True, r=True, attributeType='float', dv=0.0, min=0.0, max=1.0)
    cmds.expression(s=c_leghub+".ik = "+c_leghub+".kinematics_switch")
    cmds.expression(s=c_leghub+".fk = 1 - "+c_leghub+".kinematics_switch")
    
    
    #CREATE FOOT IK CONTROL

    cmds.polyCube(w=size[0],h=size[1],d=size[2],n=c_legik )
    set_color_control(c_legik,p.crgb_leghub)
    
    cmds.matchTransform(c_legik,j_foot)
    cmds.move(0, -4, -6,r=True,os=True,wd=True )
    cmds.setAttr(c_legik+'.translateY', 0)
    piv = cmds.xform(j_foot, q=True, ws=True, rp=True)
    cmds.xform(c_legik, ws=True, piv=(piv[0], piv[1], piv[2]) )
    cmds.setAttr(c_legik+".rotateOrder", 2)
    cmds.makeIdentity( apply=True, t=1, r=1, s=1)
    
    #SET PREFERRED ANGLE OF IK ARMS
    cmds.setAttr(arr_ik[1]+".preferredAngleX",90)

    
    #CREATE IK LINK
    cmds.ikHandle(sj=arr_ik[0], ee= arr_ik[2], n= p.i_leg )

        
    cmds.ikHandle( sj=P8A.suf.legik+jnt_foot, ee=P8A.suf.legik+jnt_ball, n=ikchain_foot )
    cmds.ikHandle( sj=P8A.suf.legik+jnt_ball, ee=P8A.suf.legik+jnt_toe, n=ikchain_ball )

    cmds.spaceLocator( p=(1, 1, 1), n=hlp_toe )
    cmds.matchTransform(hlp_toe,jnt_ball)
    cmds.setAttr(hlp_toe+".rotateOrder", 2)
    
    cmds.spaceLocator( p=(1, 1, 1), n=hlp_ball )
    cmds.matchTransform(hlp_ball,jnt_ball)
    cmds.setAttr(hlp_ball+".rotateOrder", 2)
    
    
    cmds.spaceLocator( p=(1, 1, 1), n=hlp_wiggle )
    cmds.matchTransform(hlp_wiggle,jnt_ball)
    cmds.setAttr(hlp_wiggle+".rotateOrder", 2)
    
    
    
    
    cmds.parent(hlp_toe,ctr_foot_ik)
    
    
    cmds.parent(ikchain_foot, hlp_toe)
    
    cmds.parent(hlp_wiggle, hlp_toe)
    
    cmds.parent(ikchain_ball, hlp_wiggle)
    
    cmds.parent(hlp_ball, hlp_toe)
    
    cmds.parent(ikchain_leg, hlp_ball)
    
    
    #WEIGHT THE MIXER SET TO BOTH THE IK AND FK
    
    
    for j in jointsLeg:
        cmds.orientConstraint(P8A.suf.legfk+j, P8A.suf.legmx+j, mo=True )
        cmds.orientConstraint(P8A.suf.legik+j, P8A.suf.legmx+j, mo=True )
    
    #BIND THE IK BALL
    cmds.orientConstraint(P8A.suf.legik+jnt_ball, P8A.suf.legmx+jnt_ball, mo=True )
       
   
    #CONECT IK/FK ARM JOINTS TO THE IK/FK CONTROL NODE    
    for j in jointsLeg:
        cmds.connectAttr(ctr_leghub+'.fk',P8A.suf.legmx+j+'_orientConstraint1.'+P8A.suf.legfk+j+'W0' )
        cmds.connectAttr(ctr_leghub+'.ik',P8A.suf.legmx+j+'_orientConstraint1.'+P8A.suf.legik+j+'W1' )
    
    
    
   
    
    
    #MAKE IK KNEE CONTROL
    cmds.polySphere( n=ctr_knee_ik, r=3, sx=10, sy=10)
    registerControl(ctr_knee_ik,P8A.rgb.loc)
    
    cmds.matchTransform(ctr_knee_ik,jnt_leg2)
    piv = cmds.xform(jnt_leg2, q=True, ws=True, rp=True)
    cmds.xform(ctr_knee_ik, ws=True, piv=(piv[0], piv[1], piv[2]) )
    cmds.move(0, -32, 0,r=True,os=True,wd=True )
    cmds.parent(ctr_knee_ik, ctr_foot_ik)
    cmds.poleVectorConstraint(ctr_knee_ik,ikchain_leg)

    
    
    #MAKE FK CONTROLS
    
        
    cmds.torus( r=12, hr=0.04, axis=(0, 0, 0), ssw=140, esw=40, s=4, n=ctr_leg1_fk )
    cmds.matchTransform(ctr_leg1_fk,jnt_leg1) 
    if(axis==0):
        cmds.rotate(0, 0, 35,r=True)
    else:
        cmds.rotate(0, 0, -35,r=True)
    
    cmds.move(0, 0, -10,r=True,os=True,wd=True )
    piv = cmds.xform(jnt_leg1, q=True, ws=True, rp=True)
    cmds.xform(ctr_leg1_fk, ws=True, piv=(piv[0], piv[1], piv[2]) )
    cmds.makeIdentity(apply=True, t=1, r=1, s=1)
    
    cmds.torus( r=7.5, hr=0.04, axis=(0, 0, 0), ssw=140, esw=40, s=4, n=ctr_leg2_fk )
    cmds.matchTransform(ctr_leg2_fk,jnt_leg2)             
    
    cmds.torus( r=6.25, hr=0.095, axis=(0, 0, 0), ssw=360, esw=0, n=ctr_foot_fk )
    cmds.torus( r=5.25, hr=0.095, axis=(0, 1, 0), ssw=120, esw=60, n=ctr_toe_fk )
       
          
       
    cmds.matchTransform(ctr_foot_fk, jnt_foot)
    cmds.matchTransform(ctr_toe_fk, jnt_ball)

    

    registerControl(ctr_leg1_fk,P8A.rgb.rot1)
    registerControl(ctr_leg2_fk,P8A.rgb.rot1)
    registerControl(ctr_foot_fk,P8A.rgb.rot1)
    registerControl(ctr_toe_fk,P8A.rgb.rot1)

    
    fkControls = [ctr_leg1_fk, ctr_leg2_fk, ctr_foot_fk]
    cmds.orientConstraint(ctr_leg1_fk, P8A.suf.legfk+jnt_leg1, mo=True )
    cmds.orientConstraint(ctr_leg2_fk, P8A.suf.legfk+jnt_leg2, mo=True )
    cmds.orientConstraint(ctr_foot_fk, P8A.suf.legfk+jnt_foot, mo=True )
    cmds.orientConstraint(ctr_toe_fk, P8A.suf.legfk+jnt_ball, mo=True )
    
    cmds.parent(ctr_toe_fk, ctr_foot_fk)
    cmds.parent(ctr_foot_fk, ctr_leg2_fk)
    cmds.parent(ctr_leg2_fk, ctr_leg1_fk)
      
    cmds.parent(ctr_leg1_fk,ctr_pelvis)
    
    
    #BIND BASE BONES
    cmds.orientConstraint(P8A.suf.legmx+jnt_leg1, jnt_leg1, mo=True )
    cmds.orientConstraint(P8A.suf.legmx+jnt_leg2, jnt_leg2, mo=True )
    cmds.orientConstraint(P8A.suf.legmx+jnt_foot, jnt_foot, mo=True )
    cmds.orientConstraint(P8A.suf.legmx+jnt_ball, jnt_ball, mo=True )



  
    
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
             command=autob_draft )

cmds.text( label='Create a skeleton from the draft:' , height=35 )

cmds.button( label='Output', 
             width = 100,
             command=autob_output )

                         
cmds.text( label='Customize the features of the skeleton:' , height=35 )

cmds.setParent( '..' ) 

cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(140, 30))
                                                
cmds.text( label='Spine Joints' )
autob_num_spine = cmds.intField(minValue=3, maxValue=20, step=1, value=4)

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
             command=autob_output )
               
cmds.button( label='Import Settings', 
             width = 100,
             command=autob_output )
 
cmds.setParent( '..' ) 
cmds.setParent( '..' )
            
cmds.frameLayout(label="Names",width=autob_win_y_max, collapsable=True,collapse=True)
  

cmds.text( label='Symettrical Joints will record their axis in prefix instead of suffix.' )
cmds.checkBox( label='Prefix_Axis' , height=15 )


cmds.text( label='Axis Abbreviations.' )
cmds.gridLayout(numberOfColumns=2,cellWidthHeight=(100, 20))

cmds.text( label='left' , height=15 )
autob_suffix_left = cmds.textField(text='_l')

cmds.text( label='right' , height=15 )
autob_suffix_right = cmds.textField(text='_r')
cmds.setParent( '..' )
cmds.setParent( '..' )

cmds.frameLayout(label="Joint Names",width=autob_win_y_max, collapsable=True,collapse=True)
cmds.gridLayout(numberOfColumns=2,cellWidthHeight=(100, 20))
 
            
cmds.text( label='Root' , height=15 )
autob_j_root = cmds.textField(text='root')

cmds.text( label='Pelvis' , height=15 )
autob_j_pelvis = cmds.textField(text='pelvis')

cmds.text( label='Spine' , height=15 )
autob_j_spine = cmds.textField(text='spine')

cmds.text( label='Neck' , height=15 )
autob_j_neck = cmds.textField(text='neck')

cmds.text( label='Head' , height=15 )
autob_j_head = cmds.textField(text='head')

cmds.text( label='Collar' , height=15 )
autob_j_collar = cmds.textField(text='collar')

cmds.text( label='Shoulder' , height=15 )
autob_j_shoulder = cmds.textField(text='shoulder')

cmds.text( label='Elbow' , height=15 )
autob_j_elbow = cmds.textField(text='elbow')

cmds.text( label='Hand' , height=15 )
autob_j_wrist = cmds.textField(text='hand')

cmds.text( label='Hip' , height=15 )
autob_j_hip = cmds.textField(text='hip')

cmds.text( label='Knee' , height=15 )
autob_j_knee = cmds.textField(text='knee')

cmds.text( label='Foot' , height=15 )
autob_j_foot = cmds.textField(text='foot')

cmds.text( label='Toe' , height=15 )
autob_j_toe = cmds.textField(text='Toe')

cmds.text( label='ToeTip' , height=15 )
autob_j_toetip = cmds.textField(text='ToeTip')
cmds.setParent( '..' )
cmds.setParent( '..' )
  
  
  
cmds.frameLayout(label="Control Names",width=autob_win_y_max, collapsable=True,collapse=True)
cmds.gridLayout(numberOfColumns=2,cellWidthHeight=(100, 20))
 
            
cmds.text( label='Root' , height=15 )
autob_c_root = cmds.textField(text='c_root')

cmds.text( label='Hip' , height=15 )
autob_c_hip = cmds.textField(text='c_hip')

cmds.text( label='Pelvis' , height=15 )
autob_c_pelvis = cmds.textField(text='c_pelvis')

cmds.text( label='Spine' , height=15 )
autob_c_spine = cmds.textField(text='c_spine')

cmds.text( label='Neck' , height=15 )
autob_c_neck = cmds.textField(text='neck')

cmds.text( label='Head' , height=15 )
autob_c_head = cmds.textField(text='head')

cmds.text( label='Collar' , height=15 )
autob_c_collar = cmds.textField(text='collar')

cmds.text( label='Shoulder (FK)' , height=15 )
autob_c_shoulder = cmds.textField(text='shoulder')

cmds.text( label='Elbow (FK)' , height=15 )
autob_c_elbow = cmds.textField(text='elbow')

cmds.text( label='Wrist (FK)' , height=15 )
autob_c_wrist = cmds.textField(text='wrist')

cmds.text( label='Arm (IK)' , height=15 )
autob_c_armik = cmds.textField(text='armik')

cmds.text( label='Elbow (IK)' , height=15 )
autob_c_elbowik = cmds.textField(text='elbowik')

cmds.text( label='armHub' , height=15 )
autob_c_armhub = cmds.textField(text='armhub')

cmds.text( label='Thigh' , height=15 )
autob_c_thigh = cmds.textField(text='c_thigh<')

cmds.text( label='Calf' , height=15 )
autob_c_calf = cmds.textField(text='c_calf<')

cmds.text( label='Foot' , height=15 )
autob_c_foot = cmds.textField(text='c_foot<')

cmds.text( label='legik' , height=15 )
autob_c_legik = cmds.textField(text='legik')

cmds.text( label='kneeik' , height=15 )
autob_c_kneeik = cmds.textField(text='kneeik')

cmds.text( label='leghub' , height=15 )
autob_c_leghub = cmds.textField(text='leghub')

cmds.text( label='Toe' , height=15 )
autob_c_toe = cmds.textField(text='Toe')

cmds.text( label='ToeTip' , height=15 )
autob_c_toetip = cmds.textField(text='ToeTip')
cmds.setParent( '..' )
cmds.setParent( '..' )

 
cmds.frameLayout(label="Aux Names",width=autob_win_y_max, collapsable=True,collapse=True)
cmds.gridLayout(numberOfColumns=2,cellWidthHeight=(100, 20))
cmds.setParent( '..' )
cmds.setParent( '..' )
        
cmds.frameLayout(label="Weight",width=autob_win_y_max, collapsable=True,collapse=True)
cmds.setParent( '..' )
            
cmds.frameLayout(label="Rig",width=autob_win_y_max, collapsable=True,collapse=True)

cmds.button( label='Create Rig', 
             width = 100,
             command=autob_buildrig )
cmds.setParent( '..' )
                                               
cmds.showWindow( window )