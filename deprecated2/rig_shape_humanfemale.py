import maya.cmds as cmds
import math

import sys
sys.path.append('.')

import rig_effect_basicik as IK_BASIC
reload(IK_BASIC)

import rig_effect_digits as RIGFX_DIGITS
reload(RIGFX_DIGITS)

import rig_effect_foot as RIGFX_FOOT
reload(RIGFX_FOOT)

import rig_effect_flesh as RIGFX_FLESH
reload(RIGFX_FLESH)


import rig_effect_ikfk as RIGFX_IKFK
reload(RIGFX_IKFK)

import rig_gizmo as RIG_GIZMOS
reload(RIG_GIZMOS)


import rigutils as RIGUTILS
reload(RIGUTILS)


g_left = '_l'
g_right = '_r'

class female_rig_class():
   

    def __init__(self):



        cmds.file('O:/one/asset/archive/poly/human_female_final.mb', o=True, f=True)
        
        
        cmds.modelEditor(lineWidth=1.5 )

        rgb_id1 = [1.0,0.29,0.28]
        rgb_id2 = [0.85,0.6,0.7]
        rgb_rot1 = [0.85,0.85,0.85]
        rgb_rot2 = [0.7,0.7,0.7]

    
        joints = cmds.ls(type="joint")
        

        for j in joints:
            cmds.setAttr(j+'.segmentScaleCompensate', 0)

        uid = "fem00"

        rgb_primary = [0.8,0.06,0.03]
        softer = 4
        rgb_soft = [rgb_primary[0]/softer,rgb_primary[1]/softer,rgb_primary[2]/softer]
        shd = cmds.shadingNode('lambert', name="%s_lambert" % uid, asShader=True)
        primary_shader = cmds.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
        cmds.setAttr(shd+'.color',rgb_primary[0],rgb_primary[1],rgb_primary[2], type = 'double3')
        cmds.setAttr(shd+'.transparency',1.0,1.0,1.0, type = 'double3')
        cmds.setAttr(shd+'.ambientColor', rgb_soft[0],rgb_soft[1],rgb_soft[2], type = 'double3')
        cmds.setAttr(shd+'.incandescence',rgb_soft[0],rgb_soft[1],rgb_soft[2], type = 'double3')
        cmds.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % primary_shader)

        
        root_c = RIG_GIZMOS.pyramid_shaded('c_root',primary_shader,width=10.2,axis=[0,0,-1])
        root_c.match_to('root')
        root_c.move_control_local(0,0,-3.4,movepivot=True)
        cmds.parentConstraint(root_c.id,'root',mo=True,w=1.0)
        cmds.scaleConstraint(root_c.id,'root',mo=True,w=1.0)

        #c.move_offset_control(0,0,-2)
        #c.parent(g_group_controls)
        #c_root = c.control()


        hip_c = RIG_GIZMOS.hoop('c_hip',rgb=rgb_id1,rad=30.0,hrad=0.007,axis=[0,0,1])
        hip_c.match_to('hip')
        hip_c.set_parent(root_c.id)
        hip_c.set_space_rotation(None,None,-90)
        cmds.parentConstraint(hip_c.id,"hip",mo=True,w=1.0)
        hip_c.set_channel_enabled(True,True,False)

        pelvis_c = RIG_GIZMOS.hoop('c_pelvis',rgb=rgb_rot1,rad=25.0,hrad=0.005,axis=[1,0,0])
        pelvis_c.match_to('pelvis')
        pelvis_c.set_parent(hip_c.id)
        pelvis_c.set_space_rotation(None,-90,None)
        cmds.orientConstraint(pelvis_c.id,'pelvis',mo=True,w=1.0)
        pelvis_c.set_channel_enabled(False,True,False)

        abdomen_lower_c = RIG_GIZMOS.hoop('c_abdomen_lower',rgb=rgb_rot1,rad=20.0,hrad=0.003,axis=[1,0,0])
        abdomen_lower_c.match_to('spine1')
        abdomen_lower_c.set_parent(hip_c.id)
        abdomen_lower_c.set_space_rotation(None,-90,None)
        cmds.orientConstraint(abdomen_lower_c.id,'spine1',mo=True,w=1.0)
        cmds.orientConstraint(abdomen_lower_c.id,'spine2',mo=True,w=0.5)
        abdomen_lower_c.set_channel_enabled(False,True,False)

        abdomen_upper_c = RIG_GIZMOS.hoop('c_abdomen_upper',rgb=rgb_rot1,rad=20.0,hrad=0.003,axis=[1,0,0])
        abdomen_upper_c.match_to('spine3')
        abdomen_upper_c.set_parent(abdomen_lower_c.id)
        abdomen_upper_c.set_space_rotation(None,-90,None)
        cmds.orientConstraint(abdomen_upper_c.id,'spine3',mo=True,w=1.0)
        cmds.orientConstraint(abdomen_upper_c.id,'spine2',mo=True,w=0.5)
        cmds.orientConstraint(abdomen_upper_c.id,'spine4',mo=True,w=0.5)
        abdomen_upper_c.set_channel_enabled(False,True,False)


        chest_c = RIG_GIZMOS.hoop('c_chest',rgb=rgb_rot1,rad=12.0,hrad=0.003,axis=[1,0,0])
        chest_c.match_to('spine5')
        chest_c.set_parent(abdomen_upper_c.id)
        chest_c.set_space_rotation(None,-90,None)
        cmds.orientConstraint(chest_c.id,'spine5',mo=True,w=1.0)
        cmds.orientConstraint(chest_c.id,'spine4',mo=True,w=0.5)
        cmds.orientConstraint(chest_c.id,'neck1',mo=True,w=0.3)
        chest_c.set_channel_enabled(False,True,False)



        neck_c = RIG_GIZMOS.hoop('c_neck',rgb=rgb_rot1,rad=10.0,hrad=0.003,axis=[1,0,0])
        neck_c.match_to('neck1')
        neck_c.set_parent(chest_c.id)
        neck_c.set_space_rotation(None,-90,None)
        neck_c.move_control_local(6,0,0,movepivot=True)
        cmds.orientConstraint(neck_c.id,'neck1',mo=True,w=0.7)
        cmds.orientConstraint(neck_c.id,'neck2',mo=True,w=0.6)
        neck_c.set_channel_enabled(False,True,False)


        head_c = RIG_GIZMOS.hoop('c_head',rgb=rgb_rot1,rad=14.0,hrad=0.003,axis=[1,0,0])
        head_c.match_to('head')
        head_c.set_parent(neck_c.id)
        head_c.set_space_rotation(None,-90,None)
        head_c.move_control_local(20,0,0,movepivot=True)
        cmds.orientConstraint(head_c.id,'head',mo=True,w=1.0)
        cmds.orientConstraint(head_c.id,'neck2',mo=True,w=0.4)
        head_c.set_channel_enabled(False,True,False)

        arm_joints_r = ['upperarm_r','lowerarm_r','hand_r']
        arm_joints_fk_r = ['upperarm_fk_r','lowerarm_fk_r','hand_fk_r']
        arm_joints_ik_r =['upperarm_ik_r','lowerarm_ik_r','hand_ik_r']
        
        arm_joints_l = ['upperarm_l','lowerarm_l','hand_l']
        arm_joints_fk_l = ['upperarm_fk_l','lowerarm_fk_l','hand_fk_l']
        arm_joints_ik_l =['upperarm_ik_l','lowerarm_ik_l','hand_ik_l']
        
        RIGUTILS.copy_joint_chain(arm_joints_l,arm_joints_fk_l)
        RIGUTILS.copy_joint_chain(arm_joints_l,arm_joints_ik_l)
        
        RIGUTILS.copy_joint_chain(arm_joints_r,arm_joints_fk_r)
        RIGUTILS.copy_joint_chain(arm_joints_r,arm_joints_ik_r)

        armik_obj_l = IK_BASIC.new()
        armik_obj_l.setup(arm_joints_ik_l,'armik_handle_l','ikRPsolver').go()

        armik_obj_r = IK_BASIC.new()
        armik_obj_r.setup(arm_joints_ik_r,'armik_handle_r','ikRPsolver').go()

        #armik_l_c = RIG_GIZMOS.cube_shaded('c_handik_l',primary_shader,size=[10.0,8.0,6.0],span = [1,1,1])
        armik_l_c = RIG_GIZMOS.cube('c_handik_l',rgb_id1,size=[10.0,8.0,6.0],span = [1,1,1])
        armik_l_c.match_to(armik_obj_l.joints[2]).set_parent(root_c.id).move_control_local(5,0,0).set_channel_enabled(True,True,False)
        cmds.orientConstraint(armik_l_c.id,armik_obj_l.joints[2],mo=True,w=1.0)
        cmds.parent(armik_obj_l.handle,armik_l_c.id)


        armik_r_c = RIG_GIZMOS.cube('c_handik_r',rgb_id1,size=[10.0,8.0,6.0],span = [1,1,1])
        armik_r_c.match_to(armik_obj_r.joints[2]).set_parent(root_c.id).move_control_local(5,0,0).set_channel_enabled(True,True,False)
        cmds.orientConstraint(armik_r_c.id,armik_obj_r.joints[2],mo=True,w=1.0)
        cmds.parent(armik_obj_r.handle,armik_r_c.id)


        elbowik_l_c = RIG_GIZMOS.sphere('c_elbowik_l',rgb=rgb_id1,rad=3.0)
        elbowik_l_c.match_to(armik_obj_l.joints[1])
        elbowik_l_c.set_parent(chest_c.id)
        cmds.poleVectorConstraint(elbowik_l_c.id,armik_obj_l.handle)
        elbowik_l_c.set_space_rotation(0,0,0)
        elbowik_l_c.move_control_local(0,62,0,movepivot=True)
        elbowik_l_c.set_channel_enabled(True,False,False)
        

        elbowik_r_c = RIG_GIZMOS.sphere('c_elbowik_r',rgb=rgb_id1,rad=3.0)
        elbowik_r_c.match_to(armik_obj_r.joints[1])
        elbowik_r_c.set_parent(chest_c.id)
        cmds.poleVectorConstraint(elbowik_r_c.id,armik_obj_r.handle)
        elbowik_r_c.set_space_rotation(0,0,-180)
        elbowik_r_c.move_control_local(0,-62,0,movepivot=True)
        elbowik_r_c.set_channel_enabled(True,False,False)

        clavicle_r_c = RIG_GIZMOS.hoop('c_clavicle_r',rgb=rgb_rot1,rad=9.5,hrad=0.05,axis=[1,0,0],ssw=330-180,esw=390-180)
        clavicle_r_c.match_to('clavicle_r').set_parent('spine5').set_channel_enabled(False,True,False)
        cmds.orientConstraint(clavicle_r_c.id,'clavicle_r',mo=True,w=1.0)
       
        upperarm_r_c = RIG_GIZMOS.hoop('c_upperarm_r',rgb=rgb_rot1,rad=9.5,hrad=0.05,axis=[1,0,0],ssw=320-180,esw=380-180)
        upperarm_r_c.match_to(arm_joints_fk_r[0]).set_parent(clavicle_r_c.id).set_channel_enabled(False,True,False)
        cmds.orientConstraint(upperarm_r_c.id,arm_joints_fk_r[0],mo=True,w=1.0)

        lowerarm_r_c = RIG_GIZMOS.hoop('c_lowerarm_r',rgb=rgb_rot1,rad=6.5,hrad=0.05,axis=[1,0,0])
        lowerarm_r_c.match_to(arm_joints_fk_r[1]).set_parent(upperarm_r_c.id).set_channel_enabled(False,True,False)
        cmds.orientConstraint(lowerarm_r_c.id,arm_joints_fk_r[1],mo=True,w=1.0)

        hand_r_c = RIG_GIZMOS.hoop('c_hand_r',rgb=rgb_rot1,rad=5.0,hrad=0.05,axis=[1,0,0])
        hand_r_c.match_to(arm_joints_fk_r[2]).set_parent(lowerarm_r_c.id).set_channel_enabled(False,True,False)
        cmds.orientConstraint(hand_r_c.id,arm_joints_fk_r[2],mo=True,w=1.0)

        clavicle_l_c = RIG_GIZMOS.hoop('c_clavicle_l',rgb=rgb_rot1,rad=9.5,hrad=0.05,axis=[1,0,0],ssw=330-180,esw=390-180)
        clavicle_l_c.match_to('clavicle_l').set_parent('spine5').set_channel_enabled(False,True,False)
        cmds.orientConstraint(clavicle_l_c.id,'clavicle_l',mo=True,w=1.0)

        upperarm_l_c = RIG_GIZMOS.hoop('c_upperarm_l',rgb=rgb_rot1,rad=9.5,hrad=0.05,axis=[1,0,0],ssw=320-180,esw=380-180)
        upperarm_l_c.match_to(arm_joints_fk_l[0]).set_parent(clavicle_l_c.id).set_channel_enabled(False,True,False)
        cmds.orientConstraint(upperarm_l_c.id,arm_joints_fk_l[0],mo=True,w=1.0)

        lowerarm_l_c = RIG_GIZMOS.hoop('c_lowerarm_l',rgb=rgb_rot1,rad=6.5,hrad=0.05,axis=[1,0,0])
        lowerarm_l_c.match_to(arm_joints_fk_l[1]).set_parent(upperarm_l_c.id).set_channel_enabled(False,True,False)
        cmds.orientConstraint(lowerarm_l_c.id,arm_joints_fk_l[1],mo=True,w=1.0)

        hand_l_c = RIG_GIZMOS.hoop('c_hand_l',rgb=rgb_rot1,rad=5.0,hrad=0.05,axis=[1,0,0])
        hand_l_c.match_to(arm_joints_fk_l[2]).set_parent(lowerarm_l_c.id).set_channel_enabled(False,True,False)
        cmds.orientConstraint(hand_l_c.id,arm_joints_fk_l[2],mo=True,w=1.0)

        arm_hub_r_c = RIG_GIZMOS.pyramid('c_armhub_r',rgb=rgb_rot1,width=3,axis=[0,0,1])
        arm_hub_r_c.match_to(arm_joints_r[2]).set_parent(arm_joints_r[2]).move_control_local(5,0,6,movepivot=True).set_channel_enabled(False,False,False)

        arm_hub_l_c = RIG_GIZMOS.pyramid('c_armhub_l',rgb=rgb_rot1,width=3,axis=[0,0,1])
        arm_hub_l_c.match_to(arm_joints_l[2]).set_parent(arm_joints_l[2]).move_control_local(5,0,6,movepivot=True).set_channel_enabled(False,False,False)


        arm_ikfk_r = RIGFX_IKFK.new()
        arm_ikfk_r.go(arm_hub_r_c.id, arm_joints_r, arm_joints_fk_r, arm_joints_ik_r, [upperarm_r_c.id,lowerarm_r_c.id,hand_r_c.id], [armik_r_c.id,elbowik_r_c.id])

        arm_ikfk_l = RIGFX_IKFK.new()
        arm_ikfk_l.go(arm_hub_l_c.id, arm_joints_l, arm_joints_fk_l, arm_joints_ik_l, [upperarm_l_c.id,lowerarm_l_c.id,hand_l_c.id], [armik_l_c.id,elbowik_l_c.id])

        fingers_r = RIGFX_DIGITS.new();
        fingers_r.setup(['finger_thumb$_r','finger_index$_r','finger_middle$_r','finger_ring$_r','finger_pinky$_r'],[3,3,3,3,3],'hand_r',rgb_rot2).go()

        fingers_l = RIGFX_DIGITS.new();
        fingers_l.setup(['finger_thumb$_l','finger_index$_l','finger_middle$_l','finger_ring$_l','finger_pinky$_l'],[3,3,3,3,3],'hand_l',rgb_rot2).go()



        leg_joints_r = ['thigh_r','shin_r','foot_r','ball_r','toetip_r']
        leg_joints_fk_r = ['thigh_fk_r','shin_fk_r','foot_fk_r','ball_fk_r','toetip_fk_r']
        leg_joints_ik_r =['thigh_ik_r','shin_ik_r','foot_ik_r','ball_ik_r','toetip_ik_r']

        leg_joints_l = ['thigh_l','shin_l','foot_l','ball_l','toetip_l']
        leg_joints_fk_l = ['thigh_fk_l','shin_fk_l','foot_fk_l','ball_fk_l','toetip_fk_l']
        leg_joints_ik_l =['thigh_ik_l','shin_ik_l','foot_ik_l','ball_ik_l','toetip_ik_l']

        
        RIGUTILS.copy_joint_chain(leg_joints_l,leg_joints_fk_l)
        RIGUTILS.copy_joint_chain(leg_joints_l,leg_joints_ik_l)
        
        RIGUTILS.copy_joint_chain(leg_joints_r,leg_joints_fk_r)
        RIGUTILS.copy_joint_chain(leg_joints_r,leg_joints_ik_r)

        leg_ik_l = IK_BASIC.new()
        leg_ik_l.setup(leg_joints_ik_l,'legik_handle_l','ikRPsolver').go()

        leg_ik_r = IK_BASIC.new()
        leg_ik_r.setup(leg_joints_ik_r,'legik_handle_r','ikRPsolver').go()

        legik_l_c = RIG_GIZMOS.cube('c_legik_l',rgb_id1,size=[4.0,16.0,16.0],span = [1,1,1])
        legik_l_c.match_to(leg_ik_l.joints[2])
        legik_l_c.set_parent(root_c.id)
        legik_l_c.move_control_local(6,0,0,movepivot=True)
        cmds.orientConstraint(legik_l_c.id,leg_ik_l.joints[2],mo=True,w=1.0)
        cmds.parent(leg_ik_l.handle,legik_l_c.id)

        legik_r_c = RIG_GIZMOS.cube('c_legik_r',rgb_id1,size=[4.0,16.0,16.0],span = [1,1,1])
        legik_r_c.match_to(leg_ik_r.joints[2])
        legik_r_c.set_parent(root_c.id)
        legik_r_c.move_control_local(6,0,0,movepivot=True)
        cmds.orientConstraint(legik_r_c.id,leg_ik_r.joints[2],mo=True,w=1.0)
        cmds.parent(leg_ik_r.handle,legik_r_c.id)


        kneeik_l_c = RIG_GIZMOS.sphere_shaded('c_kneeik_l',primary_shader,rad=3.0)
        kneeik_l_c.match_to(leg_ik_l.joints[1])
        kneeik_l_c.set_parent(hip_c.id)
        kneeik_l_c.set_space_rotation(0,0,0)
        kneeik_l_c.move_control_local(0,-62,0,movepivot=True)
        cmds.poleVectorConstraint(kneeik_l_c.id,leg_ik_l.handle)

        kneeik_r_c = RIG_GIZMOS.sphere_shaded('c_kneeik_r',primary_shader,rad=3.0)
        kneeik_r_c.match_to(leg_ik_r.joints[1])
        kneeik_r_c.set_parent(hip_c.id)
        kneeik_r_c.set_space_rotation(0,0,-180)
        kneeik_r_c.move_control_local(0,62,0,movepivot=True)
        cmds.poleVectorConstraint(kneeik_r_c.id,leg_ik_r.handle)

        foot_ik_r = RIGFX_FOOT.new()
        foot_ik_r.go(['foot_ik_r','ball_ik_r','toetip_ik_r'],'footik_handle_r','toeik_handle_r','foot_helper_toebase_r','foot_helper_toe_r','foot_helper_ball_r','foot_helper_wiggle_r',legik_r_c.id,leg_ik_r.handle)

        toepoint_r_c = RIG_GIZMOS.cylinder('c_toepoint_r',rgb_id2,rad=0.8,height=2.0,sx=4)
        toepoint_r_c.match_to(legik_r_c.id)
        toepoint_r_c.set_parent(legik_r_c.id)
        toepoint_r_c.move_control_local(0,-10,-9,movepivot=True)
        toepoint_r_c.set_channel_enabled(False,True,False).set_channel_rotation_enabled(False,True,False)
        cmds.expression(s=foot_ik_r.helper_wiggle+'.rotateY = '+toepoint_r_c.id+'.rotateY' )  
        cmds.transformLimits(toepoint_r_c.id, rx=(0, 0), ry=(0, 0), rz=(0, 0), erx=(True, True), ery=(False, False), erz=(True, True ))

        tiptoe_r_c = RIG_GIZMOS.cylinder('c_tiptoe_r',rgb_id2,rad=0.8,height=2.0,sx=4)
        tiptoe_r_c.match_to(legik_r_c.id)
        tiptoe_r_c.set_parent(legik_r_c.id)
        tiptoe_r_c.move_control_local(0,-10,-11,movepivot=True)
        tiptoe_r_c.set_channel_enabled(False,True,False).set_channel_rotation_enabled(False,True,False)
        cmds.expression(s=foot_ik_r.helper_ball+'.rotateY = '+tiptoe_r_c.id+'.rotateY' )
        cmds.transformLimits(tiptoe_r_c.id, rx=(0, 0), ry=(0, 70), rz=(0, 0), erx=(True, True), ery=(True, True), erz=(True, True ))

        toesquash_r_c = RIG_GIZMOS.cylinder('c_toesquash_r',rgb_id2,axis=[1,0,0],rad=0.8,height=2.0,sx=4)
        toesquash_r_c.match_to(legik_r_c.id)
        toesquash_r_c.set_parent(legik_r_c.id)
        toesquash_r_c.move_control_local(0,-10,-7,movepivot=True)
        toesquash_r_c.set_channel_enabled(False,True,False).set_channel_rotation_enabled(True,False,False)
        cmds.expression(s=foot_ik_r.helper_toe+'.rotateZ = '+toesquash_r_c.id+'.rotateX*-1' )
        cmds.transformLimits(toesquash_r_c.id, rx=(0, 0), ry=(0, 0), rz=(0, 0), erx=(False, False), ery=(True, True), erz=(True, True))

        foot_ik_l = RIGFX_FOOT.new()
        foot_ik_l.go(['foot_ik_l','ball_ik_l','toetip_ik_l'],'footik_handle_l','toeik_handle_l','foot_helper_toebase_l','foot_helper_toe_l','foot_helper_ball_l','foot_helper_wiggle_l',legik_l_c.id,leg_ik_l.handle)

        toepoint_l_c = RIG_GIZMOS.cylinder('c_toepoint_l',rgb_id2,rad=0.8,height=2.0,sx=4)
        toepoint_l_c.match_to(legik_l_c.id)
        toepoint_l_c.set_parent(legik_l_c.id)
        toepoint_l_c.move_control_local(0,10,-9,movepivot=True)
        toepoint_l_c.set_channel_enabled(False,True,False).set_channel_rotation_enabled(False,True,False)
        cmds.expression(s=foot_ik_l.helper_wiggle+'.rotateY = '+toepoint_l_c.id+'.rotateY' )  
        cmds.transformLimits(toepoint_l_c.id, rx=(0, 0), ry=(0, 0), rz=(0, 0), erx=(True, True), ery=(False, False), erz=(True, True ))

        tiptoe_l_c = RIG_GIZMOS.cylinder('c_tiptoe_l',rgb_id2,rad=0.8,height=2.0,sx=4)
        tiptoe_l_c.match_to(legik_l_c.id)
        tiptoe_l_c.set_parent(legik_l_c.id)
        tiptoe_l_c.move_control_local(0,10,-11,movepivot=True)
        tiptoe_l_c.set_channel_enabled(False,True,False).set_channel_rotation_enabled(False,True,False)
        cmds.expression(s=foot_ik_l.helper_ball+'.rotateY = '+tiptoe_l_c.id+'.rotateY' )
        cmds.transformLimits(tiptoe_l_c.id, rx=(0, 0), ry=(0, 70), rz=(0, 0), erx=(True, True), ery=(True, True), erz=(True, True ))

        toesquash_l_c = RIG_GIZMOS.cylinder('c_toesquash_l',rgb_id2,axis=[1,0,0],rad=0.8,height=2.0,sx=4)
        toesquash_l_c.match_to(legik_l_c.id)
        toesquash_l_c.set_parent(legik_l_c.id)
        toesquash_l_c.move_control_local(0,10,-7,movepivot=True)
        toesquash_l_c.set_channel_enabled(False,True,False).set_channel_rotation_enabled(True,False,False)
        cmds.expression(s=foot_ik_l.helper_toe+'.rotateZ = '+toesquash_l_c.id+'.rotateX*-1' )
        cmds.transformLimits(toesquash_l_c.id, rx=(0, 0), ry=(0, 0), rz=(0, 0), erx=(False, False), ery=(True, True), erz=(True, True))


        thigh_r_c = RIG_GIZMOS.hoop('c_thigh_r',rgb=rgb_rot1,rad=14.0,hrad=0.01,axis=[1,0,0],spans=6,ssw=270,esw=360)       
        thigh_r_c.match_to(leg_joints_r[0]).set_parent('pelvis')
        thigh_r_c.set_channel_enabled(False,True,False)
        cmds.orientConstraint(thigh_r_c.id,leg_joints_fk_r[0],mo=True,w=1.0)

        shin_r_c = RIG_GIZMOS.hoop('c_shin_r',rgb=rgb_rot1,rad= 6.5,hrad=0.01,axis=[1,0,0],spans=12,ssw=300,esw=400)       
        shin_r_c.match_to(leg_joints_fk_r[1])
        shin_r_c.set_parent(thigh_r_c.id)
        shin_r_c.set_channel_enabled(False,True,False)
        cmds.orientConstraint(shin_r_c.id,leg_joints_fk_r[1],mo=True,w=1.0)

        foot_r_c = RIG_GIZMOS.hoop('c_foot_r',rgb=rgb_rot1,rad=6.25,hrad=0.005,axis=[1,0,0],spans=12,ssw=360,esw=0)       
        foot_r_c.match_to(leg_joints_fk_r[2])
        foot_r_c.set_parent(shin_r_c.id)
        foot_r_c.set_channel_enabled(False,True,False)
        cmds.orientConstraint(foot_r_c.id,leg_joints_fk_r[2],mo=True,w=1.0)
        
        toe_r_c = RIG_GIZMOS.hoop('c_toe_r',rgb=rgb_rot1,rad=4.0,hrad=0.01,axis=[1,0,0],spans=6,ssw=130,esw=220)       
        toe_r_c.match_to(leg_joints_fk_r[3])
        toe_r_c.set_parent(foot_r_c.id)
        toe_r_c.set_channel_enabled(False,True,False)
        cmds.orientConstraint(toe_r_c.id,leg_joints_fk_r[3],mo=True,w=1.0)

        thigh_l_c = RIG_GIZMOS.hoop('c_thigh_l',rgb=rgb_rot1,rad=14.0,hrad=0.01,axis=[-1,0,0],spans=6,ssw=90,esw=180)      
        thigh_l_c.match_to(leg_joints_l[0]).set_parent('pelvis')
        thigh_l_c.set_channel_enabled(False,True,False)
        cmds.orientConstraint(thigh_l_c.id,leg_joints_fk_l[0],mo=True,w=1.0)

        shin_l_c = RIG_GIZMOS.hoop('c_shin_l',rgb=rgb_rot1,rad=6.5,hrad=0.01,axis=[1,0,0],spans=12,ssw=300,esw=400)       
        shin_l_c.match_to(leg_joints_fk_l[1])
        shin_l_c.set_parent(thigh_l_c.id)
        shin_l_c.set_channel_enabled(False,True,False)
        cmds.orientConstraint(shin_l_c.id,leg_joints_fk_l[1],mo=True,w=1.0)

        foot_l_c = RIG_GIZMOS.hoop('c_foot_l',rgb=rgb_rot1,rad=6.25,hrad=0.005,axis=[1,0,0],spans=12,ssw=360-180,esw=0-180)       
        foot_l_c.match_to(leg_joints_fk_l[2])
        foot_l_c.set_parent(shin_l_c.id)
        foot_l_c.set_channel_enabled(False,True,False)
        cmds.orientConstraint(foot_l_c.id,leg_joints_fk_l[2],mo=True,w=1.0)
        
        toe_l_c = RIG_GIZMOS.hoop('c_toe_l',rgb=rgb_rot1,rad=4.0,hrad=0.01,axis=[1,0,0],spans=6,ssw=130,esw=220)       
        toe_l_c.match_to(leg_joints_fk_l[3])
        toe_l_c.set_parent(foot_l_c.id)
        toe_l_c.set_channel_enabled(False,True,False)
        cmds.orientConstraint(toe_l_c.id,leg_joints_fk_l[3],mo=True,w=1.0)


        leg_hub_r_c = RIG_GIZMOS.pyramid('c_leghub_r',rgb=rgb_rot1,width=3,axis=[0,0,-1])
        leg_hub_r_c.match_to(leg_joints_r[2])
        leg_hub_r_c.set_parent(leg_joints_r[2])
        leg_hub_r_c.move_control_local(-4,0,-12,movepivot=True)
        leg_hub_r_c.set_channel_enabled(False,False,False)

        leg_hub_l_c = RIG_GIZMOS.pyramid('c_leghub_l',rgb=rgb_rot1,width=3,axis=[0,0,-1])
        leg_hub_l_c.match_to(leg_joints_l[2])
        leg_hub_l_c.set_parent(leg_joints_l[2])
        leg_hub_l_c.move_control_local(-4,0,-12,movepivot=True)
        leg_hub_l_c.set_channel_enabled(False,False,False)

        leg_ikfk_r = RIGFX_IKFK.new()
        leg_ikfk_r.go(leg_hub_r_c.id, leg_joints_r, leg_joints_fk_r, leg_joints_ik_r, [thigh_r_c.id,shin_r_c.id,foot_r_c.id], [legik_r_c.id,kneeik_r_c.id])

        leg_ikfk_l = RIGFX_IKFK.new()
        leg_ikfk_l.go(leg_hub_l_c.id, leg_joints_l, leg_joints_fk_l, leg_joints_ik_l, [thigh_l_c.id,shin_l_c.id,foot_l_c.id], [legik_l_c.id,kneeik_l_c.id])

        toes_r = RIGFX_DIGITS.new();
        toes_r.setup(['toe_big$_r','toe_long$_r','toe_middle$_r','toe_ring$_r','toe_little$_r'],[2,2,2,2,2],'ball_r',rgb_rot2).go()

        toes_l = RIGFX_DIGITS.new();
        toes_l.setup(['toe_big$_l','toe_long$_l','toe_middle$_l','toe_ring$_l','toe_little$_l'],[2,2,2,2,2],'ball_l',rgb_rot2).go()

        belly_c = RIG_GIZMOS.hoop('c_belly',rgb=rgb_id2,rad=1.6,hrad=0.3,axis=[1,0,0],spans=2).match_to('belly').set_parent('spine1').move_control_local(11,0,0,movepivot=True).constraint('belly',True,True,True)
        pooch_c = RIG_GIZMOS.hoop('c_pooch',rgb=rgb_id2,rad=0.6,hrad=0.3,axis=[1,0,0],spans=2).match_to('pooch').set_parent('belly').move_control_local(7.5,0,0,movepivot=True).constraint('pooch',True,True,True)


        ab_r_c = RIG_GIZMOS.hoop('c_ab_r',rgb=rgb_id2,rad=0.9,hrad=0.3,axis=[1,0,0],spans=4,sections=4,degree=1).match_to('ab_r').set_parent('spine2').move_control_local(6.5,0,0,movepivot=True).constraint('ab_r',True,True,True)
        ab_l_c = RIG_GIZMOS.hoop('c_ab_l',rgb=rgb_id2,rad=0.9,hrad=0.3,axis=[1,0,0],spans=4,sections=4,degree=1).match_to('ab_l').set_parent('spine2').move_control_local(6.5,0,0,movepivot=True).constraint('ab_l',True,True,True)

        flub_r_c = RIG_GIZMOS.hoop('c_flub_r',rgb=rgb_id2,rad=0.7,hrad=0.2,axis=[1,0,0],spans=2,sections=8,degree=1).match_to('flub_r').set_parent('spine2').move_control_local(7,0,0,movepivot=True).constraint('flub_r',True,True,True)
        flub_l_c = RIG_GIZMOS.hoop('c_flub_l',rgb=rgb_id2,rad=0.7,hrad=0.2,axis=[1,0,0],spans=2,sections=8,degree=1).match_to('flub_l').set_parent('spine2').move_control_local(7,0,0,movepivot=True).constraint('flub_l',True,True,True)

        spinae_r_c = RIG_GIZMOS.hoop('c_spinae_r',rgb=rgb_id2,rad=0.7,hrad=0.4,axis=[1,0,0],spans=4,sections=4,degree=1).match_to('spinae_r').set_parent('spine1').move_control_local(7,0,0,movepivot=True).constraint('spinae_r',True,True,True)
        spinae_l_c = RIG_GIZMOS.hoop('c_spinae_l',rgb=rgb_id2,rad=0.7,hrad=0.4,axis=[1,0,0],spans=4,sections=4,degree=1).match_to('spinae_l').set_parent('spine1').move_control_local(7,0,0,movepivot=True).constraint('spinae_l',True,True,True)

        scapula_r_c = RIG_GIZMOS.hoop('c_scapula_r',rgb=rgb_id2,rad=0.7,hrad=0.4,axis=[1,0,0],spans=4,sections=4,degree=1).match_to('scapula_r').set_parent('spine5').move_control_local(10,0,0,movepivot=True).constraint('scapula_r',True,True,True)
        scapula_l_c = RIG_GIZMOS.hoop('c_scapula_l',rgb=rgb_id2,rad=0.7,hrad=0.4,axis=[1,0,0],spans=4,sections=4,degree=1).match_to('scapula_l').set_parent('spine5').move_control_local(10,0,0,movepivot=True).constraint('scapula_l',True,True,True)

        trap_r_c = RIG_GIZMOS.hoop('c_trap_r',rgb=rgb_id2,rad=0.7,hrad=0.4,axis=[1,0,0],spans=4,sections=4,degree=1).match_to('trap_r').set_parent('neck1').move_control_local(10,0,0,movepivot=True).constraint('trap_r',True,True,True)
        trap_l_c = RIG_GIZMOS.hoop('c_trap_l',rgb=rgb_id2,rad=0.7,hrad=0.4,axis=[1,0,0],spans=4,sections=4,degree=1).match_to('trap_l').set_parent('neck1').move_control_local(10,0,0,movepivot=True).constraint('trap_l',True,True,True)

        breast_r_c = RIG_GIZMOS.hoop('c_breast_r',rgb=rgb_id2,rad=1.4,hrad=0.2,axis=[1,0,0],spans=2,sections=3,degree=1).match_to('breast_r').set_parent('spine4').move_control_local(10,0,0,movepivot=True).constraint('breast_r',True,True,True)
        breast_l_c = RIG_GIZMOS.hoop('c_breast_l',rgb=rgb_id2,rad=1.4,hrad=0.2,axis=[1,0,0],spans=2,sections=3,degree=1).match_to('breast_l').set_parent('spine4').move_control_local(10,0,0,movepivot=True).constraint('breast_l',True,True,True)

        nip_r_c = RIG_GIZMOS.hoop('c_nip_r',rgb=rgb_id2,rad=0.7,hrad=0.1,axis=[1,0,0],spans=2).match_to('nip_r').set_parent('breast_r').move_control_local(5,0,0,movepivot=True).constraint('nip_r',True,True,True)
        nip_l_c = RIG_GIZMOS.hoop('c_nip_l',rgb=rgb_id2,rad=0.7,hrad=0.1,axis=[1,0,0],spans=2).match_to('nip_l').set_parent('breast_l').move_control_local(5,0,0,movepivot=True).constraint('nip_l',True,True,True)

        cup_r_c = RIG_GIZMOS.hoop('c_cup_r',rgb=rgb_id2,rad=0.7,hrad=0.1,axis=[1,0,0],spans=2,sections=4,degree=1).match_to('cup_r').set_parent('breast_r').move_control_local(8,0,0,movepivot=True).constraint('cup_r',True,True,True)
        cup_l_c = RIG_GIZMOS.hoop('c_cup_l',rgb=rgb_id2,rad=0.7,hrad=0.1,axis=[1,0,0],spans=2,sections=4,degree=1).match_to('cup_l').set_parent('breast_l').move_control_local(8,0,0,movepivot=True).constraint('cup_l',True,True,True)

        pit_fatfx_r = RIGFX_FLESH.fatty_area().go('pit_r','clavicle_r','pit_helper_r','pit_piv_r','pit_goal_r',0.5)
        pit_r_c = RIG_GIZMOS.hoop('c_pit_r',rgb=rgb_id2,rad=0.7,hrad=0.1,axis=[1,0,0],spans=2,sections=4,degree=1).match_to(pit_fatfx_r.goal).set_parent(pit_fatfx_r.piv).move_control_local(0,0,15,movepivot=True).constraint(pit_fatfx_r.goal,True,True,True)
        RIGUTILS.constraint(pit_fatfx_r.goal,'pit_r',True,True,True)
        pit_fatfx_l = RIGFX_FLESH.fatty_area().go('pit_l','clavicle_l','pit_helper_l','pit_piv_l','pit_goal_l',0.5)
        pit_l_c = RIG_GIZMOS.hoop('c_pit_l',rgb=rgb_id2,rad=0.7,hrad=0.1,axis=[1,0,0],spans=2,sections=4,degree=1).match_to(pit_fatfx_l.goal).set_parent(pit_fatfx_l.piv).move_control_local(0,0,15,movepivot=True).constraint(pit_fatfx_l.goal,True,True,True)
        RIGUTILS.constraint(pit_fatfx_l.goal,'pit_l',True,True,True)

        bicep_r_c = RIG_GIZMOS.hoop('c_bicep_r',rgb=rgb_id2,rad=1.1,hrad=0.002,axis=[1,0,0],spans=2).match_to('bicep_r').set_parent('upperarm_twist2_r').move_control_local(5,0,0,movepivot=True).constraint('bicep_r',True,True,True)
        h = 'bicep_autoflex_r'
        bicep_r_c.create_subspace_switch(h,'bicep_goal_r','autoflex','Autoflex').add_additive()
        cmds.addAttr(bicep_r_c.id, ln='flex_multiplierX',nn='FlexMultiplierX', keyable=True, r=True, hidden=False, dv=0.003, min=0.0, max=100.0) 
        cmds.addAttr(bicep_r_c.id, ln='flex_multiplierY',nn='FlexMultiplierY', keyable=True, r=True, hidden=False, dv=0.003, min=0.0, max=100.0) 
        cmds.addAttr(bicep_r_c.id, ln='flex_multiplierZ',nn='FlexMultiplierZ', keyable=True, r=True, hidden=False, dv=0.003, min=0.0, max=100.0) 
        cmds.expression(s=h+'.scaleX = 1.0 + lowerarm_r.rotateZ*'+bicep_r_c.id+".flex_multiplierX")
        cmds.expression(s=h+'.scaleY = 1.0 + lowerarm_r.rotateZ*'+bicep_r_c.id+".flex_multiplierY")
        cmds.expression(s=h+'.scaleZ = 1.0 + lowerarm_r.rotateZ*'+bicep_r_c.id+".flex_multiplierZ")

        bicep_l_c = RIG_GIZMOS.hoop('c_bicep_l',rgb=rgb_id2,rad=1.1,hrad=0.002,axis=[1,0,0],spans=2).match_to('bicep_l').set_parent('upperarm_twist2_l').move_control_local(5,0,0,movepivot=True).constraint('bicep_l',True,True,True)
        h = 'bicep_autoflex_l'
        bicep_l_c.create_subspace_switch(h,'bicep_goal_l','autoflex','Autoflex').add_additive()
        cmds.addAttr(bicep_l_c.id, ln='flex_multiplierX',nn='FlexMultiplierX', keyable=True, r=True, hidden=False, dv=0.003, min=0.0, max=100.0) 
        cmds.addAttr(bicep_l_c.id, ln='flex_multiplierY',nn='FlexMultiplierY', keyable=True, r=True, hidden=False, dv=0.003, min=0.0, max=100.0) 
        cmds.addAttr(bicep_l_c.id, ln='flex_multiplierZ',nn='FlexMultiplierZ', keyable=True, r=True, hidden=False, dv=0.003, min=0.0, max=100.0) 
        cmds.expression(s=h+'.scaleX = 1.0 + (lowerarm_l.rotateZ*-1)*'+bicep_l_c.id+".flex_multiplierX")
        cmds.expression(s=h+'.scaleY = 1.0 + (lowerarm_l.rotateZ*-1)*'+bicep_l_c.id+".flex_multiplierY")
        cmds.expression(s=h+'.scaleZ = 1.0 + (lowerarm_l.rotateZ*-1)*'+bicep_l_c.id+".flex_multiplierZ")

        tricep_r_c = RIG_GIZMOS.hoop('c_tricep_r',rgb=rgb_id2,rad=1.1,hrad=0.002,axis=[1,0,0],spans=2).match_to('tricep_r').set_parent('upperarm_twist2_r').move_control_local(5,0,0,movepivot=True).constraint('tricep_r',True,True,True)
        h = 'tricep_autoflex_r'
        tricep_r_c.create_subspace_switch(h,'tricep_goal_r','autoflex','Autoflex').add_additive()
        cmds.addAttr(tricep_r_c.id, ln='flex_multiplierX',nn='FlexMultiplierX', keyable=True, r=True, hidden=False, dv=0.005, min=0.0, max=100.0)
        cmds.addAttr(tricep_r_c.id, ln='flex_multiplierY',nn='FlexMultiplierY', keyable=True, r=True, hidden=False, dv=0.005, min=0.0, max=100.0) 
        cmds.addAttr(tricep_r_c.id, ln='flex_multiplierZ',nn='FlexMultiplierZ', keyable=True, r=True, hidden=False, dv=0.005, min=0.0, max=100.0)
        cmds.expression(s=h+'.scaleX = 1.0+(120 - lowerarm_r.rotateZ)*'+tricep_r_c.id+".flex_multiplierX")
        cmds.expression(s=h+'.scaleY = 1.0+(120 - lowerarm_r.rotateZ)*'+tricep_r_c.id+".flex_multiplierY")
        cmds.expression(s=h+'.scaleZ = 1.0+(120 - lowerarm_r.rotateZ)*'+tricep_r_c.id+".flex_multiplierZ")

        tricep_l_c = RIG_GIZMOS.hoop('c_tricep_l',rgb=rgb_id2,rad=1.1,hrad=0.002,axis=[1,0,0],spans=2).match_to('tricep_l').set_parent('upperarm_twist2_l').move_control_local(5,0,0,movepivot=True).constraint('tricep_l',True,True,True)
        h = 'tricep_autoflex_l'
        tricep_l_c.create_subspace_switch(h,'tricep_goal_l','autoflex','Autoflex').add_additive()
        cmds.addAttr(tricep_l_c.id, ln='flex_multiplierX',nn='FlexMultiplierX', keyable=True, r=True, hidden=False, dv=0.005, min=0.0, max=100.0)
        cmds.addAttr(tricep_l_c.id, ln='flex_multiplierY',nn='FlexMultiplierY', keyable=True, r=True, hidden=False, dv=0.005, min=0.0, max=100.0)
        cmds.addAttr(tricep_l_c.id, ln='flex_multiplierZ',nn='FlexMultiplierZ', keyable=True, r=True, hidden=False, dv=0.005, min=0.0, max=100.0) 
        cmds.expression(s=h+'.scaleX = 1.0+(120 - (lowerarm_l.rotateZ*-1))*'+tricep_l_c.id+".flex_multiplierX")
        cmds.expression(s=h+'.scaleY = 1.0+(120 - (lowerarm_l.rotateZ*-1))*'+tricep_l_c.id+".flex_multiplierY")
        cmds.expression(s=h+'.scaleZ = 1.0+(120 - (lowerarm_l.rotateZ*-1))*'+tricep_l_c.id+".flex_multiplierZ")


        brach_r_c = RIG_GIZMOS.hoop('c_brach_r',rgb=rgb_id2,rad=1.1,hrad=0.002,axis=[1,0,0],spans=2).match_to('brach_r').set_parent('lowerarm_twist1_r').move_control_local(5,0,0,movepivot=True).constraint('brach_r',True,True,True)
        brach_l_c = RIG_GIZMOS.hoop('c_brach_l',rgb=rgb_id2,rad=1.1,hrad=0.002,axis=[1,0,0],spans=2).match_to('brach_l').set_parent('lowerarm_twist1_l').move_control_local(5,0,0,movepivot=True).constraint('brach_l',True,True,True)


        glute_fatfx_r = RIGFX_FLESH.fatty_area().go('glute_r','thigh_r','glute_helper_r','glute_piv_r','glute_goal_r',0.5)
        glute_r_c = RIG_GIZMOS.hoop('c_glute_r',rgb=rgb_id2,rad=1.3,hrad=0.4,axis=[1,0,0],spans=4,sections=3,degree=1).match_to(glute_fatfx_r.goal).set_parent(glute_fatfx_r.piv).set_space_rotation(10,0,90).move_control_local(14,4,-2,movepivot=True).constraint(glute_fatfx_r.goal,True,True,True)
        RIGUTILS.constraint(glute_fatfx_r.goal,'glute_r',True,True,True)
        glute_fatfx_l = RIGFX_FLESH.fatty_area().go('glute_l','thigh_l','glute_helper_l','glute_piv_l','glute_goal_l',0.5)
        glute_l_c = RIG_GIZMOS.hoop('c_glute_l',rgb=rgb_id2,rad=1.3,hrad=0.4,axis=[1,0,0],spans=4,sections=3,degree=1).match_to(glute_fatfx_l.goal).set_parent(glute_fatfx_l.piv).set_space_rotation(-10,0,90).move_control_local(14,-4,-2,movepivot=True).constraint(glute_fatfx_l.goal,True,True,True)
        RIGUTILS.constraint(glute_fatfx_l.goal,'glute_l',True,True,True)
               

        glute_inner_r_c = RIG_GIZMOS.hoop('c_glute_inner_r',rgb=rgb_id2,rad=0.8,hrad=0.11,axis=[1,0,0],spans=2).match_to('glute_inner_r').set_parent('glute_r').move_control_local(10,0,0,movepivot=True).constraint('glute_inner_r',True,True,True)
        glute_inner_l_c = RIG_GIZMOS.hoop('c_glute_inner_l',rgb=rgb_id2,rad=0.8,hrad=0.11,axis=[1,0,0],spans=2).match_to('glute_inner_l').set_parent('glute_l').move_control_local(10,0,0,movepivot=True).constraint('glute_inner_l',True,True,True)

        glute_cheek_r_c = RIG_GIZMOS.hoop('c_glute_cheek_r',rgb=rgb_id2,rad=0.8,hrad=0.11,axis=[1,0,0],spans=2).match_to('glute_cheek_r').set_parent('glute_r').move_control_local(10,0,0,movepivot=True).constraint('glute_cheek_r',True,True,True)
        glute_cheek_l_c = RIG_GIZMOS.hoop('c_glute_cheek_l',rgb=rgb_id2,rad=0.8,hrad=0.11,axis=[1,0,0],spans=2).match_to('glute_cheek_l').set_parent('glute_l').move_control_local(10,0,0,movepivot=True).constraint('glute_cheek_l',True,True,True)

        glute_bottom_r_c = RIG_GIZMOS.hoop('c_glute_bottom_r',rgb=rgb_id2,rad=0.8,hrad=0.11,axis=[1,0,0],spans=2).match_to('glute_bottom_r').set_parent('glute_r').move_control_local(10,0,0,movepivot=True).constraint('glute_bottom_r',True,True,True)
        glute_bottom_l_c = RIG_GIZMOS.hoop('c_glute_bottom_l',rgb=rgb_id2,rad=0.8,hrad=0.11,axis=[1,0,0],spans=2).match_to('glute_bottom_l').set_parent('glute_l').move_control_local(10,0,0,movepivot=True).constraint('glute_bottom_l',True,True,True)

        glute_outer_r_c = RIG_GIZMOS.hoop('c_glute_outer_r',rgb=rgb_id2,rad=0.8,hrad=0.11,axis=[1,0,0],spans=2).match_to('glute_outer_r').set_parent('glute_r').move_control_local(10,0,0,movepivot=True).constraint('glute_outer_r',True,True,True)
        glute_outer_l_c = RIG_GIZMOS.hoop('c_glute_outer_l',rgb=rgb_id2,rad=0.8,hrad=0.11,axis=[1,0,0],spans=2).match_to('glute_outer_l').set_parent('glute_l').move_control_local(10,0,0,movepivot=True).constraint('glute_outer_l',True,True,True)


        quad_r_c = RIG_GIZMOS.hoop('c_quad_r',rgb=rgb_id2,rad=1.1,hrad=0.2,axis=[1,0,0],spans=2).match_to('quad_r').set_parent('thigh_twist1_r').move_control_local(11,0,0,movepivot=True).constraint('quad_r',True,True,True)
        quad_l_c = RIG_GIZMOS.hoop('c_quad_l',rgb=rgb_id2,rad=1.1,hrad=0.2,axis=[1,0,0],spans=2).match_to('quad_l').set_parent('thigh_twist1_l').move_control_local(11,0,0,movepivot=True).constraint('quad_l',True,True,True)

        adductor_r_c = RIG_GIZMOS.hoop('c_adductor_r',rgb=rgb_id2,rad=1.1,hrad=0.1,axis=[1,0,0],spans=2).match_to('adductor_r').set_parent('thigh_twist1_r').move_control_local(7.5,0,0,movepivot=True).constraint('adductor_r',True,True,True)
        adductor_l_c = RIG_GIZMOS.hoop('c_adductor_l',rgb=rgb_id2,rad=1.1,hrad=0.1,axis=[1,0,0],spans=2).match_to('adductor_l').set_parent('thigh_twist1_l').move_control_local(7.5,0,0,movepivot=True).constraint('adductor_l',True,True,True)

        ham_r_c = RIG_GIZMOS.hoop('c_ham_r',rgb=rgb_id2,rad=1.1,hrad=0.2,axis=[1,0,0],spans=2).match_to('ham_r').set_parent('thigh_twist1_r').move_control_local(12,0,0,movepivot=True).constraint('ham_r',True,True,True)
        ham_l_c = RIG_GIZMOS.hoop('c_ham_l',rgb=rgb_id2,rad=1.1,hrad=0.2,axis=[1,0,0],spans=2).match_to('ham_l').set_parent('thigh_twist1_l').move_control_local(12,0,0,movepivot=True).constraint('ham_l',True,True,True)

        calf_inner_r_c = RIG_GIZMOS.hoop('c_calf_inner_r',rgb=rgb_id2,rad=1.1,hrad=0.002,axis=[1,0,0],spans=2).match_to('calf_inner_r').set_parent('shin_twist1_r').move_control_local(6,0,0,movepivot=True).constraint('calf_inner_r',True,True,True)
        h = 'calf_inner_autoflex_r'
        calf_inner_r_c.create_subspace_switch(h,'calf_inner_goal_r','autoflex','Autoflex').add_additive()
        cmds.addAttr(calf_inner_r_c.id, ln='flex_multiplierX',nn='FlexMultiplierX', keyable=True, r=True, hidden=False, dv=0.007, min=0.0, max=100.0) 
        cmds.addAttr(calf_inner_r_c.id, ln='flex_multiplierY',nn='FlexMultiplierY', keyable=True, r=True, hidden=False, dv=0.007, min=0.0, max=100.0) 
        cmds.addAttr(calf_inner_r_c.id, ln='flex_multiplierZ',nn='FlexMultiplierZ', keyable=True, r=True, hidden=False, dv=0.007, min=0.0, max=100.0) 
        cmds.expression(s='if (foot_r.rotateY<0){ '+h+'.scaleX = 1.0 + (foot_r.rotateY*-1)*'+calf_inner_r_c.id+".flex_multiplierX; }")
        cmds.expression(s='if (foot_r.rotateY<0){ '+h+'.scaleY = 1.0 + (foot_r.rotateY*-1)*'+calf_inner_r_c.id+".flex_multiplierY; }")
        cmds.expression(s='if (foot_r.rotateY<0){ '+h+'.scaleZ = 1.0 + (foot_r.rotateY*-1)*'+calf_inner_r_c.id+".flex_multiplierZ; }")

        calf_inner_l_c = RIG_GIZMOS.hoop('c_calf_inner_l',rgb=rgb_id2,rad=1.1,hrad=0.002,axis=[1,0,0],spans=2).match_to('calf_inner_l').set_parent('shin_twist1_l').move_control_local(6,0,0,movepivot=True).constraint('calf_inner_l',True,True,True)
        h = 'calf_inner_autoflex_l'
        calf_inner_l_c.create_subspace_switch(h,'calf_inner_goal_l','autoflex','Autoflex').add_additive()
        cmds.addAttr(calf_inner_l_c.id, ln='flex_multiplierX',nn='FlexMultiplierX', keyable=True, r=True, hidden=False, dv=0.007, min=0.0, max=100.0) 
        cmds.addAttr(calf_inner_l_c.id, ln='flex_multiplierY',nn='FlexMultiplierY', keyable=True, r=True, hidden=False, dv=0.007, min=0.0, max=100.0) 
        cmds.addAttr(calf_inner_l_c.id, ln='flex_multiplierZ',nn='FlexMultiplierZ', keyable=True, r=True, hidden=False, dv=0.007, min=0.0, max=100.0) 
        cmds.expression(s='if (foot_l.rotateY<0){ '+h+'.scaleX = 1.0 + (foot_l.rotateY*-1)*'+calf_inner_l_c.id+".flex_multiplierX; }")
        cmds.expression(s='if (foot_l.rotateY<0){ '+h+'.scaleY = 1.0 + (foot_l.rotateY*-1)*'+calf_inner_l_c.id+".flex_multiplierY; }")
        cmds.expression(s='if (foot_l.rotateY<0){ '+h+'.scaleZ = 1.0 + (foot_l.rotateY*-1)*'+calf_inner_l_c.id+".flex_multiplierZ; }")

        calf_outer_r_c = RIG_GIZMOS.hoop('c_calf_outer_r',rgb=rgb_id2,rad=1.1,hrad=0.002,axis=[1,0,0],spans=2).match_to('calf_outer_r').set_parent('shin_twist1_r').move_control_local(10,0,0,movepivot=True).constraint('calf_outer_r',True,True,True)
        h = 'calf_outer_autoflex_r'
        calf_outer_r_c.create_subspace_switch(h,'calf_outer_goal_r','autoflex','Autoflex').add_additive()
        cmds.addAttr(calf_outer_r_c.id, ln='flex_multiplierX',nn='FlexMultiplierX', keyable=True, r=True, hidden=False, dv=0.013, min=0.0, max=100.0) 
        cmds.addAttr(calf_outer_r_c.id, ln='flex_multiplierY',nn='FlexMultiplierY', keyable=True, r=True, hidden=False, dv=0.013, min=0.0, max=100.0) 
        cmds.addAttr(calf_outer_r_c.id, ln='flex_multiplierZ',nn='FlexMultiplierZ', keyable=True, r=True, hidden=False, dv=0.013, min=0.0, max=100.0) 
        cmds.expression(s='if (foot_r.rotateY>0){ '+h+'.scaleX = 1.0 + foot_r.rotateY*'+calf_outer_r_c.id+'.flex_multiplierX; }')
        cmds.expression(s='if (foot_r.rotateY>0){ '+h+'.scaleY = 1.0 + foot_r.rotateY*'+calf_outer_r_c.id+'.flex_multiplierY; }')
        cmds.expression(s='if (foot_r.rotateY>0){ '+h+'.scaleZ = 1.0 + foot_r.rotateY*'+calf_outer_r_c.id+'.flex_multiplierZ; }')

        calf_outer_l_c = RIG_GIZMOS.hoop('c_calf_outer_l',rgb=rgb_id2,rad=1.1,hrad=0.002,axis=[1,0,0],spans=2).match_to('calf_outer_l').set_parent('shin_twist1_l').move_control_local(10,0,0,movepivot=True).constraint('calf_outer_l',True,True,True)
        h = 'calf_outer_autoflex_l'
        calf_outer_l_c.create_subspace_switch(h,'calf_outer_goal_l','autoflex','Autoflex').add_additive()
        cmds.addAttr(calf_outer_l_c.id, ln='flex_multiplierX',nn='FlexMultiplierX', keyable=True, r=True, hidden=False, dv=0.013, min=0.0, max=100.0) 
        cmds.addAttr(calf_outer_l_c.id, ln='flex_multiplierY',nn='FlexMultiplierY', keyable=True, r=True, hidden=False, dv=0.013, min=0.0, max=100.0) 
        cmds.addAttr(calf_outer_l_c.id, ln='flex_multiplierZ',nn='FlexMultiplierZ', keyable=True, r=True, hidden=False, dv=0.013, min=0.0, max=100.0) 
        cmds.expression(s='if (foot_l.rotateY>0){ '+h+'.scaleX = 1.0 + foot_l.rotateY*'+calf_outer_l_c.id+'.flex_multiplierX; }')
        cmds.expression(s='if (foot_l.rotateY>0){ '+h+'.scaleY = 1.0 + foot_l.rotateY*'+calf_outer_l_c.id+'.flex_multiplierY; }')
        cmds.expression(s='if (foot_l.rotateY>0){ '+h+'.scaleZ = 1.0 + foot_l.rotateY*'+calf_outer_l_c.id+'.flex_multiplierZ; }')

        grip_l_c = RIG_GIZMOS.cross('c_grip_l',rgb = rgb_id2, size=5,thick=0.4)
        grip_l_c.socket_control('grip_palm_l',root_c.id,'grip_palm_helper_root_l','grip_palm_helper_result_l')
        grip_l_c.constraint(grip_l_c.socket_target,True,True,True)
        
        grip_r_c = RIG_GIZMOS.cross('c_grip_r',rgb = rgb_id2, size=5,thick=0.4)
        grip_r_c.socket_control('grip_palm_r',root_c.id,'grip_palm_helper_root_r','grip_palm_helper_result_r')
        grip_r_c.constraint(grip_r_c.socket_target,True,True,True)

        RIGUTILS.bind_twist('upperarm_twist1_l','lowerarm_l',3)
        RIGUTILS.bind_twist('upperarm_twist2_l','lowerarm_l',2)
        RIGUTILS.bind_twist('upperarm_twist3_l','lowerarm_l',1.2)
    
        RIGUTILS.bind_twist('upperarm_twist1_r','lowerarm_r',3)
        RIGUTILS.bind_twist('upperarm_twist2_r','lowerarm_r',2)
        RIGUTILS.bind_twist('upperarm_twist3_r','lowerarm_r',1.2)

        RIGUTILS.bind_twist('lowerarm_twist1_l','hand_l',3)
        RIGUTILS.bind_twist('lowerarm_twist2_l','hand_l',2)
        RIGUTILS.bind_twist('lowerarm_twist3_l','hand_l',1.2)
    
        RIGUTILS.bind_twist('lowerarm_twist1_r','hand_r',3)
        RIGUTILS.bind_twist('lowerarm_twist2_r','hand_r',2)
        RIGUTILS.bind_twist('lowerarm_twist3_r','hand_r',1.2)

        RIGUTILS.bind_twist('thigh_twist1_l','shin_l',2)
        RIGUTILS.bind_twist('thigh_twist2_l','shin_l',1.2)

        RIGUTILS.bind_twist('shin_twist1_l','foot_l',2)
        RIGUTILS.bind_twist('shin_twist2_l','foot_l',1.2)

        RIGUTILS.bind_twist('thigh_twist1_r','shin_r',2)
        RIGUTILS.bind_twist('thigh_twist2_r','shin_r',1.2)

        RIGUTILS.bind_twist('shin_twist1_r','foot_r',2)
        RIGUTILS.bind_twist('shin_twist2_r','foot_r',1.2)



        jaw_c = RIG_GIZMOS.hoop('c_jaw',rgb=rgb_id2,rad=0.4,hrad=0.2,axis=[1,0,0],spans=2).match_to('jaw').set_parent('head').move_control_local(14,0,0,movepivot=True).constraint('jaw',True,True,True)

        brow_center_c = RIG_GIZMOS.hoop('c_brow_center',rgb=rgb_id2,rad=0.2,hrad=0.2,axis=[1,0,0],spans=2).match_to('brow_center').set_parent('head').move_control_local(1.5,0,0,movepivot=True).constraint('brow_center',True,True,True)

        brow1_r_c = RIG_GIZMOS.hoop('c_brow1_r',rgb=rgb_id2,rad=0.2,hrad=0.2,axis=[1,0,0],spans=2).match_to('brow1_r').set_parent('head').move_control_local(1.5,0,0,movepivot=True).constraint('brow1_r',True,True,True)
        brow1_l_c = RIG_GIZMOS.hoop('c_brow1_l',rgb=rgb_id2,rad=0.2,hrad=0.2,axis=[1,0,0],spans=2).match_to('brow1_l').set_parent('head').move_control_local(1.5,0,0,movepivot=True).constraint('brow1_l',True,True,True)

        brow2_r_c = RIG_GIZMOS.hoop('c_brow2_r',rgb=rgb_id2,rad=0.2,hrad=0.2,axis=[1,0,0],spans=2).match_to('brow2_r').set_parent('head').move_control_local(1.5,0,0,movepivot=True).constraint('brow2_r',True,True,True)
        brow2_l_c = RIG_GIZMOS.hoop('c_brow2_l',rgb=rgb_id2,rad=0.2,hrad=0.2,axis=[1,0,0],spans=2).match_to('brow2_l').set_parent('head').move_control_local(1.5,0,0,movepivot=True).constraint('brow2_l',True,True,True)

        brow3_r_c = RIG_GIZMOS.hoop('c_brow3_r',rgb=rgb_id2,rad=0.2,hrad=0.2,axis=[1,0,0],spans=2).match_to('brow3_r').set_parent('head').move_control_local(1.5,0,0,movepivot=True).constraint('brow3_r',True,True,True)
        brow3_l_c = RIG_GIZMOS.hoop('c_brow3_l',rgb=rgb_id2,rad=0.2,hrad=0.2,axis=[1,0,0],spans=2).match_to('brow3_l').set_parent('head').move_control_local(1.5,0,0,movepivot=True).constraint('brow3_l',True,True,True)

        brow4_r_c = RIG_GIZMOS.hoop('c_brow4_r',rgb=rgb_id2,rad=0.2,hrad=0.2,axis=[1,0,0],spans=2).match_to('brow4_r').set_parent('head').move_control_local(1.5,0,0,movepivot=True).constraint('brow4_r',True,True,True)
        brow4_l_c = RIG_GIZMOS.hoop('c_brow4_l',rgb=rgb_id2,rad=0.2,hrad=0.2,axis=[1,0,0],spans=2).match_to('brow4_l').set_parent('head').move_control_local(1.5,0,0,movepivot=True).constraint('brow4_l',True,True,True)

        ear_r_c = RIG_GIZMOS.hoop('c_ear_r',rgb=rgb_id2,rad=0.4,hrad=0.2,axis=[1,0,0],spans=2).match_to('ear_r').set_parent('head').move_control_local(6,0,0,movepivot=True).constraint('ear_r',True,True,True)
        ear_l_c = RIG_GIZMOS.hoop('c_ear_l',rgb=rgb_id2,rad=0.4,hrad=0.2,axis=[1,0,0],spans=2).match_to('ear_l').set_parent('head').move_control_local(6,0,0,movepivot=True).constraint('ear_l',True,True,True)

        cheek_r_c = RIG_GIZMOS.hoop('c_cheek_r',rgb=rgb_id2,rad=0.4,hrad=0.2,axis=[1,0,0],spans=2).match_to('cheek_r').set_parent('head').move_control_local(4,0,0,movepivot=True).constraint('cheek_r',True,True,True)
        cheek_l_c = RIG_GIZMOS.hoop('c_cheek_l',rgb=rgb_id2,rad=0.4,hrad=0.2,axis=[1,0,0],spans=2).match_to('cheek_l').set_parent('head').move_control_local(4,0,0,movepivot=True).constraint('cheek_l',True,True,True)

        cheekbone_r_c = RIG_GIZMOS.hoop('c_cheekbone_r',rgb=rgb_id2,rad=0.4,hrad=0.2,axis=[1,0,0],spans=2).match_to('cheekbone_r').set_parent('head').move_control_local(2.5,0,0,movepivot=True).constraint('cheekbone_r',True,True,True)
        cheekbone_l_c = RIG_GIZMOS.hoop('c_cheekbone_l',rgb=rgb_id2,rad=0.4,hrad=0.2,axis=[1,0,0],spans=2).match_to('cheekbone_l').set_parent('head').move_control_local(2.5,0,0,movepivot=True).constraint('cheekbone_l',True,True,True)

        laughline_r_c = RIG_GIZMOS.hoop('c_laughline_r',rgb=rgb_id2,rad=0.4,hrad=0.2,axis=[1,0,0],spans=2).match_to('laughline_r').set_parent('head').move_control_local(2.5,0,0,movepivot=True).constraint('laughline_r',True,True,True)
        laughline_l_c = RIG_GIZMOS.hoop('c_laughline_l',rgb=rgb_id2,rad=0.4,hrad=0.2,axis=[1,0,0],spans=2).match_to('laughline_l').set_parent('head').move_control_local(2.5,0,0,movepivot=True).constraint('laughline_l',True,True,True)


def human_rig_basic(args):
    rig = female_rig_class()
    
    
def onMayaDroppedPythonFile(args):
    print("Starting")

window = cmds.window( 
    title='Human Rigger',  
    width=300,
    resizeToFitChildren=True) 

scrollLayout = cmds.scrollLayout(
    horizontalScrollBarThickness=16,
    verticalScrollBarThickness=16)
    
cmds.columnLayout(
    columnOffset=['left',0])
 

cmds.button( label='Draft', 
             width = 100,
             command=human_rig_basic )
  

cmds.setParent( '..' )
                                               
cmds.showWindow( window )