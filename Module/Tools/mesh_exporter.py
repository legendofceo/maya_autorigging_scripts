import maya.cmds as cmds
import maya.mel as mel

def export_mesh():
	mel.eval('doBakeNonDefHistory( 1, {"prePost" });') 
	filters = "Fbx Files (*.fbx)"
	filename = cmds.fileDialog2(ff=filters,fileMode=0, caption="Export As FBX")
	mel.eval('FBXResetExport')
	mel.eval('FBXExportSmoothingGroups -v 1')
	mel.eval('FBXExportInputConnections -v 0')
	mel.eval('FBXExportIncludeChildren -v 0')
	mel.eval('FBXExportBakeComplexAnimation -v 1')
	mel.eval('FBXExport -f "%s" -s' % filename[0])

               
def delete_unselected_faces():
    mel.eval("invertSelection;") 
    cmds.delete()

def invert_joint_selection():
	joint_list = cmds.ls(type="joint")
	selected = cmds.ls(sl=True) or []

	cmds.select(cl=True)

	for j in joint_list:
		if j not in selected:
			cmds.select(j,add=True)

def delete_selected_joints():

	selected = cmds.ls(sl=True) or []
	for s in selected:
		children = cmds.listRelatives(s,c=True)
		parent = cmds.listRelatives(s,p=True)

		if(children!=None):
			for c in children:
				cmds.parent(c,w=True)
				if(parent!=None):
					cmds.parent(c,parent)
				
		cmds.delete(s)

def add_minplane():
	
	selected = cmds.ls(sl=True) or []

	if selected[0]!=None:
		node = selected[0]
		mp = "mp"
		#cmds.polyPlane(n=mp, w=0.0001,h=0.0001)
		cmds.polyPlane(n=mp, w=2,h=2)
		cmds.matchTransform(mp,node)
    	cmds.skinCluster(mp,node, name=mp+'_scl',tsb=True)
    	mel.eval("polyNormal -normalMode 2 -userNormalMode 0 -ch 1 "+mp+";")


var_width = 300;
window = cmds.window( 
    title='Rig Helper',  
    width=var_width ,
    height=600,
    resizeToFitChildren=True) 

scrollLayout = cmds.scrollLayout(
    horizontalScrollBarThickness=16,
    verticalScrollBarThickness=16)
    
cmds.columnLayout(
    columnOffset=['left',0])

         
cmds.button( label='Export', 
             width = var_width ,
             command=lambda x: export_mesh() )

instructions = 'First remove poly faces that are not needed, then use invert joint selection to select all non included joints. Use remove influences from the Rigging|Skin menu (Remember to select the base shape), afterwards delete all the joints you removed influence from. Afterwards export using the above button.'

cmds.scrollField(ed=False, 
				wordWrap=True,
			    text=instructions,
			    width=var_width ,
			    height=180)

cmds.button( label='Delete Unselected Faces', 
             width = var_width ,
             command=lambda x: delete_unselected_faces() )

cmds.button( label='Invert Joint Selection', 
             width = var_width ,
             command=lambda x: invert_joint_selection() )

cmds.button( label='Delete Selected Joints', 
             width = var_width ,
             command=lambda x: delete_selected_joints() )

instructions = 'UE requires a mesh to to import a skeletalmesh. MinPlane is a micro minimal object to allow a mostly skeleton only export. Click a central joint and then run this.'


cmds.scrollField(ed=False, 
				wordWrap=True,
			    text=instructions,
			    width=var_width ,
			    height=100)


cmds.button( label='Add MinPlane', 
             width = var_width ,
             command=lambda x: add_minplane() )

cmds.setParent( '..' )
                                               
cmds.showWindow( window )

def onMayaDroppedPythonFile(args):
	print ("Starting Mesh_Exporter Menu")