#!/usr/bin/env python3
"""backfill_one_20260831_tulong.py — 补 1 集屠龙之术 (2026-08-31)

触发原因:
  daily_podcast_digest_v2.py 8-31 只挑了 2 集 (卫诗婕 + 十字路口), 平时 5 集。
  屠龙之术 8-31 发布了新一期 "模型到底吃不吃应用?--从 Canva、Figma 到美图,
  看 AI 应用公司的两种命运" 但被 days=3 黑名单屏蔽 (8-29/8-30 选过)。
  用户 2026-08-31 16:43 要求补缺失。

行为:
  1. 走 daily_podcast_digest_v2 内部函数 transcribe_episode + generate_all_notes
  2. 输出到 /mnt/c/Users/lili/Documents/LILINotes/播客转录/2026-08/2026-08-31/
  3. 复用 archive_to_obsidian (月份索引) + sync_to_daily_note (Daily Note)
  4. record_picked 把屠龙之术加入 last_picked.json (days=3 黑名单一致)

执行: python3 scripts/backfill_one_20260831_tulong.py
"""
import sys
import time
import shutil
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR))

from scripts.daily_podcast_digest_v2 import (
    transcribe_episode,
    generate_all_notes,
    archive_to_obsidian,
    sync_to_daily_note,
    record_picked,
    _safe_podcast_dirname,
    sanitize_fn,
    OUTPUT_BASE,
    log,
)

TARGET_PODCAST = "屠龙之术"
# 库里精确 title (全角? + 全角,)
TARGET_TITLE = "模型到底吃不吃应用？--从 Canva、Figma 到美图， 看 AI 应用公司的两种命运"
# episodes 表 id (episode_no 为空, 用 id 精确匹配)
TARGET_INDEX = "10146"
TODAY = "2026-08-31"

ep = {
    "podcast": TARGET_PODCAST,
    "title": TARGET_TITLE,
    "index": TARGET_INDEX,
    "category": "business_vc",
    "date": TODAY,
}

# day_root 与 daily digest 一致: /mnt/c/.../播客转录/2026-08/2026-08-31/
day_root = OUTPUT_BASE / "2026-08" / TODAY
day_root.mkdir(parents=True, exist_ok=True)
ep_dir = day_root / _safe_podcast_dirname(TARGET_PODCAST)
ep_dir.mkdir(parents=True, exist_ok=True)
tmp_dir = Path(f"/tmp/podcast_backfill_20260831_tulong")
tmp_dir.mkdir(parents=True, exist_ok=True)

print(f"[backfill] 目标: {TARGET_PODCAST} — {TARGET_TITLE}")
print(f"[backfill] 输出: {ep_dir}")

# 1. 转录
log(f"\n{'='*60}\n📻 [backfill] {TARGET_PODCAST} — {TARGET_TITLE}\n{'='*60}")
success, result = transcribe_episode(ep, tmp_dir)
if not success:
    log(f"❌ [backfill] 转录失败: {result}")
    sys.exit(1)

# 2. 归档全文稿
src = Path(result)
dst = ep_dir / f"{TARGET_PODCAST}_{sanitize_fn(TARGET_TITLE)}_全文稿.md"
shutil.copy2(src, dst)

# 3. 生成 4 类笔记
notes = generate_all_notes(dst, TARGET_PODCAST, TARGET_TITLE, ep_dir)
for name, path in notes.items():
    log(f"   ✅ {name}: {path.name}")

# 4. 更新月份索引 + Daily Note + last_picked
successful = [{"podcast": TARGET_PODCAST, "title": TARGET_TITLE,
               "transcript": dst, "notes": notes}]
archive_to_obsidian(TODAY, successful, day_root)
sync_to_daily_note(TODAY, successful, day_root)
record_picked(successful, TODAY)

log(f"\n✅ [backfill] 完成! 补 1 集: {TARGET_PODCAST}")
log(f"   路径: {ep_dir}")
log(f"   笔记: {len(notes)} 份")