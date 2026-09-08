# 2026-09-08 SQLite stale subs 保留决定

## 背景
9-07 commit `94a60cd` 意图清理 10 个 90+ 天没新集的订阅，但只更新了 `subscriptions.json`，**没同步 SQLite**。

9-08 RSS refresh 时 9 个新源 silent fail（SQLite 找不到），subagent 诊断后发现**双向漂移**：
- JSON 有 / SQLite 无：9 个新源（INSERT 已完成）
- SQLite 有 / JSON 无：10 个 stale subs（跳岛FM/杂谈匣子/OnBoard!/随机漫谈/奇想驿/MacTalk·夜航西飞/一天世界/理解万岁/虎扯电台/正经不良人）

INSERT 9 个已完成（commit 4cdb4a5），DELETE 10 个 subagent 自动 defer（因 CASCADE 风险）。

## 决定
**保持现状：10 个 stale subs 名字继续躺在 SQLite，**丽哥9-08 21:41 拍板。

## 理由
- picker 候选池筛选只看30 天新集，这 10 个 90+ 天没新集**天然不会被选中** = 软删除
- 删除 CASCADE 会连 134 episodes + 12 已转录 transcript 一起删，风险不可逆
- 留着不影响性能、不影响 picker、不影响 RSS refresh
- 万一某个 podcast 复活，数据还在

## 风险评估
- 风险：0
- 副作用：0（picker 不会选中，未来也不会）
- 维护成本：0（无需任何 cron / 脚本处理）

## 关联
- commit `94a60cd` (9-07) cleanup 10 stale subs + add 9 active new sources — JSON 部分
- commit `4cdb4a5` (9-08) chore(podcast-bridge): resync 9 new subs from JSON to SQLite
- commit `33518c7` (9-08) feat(podcast-bridge): future 5ep backfill (F1+F3)
- commit `3034541` (9-08) backfill 9-08 半拿铁 No.217 宁波往事

## 何时重审
- 如未来 9-08 ~ 9-15 daily digest 仍报 4 集，可考虑回头清理（picker 应已自动用 9 个新源补回）
- 如某个被"保留"的 stale podcast 复活但 picker 仍没选它（理论不会），重新评估