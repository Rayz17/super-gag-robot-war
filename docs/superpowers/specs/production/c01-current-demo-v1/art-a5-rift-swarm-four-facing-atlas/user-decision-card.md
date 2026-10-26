# C01E02 A5 小型突入体 Atlas 用户裁决卡

> Package: `C01CDV1_A5_RIFT_SWARM_FOUR_FACING_ATLAS_V1`  
> Candidate: `CAND_C01CDV1_A3_RIFT_SWARM_A_CARAPACE_CRAWLER_V1`  
> Slot: `ENEMY_C01CDV1_RIFT_SWARM_MASTER`  
> Lifecycle: `Candidate / runtime_allowed=false / runtime_handoff=none`

## 两份互斥候选

- `96px`: `A5_RIFT_SWARM_A_IDLE_96_384x96.png`  
  SHA-256: `1dc037874dda99e3331280f0533590f8f210411687a2d1b53265c5e62456526b`
- `128px`: `A5_RIFT_SWARM_A_IDLE_128_512x128.png`  
  SHA-256: `890a1844616c1e3864e4e46bc03ea052edc8317083b884e60b454eb2e223817e`

## 请逐项确认

1. 四朝向是否保持 A「伏壳钳足型」身份，是否存在朝向混淆？
2. 接地点、闭合红缝和扑击端是否稳定？
3. 选择 `96px` 或 `128px` 中哪一份作为具体 Demo handoff 来源？同一 slot 不能同时绑定两份。
4. 是否接受当前 Demo 六实例先共用一个母版、轻差分继续延期？
5. 是否明确批准所选 atlas 的具体文件名与上述 SHA-256？

建议回复格式：`四向通过；接地点/红缝/扑击端通过；选择96（或128）；六实例共用母版、轻差分延后；批准 <文件名> / <SHA-256> 作为Demo handoff来源`。

本裁决只允许制作人另签 exact handoff；不直接授权 Godot、Runtime promotion 或实例差分接口。
