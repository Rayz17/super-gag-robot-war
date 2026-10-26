extends SceneTree
const World=preload("res://scripts/formula_lab/linked_campaign/v6/skill_world.gd")
const Data=preload("res://scripts/formula_lab/linked_campaign/v5/rescue_data.gd")
const Palette=preload("res://scripts/formula_lab/linked_campaign/v6/art_palette.gd")
const OUT="/Users/rayz/Documents/超gag机器人大战/captures/20261014-full-direction/review/20261016-internal-upgrade/aircraft-runtime-comparison-20261022/"
func _initialize() -> void:
    call_deferred("run")
func run() -> void:
    var records: Array=[]
    for id: String in ["leiling","song"]:
        var vp: SubViewport=SubViewport.new()
        vp.size=Vector2i(1200,1200);vp.own_world_3d=true;vp.transparent_bg=false
        vp.msaa_3d=Viewport.MSAA_4X;vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS
        root.add_child(vp)
        var world_: Node3D=World.new();vp.add_child(world_);world_.set_process(false)
        var s: Dictionary=Data.create();var u: Dictionary=Data.roster()[id].duplicate(true)
        u.board="A";u.cell=Vector2i.ZERO;u.active=true;u.facing=Vector2i.DOWN
        s.units={id:u};s.fixtures={}
        world_.prepare(s,{"unit":id});world_.set_process(false)
        var actor_: Node3D=world_.actors[id];var motion_: RefCounted=world_.motions[id]
        world_.face(actor_,Vector3(0,0,1))
        for child: Node in world_.get_children():
            if child is WorldEnvironment:
                child.environment.ambient_light_color=Color(Palette.LIGHTING.ambient_color)
                child.environment.ambient_light_energy=Palette.LIGHTING.ambient
            if child is DirectionalLight3D:
                child.light_color=Color(Palette.LIGHTING.color);child.light_energy=Palette.LIGHTING.key
        for aircraft: bool in [false,true]:
            u.transformed=aircraft;s.units[id]=u;world_.sync(s);world_.set_process(false)
            world_.action_sequence.library.sample(u,actor_,motion_,"idle",.20)
            var body_: Node3D=motion_.form_body if aircraft else motion_.model
            var size_: Vector3=body_.get_meta("visual_size",Vector3.ONE*world_.visual_height(u))
            var height_: float=size_.y
            var span_: float=maxf(maxf(size_.x,size_.y),size_.z)
            var focus_: Vector3=actor_.global_position+Vector3.UP*height_*.50
            world_.camera.size=span_*1.28
            var direction_: Vector3=Vector3(.44,.56,1.2) if aircraft else Vector3(.38,.18,1.2)
            world_.camera.global_position=focus_+direction_*span_
            world_.camera.look_at(focus_)
            for frame: int in 6:await process_frame
            await RenderingServer.frame_post_draw
            var name_: String=id+("_aircraft" if aircraft else "_robot")
            var path_: String=body_.get_meta("asset_path","")
            var image_: Image=vp.get_texture().get_image()
            image_.save_png(OUT+name_+".png")
            records.append({"id":id,"aircraft":aircraft,"image":name_+".png",
              "model":path_,"model_sha256":FileAccess.get_sha256(path_),
              "source_geometry_and_paint_unchanged":true,"view":"diagnostic studio using existing game renderer",
              "visual_size":str(size_),"camera_size":world_.camera.size,
              "camera_position":str(world_.camera.global_position),"pose":"existing idle at 0.20s",
              "actual_gameplay_input":false,"same_normal_tactical_scene":false})
        vp.queue_free();await process_frame
    FileAccess.open(OUT+"runtime-model-captures.json",FileAccess.WRITE).store_string(JSON.stringify(records,"  "))
    print("Existing M08/M14 runtime models captured without asset changes.")
    quit(0)

