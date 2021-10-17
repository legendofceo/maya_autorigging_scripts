import maya.cmds as cmds



import skeleton_shared_joint as JOINT
reload(JOINT)

def sym():

    w = []

    JOINT.new('root').pos_only().center().end(w)
    JOINT.new('hip').pos_only().center().end(w)
    JOINT.new('pelvis').pos_only().center().end(w)
    JOINT.new('spine1').pos_only().center().end(w)
    JOINT.new('spine2').pos_only().center().x_only().end(w)
    JOINT.new('spine3').pos_only().center().x_only().end(w)
    JOINT.new('spine4').pos_only().center().x_only().end(w)
    JOINT.new('spine5').pos_only().center().x_only().end(w)
    JOINT.new('neck1').pos_only().center().x_only().end(w)
    JOINT.new('neck2').pos_only().center().x_only().end(w)
    JOINT.new('head').pos_only().center().x_only().end(w)

    JOINT.new('ab_r').set_sym('ab_l').pos_only().invert_socket().end(w)
    JOINT.new('spinae_r').set_sym('spinae_l').pos_only().invert_socket().end(w)
    JOINT.new('flub_r').set_sym('flub_l').pos_only().invert_socket().end(w)
    JOINT.new('belly').pos_only().center().end(w)
    JOINT.new('pooch').pos_only().center().end(w)
    JOINT.new('bulge').pos_only().center().end(w)

    JOINT.new('breath_lower').pos_only().center().end(w)
    JOINT.new('breath_upper').pos_only().center().end(w)

    #JOINT.new('pec_r').set_sym('pec_l').pos_only().invert_socket().end(w)
    JOINT.new('breast_r').set_sym('breast_l').pos_only().invert_socket().end(w)
    JOINT.new('cup_r').set_sym('cup_l').pos_only().invert_socket().end(w)
    JOINT.new('nip_r').set_sym('nip_l').pos_only().invert_socket().end(w)

    JOINT.new('pit_r').set_sym('pit_l').pos_only().invert_socket().end(w)

    JOINT.new('lat_r').set_sym('lat_l').pos_only().invert_socket().end(w)
    JOINT.new('scapula_r').set_sym('scapula_l').pos_only().invert_socket().end(w)
    JOINT.new('deltoid_r').set_sym('deltoid_l').pos_only().invert_socket().end(w)
    JOINT.new('trap_r').set_sym('trap_l').pos_only().invert_socket().end(w)

    JOINT.new('throat').pos_only().center().end(w)

    JOINT.new('clavicle_r').set_sym('clavicle_l').pos_only().invert_socket().end(w)
    JOINT.new('upperarm_r').set_sym('upperarm_l').pos_only().invert_chain().end(w)
    JOINT.new('lowerarm_r').set_sym('lowerarm_l').pos_only().invert_chain().end(w)
    JOINT.new('hand_r').set_sym('hand_l').pos_only().invert_chain().end(w)

    twist_len = cmds.getAttr('lowerarm_r.translateX')/4.0
    JOINT.new('upperarm_twist1_r').set_sym('upperarm_twist1_l').pos_only().x_only().set_tx(twist_len).end(w)
    JOINT.new('upperarm_twist2_r').set_sym('upperarm_twist2_l').pos_only().x_only().set_tx(twist_len*2).end(w)
    JOINT.new('upperarm_twist3_r').set_sym('upperarm_twist3_l').pos_only().x_only().set_tx(twist_len*3).end(w)

    twist_len = cmds.getAttr('hand_r.translateX')/4.0
    JOINT.new('lowerarm_twist1_r').set_sym('lowerarm_twist1_l').pos_only().x_only().set_tx(twist_len).end(w)
    JOINT.new('lowerarm_twist2_r').set_sym('lowerarm_twist2_l').pos_only().x_only().set_tx(twist_len*2).end(w)
    JOINT.new('lowerarm_twist3_r').set_sym('lowerarm_twist3_l').pos_only().x_only().set_tx(twist_len*3).end(w)

    JOINT.new('bicep_r').set_sym('bicep_l').pos_only().invert_socket().end(w)
    JOINT.new('tricep_r').set_sym('tricep_l').pos_only().invert_socket().end(w)
    JOINT.new('brach_r').set_sym('brach_l').pos_only().invert_socket().end(w)

    JOINT.new('finger_thumb1_r').set_sym('finger_thumb1_l').pos_only().invert_socket().end(w)
    JOINT.new('finger_thumb2_r').set_sym('finger_thumb2_l').pos_only().x_only().invert_chain().end(w)
    JOINT.new('finger_thumb3_r').set_sym('finger_thumb3_l').pos_only().x_only().invert_chain().end(w)

    JOINT.new('finger_index1_r').set_sym('finger_index1_l').pos_only().invert_socket().end(w)
    JOINT.new('finger_index2_r').set_sym('finger_index2_l').pos_only().x_only().invert_chain().end(w)
    JOINT.new('finger_index3_r').set_sym('finger_index3_l').pos_only().x_only().invert_chain().end(w)

    JOINT.new('finger_middle1_r').set_sym('finger_middle1_l').pos_only().invert_socket().end(w)
    JOINT.new('finger_middle2_r').set_sym('finger_middle2_l').pos_only().x_only().invert_chain().end(w)
    JOINT.new('finger_middle3_r').set_sym('finger_middle3_l').pos_only().x_only().invert_chain().end(w)

    JOINT.new('finger_ring1_r').set_sym('finger_ring1_l').pos_only().invert_socket().end(w)
    JOINT.new('finger_ring2_r').set_sym('finger_ring2_l').pos_only().x_only().invert_chain().end(w)
    JOINT.new('finger_ring3_r').set_sym('finger_ring3_l').pos_only().x_only().invert_chain().end(w)

    JOINT.new('finger_pinky1_r').set_sym('finger_pinky1_l').pos_only().invert_socket().end(w)
    JOINT.new('finger_pinky2_r').set_sym('finger_pinky2_l').pos_only().x_only().invert_chain().end(w)
    JOINT.new('finger_pinky3_r').set_sym('finger_pinky3_l').pos_only().x_only().invert_chain().end(w)

    JOINT.new('thigh_r').set_sym('thigh_l').pos_only().invert_socket().end(w)
    JOINT.new('shin_r').set_sym('shin_l').pos_only().x_only().invert_chain().end(w)
    JOINT.new('foot_r').set_sym('foot_l').pos_only().x_only().invert_socket().end(w)
    JOINT.new('ball_r').set_sym('ball_l').pos_only().invert_socket().end(w)
    JOINT.new('toetip_r').set_sym('toetip_l').pos_only().x_only().invert_chain().end(w)
    JOINT.new('heel_r').set_sym('heel_l').pos_only().invert_socket().end(w)

    twist_len = cmds.getAttr('shin_r.translateX')/3.0
    JOINT.new('thigh_twist1_r').set_sym('thigh_twist1_l').pos_only().x_only().set_tx(twist_len).end(w)
    JOINT.new('thigh_twist2_r').set_sym('thigh_twist2_l').pos_only().x_only().set_tx(twist_len*2).end(w)

    twist_len = cmds.getAttr('foot_r.translateX')/3.0
    JOINT.new('shin_twist1_r').set_sym('shin_twist1_l').pos_only().x_only().set_tx(twist_len).end(w)
    JOINT.new('shin_twist2_r').set_sym('shin_twist2_l').pos_only().x_only().set_tx(twist_len*2).end(w)

    JOINT.new('glute_r').set_sym('glute_l').pos_only().invert_socket().end(w)
    
    JOINT.new('glute_inner_r').set_sym('glute_inner_l').pos_only().invert_socket().end(w)
    JOINT.new('glute_bottom_r').set_sym('glute_bottom_l').pos_only().invert_socket().end(w)
    JOINT.new('glute_cheek_r').set_sym('glute_cheek_l').pos_only().invert_socket().end(w)
    JOINT.new('glute_outer_r').set_sym('glute_outer_l').pos_only().invert_socket().end(w)

    

    JOINT.new('quad_r').set_sym('quad_l').pos_only().invert_socket().end(w)
    JOINT.new('adductor_r').set_sym('adductor_l').pos_only().invert_socket().end(w)
    JOINT.new('ham_r').set_sym('ham_l').pos_only().invert_socket().end(w)

    JOINT.new('calf_inner_r').set_sym('calf_inner_l').pos_only().invert_socket().end(w)
    JOINT.new('calf_outer_r').set_sym('calf_outer_l').pos_only().invert_socket().end(w)

    JOINT.new('toe_big1_r').set_sym('toe_big1_l').pos_only().invert_socket().end(w)
    JOINT.new('toe_big2_r').set_sym('toe_big2_l').pos_only().x_only().invert_chain().end(w)

    JOINT.new('toe_long1_r').set_sym('toe_long1_l').pos_only().invert_socket().end(w)
    JOINT.new('toe_long2_r').set_sym('toe_long2_l').pos_only().x_only().invert_chain().end(w)

    JOINT.new('toe_middle1_r').set_sym('toe_middle1_l').pos_only().invert_socket().end(w)
    JOINT.new('toe_middle2_r').set_sym('toe_middle2_l').pos_only().x_only().invert_chain().end(w)

    JOINT.new('toe_ring1_r').set_sym('toe_ring1_l').pos_only().invert_socket().end(w)
    JOINT.new('toe_ring2_r').set_sym('toe_ring2_l').pos_only().x_only().invert_chain().end(w)

    JOINT.new('toe_little1_r').set_sym('toe_little1_l').pos_only().invert_socket().end(w)
    JOINT.new('toe_little2_r').set_sym('toe_little2_l').pos_only().x_only().invert_chain().end(w)

    JOINT.new('sheath_hip_sword_r').set_sym('sheath_hip_sword_l').pos_only().invert_socket().end(w)
    JOINT.new('sheath_small_dagger_r').set_sym('sheath_small_dagger_l').pos_only().invert_socket().end(w)
    JOINT.new('sheath_back_shield_r').set_sym('sheath_back_shield_l').pos_only().invert_socket().end(w)
    JOINT.new('sheath_back_quiver_r').set_sym('sheath_back_quiver_l').pos_only().invert_socket().end(w)
    JOINT.new('sheath_back_bow_r').set_sym('sheath_back_bow_l').pos_only().invert_socket().end(w)
    JOINT.new('sheath_back_sword_r').set_sym('sheath_back_sword_l').pos_only().invert_socket().end(w)
    JOINT.new('sheath_back_sword_r').set_sym('sheath_back_sword_l').pos_only().invert_socket().end(w)

    JOINT.new('grip_palm_r').set_sym('grip_palm_l').pos_only().invert_socket().end(w)
    JOINT.new('grip_shield_r').set_sym('grip_shield_l').pos_only().invert_socket().end(w)

    JOINT.new('socket_headwear').pos_only().center().end(w)

    JOINT.new('tongue1').pos_only().center().end(w)
    JOINT.new('tongue2').pos_only().center().end(w)
    JOINT.new('tongue3').pos_only().center().end(w)
    JOINT.new('tongue4').pos_only().center().end(w)
    JOINT.new('tongue5').pos_only().center().end(w)

    JOINT.new('eye_r').set_sym('eye_l').pos_only().invert_socket().end(w)
    JOINT.new('ear_r').set_sym('ear_l').pos_only().invert_socket().end(w)

    JOINT.new('jaw').pos_only().center().end(w)
    JOINT.new('chin').pos_only().center().end(w)
    JOINT.new('philtrum').pos_only().center().end(w)
    JOINT.new('nostril').pos_only().center().end(w)
    JOINT.new('squint_r').set_sym('squint_l').pos_only().invert_socket().end(w)
    JOINT.new('cheek_r').set_sym('cheek_l').pos_only().invert_socket().end(w)
    JOINT.new('cheekbone_r').set_sym('cheekbone_l').pos_only().invert_socket().end(w)
    JOINT.new('eyelid_lower1_r').set_sym('eyelid_lower1_l').pos_only().invert_socket().end(w)
    JOINT.new('eyelid_lower2_r').set_sym('eyelid_lower2_l').pos_only().invert_socket().end(w)
    JOINT.new('eyelid_lower3_r').set_sym('eyelid_lower3_l').pos_only().invert_socket().end(w)
    JOINT.new('eyelid_upper1_r').set_sym('eyelid_upper1_l').pos_only().invert_socket().end(w)
    JOINT.new('eyelid_upper2_r').set_sym('eyelid_upper2_l').pos_only().invert_socket().end(w)
    JOINT.new('eyelid_upper3_r').set_sym('eyelid_upper3_l').pos_only().invert_socket().end(w)

    JOINT.new('lip_lower_center').pos_only().center().end(w)
    JOINT.new('lip_lower1_r').set_sym('lip_lower1_l').pos_only().invert_socket().end(w)
    JOINT.new('lip_lower2_r').set_sym('lip_lower2_l').pos_only().invert_socket().end(w)
    JOINT.new('lip_lower3_r').set_sym('lip_lower3_l').pos_only().invert_socket().end(w)
    JOINT.new('lip_upper_center').pos_only().center().end(w)
    JOINT.new('lip_upper1_r').set_sym('lip_upper1_l').pos_only().invert_socket().end(w)
    JOINT.new('lip_upper2_r').set_sym('lip_upper2_l').pos_only().invert_socket().end(w)
    JOINT.new('lip_upper3_r').set_sym('lip_upper3_l').pos_only().invert_socket().end(w)
    JOINT.new('lip_corner_r').set_sym('lip_corner_l').pos_only().invert_socket().end(w)    
    JOINT.new('laughline_r').set_sym('laughline_l').pos_only().invert_socket().end(w)

    JOINT.new('brow_center').pos_only().center().end(w)
    JOINT.new('brow1_r').set_sym('brow1_l').pos_only().invert_socket().end(w)
    JOINT.new('brow2_r').set_sym('brow2_l').pos_only().invert_socket().end(w)
    JOINT.new('brow3_r').set_sym('brow3_l').pos_only().invert_socket().end(w)
    JOINT.new('brow4_r').set_sym('brow4_l').pos_only().invert_socket().end(w)

    JOINT.new('cam1').pos_only().center().end(w)
    JOINT.new('cam2').pos_only().center().end(w)
    JOINT.new('cam3').pos_only().center().end(w)
    JOINT.new('poi1').pos_only().center().end(w)
    JOINT.new('poi2').pos_only().center().end(w)
    JOINT.new('poi3').pos_only().center().end(w)
    JOINT.new('poi_rear').pos_only().center().end(w)
    JOINT.new('poi_chest').pos_only().center().end(w)
    JOINT.new('item1').pos_only().center().end(w)
    JOINT.new('item2').pos_only().center().end(w)
    JOINT.new('item3').pos_only().center().end(w)
    JOINT.new('item4').pos_only().center().end(w)

    JOINT.new('scro_r').set_sym('scro_l').pos_only().invert_socket().end(w)
    JOINT.new('genm').pos_only().center().end(w)
    JOINT.new('shaft1').pos_only().center().end(w)
    JOINT.new('shaft2').pos_only().center().end(w)
    JOINT.new('shaft3').pos_only().center().end(w)
    JOINT.new('shaft4').pos_only().center().end(w)
    JOINT.new('shaft5').pos_only().center().end(w)

    JOINT.new('genf').pos_only().center().end(w)
    JOINT.new('lab1_r').set_sym('lab1_l').pos_only().invert_socket().end(w)
    JOINT.new('lab2_r').set_sym('lab2_l').pos_only().invert_socket().end(w)
    JOINT.new('lab3_r').set_sym('lab3_l').pos_only().invert_socket().end(w)
    JOINT.new('lab4_r').set_sym('lab4_l').pos_only().invert_socket().end(w)
    JOINT.new('vay_r').set_sym('vay_l').pos_only().invert_socket().end(w)
    JOINT.new('vay_u').pos_only().center().end(w)
    JOINT.new('vay_d').pos_only().center().end(w)
    JOINT.new('stim').pos_only().center().end(w)

    JOINT.new('gena').pos_only().center().end(w)
    JOINT.new('ori_u').pos_only().center().end(w)
    JOINT.new('ori_d').pos_only().center().end(w)
    JOINT.new('ori_r').set_sym('ori_l').pos_only().invert_socket().end(w)


    print("Total Joints Edited: "+str(len(w)))
    print("Crosschecking all joints...")
    joints = cmds.ls(type='joint')

    for j in joints:
       if j not in w:
            print("Missing Joint: "+j)


def onMayaDroppedPythonFile(args):
    sym()