import maya.cmds as cmds
import math

import sys
sys.path.append('.')


g_left = '_l'
g_right = '_r'



class saved_xform():
   

    def __init__(self):
        self.has = False
       
    def set(self,node):
        suffix = node[-2:]
        if(suffix!=g_right and suffix!=g_left):
            self.has = False
            return
        else:
            if(suffix==g_right):
                self.side = 0
            elif(suffix==g_left):
                self.side = 1

            self.has = True
            self.t = cmds.xform(node, q=True, t=True, r=True)
            self.ro = cmds.xform(node, q=True, ro=True, r=True)
            self.s = cmds.xform(node, q=True, s=True, r=True)

    def apply_saved(self,targ):
        suffix = targ[-2:]
        if(suffix!=g_right and suffix!=g_left):
            return
        else:
            if(suffix==g_right):
                apply_side = 0
            elif(suffix==g_left):
                apply_side = 1

            if(self.side==apply_side):
                cmds.xform(targ, t=self.t)
                cmds.xform(targ, ro=self.ro)
                cmds.xform(targ, s=self.s)


saved = saved_xform()

def mirror_node(from_,to_):

    pos = cmds.xform(from_, q=True, t=True, r=True)
    pos[1] = pos[1]*-1

    rot = cmds.xform(from_, q=True, ro=True, r=True)
    rot[0] = rot[0]*-1
    rot[2] = rot[2]*-1

    cmds.xform(to_, t=pos)
    cmds.xform(to_, ro=rot)
    cmds.xform(to_, s=cmds.xform(from_, q=True, s=True, r=True))


def mirror_control(args):
    selected = cmds.ls(sl=True) or []
    suffix = selected[0][-2:]

    if(suffix==g_left or suffix==g_right):
        name = selected[0][:-2]
        right = name+g_right
        left = name+g_left

        if(suffix==g_right):
            mirror_node(right,left)
        elif(suffix==g_left):
            mirror_node(left,right)

def save_xform(args):
    selected = cmds.ls(sl=True) or []
    saved.set(selected[0])

def load_xform(args):
    selected = cmds.ls(sl=True) or []
    saved.apply_saved(selected[0])

window = cmds.window( 
    title='Anim Assistant',  
    width=300,
    resizeToFitChildren=True) 

scrollLayout = cmds.scrollLayout(
    horizontalScrollBarThickness=16,
    verticalScrollBarThickness=16)
    
cmds.columnLayout(
    columnOffset=['left',0])
 

cmds.button( label='Mirror Control', 
             width = 100,
             command=mirror_control )
  
cmds.button( label='Save XForm', 
             width = 100,
             command=save_xform )

cmds.button( label='Load XForm', 
             width = 100,
             command=load_xform )

cmds.setParent( '..' )
                                               
cmds.showWindow( window )