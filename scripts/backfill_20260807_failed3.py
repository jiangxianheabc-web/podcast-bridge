#!/usr/bin/env python3
"""
2026-08-07 手动 backfill: 补 3 集早上失败的（Groq Connection error / timeout）
策略: 直走 Groq 路径，跳过 bcut/jianying
失败集:
  - 井户端会议 — 【聊个球啊】40天与4年：美加墨世界杯"胜利结算"
  - 自习室 STUDY ROOM — 105 好能量｜把细胞作为方法，发现健康、代谢、生物钟的"反直觉"真相
  - 三五环 — No.228 对话滴滴曲晓楠：怕你觉得我们不安全，更怕你觉得我们绝对安全
"""
import os
import sys
from pathlib import Path

os.environ["PODCAST_BACKFILL_DATE"] = "2026-08-07"

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
import daily_podcast_digest_v2 as v2

# (podcast_name, episode_index_in_db, expected_title_for_log)
TARGETS = [
    ("自习室 STUDY ROOM", None, "105 好能量"),
    ("三五环", "No.228", "对话滴滴曲晓楠"),
]

def pick_latest_untranscribed(podcast_name: str):
    """从 db 找该播客最新 1 集且当天未转录的 episode。
    返回 (audio_url, episode_url, title, duration, published_at) 或 None
    """
    import sqlite3
    db_path = SCRIPT_DIR.parent / "podcast_library" / "library.sqlite3"
    if not db_path.exists():
        print(f"❌ db 不存在: {db_path}")
        return None
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 拿该 podcast 的最新 episodes（按 published_at desc）
    cur.execute("""
        SELECT e.id, e.title, e.audio_url, e.episode_url, e.duration_seconds, e.published_at
        FROM episodes e
        JOIN subscriptions s ON e.subscription_id = s.id
        WHERE s.name = ?
        ORDER BY e.published_at DESC
        LIMIT 10
    """, (podcast_name,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print(f"   ❌ db 里没找到 {podcast_name}")
        return None

    # 过滤：跳过已转录 + 跳过老集(>60d)
    import datetime as dt
    today = dt.datetime(2026, 8, 7)
    for r in rows:
        # 已转录检查
        if v2.is_already_transcribed(podcast_name, r["title"]):
            continue
        # 老集跳过
        if r["published_at"]:
            try:
                pub = dt.datetime.fromisoformat(r["published_at"].replace("Z", "+00:00"))
                if (today - pub.replace(tzinfo=None)).days > 60:
                    continue
            except Exception:
                pass
        # 至少要有 audio_url
        if not r["audio_url"]:
            continue
        return (r["audio_url"], r["episode_url"] or "", r["title"], r["duration_seconds"] or 0, r["published_at"] or "")
    return None


def process_one(podcast_name: str, hint: str):
    print(f"\n{'='*60}")
    print(f"🎙️ {podcast_name} — {hint}")
    print(f"{'='*60}")

    info = pick_latest_untranscribed(podcast_name)
    if not info:
        print(f"   ❌ 没找到可补的 episode")
        return False
    audio_url, episode_url, title, duration, published_at = info
    print(f"   ✅ {title[:60]}")
    print(f"   🔗 audio: {bool(audio_url)} | dur: {duration}s")
    print(f"   📅 {published_at}")

    day_root = v2.OUTPUT_BASE / "2026-08" / "2026-08-07"
    ep_dir = day_root / podcast_name
    ep_dir.mkdir(parents=True, exist_ok=True)

    safe_title = v2.sanitize_fn(title)[:40]
    output_path = ep_dir / f"{podcast_name}_{safe_title}_groq_backfill.md"

    # 防重复：output_path 已存在就跳过
    if output_path.exists():
        print(f"   ⏭️ 已存在: {output_path.name}")
        return True

    print("\n🎙️ 直接 Groq Whisper (绕开 bcut/jianying)...")
    ok, result = v2.transcribe_with_groq_audio_url(
        audio_url, title, output_path,
        language="zh", published_at=published_at
    )
    if not ok:
        print(f"   ❌ Groq 转录失败: {result}")
        # 清理空目录
        if ep_dir.exists() and not any(ep_dir.iterdir()):
            ep_dir.rmdir()
        return False

    # 读转录文本
    content = output_path.read_text(encoding="utf-8")
    transcript_text = content  # for similarity check
    v2.log("📝 生成总结性笔记...")

    # 二次校验 + 4 类笔记
    is_match, sim = v2.detect_misattribution_by_similarity(output_path, title)
    if not is_match:
        v2.log(f"    ⚠️ 相似度预警 (sim={sim:.2f})，可能错位，但允许生成并打标")
        try:
            sus_dir = Path("/root/.openclaw/workspace/state/podcast-misattribution")
            sus_dir.mkdir(parents=True, exist_ok=True)
            sus_path = sus_dir / f"20260807-backfill_sim-low_{podcast_name}_{output_path.name}"
            sus_path.write_text(
                f"# Low Similarity Warning (sim={sim:.2f})\n\n- expected_podcast: {podcast_name}\n- expected_title: {title}\n- transcript_path: {output_path}\n\n## Transcript head\n\n{transcript_text[:1500]}\n",
                encoding="utf-8"
            )
        except Exception:
            pass

    duration_match = __import__("re").search(r'\*\*时长\*\*:\s*(.+)', content)
    duration_str = duration_match.group(1) if duration_match else "未知"
    word_count = len(content.replace(' ', '').replace('\n', ''))
    safe_name = v2.sanitize_fn(f"{podcast_name}_{title}")[:40]

    ok_count = 0
    for key, gen_fn in [('product', v2.gen_product), ('structured', v2.gen_structured),
                         ('deep', v2.gen_deep), ('investment', v2.gen_investment)]:
        try:
            v2.log(f"    📝 生成 {key} 笔记（{v2.GROQ_LLM_MODEL}）...")
            path = gen_fn(content, podcast_name, title, duration_str, word_count,
                          "2026-08-07", ep_dir, safe_name, transcript_text)
            if path:
                ok_count += 1
                v2.log(f"    ✅ {key} 笔记完成: {path.name}")
        except Exception as e:
            v2.log(f"    ❌ {key} 笔记异常: {e}")

    if ok_count == 0:
        print(f"   ❌ 4 类笔记全部失败")
        return False

    print(f"   🎉 {ok_count}/4 篇笔记 + 全文稿归档完成")
    return True


def main():
    day_root = v2.OUTPUT_BASE / "2026-08" / "2026-08-07"
    day_root.mkdir(parents=True, exist_ok=True)

    success = 0
    for podcast, _idx, hint in TARGETS:
        if process_one(podcast, hint):
            success += 1

    print(f"\n{'='*60}")
    print(f"🎉 Backfill 完成: {success}/{len(TARGETS)} 集")
    print(f"{'='*60}")

    # 重写月份索引
    if success > 0:
        print("\n📁 重新生成月份索引...")
        import subprocess
        r = subprocess.run(
            ["python3", str(SCRIPT_DIR / "regenerate_monthly_index.py"), "--month", "2026-08"],
            capture_output=True, text=True, cwd=str(SCRIPT_DIR)
        )
        print(r.stdout)
        if r.returncode != 0:
            print(f"⚠️ 索引重写失败: {r.stderr}")

if __name__ == "__main__":
    main()