extends SceneTree
const D=preload("res://scripts/formula_lab/linked_campaign/rounds/round_data.gd")
const R=preload("res://scripts/formula_lab/linked_campaign/rounds/round_rules.gd")
func losses(before_: Dictionary,after_: Dictionary) -> Dictionary:
    var out: Dictionary={}
    for id: String in ["power","bridge","car"]:out[id]=int(before_.fixtures[id].hp)-int(after_.fixtures[id].hp)
    return out
func _initialize() -> void:
    var report: Dictionary={"kind":"read_only_rule_probe","cases":[]}
    for preset: String in ["balanced","engineering"]:
        var s: Dictionary=R.begin(D.create(D.PRESETS[preset]))
        var first: Dictionary=R.enemy_phase(s)
        var next: Dictionary=R.enemy_phase(first.state)
        var repeat: Dictionary=R.enemy_phase(s)
        var announced: Dictionary={}
        for p: Dictionary in first.state.pending_spawns.values():
            if p.due<=first.state.round:announced[p.board]=p.cells.size()
        var spawned: Dictionary={}
        for e: Dictionary in next.events:
            if e.type=="spawned":spawned[e.board]=int(spawned.get(e.board,0))+1
        report.cases.append({"preset":preset,"round_one_losses":losses(s,first.state),"round_two_forecast_losses":losses(first.state,next.state),"repeat_matches":first==repeat,"round_two_announced_by_board":announced,"round_two_actual_spawned":spawned,"round_one_bridge_damage_events":first.events.filter(func(e: Dictionary):return e.type=="damage" and e.target=="bridge")})
    var s: Dictionary=R.begin(D.create(D.PRESETS.engineering))
    var pathing: Dictionary=R.reachable(s,"white",30)
    var cheapest: int=999;var at: Vector2i=Vector2i(-1,-1)
    for cell: Vector2i in pathing.destinations:
        var sample: Dictionary=s.duplicate(true);sample.units.white.cell=cell
        if R.reason(sample,{"unit":"white","action":"operate","cell":sample.fixtures.power.cell,"target":"power"})=="" and int(pathing.destinations[cell])<cheapest:
            cheapest=pathing.destinations[cell];at=cell
    var counts: Dictionary={}
    for bid: String in s.boards:
        var kinds: Dictionary={};var nonfloor: int=0
        for tile: Dictionary in s.boards[bid].tiles.values():
            kinds[tile.kind]=int(kinds.get(tile.kind,0))+1
            if tile.kind!="floor":nonfloor+=1
        counts[bid]={"cells":s.boards[bid].size.x*s.boards[bid].size.y,"nonfloor_authored_tiles":nonfloor,"kinds":kinds}
    var objective: Dictionary=R.simulate(s,[{"unit":"white","action":"move","cell":at},{"unit":"white","action":"operate","cell":s.fixtures.power.cell,"target":"power"}])
    report.cases.append({"white_initial_move":s.units.white.moves,"minimum_cost_to_operate_power":cheapest,"nearest_operating_cell":str(at),"turn_one_power_operation_ok":objective.ok and objective.state.signals.power,"terrain_counts":counts})
    var after_power: Dictionary=R.enemy_phase(objective.state)
    var crane: Dictionary=R.simulate(objective.state,[{"unit":"crane","action":"move","cell":Vector2i(2,4)},{"unit":"crane","action":"lift","cell":Vector2i(2,3),"target":"c_tug","landing":Vector2i(1,1)}])
    var after_lift: Dictionary=R.enemy_phase(crane.state)
    report.cases.append({"power_on_car_steps":after_power.state.evac_step,"power_on_wait_reasons":after_power.events.filter(func(e: Dictionary):return e.type=="car_wait"),"crane_moves_then_lifts_tug_ok":crane.ok,"after_tug_lift_car_steps":after_lift.state.evac_step,"after_tug_lift_wait_reasons":after_lift.events.filter(func(e: Dictionary):return e.type=="car_wait")})
    var blast: Dictionary=D.create();blast.units.clear();blast.fixtures.clear();blast.boards.A.tiles={}
    var shooter: Dictionary=D.roster().leiling;shooter.active=true;shooter.board="A";shooter.cell=Vector2i(1,3);blast.units.leiling=shooter
    for a: Array in [["center",Vector2i(5,4)],["up",Vector2i(5,3)],["right",Vector2i(6,4)],["down",Vector2i(5,5)],["left",Vector2i(4,4)]]:
        var u: Dictionary=D.Base.enemy(a[0],"A",a[1],"claw");u.hp=10;u.max_hp=10;blast.units[a[0]]=u
    var events: Array=[];R.strike(blast,shooter,"missile",Vector2i(5,4),"A",events)
    report.cases.append({"missile_legacy_tip":D.Cat.ACTIONS.missile.tip,"missile_damage_events":events.filter(func(e: Dictionary):return e.type=="damage"),"missile_push_events":events.filter(func(e: Dictionary):return e.type=="pushed")})
    blast.units.clear();blast.units.leiling=shooter
    var big: Dictionary=D.roster().king;big.id="large_target";big.active=true;big.side="enemy";big.board="A";big.cell=Vector2i(4,3);big.hp=10;big.max_hp=10;blast.units.large_target=big
    events=[];R.strike(blast,shooter,"missile",Vector2i(5,4),"A",events)
    var hits: Array=events.filter(func(e: Dictionary):return e.type=="damage" and e.target=="large_target")
    report.cases.append({"large_target_footprint":str(big.footprint),"cross_intersects_multiple_occupied_cells":true,"damage_event_count":hits.size(),"remaining_hp":big.hp})
    var okay: bool=report.cases[0].repeat_matches and report.cases[1].repeat_matches and objective.ok and objective.state.signals.power and cheapest<=s.units.white.moves and crane.ok and after_power.state.evac_step==0 and after_lift.state.evac_step==2 and hits.size()==1 and big.hp==8
    report["checks_passed"]=okay
    print(JSON.stringify(report,"  "))
    quit(0 if okay else 1)
