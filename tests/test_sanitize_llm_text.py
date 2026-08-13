#!/usr/bin/env python3
"""
test_sanitize_llm_text.py — 验证 podcast-bridge sanitize_llm_text() 的 injection 防护

🆕 2026-08-13 subagent batch 3 LOW #3 (security-architect L):
  验证 bleach 等价保护 (html.escape) 真正阻断 HTML/JS 注入.

原任务: bleach.clean(text, tags=['b', 'i', 'code', 'pre'])
实际: bleach 不在 deps (requirements.txt 明确零依赖), html.escape() (stdlib) 达同样安全目标.
html.escape 严格度 > bleach (escape 所有 tags), 但 security 等价 (都阻断 XSS/iframe/on*=).

约束: 不引入 pytest 等新依赖 — 用 stdlib unittest, 满足"零依赖"哲学.

执行: python3 -m unittest tests/test_sanitize_llm_text.py -v
"""
import sys
import os
import unittest
from pathlib import Path

# 加 scripts/ 到 sys.path, 让 import daily_podcast_digest_v2 可解析
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


class TestSanitizeLlmText(unittest.TestCase):
    """sanitize_llm_text() 注入防护 — bleach 等价验证"""

    @classmethod
    def setUpClass(cls):
        """延迟 import (脚本可能 import 其他重依赖, 仅在测试需要时触发)"""
        from daily_podcast_digest_v2 import sanitize_llm_text
        cls.sanitize = staticmethod(sanitize_llm_text)

    def test_blocks_script_tag_injection(self):
        """N=1 主要场景: 阻断 <script>alert('xss')</script> 类注入.

        原 bleach 也会 strip, html.escape 转义为 &lt;script&gt; — 浏览器解析为文本, 不执行.
        """
        malicious = "<script>alert('xss')</script>恶意文本"
        escaped = self.sanitize(malicious)
        self.assertNotIn("<script>", escaped, f"未转义 <script>: {escaped!r}")
        self.assertNotIn("</script>", escaped, f"未转义 </script>: {escaped!r}")
        self.assertIn("&lt;script&gt;", escaped, "html.escape 应该输出 &lt;script&gt;")
        self.assertIn("恶意文本", escaped, "中文内容应保留")
        print(f"  ✓ script-tag blocked: {escaped!r}")


if __name__ == "__main__":
    unittest.main(verbosity=2)