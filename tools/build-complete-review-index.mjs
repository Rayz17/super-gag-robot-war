import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const load = p => JSON.parse(fs.readFileSync(path.join(root, p), 'utf8'));
const parse = p => { const a = fs.readFileSync(path.join(root, p), 'utf8').trimEnd().split('\n'); const h = a.shift().split('\t'); return a.map(l => Object.fromEntries(l.split('\t').map((v, i) => [h[i], v]))); };
const records = parse('review/library/FILE-MANIFEST.tsv'), stats = load('review/library/IMPORT-RESULT.json');
const origin = 'captures/20261014-full-direction/review-v2.html';
const html = fs.readFileSync(path.join(root, origin), 'utf8');
const strip = s => (s || '').replace(/<[^>]*>/g, '').replace(/\|/g, '/').replace(/\s+/g, ' ').trim();
const cards = [...html.matchAll(/<article class="card"([^>]*)>([\s\S]*?)<\/article>/g)].map(m => ({ id: m[1].match(/data-id="([^"]+)"/)?.[1], group: m[1].match(/data-group="([^"]+)"/)?.[1], name: strip(m[2].match(/<h3 class="name">([\s\S]*?)<\/h3>/)?.[1]), image: m[2].match(/<img[^>]+src="([^"]+)"/)?.[1], verdict: strip(m[2].match(/<div class="review-verdict[^>]*>([\s\S]*?)<\/div>/)?.[1]) }));
if (cards.length !== 298 || new Set(cards.map(c => c.id)).size !== 298) throw new Error('Art review card coverage mismatch');
const names = { M: '机体', H: '人物', E: '敌人与威胁', F: '形态与组件', B: '建筑与设施', S: '剧情场面', X: '动作与攻击特效', G: '战术预演图形', C: '持续状态特效', U: '界面组件', I: '操作与招式图标', T: '地形与地图', N: '动作与变形' };
const directories = path.join(root, 'review/library/galleries');
fs.mkdirSync(directories, { recursive: true });
const groupLines = [];
for (const [group, name] of Object.entries(names)) {
  const items = cards.filter(c => c.group === group);
  const lines = ['# ' + name + '：完整外援评审图录', '', '本页按原298项评审页的当前卡面机械整理，不新增采用结论。**卡面的A/B/C或“采用”是当时的评审意见，不等于用户已确认。** 正式已定源仍以[已定图册](../../art/README.md)与逐图回执为准。', '', '旧图有的已被10月新母稿替代。读故事时不要把其原有造型、能力、身份或场景布局恢复成Canon。原图、历代修订和评语均供追溯。', ''];
  for (const item of items) {
    const image = path.posix.normalize(path.posix.join(path.posix.dirname(origin), item.image));
    if (!fs.existsSync(path.join(root, image))) throw new Error('Missing gallery image: ' + image);
    lines.push('## ' + item.id + ' ' + item.name, '', '![' + item.id + ' ' + item.name + '](' + path.relative(directories, path.join(root, image)).split(path.sep).join('/') + ')', '', '原卡面意见：' + (item.verdict || '见原记录') + '。', '', '[完整原卡面](../../../' + origin + '#' + item.id + ')；其余版本及实际源文件在[全量文件清单](../FILE-MANIFEST.tsv)中按ID、名称或文件路径查询。', '');
  }
  fs.writeFileSync(path.join(directories, group + '.md'), lines.join('\n'));
  groupLines.push('| ' + name + ' | ' + items.length + ' | [' + group + '类图录](galleries/' + group + '.md) |');
}
const gib = n => (n / 1024 ** 3).toFixed(2) + ' GiB';
const scopes = Object.entries(stats.by_scope).map(([k, v]) => '| `' + k + '` | ' + v.files + ' | ' + v.git_files + ' | ' + gib(v.bytes) + ' |');
const extraScopes = ['source_2d_design_sheets', 'early_2d_candidates_and_evidence', 'historical_demo_2d'];
const extraLines = ['# 制作目录设计图、早期候选与历史Demo二维资产', '', '这些文件不属于当前已定图册，不能从文件日期或存在状态推断采用。制作设计图是二维构造参考，不提供对应三维模型、贴图或绑定。早期候选和游戏截图只用于评审与追溯。', ''];
for (const scope of extraScopes) {
  extraLines.push('## ' + scope, '', '| 原文件 | 原有身份边界 |', '| --- | --- |');
  for (const row of records.filter(row => row.scope === scope)) extraLines.push('| [' + row.path + '](../../' + row.path.split('/').map(encodeURIComponent).join('/') + ') | `' + row.status + '` |');
  extraLines.push('');
}
fs.writeFileSync(path.join(root, 'review/library/EXTRA-2D-SOURCES.md'), extraLines.join('\n'));
const top = ['# 完整二维美术与设定资料库', '', '2026-10-26补齐版。上次的[已定图册](../art/README.md)只是精选确认范围，本页才是完整评审入口。**按用户最新要求，不上传三维资产。**', '', '**不要一次读取全部材料。** 先按[总目录](../00-总目录.md)读当前故事与设定，再按问题打开对应图录和原始文件。', '', '## 先分清四种用途', '', '- 已定源：看[04号入口](../04-美术风格与已定资产.md)和原始采用回执，只在其确认范围内有效。', '- 候选与待修：完整来稿、修订、M07/M12等新批次已提供，仍未自动取得采用或运行资格。', '- 历史与反例：保留原图和原评语供追溯，不能覆盖新母稿。', '- 游戏侧二维文件：立绘、场景背景、地图、图标、二维特效等；文件存在不证明已经在当前游戏加载或通过验收。', '', '## 全部298项图录', '', '| 类型 | 项数 | 入口 |', '| --- | --- | --- |', ...groupLines, '', '[原始完整评审页](../../' + origin + ')同时保留了新批次、历史反馈与原派单链接。最新内部源图另见[captures目录](../../captures/20261014-full-direction/review/20261016-internal-upgrade/)；不能用旧卡面覆盖该目录的明确采用记录。', '', '## 设定与原图', '', '- [设定分类入口](SETTINGS.md)：世界、人物、机体/IP、阵营、空间、玩法与生产方法。', '- [完整文件清单](FILE-MANIFEST.tsv)：每份原文件的路径、用途、保存位置、SHA和采用范围。', '- [具体排除项](EXCLUSIONS.tsv)：三维、缓存、自动备份、生成测试矩阵和第三方原始工具等未混入资产。', '- [覆盖与边界说明](../05-全量资产与设定覆盖说明.md)。', '', '## 覆盖统计', '', '| 来源范围 | 原文件数 | 仓库内 | 原始体积 |', '| --- | --- | --- | --- |', ...scopes, '', '共' + stats.files + '份原文件，' + gib(stats.bytes) + '，全部按清单放在Git目录中；不是只提供文件名或缩略图。', '', '不上传三维模型、绑定、三维材质/纹理、动作源及Blender工程。相关设定说明和二维设计图仍可以审阅，但不据此声称三维制作或运行已经通过。', ''];
fs.writeFileSync(path.join(root, 'review/library/README.md'), top.join('\n'));
const readmePath = path.join(root, 'review/library/README.md');
fs.writeFileSync(readmePath, fs.readFileSync(readmePath, 'utf8').replace('## 设定与原图', '## 设定与原图\n\n- [制作设计图、早期候选与历史Demo资产](EXTRA-2D-SOURCES.md)：补充不在298卡面中的二维原图与原有用途。'));
console.log(JSON.stringify({ cards: cards.length, groups: Object.keys(names).length, source_files: records.length, pass: true }));
