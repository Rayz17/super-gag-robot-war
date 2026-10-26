"""Rigid head/antenna envelope study, not a production character model."""
import bpy, math, hashlib, json, sys
from pathlib import Path
from mathutils import Vector
OUT=Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.render.engine='BLENDER_WORKBENCH'
scene.render.resolution_x=1200;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.display.shading.light='STUDIO'
scene.display.shading.color_type='MATERIAL';scene.display.shading.show_shadows=True
scene.display.shading.show_cavity=True;scene.display.shading.cavity_type='BOTH'
scene.display.shading.show_object_outline=True;scene.display.shading.background_type='WORLD'
scene.world.color=(.90,.91,.90)
def mat(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);return m
M={k:mat(k,c) for k,c in {'ivory':(.86,.85,.80),'navy':(.055,.105,.18),'black':(.035,.04,.05),'orange':(.98,.32,.025),'steel':(.38,.43,.48),'cyan':(.03,.82,.96),'ground':(.94,.93,.9)}.items()}
parts=[];head_parts=[]
def joint(name,parent=None,loc=(0,0,0)):
 o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.parent=parent;o.location=loc;return o
def box(name,dims,loc,parent=None,material='navy',head=False,bevel=.025):
 bpy.ops.mesh.primitive_cube_add(size=1);o=bpy.context.object;o.name=name;o.dimensions=dims
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.parent=parent;o.location=loc
 o.data.materials.append(M[material]);parts.append(o)
 if head:head_parts.append(o)
 if bevel:
  b=o.modifiers.new('rounded_edges','BEVEL');b.width=bevel;b.segments=3;o.modifiers.new('normals','WEIGHTED_NORMAL')
 return o
carrier=joint('two_stage_head_carrier')
box('full_height_skull',(.78,.75,1.08),(0,0,0),carrier,'navy',True,.08)
box('ivory_forehead_cap',(.35,.06,.43),(0,-.40,.28),carrier,'ivory',True)
box('orange_forehead_camera',(.18,.055,.23),(0,-.45,.18),carrier,'orange',True)
box('camera_lens',(.105,.02,.16),(0,-.49,.18),carrier,'black',True,.01)
for i,(z,w) in enumerate([(-.16,.59),(-.29,.53),(-.42,.43)]):box('mask_plate_'+str(i),(w,.09,.18),(0,-.42,z),carrier,'ivory',True)
box('projecting_brave_chin',(.27,.25,.20),(0,-.485,-.43),carrier,'ivory',True,.04)
antenna_joints=[]
for side in [-1,1]:
 box('compact_ear_'+str(side),(.14,.43,.52),(side*.43,.035,-.045),carrier,'navy',True)
 box('eye_'+str(side),(.20,.03,.055),(side*.18,-.435,-.015),carrier,'cyan',True,.008)
 a=joint('ear_antenna_fold_'+str(side),carrier,(side*.44,.08,.18));antenna_joints.append(a)
 box('blunt_antenna_'+str(side),(.065,.08,.68),(0,0,.34),a,'ivory',True,.01)
 box('antenna_orange_insert_'+str(side),(.022,.012,.36),(0,-.046,.40),a,'orange',True,.003)
 # Longitudinal fold channels, attached to the carrier and never created mid-motion.
 box('antenna_recess_'+str(side),(.10,.72,.035),(side*.44,.40,.13),carrier,'steel',True,.01)

# Rectangular bay is cut away at the front and upper sides for inspection.
inner={'xmin':-.65,'xmax':.65,'ymin':-.78,'ymax':.99,'zmin':-.65,'zmax':.64}
box('bay_floor',(1.46,1.93,.08),(0,.105,-.69),material='ivory')
box('rear_bulkhead',(1.46,.08,1.38),(0,1.03,0),material='ivory')
for side in [-1,1]:
 box('cutaway_side_wall_'+str(side),(.08,1.93,.35),(side*.69,.105,-.48),material='ivory')
 box('head_lift_guide_'+str(side),(.07,.07,2.20),(side*.57,.88,.42),material='steel',bevel=.01)
 box('top_hinge_rail_'+str(side),(.08,1.93,.08),(side*.69,.105,.69),material='orange')
doors=[]
for side in [-1,1]:
 d=joint('split_hatch_hinge_'+str(side),None,(side*.65,.105,.68));doors.append((side,d))
 box('split_roof_hatch_'+str(side),(.65,1.77,.08),(-side*.325,0,0),d,'ivory')
 box('roof_lock_'+str(side),(.12,.16,.055),(-side*.52,-.65,.07),d,'orange')

# Occupied cab reference volume is shown as an open wire cage, not seats or a solid obstruction.
for x in [-.75,.75]:
 for y in [-2.10,-.90]:box('cab_envelope_post_'+str(len(parts)),(.025,.025,1.25),(x,y,0),material='steel',bevel=0)
for z in [-.625,.625]:
 for x in [-.75,.75]:box('cab_envelope_long_'+str(len(parts)),(.025,1.20,.025),(x,-1.50,z),material='steel',bevel=0)
 for y in [-2.10,-.90]:box('cab_envelope_cross_'+str(len(parts)),(1.50,.025,.025),(0,y,z),material='steel',bevel=0)
ground=box('ground',(12,12,.035),(0,0,-.78),material='ground',bevel=0);parts.remove(ground)
def smooth(v):
 v=max(0,min(1,v));return v*v*(3-2*v)
def pose(t):
 fold=smooth(t/.30);lower=smooth((t-.34)/.46);close=smooth((t-.84)/.16)
 carrier.location=(0,-.08*(1-lower),2.10*(1-lower))
 for a in antenna_joints:a.rotation_euler.x=-math.radians(12+78*fold)
 for side,d in doors:d.rotation_euler.y=side*math.radians(110)*(1-close)
 bpy.context.view_layer.update()
def digest():return hashlib.sha256(repr([(o.name,[tuple(v.co) for v in o.data.vertices]) for o in parts]).encode()).hexdigest()
signature=digest();samples=[]
for i in range(121):
 t=i/120;pose(t);assert digest()==signature
 assert all(max(abs(abs(v)-1) for v in o.matrix_world.to_scale())<1e-5 for o in parts)
 points=[o.matrix_world@v.co for o in head_parts for v in o.data.vertices]
 low=min(v.z for v in points)
 if low<inner['zmax']:
  # Side-wall/floor enclosure check; open roof plane is the intended entry.
  for v in points:
   if v.z<=inner['zmax']:
    assert inner['xmin']<=v.x<=inner['xmax'] and inner['ymin']<=v.y<=inner['ymax']
    assert v.z>=inner['zmin']
 samples.append({'t':t,'head_min_z':low})
pose(1);points=[o.matrix_world@v.co for o in head_parts for v in o.data.vertices]
lo=[min(v[i] for v in points) for i in range(3)];hi=[max(v[i] for v in points) for i in range(3)]
clearance={'left':lo[0]-inner['xmin'],'right':inner['xmax']-hi[0],'front_chin':lo[1]-inner['ymin'],'rear_antenna':inner['ymax']-hi[1],'floor':lo[2]-inner['zmin'],'closed_lid':inner['zmax']-hi[2]}
assert min(clearance.values())>.04,clearance
bpy.ops.object.camera_add(location=(5,-7,4.4));cam=bpy.context.object
target=Vector((0,-.05,.95));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.1;scene.camera=cam
states=[(0,'01-deployed'),(.32,'02-antennas-folded'),(.62,'03-head-lowering'),(1,'04-stored-hatch-closed')]
bpy.context.view_layer.update();view=cam.matrix_world.inverted();frame_points=[]
for t,_ in states:
 pose(t)
 for o in parts:frame_points.extend(view@(o.matrix_world@Vector(v)) for v in o.bound_box)
lx=min(v.x for v in frame_points);hx=max(v.x for v in frame_points)
ly=min(v.y for v in frame_points);hy=max(v.y for v in frame_points)
cam.location+=cam.matrix_world.to_quaternion()@Vector(((lx+hx)/2,(ly+hy)/2,0))
cam.data.ortho_scale=max(hx-lx,(hy-ly)*scene.render.resolution_x/scene.render.resolution_y)*1.12
for t,name in states:pose(t);scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
pose(0)
if '--animate' in sys.argv:
 joints=[o for o in scene.objects if o.type=='EMPTY']
 for frame in range(1,122):
  pose((frame-1)/120)
  for o in joints:o.keyframe_insert(data_path='location',frame=frame);o.keyframe_insert(data_path='rotation_euler',frame=frame)
 for o in joints:
  for c in o.animation_data.action.fcurves:
   for k in c.keyframe_points:k.interpolation='LINEAR'
 scene.frame_start=1;scene.frame_end=145;scene.render.fps=24
 scene.render.resolution_x=960;scene.render.resolution_y=800
 scene.render.image_settings.file_format='FFMPEG';scene.render.ffmpeg.format='MPEG4';scene.render.ffmpeg.codec='H264'
 scene.render.filepath=str(OUT/'M11-head-bay-motion-r7.mp4');scene.frame_set(1)
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'M11-head-bay-r7.blend'));bpy.ops.render.render(animation=True)
else:bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'M11-head-bay-r7.blend'))
report={'scope':'头部/双天线与矩形头仓的同件包络研究；不是完整整机模型','source':'build_head_bay.py','editable_model':'M11-head-bay-r7.blend','states':[{'t':t,'file':n+'.png'} for t,n in states],'motion':'M11-head-bay-motion-r7.mp4' if '--animate' in sys.argv else None,'rigid_samples_checked':len(samples),'same_geometry_signature':signature,'mesh_scaling_or_morphing_used':False,'head_design_height_width_envelope':[1.08,1.0],'antenna_count':2,'antenna_mast_length':.68,'bay_inner_bounds':inner,'stored_head_bounds':{'min':lo,'max':hi},'stored_clearance_normalized_units':clearance,'side_wall_and_floor_vertex_sweep_checked':True,'hatch_sequence':'舱盖已开→折天线→下降/后滑→关盖','cab_reference_separation':.12,'limits':['归一化草模，不是毫米尺寸或精细头部/车壳','只检查头部刚体顶点对矩形侧壁/底面及收纳终态；不是整机全三角碰撞认证','驾驶室仅隔开的包络，不证明真人乘坐和管线布置','未验证整机重心/受力/变形支撑，也未完整视觉播放检查视频'],'full_vehicle_transformation_verified':False,'continuous_visual_playback_review_performed':False,'user_accepted':False,'runtime_integrated':False}
(OUT/'head-bay-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rigid_samples':121,'stored_clearance':clearance,'full_vehicle_verified':False}))
