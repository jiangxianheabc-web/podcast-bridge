#!/usr/bin/env python3
"""backfill_two_20260831_kuaguo.py — 补第 2 集: 跨国串门儿计划 #697 (2026-08-31)

触发: 用户 2026-08-31 17:07 要求再补 2 集。
候选理由: 8-31 当天发布, AI Work PM 主题, 与用户关注 AI/工程师 契合。
episode id=10241 (库表 episodes.id), 小宇宙直链 → Groq。
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

TARGET_PODCAST = "跨国串门儿计划"
TARGET_TITLE = "#697.ChatGPT Work产品经理：AI 同事正在接管执行，你的职业价值只剩下野心与判断力？"
TARGET_INDEX = "10241"
TODAY = "2026-08-31"

ep = {"podcast": TARGET_PODCAST, "title": TARGET_TITLE, "index": TARGET_INDEX,
      "category": "business_vc", "date": TODAY}

day_root = OUTPUT_BASE / "2026-08" / TODAY
day_root.mkdir(parents=True, exist_ok=True)
ep_dir = day_root / _safe_podcast_dirname(TARGET_PODCAST)
ep_dir.mkdir(parents=True, exist_ok=True)
tmp_dir = Path(f"/tmp/podcast_backfill_20260831_kuaguo")
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
record_picked(successful, TODAY)

log(f"\n✅ [backfill] 完成: {TARGET_PODCAST}")
log(f"   路径: {ep_dir}  笔记: {len(notes)} 份")