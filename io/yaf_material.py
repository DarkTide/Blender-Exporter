import bpy
import mathutils
import yafrayinterface

def proj2int(val):
    if val ==   'NONE' : return 0
    elif val == 'X'    : return 1
    elif val == 'Y'    : return 2
    elif val == 'Z'    : return 3

class yafMaterial:
        def __init__(self, interface,mMap):
                self.yi          = interface
                self.materialMap = mMap

        def namehash(self,obj):
                nh = obj.name + "-" + str(obj.__hash__())
                return nh

        def writeTexLayer(self, name, tex_in, ulayer, mtex, chanflag, dcol):
            if chanflag == 0:
                return False

            yi = self.yi
            yi.paramsPushList()
            yi.paramsSetString("element", "shader_node")
            yi.paramsSetString("type", "layer")
            yi.paramsSetString("name", name)

            yi.paramsSetString("input", tex_in)# SEE the defination later

            #mtex is an instance of MaterialTextureSlot class


            mode = 0
            if mtex.blend_type == 'MIX':
                mode = 0
            elif mtex.blend_type == 'ADD':
                mode = 1
            elif mtex.blend_type == 'MULTIPLY':
                mode = 2
            elif mtex.blend_type == 'SUBTRACT':
                mode = 3
            elif mtex.blend_type == 'SCREEN':
                mode = 4
            elif mtex.blend_type == 'DIVIDE':
                mode = 5
            elif mtex.blend_type == 'DIFFERENCE':
                mode = 6
            elif mtex.blend_type == 'DARKEN':
                mode = 7
            elif mtex.blend_type == 'LIGHTEN':
                mode = 8


            yi.paramsSetInt("mode", mode)
            yi.paramsSetBool("stencil", mtex.use_stencil) # sync. values to Blender for re-link textures

            negative = chanflag < 0
            if mtex.invert:
                negative = not negative

            yi.paramsSetBool("negative", negative)
            yi.paramsSetBool("noRGB", mtex.use_rgb_to_intensity) #

            yi.paramsSetColor("def_col", mtex.color[0], mtex.color[1], mtex.color[2])
            yi.paramsSetFloat("def_val", mtex.default_value)
            yi.paramsSetFloat("colfac", mtex.specular_color_factor)# #colfac : Factor by which texture affects color.
            yi.paramsSetFloat("valfac", mtex.hardness_factor) # #Factor by which texture affects most variables (material and world only).


            tex = mtex.texture  # texture object instance
            # lots to do...

            isImage = ( tex.type == 'IMAGE' )
            #isImage = ( tex.yaf_tex_type == 'IMAGE' )

            if (isImage or (tex.type == 'VORONOI' and tex.color_mode != 'INTENSITY') ):
                isColored=True
            else:
                isColored=False

            useAlpha = False
            yi.paramsSetBool("color_input", isColored)

            if isImage:
                useAlpha = (tex.use_alpha) and not(tex.use_calculate_alpha)

            yi.paramsSetBool("use_alpha", useAlpha)


            doCol = len(dcol) >= 3 #see defination of dcol later on, watch the remaining parts from now on.

            if ulayer == "":
                if doCol:
                    yi.paramsSetColor("upper_color", dcol[0],dcol[1],dcol[2])
                    yi.paramsSetFloat("upper_value", 0)
                else:
                    yi.paramsSetColor("upper_color", 0,0,0)
                    yi.paramsSetFloat("upper_value", dcol[0])
            else:
                yi.paramsSetString("upper_layer", ulayer)

            yi.paramsSetBool("do_color", doCol)
            yi.paramsSetBool("do_scalar", not doCol)

            return True


        def writeMappingNode(self, name, texname, mtex):
                yi = self.yi
                yi.paramsPushList()

                yi.paramsSetString("element", "shader_node")
                yi.paramsSetString("type", "texture_mapper")
                yi.paramsSetString("name", name)
                #yi.paramsSetString("texture", self.namehash(mtex.tex))
                yi.paramsSetString("texture", mtex.texture.name)

                #'UV'  'GLOBAL' 'ORCO' , 'WINDOW', 'NORMAL' 'REFLECTION' 'STICKY' 'STRESS' 'TANGENT'
                # texture coordinates, have to disable 'sticky' in Blender
                #change to coord. type Blender, texture_coords.  for test
                yi.paramsSetString("texco", "orco")
                if mtex.texture_coords == 'UV'          :          yi.paramsSetString("texco", "uv")
                elif mtex.texture_coords == 'GLOBAL'    :          yi.paramsSetString("texco", "global")
                elif mtex.texture_coords == 'ORCO'      :          yi.paramsSetString("texco", "orco")
                elif mtex.texture_coords == 'WINDOW'    :          yi.paramsSetString("texco", "window")
                elif mtex.texture_coords == 'NORMAL'    :          yi.paramsSetString("texco", "normal")
                elif mtex.texture_coords == 'REFLECTION':          yi.paramsSetString("texco", "reflect")
                elif mtex.texture_coords == 'STICKY'    :          yi.paramsSetString("texco", "stick")
                elif mtex.texture_coords == 'STRESS'    :          yi.paramsSetString("texco", "stress")
                elif mtex.texture_coords == 'TANGENT'   :          yi.paramsSetString("texco", "tangent")

                elif mtex.texture_coords == 'OBJECT':

                    yi.paramsSetString("texco", "transformed")

                    if mtex.object is not None:

                            texmat = mtex.object.matrix_local.copy().invert()
                            rtmatrix = yafrayinterface.new_floatArray(4*4)

                            for x in range(4):
                                for y in range(4):
                                    idx = (y + x * 4)
                                    yafrayinterface.floatArray_setitem(rtmatrix, idx, texmat[x][y])

                            yi.paramsSetMemMatrix("transform", rtmatrix, True)
                            yafrayinterface.delete_floatArray(rtmatrix)

                yi.paramsSetInt("proj_x", proj2int(mtex.mapping_x))
                yi.paramsSetInt("proj_y", proj2int(mtex.mapping_y))
                yi.paramsSetInt("proj_z", proj2int(mtex.mapping_z))

                if   mtex.mapping == 'FLAT'   : yi.paramsSetString("mapping", "plain")
                elif mtex.mapping == 'CUBE'   : yi.paramsSetString("mapping", "cube")
                elif mtex.mapping == 'TUBE'   : yi.paramsSetString("mapping", "tube")
                elif mtex.mapping == 'SPHERE' : yi.paramsSetString("mapping", "sphere")

                if mtex.use_map_normal: #|| mtex->maptoneg & MAP_NORM )
                        # scale up the normal factor, it ressembles
                        # blender a bit more
                        nf = mtex.normal_factor * 5
                        yi.paramsSetFloat("bump_strength", nf)


        def writeGlassShader(self, mat, rough):

                #mat : is an instance of material
                yi = self.yi
                yi.paramsClearAll()

                if rough: # create bool property "rough"
                    yi.paramsSetString("type", "rough_glass")
                    yi.paramsSetFloat("exponent", mat.exponent )
                    yi.paramsSetFloat("alpha", mat.alpha )
                else:
                    yi.paramsSetString("type", "glass")

                yi.paramsSetFloat("IOR", mat.IOR)
                filt_col = mat.filter_color
                mir_col = mat.mirror_color
                tfilt = mat.transmit_filter
                abs_col = mat.absorption

                yi.paramsSetColor("filter_color", filt_col[0], filt_col[1], filt_col[2])
                yi.paramsSetColor("mirror_color", mir_col[0], mir_col[1], mir_col[2])
                yi.paramsSetFloat("transmit_filter", tfilt)

                yi.paramsSetColor("absorption", abs_col[0], abs_col[1], abs_col[2])
                yi.paramsSetFloat("absorption_dist", mat.absorption_dist)
                yi.paramsSetFloat("dispersion_power", mat.dispersion_power)
                yi.paramsSetBool("fake_shadows", mat.fake_shadows)

                mcolRoot = ''
                fcolRoot = ''
                bumpRoot = ''

                i=0
                used_textures = []
                for item in mat.texture_slots: # changed 'enabled' to 'use', recent change

                        if hasattr(item,'use') and (item.texture is not None) :
                                used_textures.append(item) # these are instances of materialTextureSlot

                for mtex in used_textures:

                        used = False
                        mappername = "map%x" %i

                        lname = "mircol_layer%x" % i
                        if self.writeTexLayer(lname, mappername, mcolRoot, mtex, mtex.use_map_mirror, mir_col):# sync. values
                                used = True
                                mcolRoot = lname
                        lname = "filtcol_layer%x" % i
                        if self.writeTexLayer(lname, mappername, fcolRoot, mtex, mtex.use_map_mirror, filt_col):
                                used = True
                                fcolRoot = lname
                        lname = "bump_layer%x" % i
                        if self.writeTexLayer(lname, mappername, bumpRoot, mtex, mtex.use_map_normal, [0]):
                                used = True
                                bumpRoot = lname
                        if used:
                                self.writeMappingNode(mappername, mtex.texture.name , mtex)
                                i +=1

                yi.paramsEndList()
                if len(mcolRoot) > 0:   yi.paramsSetString("mirror_color_shader", mcolRoot)
                if len(fcolRoot) > 0:   yi.paramsSetString("filter_color_shader", fcolRoot)
                if len(bumpRoot) > 0:   yi.paramsSetString("bump_shader", bumpRoot)

                return yi.createMaterial(self.namehash(mat))

        def writeGlossyShader(self, mat, coated): #mat : instance of material class
                yi = self.yi
                yi.paramsClearAll()

                if coated: # create bool property
                        yi.paramsSetString("type", "coated_glossy")
                        yi.paramsSetFloat("IOR", mat.IOR)
                else:
                        yi.paramsSetString("type", "glossy")

                diffuse_color = mat.diffuse_color
                color         = mat.color

                # TODO: textures


                yi.paramsSetColor("diffuse_color", diffuse_color[0], diffuse_color[1], diffuse_color[2])
                yi.paramsSetColor("color", color[0],color[1], color[2])
                yi.paramsSetFloat("glossy_reflect", mat.glossy_reflect)
                yi.paramsSetFloat("exponent", mat.exponent)
                yi.paramsSetFloat("diffuse_reflect", mat.diffuse_reflect)
                yi.paramsSetBool("as_diffuse", mat.as_diffuse)


                yi.paramsSetBool("anisotropic", mat.anisotropic)
                yi.paramsSetFloat("exp_u", mat.exp_u )
                yi.paramsSetFloat("exp_v", mat.exp_v )

                diffRoot = ''
                mcolRoot = ''
                glossRoot = ''
                glRefRoot = ''
                bumpRoot = ''

                i=0
                used_textures = []
                for item in mat.texture_slots:
                        if hasattr(item,'use') and (item.texture is not None) :
                                used_textures.append(item) # these are instances of materialTextureSlot

                for mtex in used_textures:

                        used = False
                        mappername = "map%x" %i

                        lname = "diff_layer%x" % i
                        if self.writeTexLayer(lname, mappername, diffRoot, mtex, mtex.use_map_color_diffuse, diffuse_color): # sync. values
                                used = True
                                diffRoot = lname
                        lname = "gloss_layer%x" % i
                        if self.writeTexLayer(lname, mappername, glossRoot, mtex, mtex.use_map_color_spec, color):
                                used = True
                                glossRoot = lname
                        lname = "glossref_layer%x" % i
                        if self.writeTexLayer(lname, mappername, glRefRoot, mtex, mtex.use_map_specular, [mat.glossy_reflect]):
                                used = True
                                glRefRoot = lname
                        lname = "bump_layer%x" % i
                        if self.writeTexLayer(lname, mappername, bumpRoot, mtex, mtex.use_map_normal, [0]):
                                used = True
                                bumpRoot = lname
                        if used:
                                self.writeMappingNode(mappername, mtex.texture.name, mtex)
                        i +=1

                yi.paramsEndList()
                if len(diffRoot)  > 0 :  yi.paramsSetString("diffuse_shader", diffRoot)
                if len(glossRoot) > 0 :  yi.paramsSetString("glossy_shader", glossRoot)
                if len(glRefRoot) > 0 :  yi.paramsSetString("glossy_reflect_shader", glRefRoot)
                if len(bumpRoot)  > 0 :  yi.paramsSetString("bump_shader", bumpRoot)

                if mat.brdf_type == "Oren-Nayar":
                        yi.paramsSetString("diffuse_brdf", "oren_nayar")
                        yi.paramsSetFloat("sigma", mat.sigma)

                return yi.createMaterial(self.namehash(mat))

        def writeShinyDiffuseShader(self, mat):

                yi = self.yi
                yi.paramsClearAll()

                yi.paramsSetString("type", "shinydiffusemat")

                #link values Yafaray / Blender
                # provisional, for test only
                #TODO: change name of 'variables'?
                
                bCol = mat.color
                mirCol = mat.mirror_color
                bSpecr = mat.specular_reflect
                bTransp = mat.transparency
                bTransl = mat.translucency
                bTransmit = mat.transmit_filter

                # TODO: all

                i = 0
                used_textures = []
                for tex_slot in mat.texture_slots:
                        if tex_slot and tex_slot.use and tex_slot.texture:
                                used_textures.append(tex_slot)

                diffRoot = ''
                mcolRoot = ''
                transpRoot = ''
                translRoot = ''
                mirrorRoot = ''
                bumpRoot = ''



                for mtex in used_textures:
                        if not mtex.texture: continue
                        used = False
                        mappername = "map%x" %i

                        if mtex.use_map_color_diffuse:
                                lname = "diff_layer%x" % i
                                if self.writeTexLayer(lname, mappername, diffRoot, mtex, mtex.use_map_color_diffuse, bCol):
                                        used = True
                                        diffRoot = lname

                        if mtex.use_map_mirror:
                                lname = "mircol_layer%x" % i
                                if self.writeTexLayer(lname, mappername, mcolRoot, mtex, mtex.use_map_mirror, mirCol):
                                        used = True
                                        mcolRoot = lname

                        if mtex.use_map_alpha:
                                lname = "transp_layer%x" % i
                                if self.writeTexLayer(lname, mappername, transpRoot, mtex, mtex.use_map_alpha, [bTransp]):
                                        used = True
                                        transpRoot = lname

                        if mtex.use_map_translucency:
                                lname = "translu_layer%x" % i
                                if self.writeTexLayer(lname, mappername, translRoot, mtex, mtex.use_map_translucency, [bTransl]):
                                        used = True
                                        translRoot = lname

                        if mtex.use_map_raymir:
                                lname = "mirr_layer%x" % i
                                if self.writeTexLayer(lname, mappername, mirrorRoot, mtex, mtex.use_map_raymir, [bSpecr]):
                                        used = True
                                        mirrorRoot = lname

                        if mtex.use_map_normal:
                                lname = "bump_layer%x" % i
                                if self.writeTexLayer(lname, mappername, bumpRoot, mtex, mtex.use_map_normal, [0]):
                                        used = True
                                        bumpRoot = lname

                        if used:
                                self.writeMappingNode(mappername, mtex.texture.name, mtex)
                        i += 1

                yi.paramsEndList()
                if len(diffRoot) > 0:
                        yi.paramsSetString("diffuse_shader", diffRoot)
                if len(mcolRoot) > 0:
                        yi.paramsSetString("mirror_color_shader", mcolRoot)
                if len(transpRoot) > 0:
                        yi.paramsSetString("transparency_shader", transpRoot)
                if len(translRoot) > 0:
                        yi.paramsSetString("translucency_shader", translRoot)
                if len(mirrorRoot) > 0:
                        yi.paramsSetString("mirror_shader", mirrorRoot)
                if len(bumpRoot) > 0:
                        yi.paramsSetString("bump_shader", bumpRoot)

                yi.paramsSetColor("color", bCol[0], bCol[1], bCol[2])
                yi.paramsSetFloat("transparency", bTransp)
                yi.paramsSetFloat("translucency", bTransl)
                yi.paramsSetFloat("diffuse_reflect", mat.diffuse_reflect)
                yi.paramsSetFloat("emit", mat.emit)
                yi.paramsSetFloat("transmit_filter", bTransmit)

                yi.paramsSetFloat("specular_reflect", bSpecr)
                yi.paramsSetColor("mirror_color", mirCol[0], mirCol[1], mirCol[2])
                yi.paramsSetBool("fresnel_effect", mat.fresnel_effect)
                yi.paramsSetFloat("IOR", mat.IOR)

                if mat.brdf_type == "Oren-Nayar":
                        yi.paramsSetString("diffuse_brdf", "oren_nayar")
                        yi.paramsSetFloat("sigma", mat.sigma)

                return yi.createMaterial(self.namehash(mat))

        def writeBlendShader(self, mat):
                yi = self.yi
                yi.paramsClearAll()

                yi.printInfo("Exporter: Blend material with: [" + mat.material1 + "] [" + mat.material2 + "]")
                yi.paramsSetString("type", "blend_mat")
                yi.paramsSetString("material1", self.namehash( bpy.data.materials[mat.material1] )  )
                yi.paramsSetString("material2", self.namehash( bpy.data.materials[mat.material2] )  )

                i=0

                diffRoot = ''
                used_textures = []
                for item in mat.texture_slots: # changed 'enabled' for 'use'
                        if hasattr(item, 'use') and (item.texture is not None) :
                                used_textures.append(item)


                for mtex in used_textures:

                        if mtex.texture.type == 'NONE':
                                continue

                        used = False
                        mappername = "map%x" %i

                        lname = "diff_layer%x" % i
                        if self.writeTexLayer(lname, mappername, diffRoot, mtex, mtex.use_map_color_diffuse, [mat.blend_value] ):
                                used = True
                                diffRoot = lname
                        if used:
                                self.writeMappingNode(mappername, mtex.texture.name, mtex)
                        i +=1

                yi.paramsEndList()
                if len(diffRoot) > 0:
                        yi.paramsSetString("mask", diffRoot)

                yi.paramsSetFloat("blend_value", mat.blend_value)
                return yi.createMaterial(self.namehash(mat))

        def writeMatteShader(self, mat):
                yi = self.yi
                yi.paramsClearAll()
                yi.paramsSetString("type", "shadow_mat")
                return yi.createMaterial(self.namehash(mat))

        def writeNullMat(self, mat):
                yi = self.yi
                yi.paramsClearAll()
                yi.paramsSetString("type", "null")
                return yi.createMaterial(self.namehash(mat))

        def writeMaterial(self, mat):
                self.yi.printInfo("Exporter: Creating Material: \"" + self.namehash(mat) + "\"")
                ymat = None
                if mat.name == "y_null":
                        ymat = self.writeNullMat(mat)
                elif mat.mat_type == "glass":
                        ymat = self.writeGlassShader(mat, False)
                elif mat.mat_type == "rough_glass":
                        ymat = self.writeGlassShader(mat, True)
                elif mat.mat_type == "glossy":
                        ymat = self.writeGlossyShader(mat, False)
                elif mat.mat_type == "coated_glossy":
                        ymat = self.writeGlossyShader(mat, True)
                elif mat.mat_type == "shinydiffusemat":
                        ymat = self.writeShinyDiffuseShader(mat)
                elif mat.mat_type == "blend":
                        ymat = self.writeBlendShader(mat)
                else:
                        ymat = self.writeNullMat(mat)
                
                self.materialMap[mat] = ymat

