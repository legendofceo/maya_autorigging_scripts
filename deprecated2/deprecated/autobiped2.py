import maya.cmds as cmds
import math

autob_win_y_max = 300

g_group_draft_h8 = 'biped_draft_h8'
g_group_skeleton_h8 = 'biped_skeleton_h8'
g_group_rig_h8 = 'biped_rig_h8'

g_right_h8 = '_r'
g_left_h8 = '_l'


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


    
def group_reset(name):
    if cmds.objExists(name):
        cmds.delete(name)            
    cmds.group( em=True, name=name)
    return name 

def add_proxy(name,radius,pos,rgb,group):
    cmds.sphere(r=radius, n=name)
    cmds.move(pos[0], pos[1], pos[2],r=True,os=True,wd=True )
    cmds.setAttr(name+'.overrideEnabled', 1)
    cmds.setAttr(name+'.overrideRGBColors', 1)
    cmds.setAttr(name+'.overrideColorR', rgb[0])
    cmds.setAttr(name+'.overrideColorG', rgb[1])
    cmds.setAttr(name+'.overrideColorB', rgb[2])
    cmds.parent(name,group)
             
                      
def biped_draft_h8(args):
  
    group = group_reset(g_group_draft_h8)
         
    d_pre = '_draft'
         

    #data = biped_dataobj_h8()
    #data.build()
          
    add_proxy('pelvis_draft',2,[0,0,80.87],[0,0,255],group)
    add_proxy('head_draft',2,[0,-3.09,161.262],[140,140,0],group) 
    add_proxy('clavicle_draft',2,[-7.461,0,136.133],[255,255,0],group)
    add_proxy('upperarm_draft',2,[-11.47,0,133.31],[255,255,0],group)
    add_proxy('lowerarm_draft',2,[-28.452,0,115.808],[255,255,0],group)
    add_proxy('hand_draft',2,[-45.15,0,95.69],[255,255,0],group)
    add_proxy('thigh_draft',2,[-8.93,0,76.22],[0,255,255],group)
    add_proxy('shin_draft',2,[-10.036, 0, 46.531],[0,140,140],group)
    add_proxy('foot_draft',2,[-13.00,0,13.48],[0,140,140],group)
    add_proxy('toe_draft',2,[-20.556,-5.487,-0.718],[140,140,0],group)
    add_proxy('toetip_draft',2,[-25.73, -13.573, -1.036],[140,140,0],group)
         
    spine_num = cmds.intField(autob_num_spine,q=True,v=True)        
    for s in range(spine_num):           
        n = 'spine'+str(s+1)+'_draft'
        span = 65.0/spine_num
        rad =  2-((2.0 / spine_num) * s)
        hue =  80-((255 / spine_num) * s)
        add_proxy(n,rad,[0,0,90+(s*span)],[255,hue,hue],group)         
 
    neck_num = cmds.intField(autob_num_neck,q=True,v=True)           
    for s in range(neck_num):
        n = 'neck'+str(s+1)+'_draft'
        span = 10.0/neck_num
        rad =  2-((2.0 / neck_num) * s)
        hue =  .3-((0.4 / neck_num) * s)        
        add_proxy(n,rad,[0,0,145+(s*span)],[hue,hue,255],group)


def get_hierarchy(name):
    list = cmds.listRelatives(name,allDescendents=True)
    listRev = []
    for j in reversed(list):
        listRev.append(j)
    return listRev        


def mirror_joint(j,suf_left):
    
    pos = cmds.xform(j,q=1,ws=1,rp=1) 
    
    if(pos[0]<0):
        par = cmds.listRelatives(j,parent=True,shapes=True)[0] 
            
        cmds.select(cl=True)
        mirrored_pos = [pos[0]*-1,pos[1],pos[2]]
        new = cmds.joint(name=j+suf_left,p=mirrored_pos)
        
        cmds.setAttr(new+'.side',2)
        cmds.setAttr(new+'.type',18)
        cmds.setAttr(new+'.drawLabel',1)
        cmds.setAttr(new+'.otherType',cmds.getAttr(j+'.otherType'),type='string')
        
        parType = cmds.nodeType(par, api=True )
        if parType=="kJoint":
            parx = cmds.xform(par,q=1,ws=1,rp=1)[0]

            if parx<0:         
                par_axis = par+suf_left                    
                cmds.parent(new,par_axis)
            else:              
                cmds.parent(new,par)
        elif parType=="kTransform":
            pass
                #cmds.parent(new,autob_group_output)
        
    
def mirror(root,suf_right,suf_left):   
            
    joints = get_hierarchy(root)
    for j in joints:
        mirror_joint(j,suf_left)
        
    joints = get_hierarchy('root')  
    for j in joints:
        pos = cmds.xform(j,q=1,ws=1,rp=1)
        if pos[0]<0:
            cmds.rename(j,j+suf_right)
            
                
def add_joint_match(name,proxy):
    cmds.joint(n=name,p=[0,0,0])
    cmds.matchTransform(name,proxy)
    cmds.setAttr(name+'.side',1)
    cmds.setAttr(name+'.type',18)
    cmds.setAttr(name+'.drawLabel',1)
    cmds.setAttr(name+'.otherType',name,type='string')
    
def biped_skeleton_h8(args):
                       
         group = group_reset(g_group_skeleton_h8)
                                    
         cmds.joint(n='root',p=[0,0,0])                 
          
         add_joint_match('pelvis','pelvis_draft')
   
         num_spine = cmds.intField(autob_num_spine,q=True,v=True)
         for i in range(num_spine):
             add_joint_match('spine'+str(i+1),'spine'+str(i+1)+'_draft')
        
         for i in range(cmds.intField(autob_num_neck,q=True,v=True)):
             add_joint_match('neck'+str(i+1),'neck'+str(i+1)+'_draft')
         
         add_joint_match('head','head_draft')
          
         cmds.select('spine'+str(num_spine),r=True)
         
         add_joint_match('clavicle','clavicle_draft')         
         add_joint_match('upperarm','upperarm_draft')
         add_joint_match('lowerarm','lowerarm_draft')
         add_joint_match('hand','hand_draft')

         cmds.select('pelvis',r=True)  
         add_joint_match('thigh','thigh_draft')        
         add_joint_match('shin','shin_draft')
         add_joint_match('foot','foot_draft')
         add_joint_match('toe','toe_draft')
         add_joint_match('toetip','toetip_draft')
         
         mirror('root',g_right_h8,g_left_h8)
         
         joints = get_hierarchy('root')
        
         for j in joints:
             cmds.setAttr(j+'.overrideEnabled', 1)
             cmds.setAttr(j+'.overrideRGBColors', 1)
             cmds.setAttr(j+'.overrideColorR', 255)
             cmds.setAttr(j+'.overrideColorG', 255)
             cmds.setAttr(j+'.overrideColorB', 255)
             
    
def set_color(name,rgb):        
    cmds.setAttr(name+'.overrideEnabled', 1)
    cmds.setAttr(name+'.overrideRGBColors', 1)
    cmds.setAttr(name+'.overrideColorR', rgb[0])
    cmds.setAttr(name+'.overrideColorG', rgb[1])
    cmds.setAttr(name+'.overrideColorB', rgb[2])
    cmds.setAttr(name+'.overrideShading', 0) 
        
def duplicate_joints(joints,new_joints): 
    par = cmds.listRelatives(joints[0], p=True)    
    new_arr = []
    
    for j,n in zip(joints, new_joints): 
        cmds.joint( p=(0, 0, 0),n=n )
        cmds.matchTransform(n,j)
        new_arr.append(n)       
    cmds.parent(new_arr[0],par)
    return new_arr
    
    
def ezrig_arm_fk(orig,syntax):
    
    names = []
    for j in orig:
        names.append(syntax.replace('@',j))
    
    chain_fk = duplicate_joints(orig,names)
    for j in chain_fk:
        set_color(j,[.2,1,.2])
         
    arm0='c_'+orig[0]       
    cmds.torus(n=arm0, r=7.5, hr=0.005, axis=[1,0,0],ssw=-230, esw=-130) 
    set_color(arm0,[0,255,0])
    cmds.matchTransform(arm0,orig[0])
    cmds.orientConstraint(arm0,chain_fk[0])
    
    arm1='c_'+orig[1]       
    cmds.torus(n=arm1, r=7.5, hr=0.005, axis=[1,0,0],ssw=-140, esw=-40) 
    set_color(arm1,[0,255,0])
    cmds.matchTransform(arm1,orig[1])
    cmds.orientConstraint(arm1,chain_fk[1])
    cmds.parent(arm1,arm0)
    
    arm2='c_'+orig[2]       
    cmds.torus(n=arm2, r=4.25, hr=0.005, axis=[1,0,0],ssw=360, esw=0) 
    set_color(arm2,[0,255,0])
    cmds.matchTransform(arm2,orig[2])
    cmds.orientConstraint(arm2,chain_fk[2])
    cmds.parent(arm2,arm1)
    
    return chain_fk
            
def ezrig_arm_ik(orig,syntax,side,ctr_hand_name,ctr_elbow_name):
    
    names = []
    for j in orig:
        names.append(syntax.replace('@',j))
    
    chain_ik = duplicate_joints(orig,names)
      
    for j in chain_ik:
        set_color(j,[1,1,0])
    cmds.torus(n=ctr_hand_name, r=7.5, hr=0.005, axis=[1,0,0],ssw=-230, esw=-130) 
    set_color(ctr_hand_name,[255,0,0])
    cmds.matchTransform(ctr_hand_name,orig[2])
    
    chain_name = syntax.replace('@','chain')+side
    
    cmds.ikHandle(sj=chain_ik[0], ee= chain_ik[2], n=chain_name )
    cmds.parent(chain_name,ctr_hand_name)
      
      
    return chain_ik


def ezrig_leg_fk(orig,syntax):
    
    names = []
    for j in orig:
        names.append(syntax.replace('@',j))
    
    chain_fk = duplicate_joints(orig,names)
    for j in chain_fk:
        set_color(j,[.2,1,.2])
         
    thigh='c_'+orig[0]       
    cmds.torus(n=thigh, r=7.5, hr=0.005, axis=[1,0,0],ssw=-230, esw=-130) 
    set_color(thigh,[0,255,0])
    cmds.matchTransform(thigh,orig[0])
    cmds.orientConstraint(thigh,chain_fk[0])
    
    shin='c_'+orig[1]       
    cmds.torus(n=shin, r=7.5, hr=0.005, axis=[1,0,0],ssw=-140, esw=-40) 
    set_color(shin,[0,255,0])
    cmds.matchTransform(shin,orig[1])
    cmds.orientConstraint(shin,chain_fk[1])
    cmds.parent(shin,thigh)
    
    foot='c_'+orig[2]       
    cmds.torus(n=foot, r=4.25, hr=0.005, axis=[1,0,0],ssw=360, esw=0) 
    set_color(foot,[0,255,0])
    cmds.matchTransform(foot,orig[2])
    cmds.orientConstraint(foot,chain_fk[2])
    cmds.parent(foot,shin)
    
    toe='c_'+orig[3]       
    cmds.torus(n=toe, r=4.25, hr=0.005, axis=[1,0,0],ssw=360, esw=0) 
    set_color(toe,[0,255,0])
    cmds.matchTransform(toe,orig[3])
    cmds.orientConstraint(toe,chain_fk[3])
    cmds.parent(toe,foot)
      
      
    return chain_fk
    
def ezrig_leg_ik(orig,syntax,side,ctr_leg_name,ctr_knee_name):
    
    names = []
    for j in orig:
        names.append(syntax.replace('@',j))
    
    chain_ik = duplicate_joints(orig,names)
      
    for j in chain_ik:
        set_color(j,[1,1,0])
    cmds.torus(n=ctr_leg_name, r=7.5, hr=0.005, axis=[1,0,0],ssw=-230, esw=-130) 
    set_color(ctr_leg_name,[255,0,0])
    cmds.matchTransform(ctr_leg_name,orig[2])
    
    chain_name_leg = syntax.replace('@','chain_leg')+side
    chain_name_foot = syntax.replace('@','chain_foot')+side
    chain_name_toe = syntax.replace('@','chain_toe')+side
    
    cmds.ikHandle(sj=chain_ik[0], ee= chain_ik[2], n=chain_name_leg )
    cmds.ikHandle(sj=chain_ik[2], ee= chain_ik[3], n=chain_name_foot )
    cmds.ikHandle(sj=chain_ik[3], ee= chain_ik[4], n=chain_name_toe )
    
    helper_toe = syntax.replace('@','helper_toe')+side
    helper_ball = syntax.replace('@','helper_ball')+side
    helper_wiggle = syntax.replace('@','helper_wiggle')+side
    
    cmds.spaceLocator(n=helper_toe)
    cmds.matchTransform(helper_toe,orig[3])
    cmds.setAttr(helper_toe+".rotateOrder", 2)
    
    cmds.spaceLocator(n=helper_ball )
    cmds.matchTransform(helper_ball,orig[3])
    cmds.setAttr(helper_ball+".rotateOrder", 2)
    
    
    cmds.spaceLocator(n=helper_wiggle )
    cmds.matchTransform(helper_wiggle,orig[3])
    cmds.setAttr(helper_wiggle+".rotateOrder", 2)
    
    cmds.polySphere( n=ctr_knee_name, r=3, sx=10, sy=10)    
    cmds.matchTransform(ctr_knee_name,orig[1])
    piv = cmds.xform(orig[2], q=True, ws=True, rp=True)
    cmds.xform(ctr_knee_name, ws=True, piv=(piv[0], piv[1], piv[2]) )
    cmds.move(0, -32, 0,r=True,os=True,wd=True )
    cmds.parent(ctr_knee_name, ctr_leg_name)
    cmds.poleVectorConstraint(ctr_knee_name,chain_name_leg)
    
    cmds.parent(helper_toe,ctr_leg_name)    
    cmds.parent(chain_name_foot, helper_toe)
    cmds.parent(helper_wiggle, helper_toe)
    cmds.parent(chain_name_toe, helper_wiggle)    
    cmds.parent(helper_ball, helper_toe)    
    cmds.parent(chain_name_leg, helper_ball)
    
    #cmds.parent(chain_name,ctr_hand_name)
      
      
    return chain_ik

def ezrig_spine_fk(chain,controls):
    pass
    
def ezrig_spine_stretchik(name,spline_chain,lower_control,upper_control):
    original_chain = spline_chain
    
    
    name_arr = []
    for j in spline_chain:
        name_arr.append(j+name)
        
    spline_chain = duplicate_joints(spline_chain,name_arr)
    num = len(spline_chain)
    
    cmds.matchTransform(lower_control,original_chain[0])
    cmds.matchTransform(upper_control,original_chain[num-1])
     
    cmds.select(cl=True)
    ikh, effector, curve = cmds.ikHandle(name='{0}_ikh'.format(name), startJoint=spline_chain[0], endEffector=spline_chain[num-1], solver='ikSplineSolver')
    
    cmds.select(cl=True)
    start_joint = cmds.joint(n='joint_start')
    cmds.select(cl=True)
    end_joint = cmds.joint(n='joint_end')
    cmds.select(cl=True)
    cmds.matchTransform(start_joint,original_chain[0])
    cmds.matchTransform(end_joint,original_chain[num-1])
    
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
    
    return spline_chain
    
                                           
def biped_rig_h8(args):
   
    group = group_reset(g_group_rig_h8)
    
    n='c_root'       
    cmds.torus(n=n, r=30.0, hr=0.02, axis=[0,0,1], msw=360, ssw=-140, esw=-40, s=2, nsp=1) 
    set_color(n,[255,0,0])
    cmds.matchTransform(n,'root')
    cmds.parent(n,group)
    
    n='c_hip'       
    cmds.torus(n=n, r=30.0, hr=0.02, axis=[0,0,1], msw=360, ssw=-140, esw=-40, s=2, nsp=1) 
    set_color(n,[1,.2,.5])
    cmds.matchTransform(n,'pelvis')
    cmds.parent(n,group)
    
    n='c_pelvis'       
    cmds.torus(n=n, r=25.0, hr=0.005, axis=[0,0,1], msw=360, ssw=-140, esw=-40, s=2, nsp=1) 
    set_color(n,[.3,1,.3])
    cmds.matchTransform(n,'pelvis')
    cmds.parent(n,group)
    
    spine_low='c_spineik_bot'       
    cmds.torus(n=spine_low, r=25.0, hr=0.005, axis=[0,0,1], msw=360, ssw=-140, esw=-40, s=2, nsp=1) 
    set_color(spine_low,[.3,1,.3])

    
    spine_high='c_spineik_top'       
    cmds.torus(n=spine_high, r=25.0, hr=0.005, axis=[0,0,1], msw=360, ssw=-140, esw=-40, s=2, nsp=1) 
    set_color(spine_high,[.3,1,.3])
    
    num_spine = cmds.intField(autob_num_spine,q=True,v=True)
    chain_spine = []
    for i in range(num_spine):
        chain_spine.append('spine'+str(i+1))
    ezrig_spine_stretchik('spineik',chain_spine,spine_low,spine_high)
        
    def do_axis(axis):
    
        if axis==1:
            suf = '_r'
        elif axis==2:
            suf = '_l'    
        
        chain_arm = ['upperarm'+suf,'lowerarm'+suf,'hand'+suf]
        chain_arm_fk = ezrig_arm_fk(chain_arm,'armfk_@')
        chain_arm_ik = ezrig_arm_ik(chain_arm,'armik_@',suf,'c_armik'+suf,'c_elbowik'+suf)

        chain_leg = ['thigh'+suf,'shin'+suf,'foot'+suf,'toe'+suf,'toetip'+suf]
        chain_leg_fk = ezrig_leg_fk(chain_leg,'legfk_@')
        chain_leg_ik = ezrig_leg_ik(chain_leg,'legik_@',suf,'c_legik'+suf,'c_kneeik'+suf)
        
    
    do_axis(1)
    do_axis(2)

  
  
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
             command=biped_draft_h8 )

cmds.text( label='Create a skeleton from the draft:' , height=35 )

cmds.button( label='Output', 
             width = 100,
             command=biped_skeleton_h8 )

cmds.button( label='Create Rig', 
             width = 100,
             command=biped_rig_h8 )
                                      
cmds.text( label='Customize the features of the skeleton:' , height=35 )

cmds.setParent( '..' ) 

cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(140, 30))
 
cmds.text( label='Control Hash' )
fi_control_hash = cmds.textField(tx='c_')
                                               
cmds.text( label='Spine Joints' )
autob_num_spine = cmds.intField(minValue=4, maxValue=6, step=1, value=6)

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
  

cmds.setParent( '..' )
                                               
cmds.showWindow( window )