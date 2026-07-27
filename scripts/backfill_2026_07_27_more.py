#!/usr/bin/env python3
"""
2026-07-27 Backfill: 补今天缺 3 集（当前 2 集 → 补到 5 集）

硬编码目标：
- 集 1: My First Million 7-15 Howard Marks (last_pick 7-25 已转录过此订阅，但具体集不同)
       → 候选：My First Million 7-17 Ray Dalio: The principles that made me a billionaire
- 集 2: Diary of a CEO 7-16 Cancer Researcher (last_pick 7-24, 7-25 已转录过此订阅) 
       → 候选：Diary of a CEO 7-17 Framework To Instantly Become... 
- 集 3: Knowledge Project 7-21 Truth Over Feelings Opendoor (last_pick NEVER → 新订阅)
       → 候选：Knowledge Project 7-21 Truth Over Feelings: Inside Opendoor's Massive Tur

设计：
- 复用 v2 的 transcribe_episode / generate_all_notes / archive_to_obsidian
- 仅替换 select_episodes → 硬编码 3 集
- 复用 PODCAST_BACKFILL_DATE 环境变量机制（v2 已支持）

注意：
- 这些是 discovered 状态（audio 还没下载）→ v2 主流程会自动下 audio
- 时长（duration_seconds）未知 → 由 v2 transcribe_episode 内部 bcut / Groq ASR 时获取

用法:
  PODCAST_BACKFILL_DATE=2026-07-27 python3 backfill_2026_07_27_more.py --dry-run
  PODCAST_BACKFILL_DATE=2026-07-27 python3 backfill_2026_07_27_more.py
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
import daily_podcast_digest_v2 as v2  # noqa: E402

# ============== 配置：放宽 staleness 边界 ==============
_ORIG_MAX_EP = v2.MAX_EPISODE_AGE_DAYS
_ORIG_MAX_SRC = v2.MAX_SOURCE_AGE_DAYS
v2.MAX_EPISODE_AGE_DAYS = 200
v2.MAX_SOURCE_AGE_DAYS = 200

# ============== 目标清单 ==============
# 优先 discovered 状态的新集 + 没 transcript_path
BACKFILL_TASKS = {
    "2026-07-27": [
        {"podcast": "My First Million", "title_keyword": "Ray Dalio"},
        {"podcast": "The Knowledge Project", "title_keyword": "Truth Over Feelings"},
        {"podcast": "Founders", "title_keyword": "Red Hat"},
    ],
}


def get_episode_by_index(podcast_name: str, target_title_keyword: str):
    """从 v2 的 get_recent_episodes 拿 episodes 列表，找匹配 title_keyword 的集"""
    eps = v2.get_recent_episodes(podcast_name, limit=30)
    if not eps:
        return None
    for ep in eps:
        if target_title_keyword in ep.get("title", ""):
            return {
                "podcast": podcast_name,
                "category": "backfill",
                "index": ep.get("index"),
                "date": ep.get("date"),
                "title": ep.get("title"),
            }
    return None


def run_one_day(today: str, tasks: list[dict]) -> tuple[list, list]:
    os.environ["PODCAST_BACKFILL_DATE"] = today

    selected = []
    not_found = []
    for task in tasks:
        print(f"\n🔍 查找: {today} → {task['podcast']} '{task['title_keyword']}'")
        ep = get_episode_by_index(task["podcast"], task["title_keyword"])
        if ep:
            selected.append(ep)
            print(f"  ✅ 找到: {ep['title'][:60]} (pub={ep.get('date')})")
        else:
            not_found.append(task)
            print(f"  ❌ 未找到: {task['podcast']} {task['title_keyword']}")

    if not selected:
        print("\n❌ 没有任何可跑集")
        return [], []

    print(f"\n🚀 准备转录 {len(selected)} 集 ({today})\n")

    # Monkey-patch select_episodes
    v2.select_episodes = lambda subs: selected
    successful, failed = [], []
    try:
        v2.main()
    except SystemExit:
        pass
    finally:
        v2.select_episodes = _orig_select_episodes

    return successful, failed


_orig_select_episodes = v2.select_episodes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default="2026-07-27")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        print("🔍 DRY-RUN 模式：只查找 episode，不会实际转录\n")
        for date, tasks in BACKFILL_TASKS.items():
            if args.date != "both" and args.date != date:
                continue
            print(f"\n=== {date} ===")
            for task in tasks:
                ep = get_episode_by_index(task["podcast"], task["title_keyword"])
                if ep:
                    print(f"  ✅ {task['podcast']} → {ep['title'][:60]} (date={ep.get('date')})")
                else:
                    print(f"  ❌ {task['podcast']} {task['title_keyword']} → NOT FOUND")
        return

    days = ["2026-07-27"] if args.date != "both" else list(BACKFILL_TASKS.keys())
    all_ok, all_fail = [], []
    for d in days:
        ok, fail = run_one_day(d, BACKFILL_TASKS[d])
        all_ok.extend(ok)
        all_fail.extend(fail)

    print(f"\n{'='*60}")
    print(f"🏁 总结果")
    print(f"   成功: {len(all_ok)} / 失败: {len(all_fail)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()