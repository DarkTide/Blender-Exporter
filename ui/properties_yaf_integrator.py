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
from bpy.types import Panel
from bl_ui.properties_render import RenderButtonsPanel

RenderButtonsPanel.COMPAT_ENGINES = {'YAFA_RENDER'}


class YAF_PT_render(RenderButtonsPanel, Panel):
    bl_label = "Integrator"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "intg_light_method")
        # test
        doSSS = False

        if scene.intg_light_method == "Direct Lighting":
            row = layout.row()
            col = row.column(align=True)
            col.prop(scene, "intg_use_caustics", toggle=True)
            if scene.intg_use_caustics:
                col.prop(scene, "intg_caustic_depth")
                col.prop(scene, "intg_photons")
                col.prop(scene, "intg_caustic_radius")
                col.prop(scene, "intg_caustic_mix")

            col = row.column(align=True)
            col.prop(scene, "intg_use_AO", toggle=True)
            if scene.intg_use_AO:
                col.prop(scene, "intg_AO_color")
                col.prop(scene, "intg_AO_samples")
                col.prop(scene, "intg_AO_distance")
            #
            col = layout.column(align=True)
            col.prop(scene, "intg_do_IC", toggle=True)
            if scene.intg_do_IC:
                col.prop(scene, "intg_IC_M_Divs")
                col.prop(scene, "intg_IC_Kappa")
            #
            doSSS = True

        elif scene.intg_light_method == "Photon Mapping":
            row = layout.row()

            row.prop(scene, "intg_bounces")

            row = layout.row()
            col = row.column(align=True)
            col.label(" Diffuse Photons:", icon='MOD_PHYSICS')
            col.prop(scene, "intg_photons")
            col.prop(scene, "intg_diffuse_radius")
            col.prop(scene, "intg_search")

            col = row.column(align=True)
            col.label(" Caustic Photons:", icon='MOD_PARTICLES')
            col.prop(scene, "intg_cPhotons")
            col.prop(scene, "intg_caustic_radius")
            col.prop(scene, "intg_caustic_mix")

            row = layout.row()
            row.prop(scene, "intg_final_gather", toggle=True, icon='FORCE_FORCE')

            if scene.intg_final_gather:
                ''' Show options UI for Final Gathering. '''
                col = layout.row()
                col.prop(scene, "intg_fg_bounces")
                col.prop(scene, "intg_fg_samples")
                col = layout.row()
                col.prop(scene, "intg_show_map", toggle=True)
            #
            else:
                ''' Else, show options for Irradiance Cache. '''
                col = layout.column(align=True)
                col.prop(scene, "intg_do_IC", toggle=True)
                if scene.intg_do_IC:
                    col.prop(scene, "intg_IC_M_Divs")
                    col.prop(scene, "intg_IC_Kappa")
            #
            doSSS = True
            '''        
            elif scene.intg_light_method == "Photon Mapping GPU":
            row = layout.row()

            row.prop(scene, "intg_bounces")

            row = layout.row()

            col = row.column(align=True)
            col.label(" Diffuse Photons:", icon='MOD_PHYSICS')
            col.prop(scene, "intg_photons")
            col.prop(scene, "intg_diffuse_radius")
            col.prop(scene, "intg_search")

            col = row.column(align=True)
            col.label(" Caustic Photons:", icon='MOD_PARTICLES')
            col.prop(scene, "intg_cPhotons")
            col.prop(scene, "intg_caustic_radius")
            col.prop(scene, "intg_caustic_mix")

            row = layout.row()
            row.prop(scene, "intg_show_map", toggle=True)

            row = layout.row()
            row.label("OpenCL Settings:")

            row = layout.row()
            row.prop(scene, "intg_ph_method")
            
            row = layout.row()
            row.prop(scene, "intg_ph_leaf_radius")
            row.prop(scene, "intg_ph_candidate_multi")
            
            row = layout.row()
            row.prop(scene, "intg_ph_area_multiplier")
            
            row = layout.row()
            row.prop(scene, "intg_fg_OCL", toggle=True)

            row = layout.row()
            row.prop(scene, "intg_ph_show_cover")
            row.prop(scene, "intg_ph_test_rays")
            row.prop(scene, "intg_ph_benchmark_ray_count")
            
            row = layout.row()
            row.prop(scene, "intg_ph_benchmark_min_tile_size")
            row.prop(scene, "intg_ph_work_group_size")
            
            doSSS = True
            '''
        elif scene.intg_light_method == "Pathtracing":
            col = layout.row()
            col.prop(scene, "intg_caustic_method")

            col = layout.row()

            if scene.intg_caustic_method in {"Path+Photon", "Photon"}:
                col.prop(scene, "intg_photons", text="Photons")
                col.prop(scene, "intg_caustic_mix", text="Caus. Mix")
                col = layout.row()
                col.prop(scene, "intg_caustic_depth", text="Caus. Depth")
                col.prop(scene, "intg_caustic_radius", text="Caus. Radius")

            col = layout.row()
            col.prop(scene, "intg_path_samples")
            col.prop(scene, "intg_bounces")
            row = layout.row()
            row.prop(scene, "intg_no_recursion")
            #
            doSSS = True

        elif scene.intg_light_method == "Debug":
            layout.row().prop(scene, "intg_debug_type")
            layout.row().prop(scene, "intg_show_perturbed_normals")

        elif scene.intg_light_method == "SPPM":
            col = layout.column()
            col.prop(scene, "intg_photons", text="Photons")
            col.prop(scene, "intg_pass_num")
            col.prop(scene, "intg_bounces", text="Bounces")
            col.prop(scene, "intg_times")
            col.prop(scene, "intg_diffuse_radius")
            col.prop(scene, "intg_search")
            col.prop(scene, "intg_pm_ire")
                
        # use for all integers ( if available )
        if doSSS:
            pass
        '''
            col = layout.column(align=True)
            col.prop(scene, "intg_useSSS", toggle=True)
            if scene.intg_useSSS:
                col.prop(scene, "intg_sssPhotons")
                col.prop(scene, "intg_sssDepth")
                col.prop(scene, "intg_singleScatterSamples")
                col.prop(scene, "intg_sssScale")
        '''
        
        

if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
