import bpy
scene = bpy.context.scene

scene.render.use_color_management = False
scene.gs_ray_depth = 2
scene.gs_shadow_depth = 2
scene.gs_threads = 1
scene.gs_gamma = 2.2
scene.gs_gamma_input = 2.2
scene.gs_tile_size = 32
scene.gs_tile_order = 'random'
scene.gs_auto_threads = True
scene.gs_clay_render = False
scene.gs_draw_params = False
scene.gs_custom_string = ''
scene.gs_premult = False
scene.gs_transp_shad = False
scene.gs_clamp_rgb = False
scene.gs_show_sam_pix = True
scene.gs_z_channel = False
scene.gs_type_render = 'into_blender'
scene.intg_light_method = 'Direct Lighting'
scene.intg_use_caustics = False
scene.intg_photons = 500000
scene.intg_caustic_mix = 100
scene.intg_caustic_depth = 10
scene.intg_caustic_radius = 1.0

# SSS settings
scene.intg_useSSS = False
scene.intg_sssPhotons = 100000
scene.intg_sssDepth = 5
scene.intg_singleScatterSamples = 32
scene.intg_sssScale = 30.0

scene.intg_use_AO = False
scene.intg_AO_samples = 32
scene.intg_AO_distance = 1.0
scene.intg_AO_color = 0.9, 0.9, 0.9
scene.intg_bounces = 4
scene.intg_diffuse_radius = 1.0
scene.intg_cPhotons = 500000
scene.intg_search = 100
scene.intg_final_gather = True
scene.intg_fg_bounces = 3

# Photonmap IC settings
scene.intg_IC_M_Divs = 10
scene.intg_IC_Kappa = 1.0
scene.intg_do_IC = True

# Photonmap GPU settings
scene.intg_ph_leaf_radius = 0.3
scene.intg_ph_candidate_multi = 50
scene.intg_ph_area_multiplier = 6.0
scene.intg_ph_show_cover = False
scene.intg_ph_test_rays = False
scene.intg_ph_benchmark_ray_count = False
scene.intg_ph_benchmark_min_tile_size = 4
scene.intg_ph_work_group_size = 32
scene.intg_fg_OCL = False
scene.intg_ph_method = 1

scene.intg_fg_samples = 16
scene.intg_show_map = False
scene.intg_caustic_method = 'None'
scene.intg_path_samples = 32
scene.intg_no_recursion = False
scene.intg_debug_type = 'dSdV'
scene.intg_show_perturbed_normals = False
scene.intg_pm_ire = False
scene.intg_pass_num = 1000
scene.intg_times = 1.0
scene.intg_photon_radius = 1.0
scene.AA_min_samples = 1
scene.AA_inc_samples = 1
scene.AA_passes = 1
scene.AA_threshold = 0.05
scene.AA_pixelwidth = 1.5
scene.AA_filter_type = 'gauss'
