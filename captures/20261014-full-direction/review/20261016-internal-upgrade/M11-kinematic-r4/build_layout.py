"""Rigid-part layout study only: no production mesh or collision certification."""
from pathlib import Path
import bpy
import math
import json
import hashlib
import sys
from mathutils import Vector

OUT=Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine='BLENDER_WORKBENCH'
scene.render.resolution_x=1200
scene.render.resolution_y=1000
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.film_transparent=False
scene.display.shading.light='STUDIO'
scene.display.shading.color_type='MATERIAL'
scene.display.shading.show_shadows=True
scene.display.shading.show_cavity=True
scene.display.shading.cavity_type='BOTH'
scene.display.shading.show_object_outline=True
scene.display.shading.background_type='WORLD'
scene.world.color=(0.88,0.88,0.88)

def mat(name,color):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);return m
M={
 'ivory':mat('Ivory shell',(0.84,0.83,0.77)),
 'navy':mat('Navy structure',(0.065,0.12,0.19)),
 'black':mat('Tires / hinges',(0.045,0.05,0.06)),
 'orange':mat('Orange wheel hubs / catches',(0.96,0.34,0.035)),
 'glass':mat('One rigid curved windshield',(0.075,0.36,0.48)),
 'cyan':mat('Eyes / lenses',(0.04,0.85,0.96)),
 'steel':mat('Sliding rails',(0.30,0.34,0.38)),
 'ground':mat('Ground',(0.93,0.92,0.88)),
}
parts=[]
def joint(name,parent=None,loc=(0,0,0)):
    o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o)
    o.empty_display_type='PLAIN_AXES';o.empty_display_size=.18
    o.parent=parent;o.location=loc;return o
def box(name,dims,loc,parent,material='ivory',bevel=.035):
    bpy.ops.mesh.primitive_cube_add(size=1)
    o=bpy.context.object;o.name=name;o.dimensions=dims
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.parent=parent;o.location=loc;o.data.materials.append(M[material])
    if bevel:
        b=o.modifiers.new('Edge round','BEVEL');b.width=bevel;b.segments=3
        o.modifiers.new('Face normals','WEIGHTED_NORMAL')
    parts.append(o);return o
def cylinder(name,r,depth,loc,parent,material='black',axis_x=False):
    bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=r,depth=depth)
    o=bpy.context.object;o.name=name;o.parent=parent;o.location=loc
    if axis_x:o.rotation_euler.y=math.pi/2
    o.data.materials.append(M[material]);parts.append(o);return o
def wheel(name,parent,loc,side):
    w=cylinder('road-wheel-'+name,.44,.23,loc,parent,'black',True)
    cylinder('hub-'+name,.21,.025,(0,0,side*.13),w,'orange')
    return w

base=joint('hip-and-central-rail')
cab=joint('cab-backward-carriage',base)
box('pelvis',(.95,.7,.45),(0,0,.15),base,'navy')
guide=joint('slide-guide-to-spine-hinge',base,(0,0,.48))
box('central-slide-guide',(.45,1.9,.18),(0,-.55,0),guide,'steel')
box('torso-spine',(.60,.35,1.75),(0,-.65,1.35),cab,'navy')

# The windshield and nose never change dimensions or split into two chest windows.
glass=box('single-windshield',(1.56,.12,.92),(0,-1.95,1.62),cab,'glass',.08)
glass.rotation_euler.x=math.radians(12)
box('windshield-top-frame',(1.76,.20,.13),(0,-1.82,2.15),cab,'ivory')
nose=box('smooth-nose-shield',(1.63,.23,.69),(0,-2.05,.83),cab,'ivory',.10)
box('nose-navy-insert',(.92,.09,.42),(0,-2.19,.90),cab,'navy',.06)
for side in [-1,1]:
    box('nose-running-light-'+str(side),(.38,.05,.07),(side*.59,-2.19,.71),cab,'orange',.018)
    # Camera windows stay attached to the chest-front side edges; no mirror stalk.
    camera=box('flush-camera-window-'+str(side),(.07,.08,.16),(side*.85,-1.83,1.55),cab,'black',.02)
    cylinder('camera-lens-'+str(side),.025,.015,(0,-.048,0),camera,'cyan').rotation_euler.x=math.pi/2

caps=[];first_carriers=[];arm_roots=[];arm_pitches=[];elbows=[];second_carriers=[]
leg_roots=[];ankles=[];foot_slides=[]
for side in [-1,1]:
    cap=joint('roof-half-hinge-'+str(side),cab)
    box('roof-shoulder-shell-'+str(side),(.79,1.26,.18),(0,0,0),cap,'ivory',.08)
    box('roof-shell-navy-edge-'+str(side),(.15,1.20,.18),(side*.35,0,-.04),cap,'navy',.03)
    caps.append((side,cap))
    carrier=joint('front-half-axle-flip-'+str(side),cab)
    box('front-wheel-flip-arm-'+str(side),(.13,.82,.13),(0,-.39,-.14),carrier,'steel',.03)
    wheel('axle1-'+str(side),carrier,(0,-.80,-.40),side)
    first_carriers.append((side,carrier))

    root=joint('arm-guide-'+str(side),cab)
    pitch=joint('shoulder-pitch-'+str(side),root)
    box('upper-arm-'+str(side),(.34,.75,.28),(0,.375,0),pitch,'navy')
    elbow=joint('elbow-'+str(side),pitch,(0,.75,0))
    box('door-forearm-shell-'+str(side),(.49,1.08,.27),(0,.54,-.32),elbow,'ivory',.06)
    box('wrist-ring-'+str(side),(.51,.13,.29),(0,1.01,-.32),elbow,'orange')
    box('hand-'+str(side),(.39,.32,.30),(0,1.23,-.32),elbow,'navy')
    carrier2=joint('second-wheel-carrier-'+str(side),elbow,(side*.27,0,0))
    box('second-wheel-fold-link-'+str(side),(.12,.13,.76),(0,0,.38),carrier2,'steel')
    wheel('axle2-'+str(side),carrier2,(0,0,.80),side)
    arm_roots.append((side,root));arm_pitches.append(pitch);elbows.append(elbow);second_carriers.append(carrier2)

    leg=joint('rear-frame-to-leg-'+str(side),base)
    box('frame-thigh-'+str(side),(.42,1.60,.32),(0,.80,0),leg,'ivory')
    knee=joint('knee-'+str(side),leg,(0,1.60,0))
    box('frame-calf-'+str(side),(.50,2.20,.38),(0,1.10,0),knee,'navy')
    box('calf-aero-cover-'+str(side),(.51,1.92,.15),(0,1.10,-.25),knee,'ivory')
    for axle,y in [(3,.40),(4,1.60)]:
        wheel('axle'+str(axle)+'-'+str(side),knee,(side*.34,y,-.10),side)
    ankle=joint('ankle-counter-rotation-'+str(side),knee,(0,2.20,0))
    foot_slide=joint('rear-bumper-foot-drop-'+str(side),ankle)
    box('rear-bumper-foot-'+str(side),(.63,.90,.35),(0,-.22,-.175),foot_slide,'ivory',.06)
    box('foot-sole-'+str(side),(.64,.92,.10),(0,-.22,-.30),foot_slide,'navy')
    leg_roots.append((side,leg));ankles.append(ankle);foot_slides.append(foot_slide)

# Three actual deck panels accordion-fold into one back rack, never a shrunken box.
deck=joint('deck-root-hinge',base,(0,.15,.65))
panel2=joint('deck-hinge-2',deck,(0,1.25,.10))
panel3=joint('deck-hinge-3',panel2,(0,1.25,.10))
for index,parent in enumerate([deck,panel2,panel3],1):
    box('freight-floor-'+str(index),(1.70,1.25,.09),(0,.625,0),parent,'navy',.02)
for parent, y in [(deck,.08),(panel3,1.17)]:
    for side in [-1,1]:box('twist-lock-'+str(len(parts)),(.15,.15,.13),(side*.76,y,.10),parent,'orange',.02)

head=joint('head-vertical-lift',cab)
helmet=box('helmet-proxy',(.64,.62,.78),(0,0,0),head,'navy',.10)
box('forehead-camera-border',(.18,.06,.29),(0,-.345,.15),head,'orange',.02)
box('forehead-camera-lens',(.10,.025,.19),(0,-.382,.15),head,'black',.02)
box('segmented-mask-proxy',(.40,.07,.31),(0,-.365,-.18),head,'ivory',.04)
for side in [-1,1]:box('eye-'+str(side),(.14,.04,.045),(side*.15,-.37,.015),head,'cyan',.01)
# Generic head envelope only; separate roof antenna superseded by user.

# Cargo is already unloaded and remains unchanged throughout this body-only study.
cargo=box('independent-unloaded-container',(1.75,3.70,1.75),(3.25,2.0,.875),None,'ivory',.04)
box('container-navy-top',(1.80,3.74,.12),(3.25,2.0,1.72),None,'navy')
for x in [-.80,.80]:
    for y in [-1.70,1.70]:box('container-corner-'+str(len(parts)),(.17,.17,.22),(3.25+x,2+y,1.61),None,'orange')
ground=box('display-ground',(24,24,.04),(0,1,-.07),None,'ground',0)
parts.remove(ground)

bpy.ops.object.camera_add(location=(12,-17,11))
cam=bpy.context.object;cam.name='study-camera'
target=Vector((.9,1.5,3.3));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=10.8;scene.camera=cam

def smooth(x):
    x=max(0,min(1,x));return x*x*(3-2*x)
def update(t):
    # The rear bumper feet deploy first. Then the original rear frame rotates
    # around fixed rear ankle points while the body moves above those feet.
    s=smooth((t-.12)/.88);theta=math.pi/2*s
    base.location=(0,3.8*(1-math.cos(theta)),.55+3.8*math.sin(theta))
    cab.location=(0,1.4*s,0)
    guide.rotation_euler.x=-math.pi/2*smooth((s-.65)/.35)
    for side,cap in caps:
        cap.location=(side*(.44+.73*s),-1.28,2.20-.40*s)
        cap.rotation_euler.y=side*math.radians(68)*s
    for side,carrier in first_carriers:
        carrier.location=(side*(.95+.20*s),-.90,.30)
        carrier.rotation_euler.x=-math.radians(110)*s
    for side,root in arm_roots:root.location=(side*(.68+.60*s),-.80-.60*s,.70+1.0*s)
    for o in arm_pitches:o.rotation_euler.x=-theta
    for o in elbows:o.rotation_euler.x=math.pi*(1-s)
    for o in second_carriers:o.rotation_euler.x=-theta
    for side,o in leg_roots:o.location=(side*(.60+.12*s),0,0);o.rotation_euler.x=-theta
    for o in ankles:o.rotation_euler.x=theta
    drop=.20*smooth(t/.12)
    for o in foot_slides:o.location.z=-drop
    deck.rotation_euler.x=theta;panel2.rotation_euler.x=-math.pi*s;panel3.rotation_euler.x=math.pi*s
    head.location=(0,-.70-.70*s,1.50+1.30*s)
    bpy.context.view_layer.update()

def geometry_digest():
    serial=[(o.name,[tuple(v.co) for v in o.data.vertices]) for o in parts]
    return hashlib.sha256(repr(serial).encode()).hexdigest()
signature=geometry_digest();road_names=[o.name for o in parts if o.name.startswith('road-wheel-')]
samples=[]
for i in range(121):
    t=i/120;update(t)
    rigid=all(max(abs(abs(v)-1) for v in o.matrix_world.to_scale())<1e-5 for o in parts)
    assert rigid and geometry_digest()==signature
    samples.append({'t':t,'road_wheel_count':len(road_names),'all_meshes_rigid':rigid})
assert len(road_names)==8
states=[(0,'01-unloaded-vehicle'),(.38,'02-cab-shift-and-arm-open'),(.72,'03-frame-down-deck-fold'),(1,'04-robot-head-up')]
# Frame every inspected state, including the lifted generic head, with one camera.
bpy.context.view_layer.update()
view=cam.matrix_world.inverted()
points=[]
for t,_ in states:
    update(t)
    for o in parts:
        points.extend(view@(o.matrix_world@Vector(v)) for v in o.bound_box)
low_x=min(v.x for v in points);high_x=max(v.x for v in points)
low_y=min(v.y for v in points);high_y=max(v.y for v in points)
offset=cam.matrix_world.to_quaternion()@Vector(((low_x+high_x)/2,(low_y+high_y)/2,0))
cam.location+=offset
cam.data.ortho_scale=max(high_x-low_x,(high_y-low_y)*scene.render.resolution_x/scene.render.resolution_y)*1.12
for t,name in states:
    update(t);scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
update(1)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'M11-rigid-layout-r4.blend'))
report={'scope':'卸柜后的本体刚体布局草模；不是生产模型或完整变形验收','states':[{'t':t,'file':name+'.png'} for t,name in states],'mesh_count':len(parts),'road_wheels':road_names,'road_wheel_count':8,'same_part_inventory_across_samples':True,'rigid_geometry_signature':signature,'rigid_samples_checked':len(samples),'mesh_scaling_or_morphing_used':False,'joint_hierarchy_used':True,'joints':['cab backward carriage','front half-axle flip links','shoulder sliders and hinges','folded elbow / forearm wheel carriers','rear frame to legs','ankle counter-rotation and rear bumper foot drop','three freight-floor hinges','head lift'],'head_location_vehicle':'驾驶室后部设备仓示意','cargo_policy':'单个货柜在研究开始前已卸下，整个本体变形研究中在地面保持尺寸与位置；不模拟装卸动作','limits':['车壳为简化包络，未完成全部局部碰撞/净空检查','未完成驾驶室可用空间、座椅/管线和部件厚度工程校验','未验证重心、地面反力、动力学与变形时支撑','头部仅使用无独立顶鳍的通用包络；R4两种整体头盔候选未做精细几何/收纳校验，非用户采用','与绘制源稿仍需反向对齐，不能把草模直接称作可制造变形机构'],'collision_clearance_verified':False,'occupant_space_verified':False,'dynamics_verified':False,'user_accepted':False,'runtime_integrated':False}
(OUT/'layout-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'rendered':4,'road_wheel_count':8,'rigid_samples':121,'full_transformation_verified':False}))
if '--animate' in sys.argv:
    joints=[o for o in scene.objects if o.type=='EMPTY']
    for frame in range(1,122):
        update((frame-1)/120)
        for o in joints:
            o.keyframe_insert(data_path='location',frame=frame)
            o.keyframe_insert(data_path='rotation_euler',frame=frame)
    for o in joints:
        for curve in o.animation_data.action.fcurves:
            for key in curve.keyframe_points:key.interpolation='LINEAR'
    scene.frame_start=1;scene.frame_end=151;scene.render.fps=24
    scene.render.resolution_x=960;scene.render.resolution_y=800
    scene.render.image_settings.file_format='FFMPEG'
    scene.render.ffmpeg.format='MPEG4';scene.render.ffmpeg.codec='H264'
    scene.render.ffmpeg.constant_rate_factor='HIGH'
    scene.render.filepath=str(OUT/'M11-layout-motion-r4.mp4')
    scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'M11-rigid-layout-r4.blend'))
    bpy.ops.render.render(animation=True)
    report['motion_file']='M11-layout-motion-r4.mp4'
    report['motion_duration_seconds']=151/24
    report['continuous_visual_playback_review_performed']=False
    (OUT/'layout-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
