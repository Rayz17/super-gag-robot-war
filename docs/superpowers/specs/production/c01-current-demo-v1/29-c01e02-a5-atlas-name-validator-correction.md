# C01E02 A5 Atlas 文件名校验修正

> Status: `producer_technical_correction / additive_to_27_and_28`
>
> Creative impact: `none`

## 问题

生成器的两份正式候选文件名由 `ATLAS_FILES` 明确定义为：

- `A5_RIFT_SWARM_A_IDLE_96_384x96.png`
- `A5_RIFT_SWARM_A_IDLE_128_512x128.png`

validator 已先按这两个配置路径读取并完成尺寸、RGBA、逐帧像素与边缘检查，但随后又用“文件名必须包含 `ATLAS` 字样”的启发式重新寻找候选，导致两个合法配置文件被误判为不存在。文件名启发式与生成器自己的 `ATLAS_FILES` 权威相冲突。

## 获准修正

只修改 `art-a5-rift-swarm-four-facing-atlas/validate_art_a5_rift_swarm_four_facing_atlas.py`：

1. 以 `set(gen.ATLAS_FILES.values())` 作为两份候选文件名的唯一权威；
2. 检查这两个配置文件均存在于 A5 根目录；
3. 继续拒绝任何额外的、名称含 `ATLAS` 且不是 overview 的未登记候选；
4. 保留后续 asset manifest、尺寸、RGBA、frame map、pivot、footprint、lifecycle 和哈希检查。

不得重命名或重编码已生成候选，不得修改 Godot、Runtime、R2 manifest、Canon 或 A4。本修正不新增用户决策，A5 完成后仍停在 96px/128px 单一选型门。
