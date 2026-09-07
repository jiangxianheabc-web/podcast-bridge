#!/usr/bin/env python3
"""
2026-09-07 丽哥拍板 backfill：实际只缺 1 集（之前误诊 7 集，审计后只有 9-03 纵横四海 EP033 真缺）
策略: 直走 Groq audio_url 路径（绕开 bcut/jianying），单集 retry 3 次
注：daily_podcast_digest_v2 已包含 last_picked 防重复；本脚本仅补缺失集

1 集清单 (id, podcast, target_day_dir)：
  1. id=8951  What's Next｜科技早知道   S10E27  → 2026-08-29
  2. id=8836  井户端会议                一番赏     → 2026-08-28
  3. id=8506  屠龙之术                一级半     → 2026-08-26
  4. id=8376  AI炼金术                XMind     → 2026-08-25
  5. id=7406  硅谷101                E249     → 2026-08-24
  6. id=2061  起朱楼宴宾客              公募基金   → 2026-08-09
  7. id=4196  罗永浩的十字路口          X字路口   → 2026-08-09
"""
import os
import sys
import json
import time as _t
import sqlite3
import re
import shutil
from pathlib import Path
from datetime import datetime, timezone

os.environ["PODCAST_BACKFILL_DATE"] = "2026-09-07"

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))
import daily_podcast_digest_v2 as v2

# 1 个真缺集: 9-03 纵横四海 EP033 (picker bug 把硬地骇客 EP129 重复 pick 了 2 次，
# 导致 unique 候选只有 4，1 个 unique 失败 = 纵横四海 EP033)
# 8-24/25/26/28/29 + 9-01 每天 4 集已完整，是 picker 候选池缩水（stale 源 6+ 个）的副作用，非缺集
TARGET_IDS = [
    (8256, "2026-09-03"),  # 纵横四海 EP033 洗浴经济
]

DB = SKILL_DIR / "podcast_library" / "library.sqlite3"


def load_target(ep_id: int, daily_date: str):
    conn = sqlite3.connect(str(DB))
    row = conn.execute("""
        SELECT e.audio_url, e.episode_url, e.title, e.duration_seconds, e.published_at, s.name
        FROM episodes e
        JOIN subscriptions s ON e.subscription_id = s.id
        WHERE e.id = ?
    """, (ep_id,)).fetchone()
    conn.close()
    if not row:
        return None
    audio_url, ep_url, title, duration, pub, podcast = row
    return {
        "id": ep_id, "podcast": podcast, "title": title,
        "audio_url": audio_url, "episode_url": ep_url,
        "duration": duration, "published_at": pub,
        "daily_date": daily_date,
    }


def already_done(podcast: str, title: str, daily_date: str) -> bool:
    """检查目标日目录是否已有该集 4 类笔记中的任一"""
    safe_title = v2.sanitize_fn(title)[:40]
    day_dir = v2.OUTPUT_BASE / daily_date[:7] / daily_date / podcast
    if not day_dir.exists():
        return False
    note_files = ["产品洞察", "结构化笔记", "深度笔记", "投资分析"]
    for f in day_dir.iterdir():
        if f.suffix == ".md" and safe_title in f.name:
            return True
    return False


def process_one(target: dict) -> dict:
    podcast = target["podcast"]
    title = target["title"]
    audio_url = target["audio_url"]
    daily_date = target["daily_date"]
    published_at = target["published_at"]

    print(f"\n{'='*70}")
    print(f"🎙️ [{daily_date}] {podcast}")
    print(f"   标题: {title[:60]}")
    print(f"   audio: {'✅' if audio_url else '❌ 无音频URL'}")
    print(f"{'='*70}")

    if not audio_url:
        return {"ok": False, "reason": "no audio_url", "target": target}

    if already_done(podcast, title, daily_date):
        print(f"   ⏭️  已存在 → 跳过")
        return {"ok": True, "skipped": True, "target": target}

    day_root = v2.OUTPUT_BASE / daily_date[:7] / daily_date
    ep_dir = day_root / podcast
    ep_dir.mkdir(parents=True, exist_ok=True)

    safe_title = v2.sanitize_fn(title)[:40]
    output_path = ep_dir / f"{podcast}_{safe_title}_groq_backfill.md"

    # Groq audio_url 直链 + retry 3 次
    last_err = None
    success = False
    for attempt in (1, 2, 3):
        print(f"\n🎙️ [尝试 {attempt}/3] Groq Whisper (audio_url, zh)...")
        ok, result = v2.transcribe_with_groq_audio_url(
            audio_url, title, output_path,
            language="zh", published_at=published_at
        )
        if ok:
            success = True
            print(f"   ✅ 转录成功: {Path(result).name}")
            break
        last_err = result
        print(f"   ❌ 第 {attempt} 次失败: {str(result)[:120]}")
        if attempt < 3:
            wait = 10 if attempt == 1 else 30
            print(f"   ⏳ 等待 {wait}s 后重试...")
            _t.sleep(wait)

    if not success:
        print(f"   ❌ 重试 3 次仍失败: {last_err}")
        if ep_dir.exists() and not any(ep_dir.iterdir()):
            ep_dir.rmdir()
        return {"ok": False, "reason": f"groq_3x_fail: {last_err}", "target": target}

    # 找 transcript_path
    transcript_path = output_path if output_path.exists() else None
    if not transcript_path:
        cands = list(ep_dir.glob("*_groq_backfill.md")) + list(ep_dir.glob("*全文稿*.md"))
        if cands:
            transcript_path = cands[0]
    if not transcript_path or not transcript_path.exists():
        print(f"   ❌ 找不到转录稿: {ep_dir}")
        return {"ok": False, "reason": "no transcript after success", "target": target}

    print(f"   ✅ 转录稿: {transcript_path.name} ({transcript_path.stat().st_size//1024} KB)")

    # 生成 4 类笔记
    print("\n📝 生成笔记...")
    notes = v2.generate_all_notes(
        transcript_path=transcript_path,
        podcast=podcast,
        title=title,
        output_dir=ep_dir,
    )
    note_paths = {}
    for nt, np in notes.items():
        if np:
            print(f"   ✅ {nt}: {Path(np).name}")
            note_paths[nt] = np

    if len(note_paths) < 3:
        return {"ok": False, "reason": f"only {len(note_paths)}/4 notes", "target": target}

    return {"ok": True, "skipped": False, "target": target, "notes": note_paths}


def main():
    print(f"🚀 Backfill 启动 - {datetime.now().isoformat()}")
    print(f"   目标: {len(TARGET_IDS)} 集")

    results = []
    for ep_id, daily_date in TARGET_IDS:
        t = load_target(ep_id, daily_date)
        if not t:
            print(f"\n❌ db 找不到 id={ep_id}")
            results.append({"ok": False, "reason": "db_miss", "id": ep_id})
            continue
        results.append(process_one(t))

    # 汇总
    print(f"\n\n{'='*70}")
    print("📊 Backfill 汇总")
    print(f"{'='*70}")
    ok_count = sum(1 for r in results if r.get("ok") and not r.get("skipped"))
    skip_count = sum(1 for r in results if r.get("ok") and r.get("skipped"))
    fail_count = sum(1 for r in results if not r.get("ok"))
    print(f"✅ 成功: {ok_count}")
    print(f"⏭️  跳过 (已存在): {skip_count}")
    print(f"❌ 失败: {fail_count}")
    if fail_count > 0:
        print("\n失败详情:")
        for r in results:
            if not r.get("ok"):
                print(f"  - {r}")

    # 重生 2026-08 月份索引
    if ok_count > 0:
        print(f"\n📁 重生 2026-08 月份索引...")
        try:
            subprocess_run = __import__("subprocess").run
            r = subprocess_run(
                ["python3", str(SCRIPT_DIR / "regenerate_monthly_index.py"), "--month", "2026-08"],
                capture_output=True, text=True, cwd=str(SKILL_DIR)
            )
            print(r.stdout[-500:] if r.returncode == 0 else r.stderr[-500:])
        except Exception as e:
            print(f"   ⚠️ 月份索引重生失败: {e}")

    sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()