import maya.cmds as cmds

def bind_twist(j,end,div):
    cmds.expression(s=j+'.rotateX='+end+'.rotateX/'+str(div))


def bind_expressions(args):
    bind_twist('upperarm_twist1_l','lowerarm_l',3)
    bind_twist('upperarm_twist2_l','lowerarm_l',2)
    bind_twist('upperarm_twist3_l','lowerarm_l',1.2)
    
    bind_twist('upperarm_twist1_r','lowerarm_r',3)
    bind_twist('upperarm_twist2_r','lowerarm_r',2)
    bind_twist('upperarm_twist3_r','lowerarm_r',1.2)

    bind_twist('lowerarm_twist1_l','hand_l',3)
    bind_twist('lowerarm_twist2_l','hand_l',2)
    bind_twist('lowerarm_twist3_l','hand_l',1.2)
    
    bind_twist('lowerarm_twist1_r','hand_r',3)
    bind_twist('lowerarm_twist2_r','hand_r',2)
    bind_twist('lowerarm_twist3_r','hand_r',1.2)

    bind_twist('thigh_twist1_l','shin_l',2)
    bind_twist('thigh_twist2_l','shin_l',1.2)

    bind_twist('shin_twist1_l','foot_l',2)
    bind_twist('shin_twist2_l','foot_l',1.2)

    bind_twist('thigh_twist1_r','shin_r',2)
    bind_twist('thigh_twist2_r','shin_r',1.2)

    bind_twist('shin_twist1_r','foot_r',2)
    bind_twist('shin_twist2_r','foot_r',1.2)


def unbind_expressions(args):

    exp = []
    exp.append('upperarm_twist1_l')
    exp.append('upperarm_twist2_l')
    exp.append('upperarm_twist3_l')
    exp.append('lowerarm_twist1_l')
    exp.append('lowerarm_twist2_l')
    exp.append('lowerarm_twist3_l')
     
    exp.append('upperarm_twist1_r')
    exp.append('upperarm_twist2_r')
    exp.append('upperarm_twist3_r')
    exp.append('lowerarm_twist1_r')
    exp.append('lowerarm_twist2_r')
    exp.append('lowerarm_twist3_r')

    exp.append('thigh_twist1_l')
    exp.append('thigh_twist2_l')
    exp.append('shin_twist1_l')
    exp.append('shin_twist2_l')

    exp.append('thigh_twist1_r')
    exp.append('thigh_twist2_r')
    exp.append('shin_twist1_r')
    exp.append('shin_twist2_r')

        
window = cmds.window( 
    title='Human Rigger',  
    width=300,
    resizeToFitChildren=True) 

scrollLayout = cmds.scrollLayout(
    horizontalScrollBarThickness=16,
    verticalScrollBarThickness=16)
    
cmds.columnLayout(
    columnOffset=['left',0])
 
cmds.button( label='Bind Expressions', 
             width = 100,
             command=bind_expressions )

cmds.button( label='Unbind Expressions', 
             width = 100,
             command=unbind_expressions )


cmds.setParent( '..' )
                                               
cmds.showWindow( window )