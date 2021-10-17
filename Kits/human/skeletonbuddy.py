import maya.cmds as cmds
import maya.mel as mel


#dagPose -save -bindPose

import sys
sys.path.append(r'O:\one\tools\maya\common')

import skeleton_data as SKELETON_DATA
reload(SKELETON_DATA)

import chi as CHI
reload(CHI)

import select_by_udim as SELECT_BY_UDIM
reload(SELECT_BY_UDIM)

g_filepath = 'O:/one/tools/maya/data/bone_data_female.json'
g_axis_left = '_l'
g_axis_right = '_r'


def unbind():
    mel.eval('gotoBindPose')
    cmds.select('female_a_shape',r=True)
    mel.eval('doDetachSkin "2" { "2","1" }') 
    
    #cmds.bindSkin(unbindKeepHistory=True,e=True)

    

def general_command(cmd,*args):
    skel = SKELETON_DATA.skeleton_h8()
    skel.from_json(g_filepath)
    
    if(cmd=='prep_skeleton'):
        skel.process()
    elif(cmd=='flex'):
        skel.flex_muscles()
    elif(cmd=='select_all_bindable'):
        skel.select_all_bindable()    
    elif(cmd=='select_eye_bindable'):
        cmds.select('eye_shape',r=True)
        cmds.select('eye_r',add=True)
        cmds.select('eye_l',add=True)   
    elif(cmd=='select_mouth_bindable'):
        cmds.select('mouth_shape',r=True)
        cmds.select('head',add=True)
        cmds.select('jaw',add=True)
    elif(cmd=='select_tongue_bindable'):
        cmds.select('tongue_shape',r=True)
        cmds.select('tongue1',add=True)
        cmds.select('tongue2',add=True)
        cmds.select('tongue3',add=True)
        cmds.select('tongue4',add=True)
        cmds.select('tongue5',add=True)
  
def export_selected(path):
    mel.eval('FBXResetExport')
    mel.eval('FBXExportSmoothingGroups -v 1')
    mel.eval('FBXExportInputConnections -v 0')
    mel.eval('FBXExportIncludeChildren -v 0')
    mel.eval('FBXExportBakeComplexAnimation -v 1')
    mel.eval('FBXExport -f "%s" -s' % path)

def prepare_for_export(node):
    cmds.select(node,r=True)
    #mel.eval('sets -e -forceElement initialShadingGroup;')
    mel.eval('doBakeNonDefHistory( 1, {"prePost" });')    
        
def output_to_ue4(type,*args):

    skel = SKELETON_DATA.skeleton_h8()
    skel.from_json(g_filepath)
    
    filter_body_full = ['bodynoskin','bodyanim','twist','socketbone','faceanim']
    filter_body_anim = ['bodynoskin','bodyanim','twist']
    shape = 'humanfemale_shape'
    
    bChi = False

    bBodyPart = False
    designation = 'female_h0_'
    
    region = 'ERROR'
    
    if type=='head':
        faces = SELECT_BY_UDIM.faces([shape],1)   
        bBodyPart = True
        region = 'head'   
    elif type=='bust':
        faces = SELECT_BY_UDIM.faces([shape],2)   
        bBodyPart = True
        region = 'bust'
        
    elif type=='legs':
        faces = SELECT_BY_UDIM.faces([shape],3)   
        bBodyPart = True
        region = 'legs'
      
    elif type=='full':
        faces = SELECT_BY_UDIM.faces([shape],1)
        faces+= SELECT_BY_UDIM.faces([shape],2)
        faces+= SELECT_BY_UDIM.faces([shape],3)
        faces+= SELECT_BY_UDIM.faces([shape],4)
        faces+= SELECT_BY_UDIM.faces([shape],5)
        bBodyPart = True
        region = 'fullbody'
              
    if bBodyPart==True:
        SELECT_BY_UDIM.trim_and_clean(faces)
        prepare_for_export(shape)
        mesh = shape
         
    result = skel.filter_by_type(filter_body_full);
            
    if type=='bodyskeleton_full' or type=='bodyskeleton_anim':
        chi = CHI.chi_h8('hip')   
        mesh = chi.id
        bChi = True    
         
    if type=='bodyskeleton_full':
        result = skel.filter_by_type(filter_body_full);
        region = 'bodyskeleton_full'
        
    if type=='bodyskeleton_anim':
        region = 'bodyskeleton_anim'
     
    final_list = skel.list_confined_parenting(result)
    
    cmds.select(final_list , r=True)
    cmds.select(mesh, add=True)
    
    export_selected("O:/one/asset/output/"+designation+region+".fbx")
    skel.restore_all_parents()
    
    if bChi==True:
        chi.delete()
    
    

    
        
        

        

    
               
g_win_width = 350

window = cmds.window( 
    title='Rig Helper',  
    width=g_win_width,
    height=600,
    resizeToFitChildren=True) 

scrollLayout = cmds.scrollLayout(
    horizontalScrollBarThickness=16,
    verticalScrollBarThickness=16)
    
cmds.columnLayout(
    columnOffset=['left',0])
 


cmds.frameLayout(label="Draft Skeleton",width=g_win_width, collapsable=False,collapse=False)
cmds.gridLayout(numberOfColumns=1, cellWidthHeight=(g_win_width-16, 30))

cmds.text( label='Place the drafting objects, or reset the drafting objects:' , height=35 )

cmds.optionMenu( label='BodyShape')
cmds.menuItem( label='male_a (MDA)' )
cmds.menuItem( label='male_b (MDB)' )
cmds.menuItem( label='male_c (MDC)')
cmds.menuItem( label='female_a (FDA)' )
cmds.menuItem( label='female_b (FDB)' )
cmds.menuItem( label='female_c (FDC)' )
cmds.menuItem( label='female_fairy_a (FFA)' )
cmds.menuItem( label='female_draka_a (FDA)' )
cmds.menuItem( label='custom' )

cmds.button( label='Prep Skeleton', 
             width = 100,
             command=lambda x: general_command ('prep_skeleton') )


cmds.button( label='Flex Muscle', 
             width = 100,
             command=lambda x: general_command ('flex') )
             
cmds.button( label='Select All Bindable', 
             width = 100,
             command=lambda x: general_command ('select_all_bindable') )
 
cmds.button( label='Select Eye Bindable', 
             width = 100,
             command=lambda x: general_command ('select_eye_bindable') )

cmds.button( label='Select Mouth Bindable', 
             width = 100,
             command=lambda x: general_command ('select_mouth_bindable') )
            
cmds.button( label='Select Tongue Bindable', 
             width = 100,
             command=lambda x: general_command ('select_tongue_bindable') )

                          
cmds.button( label='Twists - Activate', 
             width = 100,
             command=lambda x: general_command ('twists_activate') )

cmds.button( label='Twists - Deactivate', 
             width = 100,
             command=lambda x: general_command ('twists_deactivate') )
             
          
cmds.button( label='Output: Head', 
             width = 100,
             command=lambda x: output_to_ue4('head') )
                        
cmds.button( label='Output: Bust', 
             width = 100,
             command=lambda x: output_to_ue4('bust') )
             
cmds.button( label='Output: Legs', 
             width = 100,
             command=lambda x: output_to_ue4('legs') )

cmds.button( label='Output: hands', 
             width = 100,
             command=lambda x: output_to_ue4('hands') )
             
cmds.button( label='Output: Feet', 
             width = 100,
             command=lambda x: output_to_ue4('feet') )

cmds.button( label='Output: Full', 
             width = 100,
             command=lambda x: output_to_ue4('full') )
             
cmds.button( label='Output: BodySkeleton Full', 
             width = 100,
             command=lambda x: output_to_ue4('bodyskeleton_full') )

cmds.button( label='Output: BodySkeleton Anim', 
             width = 100,
             command=lambda x: output_to_ue4('bodyskeleton_anim') )
                                                    
cmds.setParent( '..' )
                                               
cmds.showWindow( window )