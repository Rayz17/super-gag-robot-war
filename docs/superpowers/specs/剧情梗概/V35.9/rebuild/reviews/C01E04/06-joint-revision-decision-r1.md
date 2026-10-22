# C01E04 五席问题合并与修订决定 r1

> Revision scope: local integrated patch, not episode rebuild
>
> Relationship seat: initial PASS retained
>
> Recheck seats: showrunner / mecha-IP / gameplay-production / canon-macro-physical

## 独立结论

| 席位 | r1 | 阻断 | 决定 |
|---|---|---|---|
| 剧情监督/连续性 | PATCH | 巨构站起后只有一秒释放，立刻回到账单与倒计时 | 补完整稳定前行、楼外获救者、舰内岗位共同释放；账单后置 |
| 机器人文化/IP/奇观 | PATCH | 皇影地图口径仍是尾部自停；WBM阶段编号漂移 | 皇影统一为中点三拍；WBM统一四态、三套主美术体加一程序中断态 |
| 游戏制作/玩法 | PATCH | 西/东与先后顺序冲突；分支资源、城市Mask、回滚快照和冷备输出不完整 | Runtime、Graybox、Asset与checker同步补齐并独立纸演 |
| 人物/关系/生活 | PASS | 无正文阻断 | 锁定旧晚饭、公开路线、唐胶/兜灯取舍和陆衡入队；新增释放不得破坏这些场面 |
| Canon/宏观/物理 | PATCH | 正文西移、Runtime东移；三态覆盖四态 | 全部统一为六锚/载荷后向东一格，四态生命周期 |

## 已应用补丁

1. `可读剧情梗概 §11`增加首个稳定区段：二十九名观众与消防线留在场外，以拍击车门回应；舰内四岗位获得数秒共同喜悦，之后才出现赔付预估。
2. Story Core、§9、制作拆分和C01章地图统一为：六锚全解、两类载荷固定、第三类解耦后，馆体向东提前位移一格。
3. WBM001统一为`FIXED_BUILDING -> PREMOVED_ONE_SECTION -> HALF_RISE -> CRUISE_CARRIER_WITH_DAMAGE`；固定、半身、巡航是三套主资产，提前位移为程序骨骼/碰撞态。
4. 皇影统一为“睁眼 -> 黑框卡右锁泊臂并加剧失衡 -> 旧拘束只阻止扩张”，不自停、不救场、不成为单位。
5. 三种载荷建立真实消费者：生活维持拥有一次全局降热与P5首动作热延迟；实体馆藏完成两格配重并拥有一次完整关键冲击缓冲；档案分支揭示真/假意图并承担6点条件冷却。
6. 非档案分支的档案冷却固定为`N/A`，所有冷却守卫条件化；三组合均可在合法动作下完成。
7. 城市阶段增加完整基础Mask、锁臂Overlay和转移表；代表路线严格三次东移，唯一可选转体只能在`EAST_1`往返。
8. `ANCHOR_LOCAL / LOADOUT_LOCAL / HALF_RISE_LOCAL / CITY_LOCAL`记录全量局部快照；RT049-052恢复身体、锁臂、双方单位位置、active writer、回合/Owner、火锁、热量、结构、分支资源和城市伤害。
9. 新人物、皇影、载荷、WBM终态等跨话资产在`RT054`前均为本地暂存；档案优先冷备以`ARCHIVE_BACKUP_MAP`进入同一原子事务并由RT055只读断言。

## 推进规则

- 四个PATCH席只复核各自阻断是否关闭，不重新审整话。
- 任一席仍为PATCH，则只处理其具体反例；同一根因最多三轮。
- 四席均PASS后，才进入C01连续阅读稿与章级回读。
