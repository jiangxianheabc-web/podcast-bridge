#!/usr/bin/env python3
"""
每日播客摘要自动化脚本
每天自动挑选8集不同类型的播客节目，转录并生成笔记
"""

import subprocess
import json
import os
import random
import sys
import time
from pathlib import Path
from datetime import datetime

# 配置
SKILL_DIR = Path("/root/.openclaw/workspace/skills/podcast-bridge")
OUTPUT_BASE = Path("/mnt/c/Users/lili/Documents/LILINotes/播客转录")
CONFIG_PATH = SKILL_DIR / "config.json"
SUBSCRIPTIONS_PATH = SKILL_DIR / "subscriptions.json"
MAX_EPISODES = 5

# 播客分类（按主题类型）
PODCAST_CATEGORIES = {
    "tech_ai": ["Latent Space", "The TWIML AI Podcast", "Practical AI", "Gradient Dissent", 
                "No Priors", "The Cognitive Revolution", "Interconnects", "The AI Daily Brief",
                "AI炼金术", "人民公园说AI", "Latent Space: The AI Engineer Podcast"],
    "business_vc": ["Acquired", "All-In", "My First Million", "42章经", "晚点聊 LateTalk",
                   "张小珺Jùn｜商业访谈录", "OnBoard!", "十字路口Crossing", "半拿铁",
                   "起朱楼宴宾客", "知行小酒馆", "罗永浩的十字路口"],
    "tech_product": ["硅谷101", "What's Next｜科技早知道", "硬地骇客", "枫言枫语",
                     "一派·Podcast（少数派）", "MacTalk·夜航西飞"],
    "culture_humanities": ["东腔西调", "跳岛FM", "一天世界", "不合时宜", "不可理论",
                          "岩中花述", "井户端会议", "日谈公园", "乱翻书"],
    "personal_growth": ["保持偏见", "天真不天真", "理解万岁", "无人知晓", "三五环",
                        "自习室 STUDY ROOM", "不丧", "杂谈匣子"],
    "startup_founder": ["Founders", "The Knowledge Project", "Diary of a CEO",
                        "Lex Fridman Podcast", "Dwarkesh Podcast", 
                        "卫诗婕｜商业漫谈 Jane's talk", "开始连接LinkStart"],
    "entertainment": ["跟宇宙结婚", "啊是猫咪呀", "皮蛋漫游记", "跨国串门儿计划",
                      "虎扯电台", "正经不良人", "西西弗高速"],
    "health_science": ["Huberman Lab"]
}

def load_subscriptions():
    """加载播客订阅列表"""
    try:
        with open(SUBSCRIPTIONS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 无法加载订阅列表: {e}")
        return []

def get_recent_episodes(podcast_name, limit=5):
    """获取播客最近几期节目"""
    try:
        result = subprocess.run(
            ["python3", str(SKILL_DIR / "transcribe.py"), "rss", "list", podcast_name, 
             "--limit", str(limit)],
            capture_output=True,
            text=True,
            timeout=30
        )
        lines = result.stdout.strip().split('\n')
        episodes = []
        for line in lines:
            if line.startswith('[#') or line.startswith('['):
                # 解析行格式: [#1] 2026-06-22 未转录 标题
                try:
                    parts = line.split(None, 3)
                    if len(parts) >= 4:
                        idx_part = parts[0].strip('[]#')
                        date = parts[1]
                        status = parts[2]
                        title = parts[3]
                        if "未转录" in status or "已转录" in status:
                            episodes.append({
                                'index': idx_part,
                                'date': date,
                                'title': title,
                                'raw_line': line
                            })
                except:
                    continue
        return episodes
    except Exception as e:
        print(f"⚠️ 获取 {podcast_name} 节目列表失败: {e}")
        return []

def select_episodes(subscriptions):
    """从所有播客中挑选8集不同类型的节目"""
    selected = []
    used_categories = set()
    
    # 建立播客名到订阅信息的映射
    sub_map = {sub['name']: sub for sub in subscriptions}
    
    # 按分类随机选择
    categories = list(PODCAST_CATEGORIES.keys())
    random.shuffle(categories)
    
    for category in categories:
        if len(selected) >= MAX_EPISODES:
            break
        if category in used_categories:
            continue
            
        # 找到该分类下的播客
        podcasts_in_cat = PODCAST_CATEGORIES[category]
        random.shuffle(podcasts_in_cat)
        
        for podcast_name in podcasts_in_cat:
            if len(selected) >= MAX_EPISODES:
                break
            if podcast_name not in sub_map:
                continue
                
            # 获取最近节目
            episodes = get_recent_episodes(podcast_name, limit=3)
            if not episodes:
                continue
                
            # 选最新一期未转录的
            for ep in episodes:
                selected.append({
                    'podcast': podcast_name,
                    'category': category,
                    'index': ep['index'],
                    'date': ep['date'],
                    'title': ep['title']
                })
                used_categories.add(category)
                break
    
    # 如果不够8集，从其他播客补充
    if len(selected) < MAX_EPISODES:
        all_names = [sub['name'] for sub in subscriptions]
        random.shuffle(all_names)
        for name in all_names:
            if len(selected) >= MAX_EPISODES:
                break
            # 检查是否已选过
            if any(s['podcast'] == name for s in selected):
                continue
            episodes = get_recent_episodes(name, limit=2)
            if episodes:
                ep = episodes[0]
                selected.append({
                    'podcast': name,
                    'category': 'misc',
                    'index': ep['index'],
                    'date': ep['date'],
                    'title': ep['title']
                })
    
    return selected[:MAX_EPISODES]

def transcribe_episode(podcast_name, episode_index, output_dir, asr_provider=None):
    """转录单集播客，支持 ASR fallback"""
    providers = [asr_provider] if asr_provider else ["bcut", "jianying"]
    
    for provider in providers:
        try:
            cmd = [
                "python3", str(SKILL_DIR / "transcribe.py"), "rss", "transcribe",
                podcast_name, str(episode_index), "--chapters"
            ]
            if provider:
                cmd.extend(["--asr-provider", provider])
            
            print(f"    🎙️ 尝试 ASR: {provider or 'default'}...")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600,
                cwd=str(SKILL_DIR)
            )
            
            # 解析输出找到转录文件路径
            output_lines = result.stdout.strip().split('\n')
            transcript_path = None
            for line in output_lines:
                if line.endswith('.md') and ('transcripts' in line or '/' in line):
                    transcript_path = line.strip()
                    break
            
            if transcript_path and Path(transcript_path).exists():
                return True, transcript_path
            else:
                # 检查默认输出位置
                lib_dir = SKILL_DIR / "podcast_library" / "transcripts"
                if lib_dir.exists():
                    recent_files = sorted(lib_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
                    if recent_files:
                        return True, str(recent_files[0])
            
            # 如果还有下一个 provider，继续尝试
            if provider != providers[-1]:
                print(f"    ⚠️ {provider} 失败，尝试备用 ASR...")
                time.sleep(5)  # 短暂延迟避免限流
                continue
            
            return False, result.stderr or "未知错误"
        except subprocess.TimeoutExpired:
            if provider == providers[-1]:
                return False, "转录超时"
            print(f"    ⏱️ {provider} 超时，尝试备用 ASR...")
            time.sleep(5)
            continue
        except Exception as e:
            if provider == providers[-1]:
                return False, str(e)
            print(f"    ⚠️ {provider} 异常: {e}，尝试备用 ASR...")
            time.sleep(5)
            continue
    
    return False, "所有 ASR provider 均失败"

def generate_notes(transcript_paths, output_dir):
    """生成总结性笔记"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 创建笔记文件
    notes_path = output_dir / f"_{today}_播客摘要笔记.md"
    
    content = f"# 播客每日摘要 {today}\n\n"
    content += f"> 今日共转录 {len(transcript_paths)} 集播客\n\n"
    
    for i, (path, info) in enumerate(transcript_paths, 1):
        content += f"## {i}. {info['podcast']} — {info['title']}\n\n"
        content += f"- **分类**: {info['category']}\n"
        content += f"- **日期**: {info['date']}\n"
        content += f"- **转录文件**: [{Path(path).name}]({path})\n\n"
        
        # 尝试读取转录稿前100行作为摘要
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:50]
                content += "**要点摘录**:\n\n"
                for line in lines:
                    line = line.strip()
                    if line.startswith('#') or line.startswith('>') or line.startswith('-'):
                        content += f"{line}\n"
                content += "\n---\n\n"
        except:
            content += "*(转录稿暂不可读)*\n\n---\n\n"
    
    content += f"\n*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"
    content += "*工具: podcast-bridge 自动转录*\n"
    
    notes_path.write_text(content, encoding='utf-8')
    return str(notes_path)

def main():
    """主流程"""
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = OUTPUT_BASE / today
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📅 今日播客摘要: {today}")
    print("=" * 50)
    
    # 1. 加载订阅
    subscriptions = load_subscriptions()
    if not subscriptions:
        print("❌ 没有播客订阅")
        sys.exit(1)
    
    print(f"📻 已加载 {len(subscriptions)} 个播客订阅")
    
    # 2. 挑选8集
    selected = select_episodes(subscriptions)
    if not selected:
        print("❌ 未能挑选到节目")
        sys.exit(1)
    
    print(f"\n🎯 已挑选 {len(selected)} 集节目:\n")
    for ep in selected:
        print(f"  [{ep['category']}] {ep['podcast']} — {ep['title']}")
    
    # 3. 转录
    print(f"\n🎙️ 开始转录...\n")
    transcript_results = []
    failed_episodes = []
    
    for ep in selected:
        print(f"  ⏳ 转录: {ep['podcast']} — {ep['title'][:50]}...")
        success, result = transcribe_episode(ep['podcast'], ep['index'], output_dir)
        if success:
            print(f"    ✅ 完成")
            transcript_results.append((result, ep))
            # 复制到输出目录
            try:
                src = Path(result)
                dst = output_dir / f"{ep['podcast'].replace('/', '_')}_{ep['title'][:30]}.md"
                import shutil
                shutil.copy2(src, dst)
            except:
                pass
        else:
            print(f"    ❌ 失败: {result}")
            failed_episodes.append((ep, result))
        # 每集之间增加延迟，避免触发限流
        time.sleep(3)
    
    # 如果有失败，尝试用备用 ASR 重试
    if failed_episodes:
        print(f"\n🔄 尝试用备用 ASR 重试 {len(failed_episodes)} 集失败节目...")
        for ep, fail_reason in failed_episodes:
            # 备用 ASR：如果之前用 bcut 失败，用 jianying 重试；反之亦然
            backup_provider = "jianying" if "bcut" in str(fail_reason).lower() else "bcut"
            print(f"  ⏳ 重试: {ep['podcast']} — {ep['title'][:50]}... (ASR: {backup_provider})")
            success, result = transcribe_episode(ep['podcast'], ep['index'], output_dir, asr_provider=backup_provider)
            if success:
                print(f"    ✅ 重试成功")
                transcript_results.append((result, ep))
                try:
                    src = Path(result)
                    dst = output_dir / f"{ep['podcast'].replace('/', '_')}_{ep['title'][:30]}.md"
                    import shutil
                    shutil.copy2(src, dst)
                except:
                    pass
            else:
                print(f"    ❌ 重试也失败: {result}")
            time.sleep(5)
    
    # 4. 生成笔记
    if transcript_results:
        print(f"\n📝 生成总结笔记...", end=" ")
        notes_path = generate_notes(transcript_results, output_dir)
        print(f"✅ {notes_path}")
    
    print(f"\n🎉 完成! 输出目录: {output_dir}")
    print(f"   成功转录: {len(transcript_results)}/{len(selected)} 集")

if __name__ == "__main__":
    main()
