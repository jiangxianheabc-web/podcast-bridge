#!/usr/bin/env python3
"""
重新生成所有月份索引页
- 扫描 播客转录/2026-MM/ 全部日目录
- 输出 播客转录/2026-MM.md 月份索引
- 同时更新月份索引中每个 pod 的笔记数量

用法：
  python3 regenerate_monthly_index.py                  # 重生全部
  python3 regenerate_monthly_index.py --month 2026-06  # 只重生一个月
  python3 regenerate_monthly_index.py --dry-run
"""
import argparse
import sys
from pathlib import Path
from datetime import datetime
import re

OBSIDIAN_ROOT = Path("/mnt/c/Users/lili/Documents/LILINotes/播客转录")
NOTE_KEYWORDS = ["产品洞察", "投资分析", "深度笔记", "结构化笔记"]
DAY_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def regenerate_month(month_dir: Path, month_str: str, dry_run: bool = False) -> int:
    """重写单月索引页，返回写入的 pod 数"""
    if not month_dir.exists():
        return 0
    
    lines = [
        "---",
        "tags: [podcast-archive, monthly]",
        f"month: {month_str}",
        "---",
        "",
        f"# 📻 播客转录 — {month_str}",
        "",
    ]
    
    days = sorted([d for d in month_dir.iterdir() if d.is_dir() and DAY_PATTERN.match(d.name)], reverse=True)
    total_pods = 0
    total_days = 0
    
    for day_dir in days:
        pods = sorted([d for d in day_dir.iterdir() if d.is_dir() and not d.name.startswith('.')])
        if not pods:
            continue
        total_days += 1
        lines.append(f"## {day_dir.name}")
        lines.append("")
        for ep_dir in pods:
            md_files = list(ep_dir.glob("*.md"))
            n = len(md_files)
            total_pods += 1
            lines.append(f"- **{ep_dir.name}** ({n})")
        lines.append("")
    
    # 顶部加统计
    header = f"共 {total_days} 天, {total_pods} 个节目\n"
    
    content = "\n".join(lines) + "\n"
    if not content.startswith("---"):
        content = "---\nt" + content
    
    if dry_run:
        print(f"[DRY-RUN] {month_str}: {total_days} 天, {total_pods} pod")
        print(content[:500])
    else:
        out = OBSIDIAN_ROOT / f"{month_str}.md"
        out.write_text(content, encoding="utf-8")
        print(f"✅ {month_str}: 写了 {total_pods} pod → {out}")
    
    return total_pods


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", help="指定月份 2026-07")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    
    if args.month:
        month_dir = OBSIDIAN_ROOT / args.month
        regenerate_month(month_dir, args.month, args.dry_run)
        return
    
    # 扫描所有月份
    months = sorted([d for d in OBSIDIAN_ROOT.iterdir() if d.is_dir() and re.match(r"^\d{4}-\d{2}$", d.name)])
    print(f"=" * 60)
    print(f"📋 找到 {len(months)} 个月份目录")
    print(f"=" * 60)
    
    total = 0
    for m in months:
        n = regenerate_month(m, m.name, args.dry_run)
        total += n
    
    print(f"\n🏁 完成: 处理 {len(months)} 个月, 共 {total} 个 pod")


if __name__ == "__main__":
    main()