import maya.cmds as cmds
import json


g_axis_left = '_l'
g_axis_right = '_r'

#dagPose -save -bindPose


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
    
def check_key(key,json):
    if key in json:
        return True
    else:
        return False  
                    
    
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
    
    def flex(self):
        if self.muscle == True:
            cmds.setAttr(self.id+'.scaleX',2.0)
            cmds.setAttr(self.id+'.scaleY',2.0)
            cmds.setAttr(self.id+'.scaleZ',2.0)
           
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
        self.radius = bone['radius']
        self.rgb = bone['rgb']   
        
        self.muscle = False
        self.is_root = False
        
        if check_key('flex',bone):
            self.muscle = True
        if check_key('is_root',bone):
            self.is_root = True
            
            
            
    def output_nodes(self):
        return [self.id]

    def process(self):
        clear_rotations(self.id)

        if self.is_root:
            cmds.setAttr(self.id+'.drawStyle',2)
            ensure_position(self.id,0,0,0)
        
        cmds.setAttr(self.id+'.radius', self.radius) 
        cmds.setAttr(self.id+'.overrideEnabled', 1)
        cmds.setAttr(self.id+'.overrideRGBColors', 1)
        cmds.setAttr(self.id+'.overrideColorR', self.rgb[0])
        cmds.setAttr(self.id+'.overrideColorG', self.rgb[1])
        cmds.setAttr(self.id+'.overrideColorB', self.rgb[2])
            
    def restore_parent(self):
        
        if(self.is_root==False):
            par = cmds.listRelatives(self.id,parent=True,shapes=True)[0]
            
            if(par!=self.parent):
                cmds.parent(self.id,self.parent)
              
    def __init__(self,bone):        
        self.setup(bone)
        
        if(self.is_root==False):
            self.parent = cmds.listRelatives(self.id,parent=True,shapes=True)[0] 
        
        
        
        
        
class bone_sym_h8(bone_h8):
    
    def select_available(self):
        cmds.select(self.id+g_axis_left,add=True)
        cmds.select(self.id+g_axis_right,add=True)
     
    def flex(self):
        if self.muscle == True:
            cmds.setAttr(self.id+g_axis_right+'.scaleX',2.0)
            cmds.setAttr(self.id+g_axis_right+'.scaleY',2.0)
            cmds.setAttr(self.id+g_axis_right+'.scaleZ',2.0)
            cmds.setAttr(self.id+g_axis_left+'.scaleX',2.0) 
            cmds.setAttr(self.id+g_axis_left+'.scaleY',2.0)
            cmds.setAttr(self.id+g_axis_left+'.scaleZ',2.0)
            
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

    def output_nodes(self):
        return [self.id+g_axis_right,self.id+g_axis_left]
        
    def process(self):
        
        cmds.setAttr(self.id+g_axis_right+'.radius', self.radius)      
        cmds.setAttr(self.id+g_axis_left+'.radius', self.radius) 

        #cmds.sets([self.name+g_axis_right,self.name+g_axis_left], add=set )
        
        cmds.setAttr(self.id+g_axis_right+'.overrideEnabled', 1)
        cmds.setAttr(self.id+g_axis_right+'.overrideRGBColors', 1)

        cmds.setAttr(self.id+g_axis_right+'.overrideColorR', self.rgb[0])
        cmds.setAttr(self.id+g_axis_right+'.overrideColorG', self.rgb[1])
        cmds.setAttr(self.id+g_axis_right+'.overrideColorB', self.rgb[2])
        
        cmds.setAttr(self.id+g_axis_left+'.overrideEnabled', 1)
        cmds.setAttr(self.id+g_axis_left+'.overrideRGBColors', 1)
        cmds.setAttr(self.id+g_axis_left+'.overrideColorR', self.rgb[0])
        cmds.setAttr(self.id+g_axis_left+'.overrideColorG', self.rgb[1])
        cmds.setAttr(self.id+g_axis_left+'.overrideColorB', self.rgb[2])
        
        if self.sym!='twist':
            clear_rotations(self.id+g_axis_right)
            clear_rotations(self.id+g_axis_left)
        
        pos = cmds.xform(self.id+g_axis_right,q=True,ws=True,t=True) 
        jo = get_joint_orientation(self.id+g_axis_right)       
        
        
        if self.sym=='x':
            cmds.xform(self.id+g_axis_left,ws=True,t=[pos[0]*-1,pos[1],pos[2]]) 
        
        if self.sym=='limbsocket': 
            cmds.xform(self.id+g_axis_left,ws=True,t=[pos[0]*-1,pos[1],pos[2]]) 
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
    
    def restore_parent(self):
        par = cmds.listRelatives(self.id+g_axis_right,parent=True,shapes=True)[0]
        if(par!=self.parent[0]):
            
            cmds.parent(self.id+g_axis_right,self.parent[0])
            cmds.parent(self.id+g_axis_left,self.parent[1])
                        
    def __init__(self,bone):        
        self.setup(bone)
        
        self.parent = []
        self.parent.append(cmds.listRelatives(self.id+g_axis_right,parent=True,shapes=True)[0])
        self.parent.append(cmds.listRelatives(self.id+g_axis_left,parent=True,shapes=True)[0])
        
        
        self.sym = bone['sym']
         

        
class twist_h8:
    
    def activate(self):  
            
                
        for i in range(self.num):
            tw = self.syntax.replace('$',str(i+1))
            
            if check_key('sym',data):             
                cmds.expression(s=tw+g_axis_right+'.rotateX='+self.end+g_axis_right+'.rotateX/'+str(num-i))
                cmds.expression(s=tw+g_axis_left+'.rotateX='+self.end+g_axis_left+'.rotateX/'+str(num-i))
            else:
                cmds.expression(s=tw+'.rotateX='+self.end+'.rotateX/'+str(num-i))
            
    def deactivate(self): 
        
        for i in range(self.num):
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
                        
      
    def __init__(self,data): 
        self.data = data
        self.num = data['num']    
        self.start = data['start']
        self.end = data['end']
        self.syntax = data['syntax']
        self.sym = data['sym']
        
class skeleton_h8:

    def select_all(self):
        cmds.select(j.id,add=True)
     
    def flex_muscles(self):
         for j in self.arr:
            j.flex()
      
    def select_by_type(self,types):
         for j in self.arr:
             for t in types:
                  if j.type == t:
                      j.select_available()
    
    def filter_by_type(self,types):
         arr = []
         
         for j in self.arr:
             for t in types:
                  if j.type == t:
                      arr.append(j)
         return arr                    
                   
                      
    def restore_all_parents(self):
        for j in self.arr:
            j.restore_parent() 
                              
    def process(self):
        
        for j in self.arr:
            j.process()
        
        for t in self.twists:
            
            for i in range(2):
                pow = t.num+1
                if i==0:
                    suf = '_r'
                elif i==1:
                    suf = '_l'
                
                 
                len = (cmds.getAttr(t.end+suf+'.translateX')/pow)
                
                for ii in range(t.num):
                    tw = t.syntax.replace('$',str(ii+1))+suf                    
                    set_local_translation(tw,[len*(ii+1),0,0])
        
        for j in self.locators:
            
            if check_key('snapto',j):
                id = j['id']
                cmds.matchTransform(id+g_axis_right,j['snapto']+g_axis_right)
                            
        for j in self.locators:
            
            if j['sym'] == 'x':
                id = j['id']
                pos = cmds.xform(id+g_axis_right,q=True,ws=True,t=True) 
                cmds.xform(id+g_axis_left,ws=True,t=[pos[0]*-1,pos[1],pos[2]]) 
               
    def add(self,obj): 
        self.arr.append(obj)
        self.r[obj.id] = obj
    
    def set_twists(self,twists):
        for t in twists:
            self.twists.append(twist_h8(t))

    def set_locators(self,locators):
        self.locators = locators
        
    def select_all(self):
        
        for j in self.arr:
            j.select_all()
    
    def select_all_bindable(self):        
        for j in self.arr:
            if j.type == 'bodyanim' or j.type == 'faceanim':
  
                j.select_available()

    def activate_twists(self):
                             
        for t in self.twists:
            t.activate()
        
    def deactivate_twists(self):
                                     
        for t in self.twists:
            t.deactivate()
        
    def label(self):
        
        for j in self.arr:
            j.label()
          
    def get(self,key):
        return self.r[key]
    
    def list_confined_parenting(self,list):

        actual_list = []
        for j in list:
            nodes = j.output_nodes()
            for n in nodes:
                actual_list.append(n)
         
        for j in actual_list:

            if(j!='root'):                 
                complete = False
                while complete==False:     
                    par = cmds.listRelatives(j,parent=True,shapes=True)[0]
                                                    
                    if par in actual_list:
                        complete = True
                    else:
                        par2 = cmds.listRelatives(par,parent=True,shapes=True)[0]
                        cmds.parent(j,par2)
        return actual_list
                                   
    def from_json(self,path):
            
        f = open(path, 'r')
        skeleton_data = json.loads(f.read())
        
        bones = skeleton_data['bones']
        bone_num = len(bones)
        
        for b in bones:
            if "sym" in b:
                self.add(bone_sym_h8(b))
            else:
                self.add(bone_h8(b))
        
        twists = skeleton_data['twists']
        twist_num = len(twists)
        self.set_twists(twists);
        
        locators = skeleton_data['locators']
        self.set_locators(locators)
    
    
    def __init__(self):        
        self.arr = []
        self.r = {}
        self.twists = []