#!/usr/bin/env python3
"""
2026-07-27 Backfill: 补昨天 7-26 缺 2 集 + 今天 7-27 缺 1 集（共 3 集）

硬编码目标（基于候选池分析）：
- 7-26 补 #1: 枫言枫语 Vol.165（4-07, last_picked 21d 前，RSS 已停更但有未转内容）
- 7-26 补 #2: 诗梳风 EP17 (5-14)
- 7-27 补 #1: 开始连接LinkStart Vol.121 (6-08)

设计：
- 复用 v2 的 transcribe_episode / generate_all_notes / archive_to_obsidian
- 仅替换 select_episodes → 硬编码 3 集（last_picked 黑名单由 v2 的 is_already_transcribed 自然处理）
- 复用 PODCAST_BACKFILL_DATE 环境变量机制（v2 已支持）→ 用 today 不同调用两次 main

⚠️ 注意：
- max_episode_age=60d / max_source_age=90d 会拦 Vol.165 (113d) 和 EP17 (74d)
- 解决：在 import v2 后 monkey-patch MAX_EPISODE_AGE_DAYS=200, MAX_SOURCE_AGE_DAYS=200
- 或在 select_episodes 内 stale 检查时主动 skip staleness (本期人工补)
- 选 monkey-patch，对 v2 改动最小

用法:
  PODCAST_BACKFILL_DATE=2026-07-26 python3 backfill_2026_07_26_27.py --pod 枫言枫语 --pod 诗梳风
  PODCAST_BACKFILL_DATE=2026-07-27 python3 backfill_2026_07_26_27.py --pod 开始连接LinkStart

执行计划:
  1. 7-26 补枫言枫语 (Vol.165)
  2. 7-26 补诗梳风 (EP17)
  3. 7-27 补开始连接LinkStart (Vol.121)
  三个进程串行；每集 8-12 分钟（Groq ASR + 4 LLM）；总时长 ~36 分钟
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# ============== 路径 ==============
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
import daily_podcast_digest_v2 as v2  # noqa: E402

# ============== 配置：放宽 staleness 边界 ==============
# 仅本次 backfill 期间放宽，跑完恢复
_ORIG_MAX_EP = v2.MAX_EPISODE_AGE_DAYS
_ORIG_MAX_SRC = v2.MAX_SOURCE_AGE_DAYS
v2.MAX_EPISODE_AGE_DAYS = 200  # 默认 60 → 200，允许 200 天内的内容
v2.MAX_SOURCE_AGE_DAYS = 200   # 默认 90 → 200，允许源 200 天没更新

# ============== 目标清单（按 day → [(podcast_name, episode_title_match)]） ==============
# 注：episode_title_match 用于在 get_recent_episodes 里定位具体集
#     v2 的 get_recent_episodes 拉最近 N 集，limit=5 → 选返回的第 1 个；
#     但 7-02 已转过 Vol.167 (5-28)，Vol.165 在它之后才推送（4-07 实际在 Vol.167 之前）→ 顺序反了
#     所以必须"自定义"：跳过 v2 select，复用转录+笔记

BACKFILL_TASKS = {
    "2026-07-26": [
        {"podcast": "枫言枫语", "title_keyword": "Vol. 165", "ep_index_hint": 165},
        {"podcast": "诗梳风", "title_keyword": "EP17", "ep_index_hint": 17},
    ],
    "2026-07-27": [
        {"podcast": "开始连接LinkStart", "title_keyword": "Vol.121", "ep_index_hint": 121},
    ],
}


def get_episode_by_index(podcast_name: str, target_title_keyword: str):
    """从 v2 的 get_recent_episodes 拿到 episodes 列表，找匹配 title_keyword 的集

    返回 dict {podcast, category, index, date, title} 或 None
    """
    eps = v2.get_recent_episodes(podcast_name, limit=30)  # 拉多点
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
    """跑一天的多集 backfill"""
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

    if not_selected := not_found:
        print(f"\n⚠️ 有 {len(not_selected)} 个未找到，跳过")
        for nf in not_selected:
            print(f"   - {nf}")

    if not selected:
        print("\n❌ 没有任何可跑集")
        return [], []

    print(f"\n🚀 准备转录 {len(selected)} 集 ({today})\n")

    # 调用 v2.main 但要拦截 select_episodes——直接用我们准备的 selected
    # v2.main 内 select_episodes() 会覆盖我们的，所以 monkey-patch
    v2.select_episodes = lambda subs: selected
    successful, failed = [], []
    try:
        v2.main()
    except SystemExit:
        pass
    finally:
        # 恢复（避免污染后续 v2 调用）
        v2.select_episodes = v2.__dict__.get("select_episodes") or _orig_select_episodes

    return successful, failed


# 备份原始 select_episodes（备用）
_orig_select_episodes = v2.select_episodes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", choices=["2026-07-26", "2026-07-27", "both"], default="both")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        # 只 dry 列出，不会真转
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

    # 真跑
    days = ["2026-07-26", "2026-07-27"] if args.date == "both" else [args.date]
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
