#!/usr/bin/env python3
"""backfill_three_20260831_aijin.py — 补第 3 集: AI炼金术 OPC (2026-08-29)

触发: 用户 2026-08-31 17:07 要求再补 2 集。
候选理由: 8-29 发布, FDE/Forward Deployed Engineer 主题, 与用户 MPLS 工程师
背景 + AI 时代职业转型关注高度契合。
episode id=9586, 喜马拉雅音频 URL → Groq fallback。
"""
import sys
import shutil
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR))

from scripts.daily_podcast_digest_v2 import (
    transcribe_episode, generate_all_notes, archive_to_obsidian,
    sync_to_daily_note, record_picked, _safe_podcast_dirname,
    sanitize_fn, OUTPUT_BASE, log,
)

TARGET_PODCAST = "AI炼金术"
TARGET_TITLE = "OPC 已经凉了，FDE 会有光明的未来么？"
TARGET_INDEX = "9586"
TODAY = "2026-08-31"

ep = {"podcast": TARGET_PODCAST, "title": TARGET_TITLE, "index": TARGET_INDEX,
      "category": "tech_ai", "date": TODAY}

day_root = OUTPUT_BASE / "2026-08" / TODAY
day_root.mkdir(parents=True, exist_ok=True)
ep_dir = day_root / _safe_podcast_dirname(TARGET_PODCAST)
ep_dir.mkdir(parents=True, exist_ok=True)
tmp_dir = Path(f"/tmp/podcast_backfill_20260831_aijin")
tmp_dir.mkdir(parents=True, exist_ok=True)

log(f"\n{'='*60}\n📻 [backfill] {TARGET_PODCAST} — {TARGET_TITLE}\n{'='*60}")
success, result = transcribe_episode(ep, tmp_dir)
if not success:
    log(f"❌ [backfill] 转录失败: {result}")
    sys.exit(1)

src = Path(result)
dst = ep_dir / f"{TARGET_PODCAST}_{sanitize_fn(TARGET_TITLE)}_全文稿.md"
shutil.copy2(src, dst)

notes = generate_all_notes(dst, TARGET_PODCAST, TARGET_TITLE, ep_dir)
for name, path in notes.items():
    log(f"   ✅ {name}: {path.name}")

successful = [{"podcast": TARGET_PODCAST, "title": TARGET_TITLE,
               "transcript": dst, "notes": notes}]
# 多个 backfill 并行时, archive/sync 由最后一个 backfill 或主脚本统一调用
# 本脚本是最后一个, 负责刷新月份索引 + Daily Note
from scripts.daily_podcast_digest_v2 import archive_to_obsidian, sync_to_daily_note
archive_to_obsidian(TODAY, successful, day_root)
sync_to_daily_note(TODAY, successful, day_root)
record_picked(successful, TODAY)

log(f"\n✅ [backfill] 完成: {TARGET_PODCAST}")
log(f"   路径: {ep_dir}  笔记: {len(notes)} 份")