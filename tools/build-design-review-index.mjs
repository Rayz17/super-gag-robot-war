import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const cards = JSON.parse(fs.readFileSync(path.join(root, 'review/library/DESIGN-CARDS.json'))).selected_design_cards;
const stats = JSON.parse(fs.readFileSync(path.join(root, 'review/library/IMPORT-RESULT.json')));
const parse = name => {
  const lines = fs.readFileSync(path.join(root, name), 'utf8').trimEnd().split('\n');
  const keys = lines.shift().split('\t');
  return lines.map(line => Object.fromEntries(line.split('\t').map((value, i) => [keys[i], value])));
};
const records = parse('review/library/FILE-MANIFEST.tsv');
const names = { M: '机体', H: '人物', E: '敌人与威胁', F: '形态与组件', B: '建筑与设施', S: '剧情场面', T: '环境与地表设计', N: '招牌动作与变形设计' };
const gallery = path.join(root, 'review/library/galleries');
for (const file of fs.readdirSync(gallery)) if (!names[path.basename(file, '.md')]) fs.unlinkSync(path.join(gallery, file));
const groups = [];
for (const [group, label] of Object.entries(names)) {
  const items = cards.filter(card => card.group === group);
  const lines = ['# ' + label, '', '外部故事与设定评审用设计图。原卡面评语不等于用户逐图采用；最新确认范围看[已定设计图册](../../art/README.md)。本页不提供UI/UE、运行截图或三维资产。', ''];
  for (const card of items) {
    if (!fs.existsSync(path.join(root, card.image))) throw new Error('Missing design image: ' + card.image);
    lines.push('## ' + card.id + ' ' + card.name, '', '![' + card.id + '](' + path.relative(gallery, path.join(root, card.image)) + ')', '', '原卡面意见：' + (card.verdict || '未单列') + '。', '', '该条从原298项评审中抽取，来源及摘要见[设计卡清单](../DESIGN-CARDS.json)。版本与采用依据见[文件清单](../FILE-MANIFEST.tsv)。', '');
  }
  fs.writeFileSync(path.join(gallery, group + '.md'), lines.join('\n'));
  groups.push('| ' + label + ' | ' + items.length + ' | [' + group + '类](galleries/' + group + '.md) |');
}
const images = records.filter(row => /\.(?:png|jpe?g|webp|svg|psd|kra|ora|xcf|aseprite|ase)$/i.test(row.path));
fs.writeFileSync(path.join(root, 'review/library/README.md'), [
  '# 外部评审：设计美术与设定资料库', '',
  '按用户2026-10-26最新范围整理：只提供有助于理解故事、人物、机体与世界的设计美术，**不提供UI/UE或三维资产**。玩法与剧情文字仍可查询，但不要求评审实现或界面。', '',
  '先读[总目录](../00-总目录.md)中的当前故事，再按问题查图。不要把历史图、未确认候选或旧画风覆盖当前设定。', '',
  '## 两个入口', '',
  '- [已定设计图册](../art/README.md)：原始采用范围与逐图依据，54份确认源设计保持不变。',
  '- 本页分类图录：从原298项清单筛出134项设计对象，连同相关修订/候选原图。不是134项全部已确认。', '',
  '| 类型 | 设计项 | 图录 |', '| --- | --- | --- |', ...groups, '',
  '## 资料与边界', '',
  '- [设定入口](SETTINGS.md)：世界、人物、机体/IP、阵营、空间和玩法。',
  '- [补充设计图原文件](EXTRA-2D-SOURCES.md)：制作目录概念稿、立绘、构造图和历史设计参考。',
  '- [完整文件清单](FILE-MANIFEST.tsv)：原路径、字节、SHA与状态。',
  '- [排除记录](EXCLUSIONS.tsv)：UI/UE、执行证据、三维、缓存等。',
  '- [覆盖说明](../05-全量资产与设定覆盖说明.md)。', '',
  `当前共${records.length}份源文件，其中${images.length}份设计图文件（含不同版本、重复引用和SVG），原始合计${(stats.bytes / 1024 ** 3).toFixed(2)} GiB。文件数不等于独立设计数或验收数。`, '',
  '未纳入：G战术提示、C状态特效、U界面、I图标、X执行特效、N01–N08共享动作制作稿；运行截图、HUD/控件、三维模型/贴图/绑定、录屏。原始文字记录可能提及这些内容，不构成该类资产交付。', '',
  '已定、授权派生、Candidate和History按原记录分开。上传不是新增采用或运行验收。', '',
].join('\n'));
const extras = images.filter(row => row.scope !== 'full_art_direction');
const extra = ['# 补充设计图原文件', '', '只列设计类图片，不含界面、运行截图和三维源。各版本保持原有身份；旧稿不覆盖当前确认。', ''];
for (const scope of [...new Set(extras.map(row => row.scope))]) {
  extra.push('## ' + scope, '', '| 设计文件 | 原身份 |', '| --- | --- |');
  for (const row of extras.filter(row => row.scope === scope)) extra.push('| [' + path.basename(row.path) + '](../../' + row.path.split('/').map(encodeURIComponent).join('/') + ') | `' + row.status + '` |');
  extra.push('');
}
fs.writeFileSync(path.join(root, 'review/library/EXTRA-2D-SOURCES.md'), extra.join('\n'));
const curated = parse('review/art/ASSET-MANIFEST.tsv');
const lines = ['# 已定设计与视觉参考', '', '仅设计美术，不含UI/UE和三维资产。状态与确认范围沿用原始采用记录，授权派生和历史参考不会因同步升格。', ''];
for (const id of [...new Set(curated.map(row => row.asset_id))].filter(id => id !== 'PROVENANCE')) {
  const items = curated.filter(row => row.asset_id === id);
  const hero = items.find(row => row.status === 'confirmed_source_design') || items[0];
  lines.push('## ' + id + ' ' + hero.name, '', '![' + hero.name + '](../../' + hero.path + ')', '', '| 文件 | 状态与确认范围 |', '| --- | --- |');
  for (const row of items) lines.push('| [' + path.basename(row.path) + '](../../' + row.path + ') | `' + row.status + '`；' + row.scope + '；[依据](../../' + row.receipt + ') |');
  lines.push('');
}
lines.push('逐图尺寸、字节和SHA见[资产清单](ASSET-MANIFEST.tsv)。M07/M12等未确认新图在[候选图录](../library/README.md)，不在本页冒充已定。', '');
fs.writeFileSync(path.join(root, 'review/art/README.md'), lines.join('\n'));
console.log(JSON.stringify({ cards: cards.length, images: images.length, files: records.length, pass: true }));
