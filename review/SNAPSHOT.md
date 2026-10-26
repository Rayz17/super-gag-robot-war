# 外部评审资料快照

2026-10-26，按最新用户范围：故事、设定、玩法文字与设计类美术；不含UI/UE、运行截图和三维资产。原工程、Canon、Story Chain及用户验收未修改。

- [总目录](00-总目录.md)：阅读顺序。
- [设计资料库](library/README.md)：134项设计对象及相关原图/修订。
- [覆盖说明](05-全量资产与设定覆盖说明.md)：来源和排除边界。
- [文本清单](SOURCE-MANIFEST.tsv)、[完整文件清单](library/FILE-MANIFEST.tsv)：原路径、大小和指纹。
- [已定图册](art/README.md)：54份确认源设计与其有限确认范围；其他候选、授权派生及历史参考不升格。

原129份精选清单留在[历史清单](history/d8ca567-ASSET-MANIFEST.tsv)。本次按新范围移出其中的界面整帧/战术画面参考，并保留原先发布的Git历史，不改写旧提交。

## 验证

[文本与导航](VALIDATION.json)、[精选源图](art/VALIDATION.json)、[完整清单](library/VALIDATION.json)分别检查实际文件、字节、SHA、图片尺寸、导航与范围。原始历史文件可能引用本轮明确排除的制作素材，不能据此要求恢复UI或三维。当前人工整理的阅读入口必须可打开。

本地检查不等于已上传；发布后单独核对远端Git树。文件完整也不等于美术、故事或玩法质量通过。

## 维护

资料在隔离评审仓库整理，不改原项目工作区。源文件不缩图、不改设定。原导出工具保留历史用途，但不能直接覆盖当前设计范围；同步时需先按最新范围过滤，再生成设计图录、验证并显式发布。

```bash
node tools/filter-design-review.mjs
node tools/build-design-review-index.mjs
node tools/validate-complete-review.mjs
node tools/validate-review-snapshot.mjs
node tools/validate-art-supplement.mjs
```
