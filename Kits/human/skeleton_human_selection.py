import maya.cmds as cmds

import skeleton_manager as SKELETON_MANAGER
reload(SKELETON_MANAGER)


def get():

	gmesh = "mesh"

	skel = SKELETON_MANAGER.new()
	skel.add('root').g(gmesh)
	skel.add('hip').g(gmesh)
	skel.add('pelvis').g(gmesh)
	skel.add('spine1').g(gmesh)
	skel.add('spine2').g(gmesh)
	skel.add('spine3').g(gmesh)
	skel.add('spine4').g(gmesh)
	skel.add('spine5').g(gmesh)
	skel.add('neck1').g(gmesh)
	skel.add('neck2').g(gmesh)
	skel.add('head').g(gmesh)
	skel.add('ab_r').g(gmesh)
	skel.add('ab_l').g(gmesh)
	skel.add('spinae_r').g(gmesh)
	skel.add('spinae_l').g(gmesh)
	skel.add('flub_r').g(gmesh)
	skel.add('flub_l').g(gmesh)
	skel.add('belly').g(gmesh)
	skel.add('pooch').g(gmesh)
	skel.add('bulge').g(gmesh)
	skel.add('breath_lower').g(gmesh)
	skel.add('breath_upper').g(gmesh)
	skel.add('breast_r').g(gmesh)
	skel.add('breast_l').g(gmesh)
	skel.add('cup_r').g(gmesh)
	skel.add('cup_l').g(gmesh)
	skel.add('nip_r').g(gmesh)
	skel.add('nip_l').g(gmesh)
	skel.add('pit_r').g(gmesh)
	skel.add('pit_l').g(gmesh)
	skel.add('lat_r').g(gmesh)
	skel.add('lat_l').g(gmesh)
	skel.add('scapula_r').g(gmesh)
	skel.add('scapula_l').g(gmesh)
	skel.add('deltoid_r').g(gmesh)
	skel.add('deltoid_l').g(gmesh)
	skel.add('trap_r').g(gmesh)
	skel.add('trap_l').g(gmesh)
	skel.add('throat').g(gmesh)
	skel.add('clavicle_r').g(gmesh)
	skel.add('clavicle_l').g(gmesh)
	skel.add('lowerarm_r').g(gmesh)
	skel.add('lowerarm_l').g(gmesh)
	skel.add('hand_r').g(gmesh)
	skel.add('hand_l').g(gmesh)
	skel.add('upperarm_twist1_r').g(gmesh)
	skel.add('upperarm_twist1_l').g(gmesh)
	skel.add('upperarm_twist2_r').g(gmesh)
	skel.add('upperarm_twist2_l').g(gmesh)
	skel.add('upperarm_twist3_r').g(gmesh)
	skel.add('upperarm_twist3_l').g(gmesh)
	skel.add('lowerarm_twist1_r').g(gmesh)
	skel.add('lowerarm_twist1_l').g(gmesh)
	skel.add('lowerarm_twist2_r').g(gmesh)
	skel.add('lowerarm_twist2_l').g(gmesh)
	skel.add('lowerarm_twist3_r').g(gmesh)
	skel.add('lowerarm_twist3_l').g(gmesh)
	skel.add('bicep_r').g(gmesh)
	skel.add('bicep_l').g(gmesh)
	skel.add('tricep_r').g(gmesh)
	skel.add('tricep_l').g(gmesh)
	skel.add('brach_r').g(gmesh)
	skel.add('brach_l').g(gmesh)

	skel.add('finger_thumb1_r').g(gmesh)
	skel.add('finger_thumb1_l').g(gmesh)
	skel.add('finger_thumb2_r').g(gmesh)
	skel.add('finger_thumb2_l').g(gmesh)
	skel.add('finger_thumb3_r').g(gmesh)
	skel.add('finger_thumb3_l').g(gmesh)

	skel.add('finger_index1_r').g(gmesh)
	skel.add('finger_index1_l').g(gmesh)
	skel.add('finger_index2_r').g(gmesh)
	skel.add('finger_index2_l').g(gmesh)
	skel.add('finger_index3_r').g(gmesh)
	skel.add('finger_index3_l').g(gmesh)

	skel.add('finger_middle1_r').g(gmesh)
	skel.add('finger_middle1_l').g(gmesh)
	skel.add('finger_middle2_r').g(gmesh)
	skel.add('finger_middle2_l').g(gmesh)
	skel.add('finger_middle3_r').g(gmesh)
	skel.add('finger_middle3_l').g(gmesh)

	skel.add('finger_ring1_r').g(gmesh)
	skel.add('finger_ring1_l').g(gmesh)
	skel.add('finger_ring2_r').g(gmesh)
	skel.add('finger_ring2_l').g(gmesh)
	skel.add('finger_ring3_r').g(gmesh)
	skel.add('finger_ring3_l').g(gmesh)

	skel.add('finger_pinky1_r').g(gmesh)
	skel.add('finger_pinky1_l').g(gmesh)
	skel.add('finger_pinky2_r').g(gmesh)
	skel.add('finger_pinky2_l').g(gmesh)
	skel.add('finger_pinky3_r').g(gmesh)
	skel.add('finger_pinky3_l').g(gmesh)


	skel.add('thigh_r').g(gmesh)
	skel.add('thigh_l').g(gmesh)
	skel.add('shin_r').g(gmesh)
	skel.add('shin_l').g(gmesh)
	skel.add('foot_r').g(gmesh)
	skel.add('foot_l').g(gmesh)
	skel.add('ball_r').g(gmesh)
	skel.add('ball_l').g(gmesh)
	skel.add('toetip_r').g(gmesh)
	skel.add('toetip_l').g(gmesh)
	skel.add('heel_r').g(gmesh)
	skel.add('heel_l').g(gmesh)


	skel.add('thigh_twist1_r').g(gmesh)
	skel.add('thigh_twist1_l').g(gmesh)
	skel.add('thigh_twist2_r').g(gmesh)
	skel.add('thigh_twist2_l').g(gmesh)
	skel.add('shin_twist1_r').g(gmesh)
	skel.add('shin_twist1_l').g(gmesh)
	skel.add('shin_twist2_r').g(gmesh)
	skel.add('shin_twist2_l').g(gmesh)

	skel.add('glute_r').g(gmesh)
	skel.add('glute_l').g(gmesh)

	skel.add('glute_inner_r').g(gmesh)
	skel.add('glute_inner_l').g(gmesh)
	skel.add('glute_bottom_r').g(gmesh)
	skel.add('glute_bottom_l').g(gmesh)
	skel.add('glute_cheek_r').g(gmesh)
	skel.add('glute_cheek_l').g(gmesh)
	skel.add('glute_outer_r').g(gmesh)
	skel.add('glute_outer_l').g(gmesh)

	skel.add('quad_r').g(gmesh)
	skel.add('quad_l').g(gmesh)
	skel.add('adductor_r').g(gmesh)
	skel.add('adductor_l').g(gmesh)
	skel.add('ham_r').g(gmesh)
	skel.add('ham_l').g(gmesh)
	skel.add('calf_inner_r').g(gmesh)
	skel.add('calf_inner_l').g(gmesh)
	skel.add('calf_outer_r').g(gmesh)
	skel.add('calf_outer_l').g(gmesh)

	skel.add('toe_big1_r').g(gmesh)
	skel.add('toe_big1_l').g(gmesh)
	skel.add('toe_big2_r').g(gmesh)
	skel.add('toe_big2_l').g(gmesh)

	skel.add('toe_long1_r').g(gmesh)
	skel.add('toe_long1_l').g(gmesh)
	skel.add('toe_long2_r').g(gmesh)
	skel.add('toe_long2_l').g(gmesh)

	skel.add('toe_middle1_r').g(gmesh)
	skel.add('toe_middle1_l').g(gmesh)
	skel.add('toe_middle2_r').g(gmesh)
	skel.add('toe_middle2_l').g(gmesh)

	skel.add('toe_ring1_r').g(gmesh)
	skel.add('toe_ring1_l').g(gmesh)
	skel.add('toe_ring2_r').g(gmesh)
	skel.add('toe_ring2_l').g(gmesh)

	skel.add('toe_little1_r').g(gmesh)
	skel.add('toe_little1_l').g(gmesh)
	skel.add('toe_little2_r').g(gmesh)
	skel.add('toe_little2_l').g(gmesh)

	skel.add('sheath_hip_sword_r').g(gmesh)
	skel.add('sheath_hip_sword_l').g(gmesh)
	skel.add('sheath_small_dagger_r').g(gmesh)
	skel.add('sheath_small_dagger_l').g(gmesh)
	skel.add('sheath_back_shield_r').g(gmesh)
	skel.add('sheath_back_shield_l').g(gmesh)
	skel.add('sheath_back_quiver_r').g(gmesh)
	skel.add('sheath_back_quiver_l').g(gmesh)
	skel.add('sheath_back_bow_r').g(gmesh)
	skel.add('sheath_back_bow_l').g(gmesh)
	skel.add('sheath_back_sword_r').g(gmesh)
	skel.add('sheath_back_sword_l').g(gmesh)
	skel.add('grip_palm_r').g(gmesh)
	skel.add('grip_palm_l').g(gmesh)
	skel.add('grip_shield_r').g(gmesh)
	skel.add('grip_shield_l').g(gmesh)

	skel.add('socket_headwear').g(gmesh)

	skel.add('tongue1').g(gmesh)
	skel.add('tongue2').g(gmesh)
	skel.add('tongue3').g(gmesh)
	skel.add('tongue4').g(gmesh)
	skel.add('tongue5').g(gmesh)

	skel.add('eye_r').g(gmesh)
	skel.add('eye_l').g(gmesh)

	skel.add('ear_r').g(gmesh)
	skel.add('ear_l').g(gmesh)

	skel.add('jaw').g(gmesh)
	skel.add('chin').g(gmesh)
	skel.add('philtrum').g(gmesh)
	skel.add('nostril').g(gmesh)
	skel.add('squint_r').g(gmesh)
	skel.add('squint_l').g(gmesh)
	skel.add('cheek_r').g(gmesh)
	skel.add('cheek_l').g(gmesh)
	skel.add('cheekbone_r').g(gmesh)
	skel.add('cheekbone_l').g(gmesh)

	skel.add('eyelid_lower1_r').g(gmesh)
	skel.add('eyelid_lower1_l').g(gmesh)
	skel.add('eyelid_lower2_r').g(gmesh)
	skel.add('eyelid_lower2_l').g(gmesh)
	skel.add('eyelid_lower3_r').g(gmesh)
	skel.add('eyelid_lower3_l').g(gmesh)

	skel.add('eyelid_upper1_r').g(gmesh)
	skel.add('eyelid_upper1_l').g(gmesh)
	skel.add('eyelid_upper2_r').g(gmesh)
	skel.add('eyelid_upper2_l').g(gmesh)
	skel.add('eyelid_upper3_r').g(gmesh)
	skel.add('eyelid_upper3_l').g(gmesh)

	skel.add('lip_lower_center').g(gmesh)

	skel.add('lip_lower1_r').g(gmesh)
	skel.add('lip_lower1_l').g(gmesh)
	skel.add('lip_lower2_r').g(gmesh)
	skel.add('lip_lower2_l').g(gmesh)
	skel.add('lip_lower3_r').g(gmesh)
	skel.add('lip_lower3_l').g(gmesh)

	skel.add('lip_upper_center').g(gmesh)

	skel.add('lip_upper1_r').g(gmesh)
	skel.add('lip_upper1_l').g(gmesh)
	skel.add('lip_upper2_r').g(gmesh)
	skel.add('lip_upper2_l').g(gmesh)
	skel.add('lip_upper3_r').g(gmesh)
	skel.add('lip_upper3_l').g(gmesh)

	skel.add('lip_corner_r').g(gmesh)
	skel.add('lip_corner_l').g(gmesh)

	skel.add('laughline_r').g(gmesh)
	skel.add('laughline_l').g(gmesh)

	skel.add('brow_center').g(gmesh)
	skel.add('brow1_r').g(gmesh)
	skel.add('brow1_l').g(gmesh)
	skel.add('brow2_r').g(gmesh)
	skel.add('brow2_l').g(gmesh)
	skel.add('brow3_r').g(gmesh)
	skel.add('brow3_l').g(gmesh)
	skel.add('brow4_r').g(gmesh)
	skel.add('brow4_l').g(gmesh)

	skel.add('cam1').g(gmesh)
	skel.add('cam2').g(gmesh)
	skel.add('cam3').g(gmesh)

	skel.add('poi1').g(gmesh)
	skel.add('poi2').g(gmesh)
	skel.add('poi3').g(gmesh)

	skel.add('poi_rear').g(gmesh)
	skel.add('poi_chest').g(gmesh)

	skel.add('item1').g(gmesh)
	skel.add('item2').g(gmesh)
	skel.add('item3').g(gmesh)
	skel.add('item4').g(gmesh)

	skel.add('scro_r').g(gmesh)
	skel.add('scro_l').g(gmesh)
	skel.add('shaft1').g(gmesh)
	skel.add('shaft2').g(gmesh)
	skel.add('shaft3').g(gmesh)
	skel.add('shaft4').g(gmesh)
	skel.add('shaft5').g(gmesh)

	skel.add('genf').g(gmesh)
	skel.add('lab1_r').g(gmesh)
	skel.add('lab1_l').g(gmesh)
	skel.add('lab2_r').g(gmesh)
	skel.add('lab2_l').g(gmesh)
	skel.add('lab3_r').g(gmesh)
	skel.add('lab3_l').g(gmesh)
	skel.add('lab4_r').g(gmesh)
	skel.add('lab4_l').g(gmesh)
	skel.add('vay_r').g(gmesh)
	skel.add('vay_l').g(gmesh)
	skel.add('vay_u').g(gmesh)
	skel.add('vay_d').g(gmesh)
	skel.add('stim').g(gmesh)

	skel.add('gena').g(gmesh)
	skel.add('ori_r').g(gmesh)
	skel.add('ori_l').g(gmesh)
	skel.add('ori_u').g(gmesh)
	skel.add('ori_d').g(gmesh)

	return skel