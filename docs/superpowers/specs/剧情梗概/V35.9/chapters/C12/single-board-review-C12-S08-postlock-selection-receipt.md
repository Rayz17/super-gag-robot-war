# C12-S08 锁后定点修正：逐机选择运行回执

Review ID: V35.9-C12-S08-POSTLOCK-SELECTION-RECEIPT  
Author Slot ID: V357-C12-S08  
Reviewer Mode: single-context fallback / S09 preflight machine-closure audit  
Status: resolved_post_lock_machine_correction  

## 1. 发现原因

S09必须把每台实际机体分入中央残舰、七海护航、作者驳船或独立声部。预检S08下游适配时发现，原合同虽然证明标准只能强制2台、低评价只能强制3台，也逐候选记录了停止条件和代价，但成功执行与S09适配保存的是`SELECT_EXACT_2/3...`选择公式，并非本周目实际选中的单位ID。

因此原状态可以证明“数量合法”，却不能让S09回答“究竟哪两台被纪存强迫、哪台因此优先拒绝他的舰群”。这是逐机政治后果的机器闭包漏洞，不能带入下一槽。

## 2. 修正

- 新增`v35_9_c12_s08_runtime_selection_receipt_contract_v35_9.tsv`，分别定义标准与低评价回执。
- 运行时必须保存`C12S08_ACTIVE_UNIT_IDS`、`C12S08_FORCED_UNIT_IDS`和`C12S08_FORCED_STOP_RECORDS_BY_UNIT_ID`。
- 活动单位必须是候选域中按身体、控制、伤损、路线和显式排除解析出的1至8个唯一ID。
- 强制单位必须是实际活动或有效锁泊自动体中的唯一2/3个ID；皇影不可被强制，共享身体不可重复。
- 成功执行与7872条S09适配不再传选择公式，而是引用标准/低评价运行回执；逐机身体代价、停止记录和拒绝/第三方保管权随ID进入S09。
- Checker新增两条回执合同、执行引用和适配引用门禁；缺运行回执或只传集合标签均失败。

## 3. 结果

重新生成20张S08机器表后，S08单槽检查通过，仅保留既有重型拆分警告；Canon smoke在图谱同步后继续执行。本修正不改可读故事、强制数量、WBM004/WBM005顺序或三轮采用结论，只把原本承诺的“具名”落实为可供S09读取的精确运行状态。
