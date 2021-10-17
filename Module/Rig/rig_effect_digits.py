import maya.cmds as cmds

import rig_gizmo as RIG_GIZMOS
reload(RIG_GIZMOS)

class new():
           
    def setup(self,joints,bends,parent,rgb):
        self.joints = joints
        self.parent = parent
        self.bends = bends
        self.rgb = rgb

        return self
                        
    def go(self):              

         index=-1
         for j in self.joints:           
            index+=1
            fing_arr = []        
            for i in range(self.bends[index]):
            
                if i==0:
                    rad = 1.8
                elif i==1:
                    rad = 1.6
                elif i==2:
                    rad = 1.4
                    
                ix = i+1
                ix_str = str(ix)

                new_name = j.replace("$", ix_str)

                c = RIG_GIZMOS.sphere("c_"+new_name,rgb=self.rgb,rad=0.4)
                c.move_control_local(0,0,2)
                fing_arr.append(c)              
                targ_joint = new_name
                c.match_to(targ_joint)  
                
                #if i!=0:
                #    c.lock_rot(True,False,True)
                    
                if i == 0:
                    c.set_parent(self.parent)
                else:
                    c.set_parent(fing_arr[i-1].id)

                cmds.orientConstraint(c.id,targ_joint,mo=True,w=1.0)     