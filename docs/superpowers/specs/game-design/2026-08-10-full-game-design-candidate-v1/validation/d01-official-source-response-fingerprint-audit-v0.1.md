# D01 官方来源响应指纹审计 v0.1

> Status: `Candidate research evidence / metadata-only / no Canon, Reader or Runtime authority`
>
> Capture window: `2026-08-10T12:14:52Z`–`2026-08-10T12:20:52Z`

## 结论

[source-response-fingerprints.tsv](../research/source-response-fingerprints.tsv) 已把 [source-evidence-ledger.tsv](../research/source-evidence-ledger.tsv) 的 15 条关键一手来源逐条绑定到本次真实 HTTP 请求结果：

- `13/15` 得到 HTTP 2xx 响应体，并记录最终 URL、内容类型、字节数与响应体 SHA-256；
- `2/15` 未取得响应体，均明确保留失败原因，`raw_sha256` 为空；
- 不保存网页／PDF正文，也不保存摘录，因此不存在以长文本副本代替官方来源的问题；
- 指纹只证明“本次 curl 写出的响应体字节是什么”，不证明页面定位在渲染后 DOM 中仍存在，更不证明任何候选机制已被本项目采用。

## 失败项

| evidence | 结果 | 边界 |
| --- | --- | --- |
| `SEV008` | XCOM 官方文章先发生 HTTP/2 framing error，改用 HTTP/1.1 后连接被对端重置；HTTP status 为 `000` | 本轮没有新响应体或哈希，不能把原 ledger 的人工定位称为本次重新验证 |
| `SEV009` | 2K 官方 PDF 请求超过 100 秒仍未返回可记录的响应元数据，随后终止 | HTTP status、最终 URL与内容类型均记为 `NOT_OBSERVED`，没有伪造 PDF 哈希 |

这两项仍可作为原 ledger 的人工核查记录，但本指纹层只给出“当前未恢复”；若它们承担关键取舍，应在后续受控刷新中重新抓取或换用同一发行商的可访问官方手册入口。

## 动态内容边界

- 所有 HTML 行都标注：未运行浏览器渲染，客户端注入内容可能不在响应体内；CDN、时间戳、A/B 或资源清单变化也可能造成哈希漂移。
- `SEV003` 在同一轮数分钟内的两次成功响应出现不同 SHA-256；表中仅保存较晚一次，不能把该哈希当成稳定内容版本号。
- `locator` 机械继承自原 ledger 并由 checker 锁定；因为正文未留存，checker 不声称 locator 字符串实际出现在响应体中。
- `raw_sha256` 指 curl 跟随重定向后写出的实体响应体字节，不含 HTTP headers、TLS 或传输帧。

## 只读验证

```bash
python3 -B docs/superpowers/specs/game-design/2026-08-10-full-game-design-candidate-v1/scripts/check_d01_source_response_fingerprints.py
```

校验器不联网、不写文件；它锁定 15 行一对一关系、ledger URL／locator、官方 HTTPS host、UTC 时间、成功哈希格式，以及失败项不得伪造哈希的语义。
