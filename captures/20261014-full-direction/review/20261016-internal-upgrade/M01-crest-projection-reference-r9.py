"""Projection-only crest reference, not a replacement head or runtime asset."""
from pathlib import Path
import bpy
from mathutils import Vector

OUT = Path(__file__).resolve().parent / 'refs'
OUT.mkdir(exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def material(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    shader = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    shader.inputs[0].default_value = (*color, 1)
    next(s for s in shader.inputs if s.identifier == 'Roughness').default_value = 0.65
    return m

ivory = material('ivory crest banks and exterior walls', (0.88, 0.83, 0.70))
gold = material('gold floor of central dorsal recess ONLY', (0.95, 0.48, 0.015))
teal = material('teal placeholder skull', (0.015, 0.40, 0.46))
dark = material('groove recess shadow', (0.10, 0.10, 0.075))

# Coordinates: x = left/right; y = forehead(-) to occiput(+); z = up.
profile = [(-0.98,0.18,0.23),(-0.99,0.38,0.30),(-0.92,0.62,0.33),
           (-0.80,0.86,0.33),(-0.60,1.06,0.31),(-0.32,1.20,0.29),
           (-0.02,1.26,0.27),(0.28,1.24,0.26),(0.54,1.17,0.25),
           (0.68,1.10,0.25)]

def ribbon(name, left, right, indices, surface_offset, thickness, mat):
    verts = []
    for i in indices:
        y,z,w = profile[i]
        lo,hi = left(w),right(w)
        verts += [(lo,y,z+surface_offset),(hi,y,z+surface_offset),
                  (lo,y,z+surface_offset-thickness),(hi,y,z+surface_offset-thickness)]
    faces = []
    for j in range(len(indices)-1):
        a,b = j*4,(j+1)*4
        faces += [(a,a+1,b+1,b),(a+2,b+2,b+3,a+3),
                  (a,b,b+2,a+2),(a+1,a+3,b+3,b+1)]
    faces += [(0,2,3,1), tuple(range((len(indices)-1)*4,len(indices)*4))]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts,[],faces)
    mesh.update()
    obj = bpy.data.objects.new(name,mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    bevel = obj.modifiers.new('small physical edge bevel','BEVEL')
    bevel.width = 0.008
    bevel.segments = 1
    return obj

all_indices=list(range(len(profile)))
# Complete ivory OUTSIDE walls are never colored gold.
ribbon('left solid ivory bank',lambda w:-w,lambda w:-0.065,all_indices,0,0.16,ivory)
ribbon('right solid ivory bank',lambda w:0.065,lambda w:w,all_indices,0,0.16,ivory)
ribbon('ivory central backing',lambda w:-0.066,lambda w:0.066,all_indices,-0.055,0.11,ivory)
# Only the floor of the narrow TOP center recess receives gold.
ribbon('long gold center recess floor',lambda w:-0.055,lambda w:0.055,list(range(3,10)),-0.04,0.008,gold)
ribbon('short separate forehead inset',lambda w:-0.045,lambda w:0.045,[0,1],-0.035,0.008,gold)
ribbon('ivory bridge between the two gold details',lambda w:-0.066,lambda w:0.066,[1,2,3],0,0.16,ivory)

bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24,location=(0,0,0))
shell=bpy.context.object
shell.name='shape guide skull only - not final M01 head'
shell.scale=(1,1,1.035)
shell.data.materials.append(teal)
for poly in shell.data.polygons: poly.use_smooth=True

world=bpy.data.worlds.new('neutral studio')
bpy.context.scene.world=world
world.use_nodes=True
background=next(n for n in world.node_tree.nodes if n.type=='BACKGROUND')
background.inputs[0].default_value=(0.72,0.77,0.81,1)
background.inputs[1].default_value=0.45
bpy.ops.object.light_add(type='AREA',location=(-3,-4,6))
bpy.context.object.data.energy=600
bpy.context.object.data.shape='DISK'
bpy.context.object.data.size=5

bpy.ops.object.camera_add()
cam=bpy.context.object
cam.data.type='ORTHO'
cam.data.ortho_scale=2.65
scene=bpy.context.scene
scene.camera=cam
scene.render.engine='BLENDER_EEVEE_NEXT'
scene.render.resolution_x=900
scene.render.resolution_y=900
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.image_settings.color_mode='RGBA'
scene.render.film_transparent=True
scene.view_settings.view_transform='Standard'

def set_view(location):
    cam.location=location
    cam.rotation_euler=(Vector((0,0,0.35))-cam.location).to_track_quat('-Z','Y').to_euler()

set_view((0,-6,2.5))
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'M01-crest-cross-section-r9.blend'))
for name,loc in [('front',(0,-6,2.5)),('three-quarter',(3.2,-5.2,2.7))]:
    set_view(loc)
    scene.render.filepath=str(OUT/f'M01-crest-center-groove-{name}-r9.png')
    bpy.ops.render.render(write_still=True)
