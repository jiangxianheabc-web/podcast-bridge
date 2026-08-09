#!/usr/bin/env python3
"""
2026-08-09 手动 backfill: 补 2 集早上失败的（Groq 403 Access denied 瞬时错误）
策略: 直走 Groq audio_url 路径（绕开 bcut/jianying），单集 retry 3 次 + 退避 10s/30s
失败集（2026-08-09 08:00 v2 主流程选中但 Groq 403）:
  - 开始连接LinkStart — Vol.128｜硅谷把 FDE 当 mini CTO 招？
  - 屠龙之术 — 2026AI狂飙、资本抽水与我们的"恩格斯暂停"---串台进击波财经

2026-08-10 丽哥指令：每天必须 5 集，本脚本作为 8-09 一次性兜底。
"""
import os
import sys
import time as _t
import re
import json
import shutil
from pathlib import Path

os.environ["PODCAST_BACKFILL_DATE"] = "2026-08-09"

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
import daily_podcast_digest_v2 as v2

# Hard-code targets（避免 rglob 全树扫超时；从 db 查好直接传）
TARGETS = [
    {
        "podcast": "开始连接LinkStart",
        "title": "Vol.128｜硅谷把 FDE 当 mini CTO 招？聊聊爆火的 AI 新职业",
        "audio_url": "https://dts-api.xiaoyuzhoufm.com/track/63ff0da51b1faf8a0b70b337/6a72a3dbab3a91c24a0ffc60/media.xyzcdn.net/63ff0da51b1faf8a0b70b337/lhfW1DKUJ-MY7GJ2Q55DQR0fgzfq.m4a",
        "published_at": "2026-08-05T02:52:07+00:00",
    },
    {
        "podcast": "屠龙之术",
        "title": "2026AI狂飙、资本抽水与我们的“恩格斯暂停”---串台进击波财经",
        "audio_url": "https://dts-api.xiaoyuzhoufm.com/track/6507bc165c88d2412626b401/6a5ee6f76356eb2d9be5d600/media.xyzcdn.net/6507bc165c88d2412626b401/llgbzyL7u_JPwMNkSRukXuiVNExC.m4a",
        "published_at": "2026-07-21T03:37:32+00:00",
    },
]


def already_done(podcast: str, title: str) -> bool:
    """仅检查目标日目录（不 rglob 全树）"""
    safe_title = v2.sanitize_fn(title)[:40]
    day_dir = v2.OUTPUT_BASE / "2026-08" / "2026-08-09" / podcast
    if not day_dir.exists():
        return False
    for f in day_dir.iterdir():
        # 全文稿/4 类笔记任一存在即视为已转录（2026-08-09 是新目录，0 笔记 = 未做）
        if f.suffix == ".md" and safe_title in f.name:
            return True
    return False


def process_one(target: dict) -> bool:
    podcast = target["podcast"]
    title = target["title"]
    audio_url = target["audio_url"]
    published_at = target["published_at"]

    print(f"\n{'='*60}")
    print(f"🎙️ {podcast}")
    print(f"   标题: {title[:60]}")
    print(f"{'='*60}")

    if already_done(podcast, title):
        print(f"   ⏭️ 已存在（2026-08-09/{podcast}/）→ 跳过")
        return True

    day_root = v2.OUTPUT_BASE / "2026-08" / "2026-08-09"
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
        print(f"   ❌ 第 {attempt} 次失败: {result}")
        if attempt < 3:
            wait = 10 if attempt == 1 else 30
            print(f"   ⏳ 等待 {wait}s 后重试...")
            _t.sleep(wait)

    if not success:
        print(f"   ❌ 重试 3 次仍失败: {last_err}")
        # 清理空目录
        if ep_dir.exists() and not any(ep_dir.iterdir()):
            ep_dir.rmdir()
        return False

    # 二次校验 + 4 类笔记
    content = output_path.read_text(encoding="utf-8")
    is_match, sim = v2.detect_misattribution_by_similarity(output_path, title)
    if not is_match:
        v2.log(f"    ⚠️ 相似度预警 (sim={sim:.2f})，可能错位，但允许生成并打标")
        try:
            sus_dir = Path("/root/.openclaw/workspace/state/podcast-misattribution")
            sus_dir.mkdir(parents=True, exist_ok=True)
            sus_path = sus_dir / f"20260809-backfill_sim-low_{podcast}_{output_path.name}"
            sus_path.write_text(
                f"# Low Similarity Warning (sim={sim:.2f})\n\n- expected_podcast: {podcast}\n- expected_title: {title}\n- transcript_path: {output_path}\n\n## Transcript head\n\n{content[:1500]}\n",
                encoding="utf-8"
            )
        except Exception:
            pass

    duration_match = re.search(r'\*\*时长\*\*:\s*(.+)', content)
    duration_str = duration_match.group(1) if duration_match else "未知"
    word_count = len(content.replace(' ', '').replace('\n', ''))
    safe_name = v2.sanitize_fn(f"{podcast}_{title}")[:40]

    v2.log("📝 生成总结性笔记...")
    ok_count = 0
    for key, gen_fn in [('product', v2.gen_product), ('structured', v2.gen_structured),
                         ('deep', v2.gen_deep), ('investment', v2.gen_investment)]:
        try:
            v2.log(f"    📝 生成 {key} 笔记（{v2.GROQ_LLM_MODEL}）...")
            path = gen_fn(content, podcast, title, duration_str, word_count,
                          "2026-08-09", ep_dir, safe_name, content)
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
    day_root = v2.OUTPUT_BASE / "2026-08" / "2026-08-09"
    day_root.mkdir(parents=True, exist_ok=True)

    # 备份 last_picked（参照 8-07 模板：保留作为永久去重）
    last_picked_path = v2.LAST_PICKED_PATH
    backup_path = Path(f"/root/.openclaw/workspace/backups/podcast-backfill-last-picked-20260809.json")
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    if last_picked_path.exists() and not backup_path.exists():
        shutil.copy2(last_picked_path, backup_path)
        print(f"📦 备份 last_picked → {backup_path}")

    success = 0
    for t in TARGETS:
        if process_one(t):
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

    # 更新 last_picked（backfill 永久标记）
    if success > 0:
        try:
            data = json.loads(last_picked_path.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        for t in TARGETS:
            data.setdefault(t["podcast"], [])
            if "2026-08-09" not in data[t["podcast"]]:
                data[t["podcast"]].append("2026-08-09")
        last_picked_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"📝 已更新 last_picked: {len(TARGETS)} 集 2026-08-09 标记")


if __name__ == "__main__":
    main()
