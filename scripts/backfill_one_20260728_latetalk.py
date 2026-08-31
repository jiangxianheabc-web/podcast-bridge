#!/usr/bin/env python3
"""
2026-07-28 手动补 1 集: 晚点聊 LateTalk #174 (AI 冲击企业软件巨头, SAP 原欣)
直接走 Groq 路径 (bcut/jianying 对 pdst.fm 不识别会卡 5min+ 超时)
"""
import os
import sys
from pathlib import Path

os.environ["PODCAST_BACKFILL_DATE"] = "2026-07-28"

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
import daily_podcast_digest_v2 as v2

# 单集配置
PODCAST = "晚点聊 LateTalk"
INDEX = "#1631"  # episode_no=174 字段为空, 用 id=1631


def main():
    day_root = v2.OUTPUT_BASE / "2026-07" / "2026-07-28"
    ep_dir = day_root / PODCAST
    ep_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎙️ 手动补集: {PODCAST} #{INDEX}")
    print(f"   输出目录: {ep_dir}")

    # 1. 拿 episode
    info = v2.get_episode_info(PODCAST, INDEX)
    if not info:
        print(f"❌ 找不到 episode #{INDEX}")
        if ep_dir.exists() and not any(ep_dir.iterdir()):
            ep_dir.rmdir()
        sys.exit(1)
    audio_url, episode_url, title, duration_seconds, published_at = info
    print(f"   ✅ {title[:60]}")
    print(f"   🔗 audio: {bool(audio_url)}")
    print(f"   📅 {published_at}")

    if "--dry-run" in sys.argv:
        return

    # 2. 直走 Groq (audio_url 路径, 跳过 bcut/jianying)
    safe_title = v2.sanitize_fn(title)[:40]
    output_path = ep_dir / f"{PODCAST}_{safe_title}_groq.md"

    print("\n🎙️ 直接 Groq Whisper (绕开 bcut)...")
    ok, result = v2.transcribe_with_groq_audio_url(
        audio_url, title, output_path, language="zh", published_at=published_at
    )
    if not ok:
        print(f"❌ Groq 失败: {result}")
        if ep_dir.exists() and not any(ep_dir.iterdir()):
            ep_dir.rmdir()
            print("   🧹 已清理空目录")
        sys.exit(1)

    # 找 transcript_path
    transcript_path = output_path if output_path.exists() else None
    if not transcript_path:
        cands = list(ep_dir.glob("*全文稿*.md")) + list(ep_dir.glob("*_groq.md"))
        if cands:
            transcript_path = cands[0]
    if not transcript_path or not transcript_path.exists():
        print(f"❌ 找不到转录稿: {ep_dir}")
        sys.exit(1)
    print(f"   ✅ 转录稿: {transcript_path.name} ({transcript_path.stat().st_size//1024} KB)")

    # 3. 生成 4 类笔记
    print("\n📝 生成笔记...")
    notes = v2.generate_all_notes(
        transcript_path=transcript_path,
        podcast=PODCAST,
        title=title,
        output_dir=ep_dir,
    )
    for nt, np in notes.items():
        if np:
            print(f"   ✅ {nt}: {Path(np).name}")
        else:
            print(f"   ❌ {nt}: 失败")

    # 4. 归档
    print("\n📦 归档...")
    try:
        v2.archive_to_obsidian("2026-07-28", [{"podcast": PODCAST, "index": "174", "title": title}], ep_dir)
        print("   ✅ 已归档")
    except Exception as e:
        print(f"   ⚠️ 归档失败: {e}")

    print(f"\n✅ 完成: {ep_dir}")


if __name__ == "__main__":
    main()