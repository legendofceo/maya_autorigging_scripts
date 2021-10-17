import maya.cmds as cmds
import maya.mel as mel
import json

g_filepath = 'C:\\Users\\16C24E\\Desktop\\bone_data_female.json'
g_axis_left = '_l'
g_axis_right = '_r'

g_jrad_sheath = 0.7
g_jrad_face = 0.25

g_jcol_weighted = [1,1,1]
g_jcol_face = [1,.5,0]
g_jcol_sheath = [1,1,0]
g_jcol_size = [0,1,0]
g_jcol_genf = [0.8,0.4,0.8]
g_jcol_genm = [0.2,0.8,1.0]

g_set_basic = 'bones_basic'
g_set_face = 'bones_face'
g_set_genm = 'bones_genm'
g_set_genf = 'bones_genf'
g_set_sheath = 'bones_sheath'

g_type_basic = 1
g_type_face = 2
g_type_bodyunique = 3
g_type_helper = 4
g_type_sheath = 5


def create_layer(name):
    
    if cmds.objExists(name) == False:
        cmds.sets(n=name)

def check_key(key,json):
    if key in json:
        return True
    else:
        return False  
 
        
        
                         
def get_skeleton():
    skel = skeleton_h8()
    
    f = open(g_filepath, 'r')
    skeleton_data = json.loads(f.read())
    
    bones = skeleton_data['bones']
    bone_num = len(bones)
    
    for b in bones:
        if "sym" in b:
            skel.add(bone_sym_h8(b))
        else:
            skel.add(bone_h8(b))
    
    twists = skeleton_data['twists']
    twist_num = len(twists)
    
    skel.set_twists(twists);
    return skel          

def ensure_position(node,x,y,z):
    pos = cmds.xform(node,q=True,ws=True,t=True)      
    if pos[0]!=x or pos[1]!=y or pos[2]!=z:
        print("Position not ensured: "+node)
 
def force_down_x(id):
    cmds.setAttr(id+'.translateY',0)
    cmds.setAttr(id+'.translateZ',0)

def clear_rotations(id):
    cmds.setAttr(id+'.rotateX',0)   
    cmds.setAttr(id+'.rotateY',0)
    cmds.setAttr(id+'.rotateZ',0)
              
class bone_h8:
    
    def select_available(self):
        cmds.select(self.id,add=True)
     
    def unparent_set():
        cmds.parent(self.id,w=True)
    
    def label(self):
        cmds.setAttr(self.id+'.otherType', self.id,type='string')     
        cmds.setAttr(self.id+'.type', 18)
        cmds.setAttr(self.id+'.side', 0)
        cmds.setAttr(self.id+'.drawLabel', 1)
    
    def setup(self,bone):
        self.id = bone['id']
        self.type = bone['type']
        
        if check_key('is_root',bone):
            cmds.setAttr(self.id+'.drawStyle',2)
            ensure_position(self.id,0,0,0)
    
    def process(self):
        clear_rotations(self.id)

          
    def __init__(self,bone):        
        self.setup(bone)
        
        cmds.setAttr(self.id+'.radius', bone['radius']) 
        #cmds.sets([self.name], add=set )
        cmds.setAttr(self.id+'.overrideEnabled', 1)
        cmds.setAttr(self.id+'.overrideRGBColors', 1)
        cmds.setAttr(self.id+'.overrideColorR', bone['rgb'][0])
        cmds.setAttr(self.id+'.overrideColorG', bone['rgb'][1])
        cmds.setAttr(self.id+'.overrideColorB', bone['rgb'][2])
        
        
        
class bone_sym_h8(bone_h8):
    
    def select_available(self):
        cmds.select(self.id+g_axis_left,add=True)
        cmds.select(self.id+g_axis_right,add=True)
        
    def unparent_set():
        cmds.parent(self.id+g_axis_left,w=True)
        cmds.parent(self.id+g_axis_right,w=True)
        
    def label(self):
        cmds.setAttr(self.id+g_axis_right+'.otherType', self.id,type='string')     
        cmds.setAttr(self.id+g_axis_right+'.type', 18)
        cmds.setAttr(self.id+g_axis_right+'.side', 2)
        cmds.setAttr(self.id+g_axis_right+'.drawLabel', 1)
        cmds.setAttr(self.id+g_axis_left+'.otherType', self.id,type='string')     
        cmds.setAttr(self.id+g_axis_left+'.type', 18)
        cmds.setAttr(self.id+g_axis_left+'.side', 1)
        cmds.setAttr(self.id+g_axis_left+'.drawLabel', 1)  

    def process(self):
        
        if self.sym!='twist':
            clear_rotations(self.id+g_axis_right)
            clear_rotations(self.id+g_axis_left)
        
        pos = cmds.xform(self.id+g_axis_right,q=True,ws=True,t=True) 
        jo = get_joint_orientation(self.id+g_axis_right)       
        
        
        if self.sym=='x':
            cmds.xform(self.id+g_axis_left,ws=True,t=[pos[0]*-1,pos[1],pos[2]]) 
        
        if self.sym=='limbsocket': 
            jo[0]=jo[0]-180
            jo[1]=jo[1]*-1
            jo[2] = 90+(90-jo[2])
            set_joint_orientation(self.id+g_axis_left,jo)
        
        if self.sym=='limbpartial':
            cmds.xform(self.id+g_axis_left,ws=True,t=[pos[0]*-1,pos[1],pos[2]])  
            force_down_x(self.id+g_axis_right)
            force_down_x(self.id+g_axis_left)   
        
        if self.sym=='kuckle':
            jo[0]=jo[0]*-1
            jo[1]=jo[1]*-1
            jo[2]=jo[2]*-1
            set_joint_orientation(self.id+g_axis_left,jo)
            cmds.xform(self.id+g_axis_left,ws=True,t=[pos[0]*-1,pos[1]*-1,pos[2]*-1]) 
            
        if self.sym=='limb': 
            jo[0]=jo[0]*-1
            jo[1]=jo[1]*-1
            jo[2]=jo[2]*-1
            set_joint_orientation(self.id+g_axis_left,jo)
            cmds.xform(self.id+g_axis_left,ws=True,t=[pos[0]*-1,pos[1],pos[2]]) 
            force_down_x(self.id+g_axis_right)
            force_down_x(self.id+g_axis_left) 
            
        if self.sym=='twist':
            force_down_x(self.id+g_axis_right)
            force_down_x(self.id+g_axis_left) 
                     
    def __init__(self,bone):        
        self.setup(bone)
        
        self.sym = bone['sym']
                
        cmds.setAttr(self.id+g_axis_right+'.radius', bone['radius'])      
        cmds.setAttr(self.id+g_axis_left+'.radius', bone['radius']) 

        #cmds.sets([self.name+g_axis_right,self.name+g_axis_left], add=set )
        
        cmds.setAttr(self.id+g_axis_right+'.overrideEnabled', 1)
        cmds.setAttr(self.id+g_axis_right+'.overrideRGBColors', 1)

        cmds.setAttr(self.id+g_axis_right+'.overrideColorR', bone['rgb'][0])
        cmds.setAttr(self.id+g_axis_right+'.overrideColorG', bone['rgb'][1])
        cmds.setAttr(self.id+g_axis_right+'.overrideColorB', bone['rgb'][2])
        
        cmds.setAttr(self.id+g_axis_left+'.overrideEnabled', 1)
        cmds.setAttr(self.id+g_axis_left+'.overrideRGBColors', 1)
        cmds.setAttr(self.id+g_axis_left+'.overrideColorR', bone['rgb'][0])
        cmds.setAttr(self.id+g_axis_left+'.overrideColorG', bone['rgb'][1])
        cmds.setAttr(self.id+g_axis_left+'.overrideColorB', bone['rgb'][2])
        

        
         
class skeleton_h8:

    def select_all(self):
        cmds.select(j.id,add=True)
     
    def process(self):
        
        for j in self.arr:
            j.process()
        
        for t in self.twists:
            
            for i in range(2):
                pow = t['num']+1
                if i==0:
                    suf = '_r'
                elif i==1:
                    suf = '_l'
                
                 
                len = (cmds.getAttr(t['end']+suf+'.translateX')/pow)
                
                for ii in range(t['num']):
                    tw = t['syntax'].replace('$',str(ii+1))+suf                    
                    set_local_translation(tw,[len*(ii+1),0,0])
         
               
    def add(self,obj): 
        self.arr.append(obj)
        self.r[obj.id] = obj
    
    def set_twists(self,twists):
        self.twists = twists
           
    def select_all(self):
        
        for j in self.arr:
            j.select_all()
    
    def select_all_bindable(self):        
        for j in self.arr:
            if j.type == 'bodyanim' or j.type == 'faceanim':
                j.select_available()
    
    def label(self):
        
        for j in self.arr:
            j.label()
          
    def get(self,key):
        return self.r[key]
           
    def __init__(self):        
        self.arr = []
        self.r = {}
                      


def get_hierarchy(name):
    list = cmds.listRelatives(name,allDescendents=True)
    listRev = []
    for j in reversed(list):
        listRev.append(j)
    return listRev        



def unbind():
    mel.eval('gotoBindPose')
    cmds.select('female_a_shape',r=True)
    mel.eval('doDetachSkin "2" { "2","1" }') 
    
    #cmds.bindSkin(unbindKeepHistory=True,e=True)

    

def set_joint_orientation(name,rot):
    cmds.setAttr(name+'.jointOrientX',rot[0])    
    cmds.setAttr(name+'.jointOrientY',rot[1])
    cmds.setAttr(name+'.jointOrientZ',rot[2])  

def get_joint_orientation(name):
    x = cmds.getAttr(name+'.jointOrientX')    
    y = cmds.getAttr(name+'.jointOrientY')
    z = cmds.getAttr(name+'.jointOrientZ')  
    return [x,y,z]
    
           
def set_local_translation(name,pos):
    
    cmds.setAttr(name+'.translateX',pos[0])    
    cmds.setAttr(name+'.translateY',pos[1])
    cmds.setAttr(name+'.translateZ',pos[2])    

def set_joint_orientation(name,pos):
    
    cmds.setAttr(name+'.jointOrientX',pos[0])    
    cmds.setAttr(name+'.jointOrientY',pos[1])
    cmds.setAttr(name+'.jointOrientZ',pos[2]) 
    
    
def measure_chain(start,end):
    n = 'TEMPLOCATORDELETE'
    cmds.spaceLocator(n=n)
    cmds.matchTransform(n,end)
    cmds.parent(n,start)
    val = cmds.getAttr(n+'.translateX')
    cmds.delete(n)
    return val
    
    
def twist_bones(ax):
    
    invert = 1
    if ax==0:
        axis = '_r'
    elif ax==1:
        axis = '_l'
        invert = -1
     
       
    len_upperarm = measure_chain('upperarm_r','lowerarm_r')/4*invert
    len_lowerarm = measure_chain('lowerarm_r','hand_r')/4*invert   
    
            
    set_local_translation('upperarm_twist1'+axis,[len_upperarm,0,0])
    set_local_translation('upperarm_twist2'+axis,[len_upperarm*2,0,0])
    set_local_translation('upperarm_twist3'+axis,[len_upperarm*3,0,0])
    
    set_local_translation('lowerarm_twist1'+axis,[len_lowerarm,0,0])
    set_local_translation('lowerarm_twist2'+axis,[len_lowerarm*2,0,0])
    set_local_translation('lowerarm_twist3'+axis,[len_lowerarm*3,0,0])
   
    len_thigh = measure_chain('thigh_r','calf_r')/3*invert
    len_calf = measure_chain('calf_r','foot_r')/3*invert   
    
    
    set_local_translation('thigh_twist1'+axis,[len_thigh,0,0])
    set_local_translation('thigh_twist2'+axis,[len_thigh*2,0,0])
    set_local_translation('calf_twist1'+axis,[len_calf,0,0])
    set_local_translation('calf_twist2'+axis,[len_calf*2,0,0])


def prepare_skeleton(args):
    skel = get_skeleton()
    skel.process()
    
    #skel.label()
    #mirror_pivots()
    #mirror_joints()
    #twist_bones(0)
    #twist_bones(1)
                          
    #unbind()
    #twist_bones(0)
    #twist_bones(1)
    #
    #skel.select_all_bindable()
    
def select_all_bindable(args):
    skel = get_skeleton()
    skel.select_all_bindable()

def crop_region(base_name,set_name,output_name):
      
    cmds.select(cmds.sets(set_name,q=True))
    cmds.select(base_name+'.f[*]', tgl=True)
    cmds.rename(base_name,output_name)
    cmds.delete()

def do_crop_region(shape,set,output,*args):
       
    this_file = cmds.file(q=True, sn=True)
    cmds.file(this_file, o=True, f=True)
    crop_region(shape,set,output)
    cmds.bakePartialHistory(output,prePostDeformers=False )



def make_all_twists(args):

    f = open(g_filepath, 'r')
    skeleton_data = json.loads(f.read())        
    twists = skeleton_data['twists']
                         
    for t in twists:
        make_twist(t)
        
def delete_all_twists(args):
    
    f = open(g_filepath, 'r')
    skeleton_data = json.loads(f.read())        
    twists = skeleton_data['twists']
                         
    for t in twists:
        delete_twist(t)
        
def make_twist(data):   

    
    num = data['num']
    for i in range(num):
        tw = data['syntax'].replace('$',str(i+1))
        
        if check_key('sym',data):             
            cmds.expression(s=tw+g_axis_right+'.rotateX='+data['end']+g_axis_right+'.rotateX/'+str(num-i))
            cmds.expression(s=tw+g_axis_left+'.rotateX='+data['end']+g_axis_left+'.rotateX/'+str(num-i))
        else:
            cmds.expression(s=tw+'.rotateX='+data['end']+'.rotateX/'+str(num-i))
            
def delete_twist(data): 
    
    num = data['num']
    for i in range(num):
        tw = data['syntax'].replace('$',str(i+1))
        
        if check_key('sym',data):
            print(tw+g_axis_right)
            cmds.select (tw+g_axis_right, replace=1)
            cmds.delete (expressions=1)
             
            cmds.select (tw+g_axis_left, replace=1)
            cmds.delete (expressions=1)
            
        else:
            cmds.select (tw, replace=1)
            cmds.delete (expressions=1)

        
        

        

    
               
g_win_width = 500

window = cmds.window( 
    title='Rig Helper',  
    width=g_win_width,
    resizeToFitChildren=True) 

scrollLayout = cmds.scrollLayout(
    horizontalScrollBarThickness=16,
    verticalScrollBarThickness=16)
    
cmds.columnLayout(
    columnOffset=['left',0])
 


cmds.frameLayout(label="Draft Skeleton",width=g_win_width, collapsable=True,collapse=False)
cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(g_win_width-16, 40))

cmds.text( label='Place the drafting objects, or reset the drafting objects:' , height=35 )

cmds.button( label='Prep Skeleton', 
             width = 100,
             command=prepare_skeleton )


cmds.button( label='Select All Bindable', 
             width = 100,
             command=select_all_bindable )
 
cmds.button( label='Set Twists', 
             width = 100,
             command=make_all_twists )

cmds.button( label='Delete Twists', 
             width = 100,
             command=delete_all_twists )
             
                          
cmds.button( label='Crop Head', 
             width = 100,
             command=lambda x: do_crop_region('female_a_shape','region_head','head_shape') )
                        
cmds.button( label='Crop Torso', 
             width = 100,
             command=lambda x: do_crop_region('female_a_shape','region_torso','torso_shape') )
             
cmds.button( label='Crop Legs', 
             width = 100,
             command=lambda x: do_crop_region('female_a_shape','region_legs','legs_shape') )

cmds.button( label='Crop hands', 
             width = 100,
            command=lambda x: do_crop_region('female_a_shape','region_hands','hands_shape') )
             
cmds.button( label='Crop Feet', 
             width = 100,
             command=lambda x: do_crop_region('female_a_shape','region_feet','feet_shape') )
                          
cmds.setParent( '..' )
                                               
cmds.showWindow( window )

get_skeleton()