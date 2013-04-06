# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import bpy
from sys import platform
from bpy.props import (IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       BoolProperty,
                       StringProperty)

Scene = bpy.types.Scene


# set fileformat for image saving on same format as in YafaRay, both have default PNG
def call_update_fileformat(self, context):
    scene = context.scene
    render = scene.render
    if scene.img_output is not render.image_settings.file_format:
        render.image_settings.file_format = scene.img_output
        if render.image_settings.file_format == "OPEN_EXR" and scene.gs_z_channel:
            render.image_settings.use_zbuffer = True


def register():
    # Default Gamma values for Windows = 2.2, for Linux and MacOS = 1.8
    if platform == "win32":
        gamma = 2.20
    else:
        gamma = 1.80

    ########### YafaRays general settings properties #############
    Scene.gs_ray_depth = IntProperty(
        name="Ray depth",
        description="Maximum depth for recursive raytracing",
        min=0, max=64, default=2)

    Scene.gs_shadow_depth = IntProperty(
        name="Shadow depth",
        description="Max. depth for transparent shadows calculation (if enabled)",
        min=0, max=64, default=2)

    Scene.gs_threads = IntProperty(
        name="Threads",
        description="Number of threads to use for rendering",
        min=1, default=1)

    Scene.gs_gamma = FloatProperty(
        name="Gamma",
        description="Gamma correction applied to final output, inverse correction "
                    "of textures and colors is performed",
        min=0, max=5, default=gamma)

    Scene.gs_gamma_input = FloatProperty(
        name="Gamma input",
        description="Gamma correction applied to input",
        min=0, max=5, default=gamma)

    Scene.gs_tile_size = IntProperty(
        name="Tile size",
        description="Size of the render buckets (tiles)",
        min=0, max=1024, default=32)

    Scene.gs_tile_order = EnumProperty(
        name="Tile order",
        description="Selects tiles order type",
        items=(
            ('linear', "Linear", ""),
            ('random', "Random", "")
        ),
        default='random')

    Scene.gs_auto_threads = BoolProperty(
        name="Auto threads",
        description="Activate thread number auto detection",
        default=True)

    Scene.gs_clay_render = BoolProperty(
        name="Render clay",
        description="Override all materials with a white diffuse material",
        default=False)

    # added clay color property
    Scene.gs_clay_col = FloatVectorProperty(
        name="Clay color",
        description="Color of clay render material",
        subtype='COLOR',
        min=0.0, max=1.0,
        default=(0.8, 0.8, 0.8))

    Scene.gs_mask_render = BoolProperty(
        name="Render mask",
        description="Renders an object mask pass with different colors",
        default=False)

    Scene.gs_draw_params = BoolProperty(
        name="Draw parameters",
        description="Write the render parameters below the image",
        default=False)
        
    Scene.transparent_background = BoolProperty(
        name="Transparent Background",
        description="Render the background as Transparent",
        default=True)

    Scene.gs_custom_string = StringProperty(
        name="Custom string",
        description="Custom string will be added to the info bar, "
                    "use it for CPU, RAM etc",
        default="")

    Scene.gs_premult = BoolProperty(
        name="Premultiply",
        description="Premultipy Alpha channel for renders with transparent background",
        default=False)

    Scene.gs_transp_shad = BoolProperty(
        name="Transparent shadows",
        description="Compute transparent shadows",
        default=False)

    Scene.gs_clamp_rgb = BoolProperty(
        name="Clamp RGB",
        description="Reduce the color's brightness to a low dynamic range",
        default=False)

    Scene.gs_show_sam_pix = BoolProperty(
        name="Show sample pixels",
        description="Masks pixels marked for resampling during adaptive passes",
        default=True)

    Scene.gs_z_channel = BoolProperty(
        name="Render depth map",
        description="Render depth map (Z-Buffer)",
        default=False)

    Scene.gs_verbose = BoolProperty(
        name="Log info to console",
        description="Print YafaRay engine log messages in console window",
        default=True)

    Scene.gs_type_render = EnumProperty(
        name="Render",
        description="Choose the render output method",
        items=(
            ('file', "Image file", "Render the Scene and write it to an Image File when finished"),
            ('into_blender', "Into Blender", "Render the Scene into Blenders Renderbuffer"),
            ('xml', "XML file", "Export the Scene to a XML File")
        ),
        default='into_blender')

    ######### YafaRays own image output property ############
    Scene.img_output = EnumProperty(
        name="Image File Type",
        description="Image will be saved in this file format",
        items=(
            ('PNG', " PNG (Portable Network Graphics)", ""),
            ('TARGA', " TGA (Truevision TARGA)", ""),
            ('JPEG', " JPEG (Joint Photographic Experts Group)", ""),
            ('TIFF', " TIFF (Tag Image File Format)", ""),
            ('OPEN_EXR', " EXR (IL&M OpenEXR)", ""),
            ('HDR', " HDR (Radiance RGBE)", "")
        ),
        default='PNG', update=call_update_fileformat)

    ########### YafaRays integrator properties #############
    Scene.intg_light_method = EnumProperty(
        name="Lighting Method",
        items=(
            ('Direct Lighting', "Direct Lighting", ""),
            #('Direct Lighting IC', "Direct Lighting IC", ""),
            ('Photon Mapping', "Photon Mapping", ""),
            #('Photon Mapping IC', "Photon Mapping IC", ""),
            ('Photon Mapping GPU', "Photon Mapping GPU", ""),
            ('Pathtracing', "Pathtracing", ""),
            ('Debug', "Debug", ""),
            ('Bidirectional', "Bidirectional", ""),
            ('SPPM', "SPPM", "")
        ),
        default='Direct Lighting')

    Scene.intg_use_caustics = BoolProperty(
        name="Caustic Photons",
        description="Enable photon map for caustics only",
        default=False)

    Scene.intg_photons = IntProperty(
        name="Photons",
        description="Number of photons to be shot",
        min=1, max=100000000,
        default=500000)

    Scene.intg_caustic_mix = IntProperty(
        name="Caustic Mix",
        description="Max. number of photons to mix (blur)",
        min=1, max=10000,
        default=100)

    Scene.intg_caustic_depth = IntProperty(
        name="Caustic Depth",
        description="Max. number of scatter events for photons",
        min=0, max=50,
        default=10)

    Scene.intg_caustic_radius = FloatProperty(
        name="Caustic Radius",
        description="Max. radius to search for photons",
        min=0.0001, max=100.0,
        default=1.0)

    Scene.intg_use_AO = BoolProperty(
        name="Ambient Occlusion",
        description="Enable ambient occlusion",
        default=False)

    Scene.intg_AO_samples = IntProperty(
        name="Samples",
        description="Number of samples for ambient occlusion",
        min=1, max=1000,
        default=32)

    Scene.intg_AO_distance = FloatProperty(
        name="Distance",
        description=("Max. occlusion distance,"
                     " Surfaces further away do not occlude ambient light"),
        min=0.0, max=10000.0,
        default=1.0)

    Scene.intg_AO_color = FloatVectorProperty(
        name="AO Color",
        description="Color Settings", subtype='COLOR',
        min=0.0, max=1.0,
        default=(0.9, 0.9, 0.9))

    Scene.intg_bounces = IntProperty(
        name="Depth",
        description="",
        min=1,
        default=4)

    Scene.intg_diffuse_radius = FloatProperty(
        name="Search radius",
        description="Radius to search for diffuse photons",
        min=0.001,
        default=1.0)

    Scene.intg_cPhotons = IntProperty(
        name="Count",
        description="Number of caustic photons to be shot",
        min=1, default=500000)

    Scene.intg_search = IntProperty(
        name="Search count",
        description="Maximum number of diffuse photons to be filtered",
        min=1, max=10000,
        default=100)

    Scene.intg_final_gather = BoolProperty(
        name="Final Gather",
        description="Use final gathering (recommended)",
        default=True)
    
    # Photonmap IC settings /--------------------------------------->
    Scene.intg_do_IC = BoolProperty(
        name="Use Irradiance Cache",
        description="Enable the use of Irradiance Cache",
        default=True)

    Scene.intg_IC_M_Divs = IntProperty(
        name="Max Samples",
        description="Maximum number of samples per IC record",
        min=1, max=50,
        default=10)

    Scene.intg_IC_Kappa = FloatProperty(
        name="Accuracy",
        description="The higher the value the smaller the IC record radius",
        min=0.1, max=3,
        default=1)

    # Photonmap GPU settings

    Scene.intg_ph_leaf_radius = FloatProperty(
        name="Disk Radius",
        description="The radius of the disks generated on the triangles in the scene",
        min=0.0001, max=1000.0,
        default=0.3)

    Scene.intg_ph_candidate_multi = IntProperty(
        name="Point Candidantes",
        description="Number of candidates for each point sample in best candidate sampling",
        min=10, max=100,
        default=50)        

    Scene.intg_ph_area_multiplier = FloatProperty(
        name="Area Multiplier",
        description="Number of disks to generate per unit area",
        min=0.1, max=50.0,
        default=6.0)        

    Scene.intg_ph_show_cover = BoolProperty(
        name="Show Cover",
        description="Preview the scene color coded by intersection errors (gray - good, green - background, red - wrong triangle or point, blue - didn't hit but should, pink - hit but shouldn't have)",
        default=False)

    Scene.intg_ph_test_rays = BoolProperty(
        name="Test Intersections",
        description="Compare the intersections computed in OpenCL with a reference",
        default=False)

    Scene.intg_ph_benchmark_ray_count = BoolProperty(
        name="Benchmark",
        description="Run benchmarking tests",
        default=False)
        
    Scene.intg_ph_benchmark_min_tile_size = IntProperty(
        name="Min Tile Size",
        description="Minimal tile size for benchmarking",
        min=1, max=10000,
        default=4)       

    Scene.intg_ph_work_group_size = IntProperty(
        name="Work Unit Number",
        description="Depends on GPU working units available",
        min=1, max=2048,
        default=32)   
        
    Scene.intg_fg_OCL = BoolProperty(
        name="OpenCL Final Gather",
        description="Use OpenCL for Final Gather",
        default=False)        

    Scene.intg_ph_method = EnumProperty(
        name="Intersection method",
        description="Choose GPU intersection method",
        items=(
            ('Triangle', "Triangle", ""),
            ('Sphere Hierarchy', "Sphere Hierarchy", ""),
            ('Disk culled', "Disk culled", ""),
            ('Sphere Hierarchy VEC', "Sphere Hierarchy VEC", ""),
            ('Triangle VEC', "Triangle VEC", "")
        ),
        default='Disk culled')
    #----------------------------------->    
    Scene.intg_fg_bounces = IntProperty(
        name="Bounces",
        description="Allow gather rays to extend to paths of this length",
        min=1, max=20,
        default=3)

    Scene.intg_fg_samples = IntProperty(
        name="Samples",
        description="Number of samples for final gathering",
        min=1,
        default=16)

    Scene.intg_show_map = BoolProperty(
        name="Show radiance map",
        description="Directly show radiance map, useful to calibrate the photon map (disables final gathering step)",
        default=False)

    Scene.intg_caustic_method = EnumProperty(
        name="Caustic Method",
        items=(
            ('None', "None", ""),
            ('Path', "Path", ""),
            ('Path+Photon', "Path+Photon", ""),
            ('Photon', "Photon", "")),
        description="Choose caustic rendering method",
        default='None')

    Scene.intg_path_samples = IntProperty(
        name="Path Samples",
        description="Number of path samples per pixel sample",
        min=1,
        default=32)

    Scene.intg_no_recursion = BoolProperty(
        name="No Recursion",
        description="No recursive raytracing, only pure path tracing",
        default=False)
    
    # SSS settings ----------------------->
    Scene.intg_useSSS = BoolProperty(
        name="Use SSS",
        description="Enable SSS photon map",
        default=False)

    Scene.intg_sssPhotons = IntProperty(
        name="SSS Photons",
        description="Number of SSS photons to be shot",
        min=1, max=100000000,
        default=100000)

    Scene.intg_sssDepth = IntProperty(
        name="SSS Depth",
        description="Max. number of photon scattering events",
        min=1, max=64,
        default=5)

    Scene.intg_singleScatterSamples = IntProperty(
        name="Single Scattering Samples",
        description="Number of samples for single scattering estimation",
        min=0, max=256,
        default=32)

    Scene.intg_sssScale = FloatProperty(
        name="Scale",
        description="Scale factor that helps fixing the unit scale, in case 1 blender is not equal to 1 meter",
        min=0.0001, max=1000.0,
        default=30.0)
    #-------------------------------->
    Scene.intg_debug_type = EnumProperty(
        name="Debug type",
        items=(
            ('N', "N", ""),
            ('dPdU', "dPdU", ""),
            ('dPdV', "dPdV", ""),
            ('NU', "NU", ""),
            ('NV', "NV", ""),
            ('dSdU', "dSdU", ""),
            ('dSdV', "dSdV", "")),
        default='dSdV')

    Scene.intg_show_perturbed_normals = BoolProperty(
        name="Show perturbed normals",
        description="Show the normals perturbed by bump and normal maps",
        default=False)

    Scene.intg_pm_ire = BoolProperty(
        name="PM IRE",
        default=False)

    Scene.intg_pass_num = IntProperty(
        name="Passes",
        min=1,
        default=1000)

    Scene.intg_times = FloatProperty(
        name="Radius factor",
        min=0.0,
        default=1.0)

    Scene.intg_photon_radius = FloatProperty(
        name="Search radius",
        min=0.0,
        default=1.0)

    ######### YafaRays anti-aliasing properties ###########
    Scene.AA_min_samples = IntProperty(
        name="Samples",
        description="Number of samples for first AA pass",
        min=1,
        default=1)

    Scene.AA_inc_samples = IntProperty(
        name="Additional Samples",
        description="Number of samples for additional AA passes",
        min=1,
        default=1)

    Scene.AA_passes = IntProperty(
        name="Passes",
        description=("Number of anti-aliasing passes,"
                     " Adaptive sampling (passes > 1) uses different pattern"),
        min=1,
        default=1)

    Scene.AA_threshold = FloatProperty(
        name="Threshold",
        description="Color threshold for additional AA samples in next pass",
        min=0.0, max=1.0, precision=4,
        default=0.05)

    Scene.AA_pixelwidth = FloatProperty(
        name="Pixelwidth",
        description="AA filter size",
        min=1.0, max=20.0, precision=3,
        default=1.5)

    Scene.AA_filter_type = EnumProperty(
        name="Filter",
        items=(
            ('box', "Box", "AA filter type"),
            ('mitchell', "Mitchell", "AA filter type"),
            ('gauss', "Gauss", "AA filter type"),
            ('lanczos', "Lanczos", "AA filter type")
        ),
        default="gauss")


def unregister():
    Scene.gs_ray_depth
    Scene.gs_shadow_depth
    Scene.gs_threads
    Scene.gs_gamma
    Scene.gs_gamma_input
    Scene.gs_tile_size
    Scene.gs_tile_order
    Scene.gs_auto_threads
    Scene.gs_clay_render
    Scene.gs_clay_col
    Scene.gs_mask_render
    Scene.gs_draw_params
    Scene.gs_custom_string
    Scene.gs_premult
    Scene.gs_transp_shad
    Scene.gs_clamp_rgb
    Scene.gs_show_sam_pix
    Scene.gs_z_channel
    Scene.gs_verbose
    Scene.gs_type_render

    Scene.img_output

    Scene.intg_light_method
    Scene.intg_use_caustics
    Scene.intg_photons
    Scene.intg_caustic_mix
    Scene.intg_caustic_depth
    Scene.intg_caustic_radius
    Scene.intg_use_AO
    Scene.intg_AO_samples
    Scene.intg_AO_distance
    Scene.intg_AO_color
    Scene.intg_bounces
    Scene.intg_diffuse_radius
    Scene.intg_cPhotons
    Scene.intg_search
    Scene.intg_final_gather
    Scene.intg_fg_bounces
    Scene.intg_fg_samples
    Scene.intg_show_map
    Scene.intg_caustic_method
    Scene.intg_path_samples
    Scene.intg_no_recursion
    Scene.intg_debug_type
    Scene.intg_show_perturbed_normals
    Scene.intg_pm_ire
    Scene.intg_pass_num
    Scene.intg_times
    Scene.intg_photon_radius

    Scene.AA_min_samples
    Scene.AA_inc_samples
    Scene.AA_passes
    Scene.AA_threshold
    Scene.AA_pixelwidth
    Scene.AA_filter_type
    
    ##-- IC values
    Scene.intg_do_IC
    Scene.intg_IC_M_Divs
    Scene.intg_IC_Kappa

    #-- gpu

    Scene.intg_ph_leaf_radius
    Scene.intg_ph_candidate_multi
    Scene.intg_ph_area_multiplier
    Scene.intg_ph_show_cover
    Scene.intg_ph_test_rays
    Scene.intg_ph_benchmark_ray_count
    Scene.intg_ph_benchmark_min_tile_size
    Scene.intg_ph_work_group_size
    Scene.intg_fg_OCL
    Scene.intg_ph_method

    #/--- SSS

    Scene.intg_useSSS
    Scene.intg_sssPhotons
    Scene.intg_sssDepth
    Scene.intg_singleScatterSamples
    Scene.intg_sssScale
