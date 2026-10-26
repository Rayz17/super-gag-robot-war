# G2-A2-C2 输入、权威与写域回执

日期：2026-08-20  
任务：`96 / G2_A2_C2_SCREEN_INPUT_TIMELINE_AND_EMBODIED_CONSEQUENCE`

## 输入锁

| 输入 | SHA-256 | 用途 |
|---|---|---|
| 96号唯一任务书 | `b39e315d15670973c8f2b73b5277adccd4ef1180ce7783a692d94d6034a807d3` | 本次施工边界 |
| 94号上游制作人回执 | `f404ccc6d765b34b2a3d738a675d061d419a3c6c5d3dde5bf41ff51b5338c78f` | Task89/93 Lookdev前提签收 |
| interface 1.6.2（派工时） | `8fdad825167723a0b6180d4cd86dfbb02262865e11483db3334af1a50ccadd99` | 原始输入锁 |
| production board（派工时） | `a87862e59b226cf398e72a6fabcfd9e4ae2452de0a05b1421319ecd279e7aebb` | 原始门状态 |
| interface 1.6.3（收口时） | `cdea5bd2f1715c076b4050cbc4f41ad203e94b896eed10e04e518f5bd483e312` | Call02失败/C3 blocked动态同步 |
| production board（收口时） | `8758870be3904f5cb51b004ee8175d8df40820223c07f3f72c60968668e79a08` | Task96 dispatched / P98 blocked待交付 |
| Task89/93历史交付哈希 | `d44d55ec65a90678afd2192fbe5a3a7c60e2a59b73ed2075cf3aa4026a83f4e3` | `main-g2-a2-c1/**`只读复验 |

`chao-gag-canon` 已用于查询 Hard / Working / Candidate / History；本交付仅是 Candidate proxy，不改 Canon、Runtime、Default Entry 或 save。

## 唯一写域

- `game-godot/**/m3_golden_slice/g2_a2_visual_compositor/**`内的C2输入适配、产品UI、Proxy FX、表现cue与专用非默认Scene；
- 专用`g2_a2_c2_*`测试、InputEvent replay、capture/performance driver、外部validator与runner；
- `main-g2-a2-c2/**`证据树。

最后的城市炮 fail-closed 修复只改现有visual compositor adapter消费语义：缺字段默认`false`，仅明确T4表现帧可开启。Resolver、Session、PerformanceDirector逻辑时序与world result未改。

C2入口没有把旧C1 adapter的`copy_readback()`整包交给产品UI，而是显式净化为固定公共copy白名单：`jicun_line / objective / timeline / top_threats`。`strategy_a / strategy_b`及任何静态责任结果键都不会进入C2 UI调用图；本次copy边界修复没有再修改旧C1 adapter。

## 隔离结果

Task89/93历史manifest逐项校验通过；未执行`git add / commit / clean`，未回滚共享树改动。末态为`approved_handoffs=[] / real_art_loaded=0 / call02_pixels_loaded=false`；Call02已视觉失败，Task99/C3仍blocked，本任务没有接入或预做真实Atlas。C2只在专用非默认Scene与证据树内收口，不晋级Runtime、Default Entry或save。
