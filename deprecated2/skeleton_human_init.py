import maya.cmds as cmds

import skeleton_shared_joint as JOINT
reload(JOINT)

def init():


    w = []

    rgb_center = [0.7,0.7,0.6]  
    rgb_side = [0.55,0.55,0.45]
    rgb_twist = [0.8,0.4,0.0]
    rgb_flex = [0.8,0.2,0.2]
    rgb_socket = [1.0,0.6,0.0]
    rgb_poi = [0.0,0.3,1.0]
    rgb_special = [0.2,0.7,0.4]
    rgb_face = [0.4,0.4,0.3]
    rgb_tongue = [0.9,0.5,0.5]
    rgb_genm = [0.3,0.6,1.0]
    rgb_genf = [0.7,0.5,0.5]
    rgb_gena = [0.6,0.2,0.6]

    JOINT.new('root').label('root').size(2.0).set_rgb(rgb_center).end(w)
    JOINT.new('hip').label('hip').size(1.0).set_rgb(rgb_center).end(w)
    JOINT.new('pelvis').label('pelvis').size(0.5).set_rgb(rgb_center).end(w)
    JOINT.new('spine1').label('spine1').size(1.0).set_rgb(rgb_center).end(w)
    JOINT.new('spine2').label('spine2').size(1.0).set_rgb(rgb_center).end(w)
    JOINT.new('spine3').label('spine3').size(1.0).set_rgb(rgb_center).end(w)
    JOINT.new('spine4').label('spine4').size(1.0).set_rgb(rgb_center).end(w)
    JOINT.new('spine5').label('spine5').size(1.0).set_rgb(rgb_center).end(w)
    JOINT.new('neck1').label('neck1').size(1.0).set_rgb(rgb_center).end(w)
    JOINT.new('neck2').label('neck2').size(1.0).set_rgb(rgb_center).end(w)
    JOINT.new('neck1').label('neck1').size(1.0).set_rgb(rgb_center).end(w)
    JOINT.new('head').label('head').size(1.0).set_rgb(rgb_center).end(w)
    JOINT.new('clavicle_r').set_sym('clavicle_l').label('clavicle').size(1.4).axis().set_rgb(rgb_side).end(w)
    JOINT.new('upperarm_r').set_sym('upperarm_l').label('upperarm').size(0.6).axis().set_rgb(rgb_side).end(w)
    JOINT.new('lowerarm_r').set_sym('lowerarm_l').label('lowerarm').size(0.5).axis().set_rgb(rgb_side).end(w)
    JOINT.new('hand_r').set_sym('hand_l').label('hand').size(0.5).axis().set_rgb(rgb_side).end(w)

    JOINT.new('upperarm_twist1_r').set_sym('upperarm_twist1_l').label('upperarm_twist1').size(1.2).axis().set_rgb(rgb_twist).end(w)
    JOINT.new('upperarm_twist2_r').set_sym('upperarm_twist2_l').label('upperarm_twist2').size(1.0).axis().set_rgb(rgb_twist).end(w)
    JOINT.new('upperarm_twist3_r').set_sym('upperarm_twist3_l').label('upperarm_twist3').size(0.8).axis().set_rgb(rgb_twist).end(w)

    JOINT.new('lowerarm_twist1_r').set_sym('lowerarm_twist1_l').label('lowerarm_twist1').size(1.2).axis().set_rgb(rgb_twist).end(w)
    JOINT.new('lowerarm_twist2_r').set_sym('lowerarm_twist2_l').label('lowerarm_twist2').size(1.0).axis().set_rgb(rgb_twist).end(w)
    JOINT.new('lowerarm_twist3_r').set_sym('lowerarm_twist3_l').label('lowerarm_twist3').size(0.8).axis().set_rgb(rgb_twist).end(w)

    JOINT.new('finger_thumb1_r').set_sym('finger_thumb1_l').label('finger_thumb1').size(0.5).axis().set_rgb(rgb_side).end(w)
    JOINT.new('finger_thumb2_r').set_sym('finger_thumb2_l').label('finger_thumb2').size(0.4).axis().set_rgb(rgb_side).end(w)
    JOINT.new('finger_thumb3_r').set_sym('finger_thumb3_l').label('finger_thumb3').size(0.3).axis().set_rgb(rgb_side).end(w)

    JOINT.new('finger_index1_r').set_sym('finger_index1_l').label('finger_index1').size(0.5).axis().set_rgb(rgb_side).end(w)
    JOINT.new('finger_index2_r').set_sym('finger_index2_l').label('finger_index2').size(0.4).axis().set_rgb(rgb_side).end(w)
    JOINT.new('finger_index3_r').set_sym('finger_index3_l').label('finger_index3').size(0.3).axis().set_rgb(rgb_side).end(w)

    JOINT.new('finger_middle1_r').set_sym('finger_middle1_l').label('finger_middle1').size(0.5).axis().set_rgb(rgb_side).end(w)
    JOINT.new('finger_middle2_r').set_sym('finger_middle2_l').label('finger_middle2').size(0.4).axis().set_rgb(rgb_side).end(w)
    JOINT.new('finger_middle3_r').set_sym('finger_middle3_l').label('finger_middle3').size(0.3).axis().set_rgb(rgb_side).end(w)

    JOINT.new('finger_ring1_r').set_sym('finger_ring1_l').label('finger_ring1').size(0.5).axis().set_rgb(rgb_side).end(w)
    JOINT.new('finger_ring2_r').set_sym('finger_ring2_l').label('finger_ring2').size(0.4).axis().set_rgb(rgb_side).end(w)
    JOINT.new('finger_ring3_r').set_sym('finger_ring3_l').label('finger_ring3').size(0.3).axis().set_rgb(rgb_side).end(w)

    JOINT.new('finger_pinky1_r').set_sym('finger_pinky1_l').label('finger_pinky1').size(0.5).axis().set_rgb(rgb_side).end(w)
    JOINT.new('finger_pinky2_r').set_sym('finger_pinky2_l').label('finger_pinky2').size(0.4).axis().set_rgb(rgb_side).end(w)
    JOINT.new('finger_pinky3_r').set_sym('finger_pinky3_l').label('finger_pinky3').size(0.3).axis().set_rgb(rgb_side).end(w)

    JOINT.new('thigh_r').set_sym('thigh_l').label('thigh').size(1.2).axis().set_rgb(rgb_side).end(w)
    JOINT.new('shin_r').set_sym('shin_l').label('shin').size(0.8).axis().set_rgb(rgb_side).end(w)
    JOINT.new('foot_r').set_sym('foot_l').label('foot').size(1.0).axis().set_rgb(rgb_side).end(w)

    JOINT.new('ball_r').set_sym('ball_l').label('ball').size(0.5).axis().set_rgb(rgb_side).end(w)
    JOINT.new('toetip_r').set_sym('toetip_l').label('toetip').size(0.6).axis().set_rgb(rgb_side).end(w)
    JOINT.new('heel_r').set_sym('heel_l').label('heel').size(1.5).axis().set_rgb(rgb_side).end(w)

    JOINT.new('thigh_twist1_r').set_sym('thigh_twist1_l').label('thigh_twist1').size(1.2).axis().set_rgb(rgb_twist).end(w)
    JOINT.new('thigh_twist2_r').set_sym('thigh_twist2_l').label('thigh_twist2').size(1.0).axis().set_rgb(rgb_twist).end(w)

    JOINT.new('shin_twist1_r').set_sym('shin_twist1_l').label('shin_twist1').size(1.2).axis().set_rgb(rgb_twist).end(w)
    JOINT.new('shin_twist2_r').set_sym('shin_twist2_l').label('shin_twist2').size(1.0).axis().set_rgb(rgb_twist).end(w)

    JOINT.new('toe_big1_r').set_sym('toe_big1_l').label('toe_big1').size(0.3).axis().set_rgb(rgb_side).end(w)
    JOINT.new('toe_big2_r').set_sym('toe_big2_l').label('toe_big2').size(0.18).axis().set_rgb(rgb_side).end(w)

    JOINT.new('toe_long1_r').set_sym('toe_long1_l').label('toe_long1').size(0.28).axis().set_rgb(rgb_side).end(w)
    JOINT.new('toe_long2_r').set_sym('toe_long2_l').label('toe_long2').size(0.16).axis().set_rgb(rgb_side).end(w)

    JOINT.new('toe_middle1_r').set_sym('toe_middle1_l').label('toe_middle1').size(0.26).axis().set_rgb(rgb_side).end(w)
    JOINT.new('toe_middle2_r').set_sym('toe_middle2_l').label('toe_middle2').size(0.14).axis().set_rgb(rgb_side).end(w)

    JOINT.new('toe_ring1_r').set_sym('toe_ring1_l').label('toe_ring1').size(0.24).axis().set_rgb(rgb_side).end(w)
    JOINT.new('toe_ring2_r').set_sym('toe_ring2_l').label('toe_ring2').size(0.12).axis().set_rgb(rgb_side).end(w)

    JOINT.new('toe_little1_r').set_sym('toe_little1_l').label('toe_little1').size(0.22).axis().set_rgb(rgb_side).end(w)
    JOINT.new('toe_little2_r').set_sym('toe_little2_l').label('toe_little2').size(0.11).axis().set_rgb(rgb_side).end(w)

    JOINT.new('spinae_r').set_sym('spinae_l').label('spinae').size(0.7).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('bulge').label('bulge').size(0.5).set_rgb(rgb_flex).end(w)
    JOINT.new('ab_r').set_sym('ab_l').label('ab').size(0.6).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('belly').label('belly').size(0.8).set_rgb(rgb_flex).end(w)
    JOINT.new('pooch').label('pooch').size(0.5).set_rgb(rgb_flex).end(w)
    JOINT.new('flub_r').set_sym('flub_l').label('flub').size(0.7).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('lat_r').set_sym('lat_l').label('lat').size(0.7).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('pit_r').set_sym('pit_l').label('pit').size(0.7).axis().set_rgb(rgb_flex).end(w)
   #JOINT.new('pec_r').set_sym('pec_l').label('pec').size(0.7).axis().set_rgb(rgb_side).end(w)
    JOINT.new('breast_r').set_sym('breast_l').label('breast').size(0.7).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('cup_r').set_sym('cup_l').label('cup').size(0.7).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('nip_r').set_sym('nip_l').label('nip').size(0.7).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('deltoid_r').set_sym('deltoid_l').label('deltoid').size(1.0).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('trap_r').set_sym('trap_l').label('trap').size(0.7).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('scapula_r').set_sym('scapula_l').label('scapula').size(0.7).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('breath_upper').label('breath_upper').size(0.5).set_rgb(rgb_flex).end(w)
    JOINT.new('breath_lower').label('breath_lower').size(0.5).set_rgb(rgb_flex).end(w)
    JOINT.new('throat').label('throat').size(0.4).set_rgb(rgb_flex).end(w)
    JOINT.new('bicep_r').set_sym('bicep_l').label('bicep').size(0.5).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('tricep_r').set_sym('tricep_l').label('tricep').size(0.5).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('brach_r').set_sym('brach_l').label('brach').size(0.5).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('glute_r').set_sym('glute_l').label('glute').size(0.7).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('glute_inner_r').set_sym('glute_inner_l').label('glute_inner').size(0.7).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('glute_bottom_r').set_sym('glute_bottom_l').label('glute_bottom').size(0.7).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('glute_cheek_r').set_sym('glute_cheek_l').label('glute_cheek').size(0.7).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('glute_outer_r').set_sym('glute_outer_l').label('glute_outer').size(0.7).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('quad_r').set_sym('quad_l').label('quad').size(0.5).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('adductor_r').set_sym('adductor_l').label('adductor').size(0.5).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('ham_r').set_sym('ham_l').label('ham').size(0.5).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('calf_inner_r').set_sym('calf_inner_l').label('calf_inner').size(0.5).axis().set_rgb(rgb_flex).end(w)
    JOINT.new('calf_outer_r').set_sym('calf_outer_l').label('calf_outer').size(0.5).axis().set_rgb(rgb_flex).end(w)

    JOINT.new('socket_headwear').label('socket_headwear').size(0.5).set_rgb(rgb_socket).end(w)

    JOINT.new('sheath_hip_sword_r').set_sym('sheath_hip_sword_l').label('sheath_hip_sword').size(1.0).axis().set_rgb(rgb_socket).end(w)
    JOINT.new('grip_shield_r').set_sym('grip_shield_l').label('grip_shield').size(1.0).axis().set_rgb(rgb_socket).end(w)
    JOINT.new('grip_palm_r').set_sym('grip_palm_l').label('grip_palm').size(1.0).axis().set_rgb(rgb_socket).end(w)
    JOINT.new('sheath_small_dagger_r').set_sym('sheath_small_dagger_l').label('sheath_small_dagger').size(0.7).axis().set_rgb(rgb_socket).end(w)
    JOINT.new('sheath_back_quiver_r').set_sym('sheath_back_quiver_l').label('sheath_back_quiver').size(0.7).axis().set_rgb(rgb_socket).end(w)
    JOINT.new('sheath_back_bow_r').set_sym('sheath_back_bow_l').label('sheath_back_bow').size(0.7).axis().set_rgb(rgb_socket).end(w)
    JOINT.new('sheath_back_sword_r').set_sym('sheath_back_sword_l').label('sheath_back_sword').size(0.7).axis().set_rgb(rgb_socket).end(w)
    JOINT.new('sheath_back_shield_r').set_sym('sheath_back_shield_l').label('sheath_back_shield').size(0.7).axis().set_rgb(rgb_socket).end(w)


    JOINT.new('tongue1').label('tongue1').size(0.5).set_rgb(rgb_tongue).end(w)
    JOINT.new('tongue2').label('tongue2').size(0.45).set_rgb(rgb_tongue).end(w)
    JOINT.new('tongue3').label('tongue3').size(0.4).set_rgb(rgb_tongue).end(w)
    JOINT.new('tongue4').label('tongue4').size(0.35).set_rgb(rgb_tongue).end(w)
    JOINT.new('tongue5').label('tongue5').size(0.3).set_rgb(rgb_tongue).end(w)

    JOINT.new('jaw').label('jaw').size(0.4).set_rgb(rgb_face).end(w)
    JOINT.new('eye_r').set_sym('eye_l').label('eye').size(0.6).axis().set_rgb(rgb_face).end(w)
    JOINT.new('ear_r').set_sym('ear_l').label('ear').size(0.6).axis().set_rgb(rgb_face).end(w)
    JOINT.new('chin').label('chin').size(0.4).set_rgb(rgb_face).end(w)
    JOINT.new('lip_upper_center').label('lip_upper_center').size(0.4).set_rgb(rgb_face).end(w)
    JOINT.new('lip_upper1_r').set_sym('lip_upper1_l').label('lip_upper1').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('lip_upper2_r').set_sym('lip_upper2_l').label('lip_upper2').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('lip_upper3_r').set_sym('lip_upper3_l').label('lip_upper3').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('lip_lower_center').label('lip_lower_center').size(0.4).set_rgb(rgb_face).end(w)
    JOINT.new('lip_lower1_r').set_sym('lip_lower1_l').label('lip_lower1').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('lip_lower2_r').set_sym('lip_lower2_l').label('lip_lower2').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('lip_lower3_r').set_sym('lip_lower3_l').label('lip_lower3').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('lip_corner_r').set_sym('lip_corner_l').label('lip_corner').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('philtrum').label('philtrum').size(0.4).set_rgb(rgb_face).end(w)
    JOINT.new('nostril').label('nostril').size(0.4).set_rgb(rgb_face).end(w)
    JOINT.new('cheek_r').set_sym('cheek_l').label('cheek').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('cheekbone_r').set_sym('cheekbone_l').label('cheekbone').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('laughline_r').set_sym('laughline_l').label('laughline').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('squint_r').set_sym('squint_l').label('squint').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('eyelid_lower1_r').set_sym('eyelid_lower1_l').label('eyelid_lower1').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('eyelid_lower2_r').set_sym('eyelid_lower2_l').label('eyelid_lower2').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('eyelid_lower3_r').set_sym('eyelid_lower3_l').label('eyelid_lower3').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('eyelid_upper1_r').set_sym('eyelid_upper1_l').label('eyelid_upper1').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('eyelid_upper2_r').set_sym('eyelid_upper2_l').label('eyelid_upper2').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('eyelid_upper3_r').set_sym('eyelid_upper3_l').label('eyelid_upper3').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('brow_center').label('brow_center').size(0.4).set_rgb(rgb_face).end(w)
    JOINT.new('brow1_r').set_sym('brow1_l').label('brow1').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('brow2_r').set_sym('brow2_l').label('brow2').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('brow3_r').set_sym('brow3_l').label('brow3').size(0.2).axis().set_rgb(rgb_face).end(w)
    JOINT.new('brow4_r').set_sym('brow4_l').label('brow4').size(0.2).axis().set_rgb(rgb_face).end(w)

    JOINT.new('genm').label('genm').size(0.4).set_rgb(rgb_genm).end(w)
    JOINT.new('scro_r').set_sym('scro_l').label('scro').size(1.0).axis().set_rgb(rgb_genm).end(w)
    JOINT.new('shaft1').label('shaft1').size(0.7).set_rgb(rgb_genm).end(w)
    JOINT.new('shaft2').label('shaft2').size(0.7).set_rgb(rgb_genm).end(w)
    JOINT.new('shaft3').label('shaft3').size(0.7).set_rgb(rgb_genm).end(w)
    JOINT.new('shaft4').label('shaft4').size(0.7).set_rgb(rgb_genm).end(w)
    JOINT.new('shaft5').label('shaft5').size(0.7).set_rgb(rgb_genm).end(w)

    JOINT.new('genf').label('genm').size(0.5).set_rgb(rgb_genf).end(w)
    JOINT.new('stim').label('stim').size(0.3).set_rgb(rgb_genf).end(w)
    JOINT.new('lab1_r').set_sym('lab1_l').label('lab1').size(0.2).axis().set_rgb(rgb_genf).end(w)
    JOINT.new('lab2_r').set_sym('lab2_l').label('lab2').size(0.2).set_rgb(rgb_genf).end(w)
    JOINT.new('lab3_r').set_sym('lab3_l').label('lab3').size(0.2).set_rgb(rgb_genf).end(w)
    JOINT.new('lab4_r').set_sym('lab4_l').label('lab4').size(0.2).set_rgb(rgb_genf).end(w)
    JOINT.new('vay_r').set_sym('vay_l').label('vay_side').size(0.2).set_rgb(rgb_genf).end(w)
    JOINT.new('vay_u').label('vay_upper').size(0.2).set_rgb(rgb_genf).end(w)
    JOINT.new('vay_d').label('vay_lower').size(0.2).set_rgb(rgb_genf).end(w)

    JOINT.new('gena').label('gena').size(0.5).set_rgb(rgb_gena).end(w)
    JOINT.new('ori_r').set_sym('ori_l').label('ori_side').size(0.2).axis().set_rgb(rgb_gena).end(w)
    JOINT.new('ori_u').label('ori_upper').size(0.2).set_rgb(rgb_gena).end(w)
    JOINT.new('ori_d').label('ori_lower').size(0.2).set_rgb(rgb_gena).end(w)

    JOINT.new('cam1').label('cam1').size(1.0).set_rgb(rgb_special).end(w)
    JOINT.new('cam2').label('cam1').size(1.0).set_rgb(rgb_special).end(w)
    JOINT.new('cam3').label('cam1').size(1.0).set_rgb(rgb_special).end(w)

    JOINT.new('poi1').label('poi1').size(1.0).set_rgb(rgb_special).end(w)
    JOINT.new('poi2').label('poi2').size(1.0).set_rgb(rgb_special).end(w)
    JOINT.new('poi3').label('poi3').size(1.0).set_rgb(rgb_special).end(w)

    JOINT.new('item1').label('item1').size(1.0).set_rgb(rgb_special).end(w)
    JOINT.new('item2').label('item2').size(1.0).set_rgb(rgb_special).end(w)
    JOINT.new('item3').label('item3').size(1.0).set_rgb(rgb_special).end(w)
    JOINT.new('item4').label('item4').size(1.0).set_rgb(rgb_special).end(w)

    JOINT.new('poi_rear').label('poi_rear').size(0.4).set_rgb(rgb_poi).end(w)
    JOINT.new('poi_chest').label('poi_chest').size(0.4).set_rgb(rgb_poi).end(w)

    print("Total Joints Edited: "+str(len(w)))
    print("Crosschecking all joints...")
    joints = cmds.ls(type='joint')

    for j in joints:
       if j not in w:
            print("Missing Joint: "+j)


def onMayaDroppedPythonFile(args):
    init()