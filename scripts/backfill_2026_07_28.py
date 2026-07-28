#!/usr/bin/env python3
"""
2026-07-28 Backfill: 给今天补 5 集（中文优先 + 从未选过）

候选（基于 transcribe.py rss list 实时拉取结果 2026-07-28 10:50）：
1. 卫诗婕｜商业漫谈 Jane's talk — #39 77.智元/觅蜂/具身智能
2. 知行小酒馆 — #35 E239 沈帅波 自媒体
3. 42章经 — #34 泡沫 4 必要不充分 + 朱宁
4. 硬地骇客 — EP127 Agent 接管真实生产力
5. 硅谷101 — E239 SpaceX 太空算力

设计：
- 复用 v2.7.2 的 transcribe_episode / generate_all_notes / archive_to_obsidian
- monkey-patch select_episodes() → 硬编码 5 集
- PODCAST_BACKFILL_DATE=2026-07-28 让 v2 输出到今天目录
- 放宽 staleness 边界（这些源最近 14-19 天没更新，但有 6 月内容）

⚠️ 注意：
- is_already_transcribed 由 v2 自动处理
- 不更新 last_picked（保持今天选中状态以供明早 4 天窗口用）
- 实际写 Obsidian 7-28/<podcast>/{5个md}

用法:
  python3 backfill_2026_07_28.py --dry-run  # 只看候选
  python3 backfill_2026_07_28.py             # 实际跑
"""

from __future__ import annotations
import argparse
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
import daily_podcast_digest_v2 as v2  # noqa: E402

# 放宽 staleness（这些源 14-19 天没更新，但有 6 月内容值得补）
_ORIG_MAX_EP = v2.MAX_EPISODE_AGE_DAYS
_ORIG_MAX_SRC = v2.MAX_SOURCE_AGE_DAYS
v2.MAX_EPISODE_AGE_DAYS = 60
v2.MAX_SOURCE_AGE_DAYS = 90

# 硬编码 5 集目标
BACKFILL_TARGETS = [
    {"podcast": "卫诗婕｜商业漫谈 Jane's talk", "index": "39"},
    {"podcast": "知行小酒馆", "index": "35"},
    {"podcast": "42章经", "index": "34"},
    {"podcast": "硬地骇客", "index": "127"},
    {"podcast": "硅谷101", "index": "22"},
]

# 备份原始 select_episodes
_orig_select_episodes = v2.select_episodes


def find_episode(podcast_name: str, target_index: str):
    """从 v2.get_recent_episodes 找匹配 index 的集"""
    eps = v2.get_recent_episodes(podcast_name, limit=10)
    for ep in eps:
        if str(ep.get("index")) == str(target_index):
            return {
                "podcast": podcast_name,
                "category": "backfill",
                "index": ep.get("index"),
                "date": ep.get("date"),
                "title": ep.get("title"),
            }
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=5, help="跑几集（默认 5）")
    args = parser.parse_args()

    today = "2026-07-28"
    os.environ["PODCAST_BACKFILL_DATE"] = today

    print(f"🎯 2026-07-28 backfill，目标 {args.limit} 集")
    print(f"⚙️  MAX_EP_AGE={v2.MAX_EPISODE_AGE_DAYS}d, MAX_SRC_AGE={v2.MAX_SOURCE_AGE_DAYS}d")
    print(f"📅 输出目录: {v2.OUTPUT_BASE}/{today[:7]}/{today}/")
    print()

    selected = []
    not_found = []
    for target in BACKFILL_TARGETS[:args.limit]:
        print(f"🔍 查找: {target['podcast']} #{target['index']}")
        ep = find_episode(target["podcast"], target["index"])
        if ep:
            selected.append(ep)
            print(f"  ✅ {ep['title'][:80]}")
        else:
            not_found.append(target)
            print(f"  ❌ 未找到（可能 RSS 失效）")

    if not_found:
        print(f"\n⚠️ {len(not_found)} 个未找到：")
        for nf in not_found:
            print(f"   - {nf['podcast']} #{nf['index']}")

    if not selected:
        print("\n❌ 没有可跑集")
        return 1

    if args.dry_run:
        print(f"\n🔍 DRY-RUN: 找到 {len(selected)} 集，不会实际转录")
        for ep in selected:
            print(f"   {ep['podcast']} #{ep['index']} → {ep['title'][:80]}")
        return 0

    print(f"\n🚀 开始转录 {len(selected)} 集 (PODCAST_BACKFILL_DATE={today})\n")

    # monkey-patch select_episodes → 跳过自动选择
    v2.select_episodes = lambda subs: selected
    try:
        v2.main()
    except SystemExit:
        pass
    except Exception as e:
        print(f"\n❌ 异常: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        v2.select_episodes = _orig_select_episodes
        v2.MAX_EPISODE_AGE_DAYS = _ORIG_MAX_EP
        v2.MAX_SOURCE_AGE_DAYS = _ORIG_MAX_SRC

    print(f"\n✅ 跑完。请检查: /mnt/c/Users/lili/Documents/LILINotes/播客转录/2026-07/2026-07-28/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
