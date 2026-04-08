#!/usr/bin/env python3
"""Sync Dida365 inbox URLs to Cubox, summarize each, report to Telegram.

Uses asyncio + aiohttp for concurrent processing of all tasks.
"""

import asyncio
import json
import os
import re
import sys
from datetime import datetime

import aiohttp

DIDA365_TOKEN = os.environ.get("DIDA365_ACCESS_TOKEN", "")
CUBOX_API_KEY = os.environ.get("CUBOX_API_KEY", "")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = "5166227669"
GLM_API_KEY = os.environ.get("Z_AI_API_KEY", "")
DIDA365_API = "https://api.dida365.com/open/v1"
INBOX_ID = "inbox"
STATE_FILE = os.environ.get("DIDA_CUBOX_STATE_FILE", "/home/z/my-project/.dida_cubox_sync.json")
FETCH_SCRIPT = os.environ.get(
    "FETCH_SCRIPT_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".agents", "skills", "web-content-fetcher", "scripts", "fetch.py"),
)
ZAI_CLI = os.environ.get("ZAI_CLI_PATH", "zai-cli")

# Concurrency limit for web fetching & GLM calls
CONCURRENCY = 5
TIMEOUT = aiohttp.ClientTimeout(total=60)


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {"saved_titles": []}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def extract_url_and_title(task):
    """Extract (url, title) from a Dida365 task. Returns (None, None) if no URL."""
    title = task.get("title", "") or ""
    content = task.get("content") or ""

    m = re.search(r'\[(.+?)\]\((https?://[^\)]+)\)', title)
    if m:
        return m.group(2), m.group(1)

    if title.startswith("http"):
        return title, ""

    # content field may contain URL (e.g. YouTube links from mobile)
    if content.startswith("http"):
        return content, title

    # Also check for URLs anywhere in content
    m = re.search(r'(https?://[^\s]+)', content)
    if m:
        return m.group(1), title

    return None, None


async def save_to_cubox(session, url, title=""):
    payload = json.dumps({"type": "url", "content": url, "title": title})
    try:
        async with session.post(CUBOX_API_KEY, data=payload, headers={"Content-Type": "application/json"}, timeout=aiohttp.ClientTimeout(total=15)) as resp:
            data = await resp.json(content_type=None)
            return data.get("code") == 200
    except Exception:
        return False


async def send_telegram(session, text):
    if not TELEGRAM_TOKEN:
        return
    if len(text) > 4000:
        text = text[:3900] + "\n\n... (内容过长已截断)"
    try:
        await session.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": text},
            timeout=aiohttp.ClientTimeout(total=10),
        )
    except Exception:
        pass


async def delete_dida_task(session, project_id, task_id):
    try:
        async with session.delete(
            f"{DIDA365_API}/project/{project_id}/task/{task_id}",
            headers={"Authorization": f"Bearer {DIDA365_TOKEN}"},
            timeout=aiohttp.ClientTimeout(total=10),
        ) as resp:
            return resp.status == 200
    except Exception:
        return False


async def read_url_content(url):
    """Try fetch.py first (handles WeChat etc.), fallback to zai-cli (handles B站 etc.), then direct HTTP. Returns (content, method)."""
    # Method 1: fetch.py (web-content-fetcher) — handles JS-rendered pages like WeChat
    try:
        proc = await asyncio.create_subprocess_exec(
            "python3", FETCH_SCRIPT, url,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=30)
        web_content = stdout.decode("utf-8", errors="replace")
        if web_content and len(web_content.strip()) >= 50 and not web_content.startswith("Error"):
            return web_content, "fetch.py"
    except Exception:
        pass

    # Method 2: zai-cli read — handles B站 etc., returns JSON with title/description/content
    try:
        proc = await asyncio.create_subprocess_exec(
            ZAI_CLI, "read", url, "--no-images",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=30)
        data = json.loads(stdout.decode("utf-8", errors="replace"))
        # Prefer description (video/article meta) over content (often just nav/recommendations)
        parts = []
        desc = data.get("description", "")
        if desc and len(desc) >= 30:
            parts.append(desc)
        content_items = data.get("content", [])
        for item in content_items:
            if item.get("type") == "text":
                text = item.get("text", "").strip()
                if text and len(text) >= 20:
                    parts.append(text)
        web_content = "\n\n".join(parts)
        if len(web_content.strip()) >= 50:
            return web_content, "zai-cli"
    except Exception:
        pass

    # Method 3: direct HTTP fetch via aiohttp
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as s:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            }
            async with s.get(url, headers=headers) as resp:
                html = await resp.text(errors="replace")
                # Simple text extraction: strip tags
                text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
                text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
                text = re.sub(r'<[^>]+>', ' ', text)
                text = re.sub(r'&[a-zA-Z]+;', ' ', text)
                text = re.sub(r'\s+', ' ', text).strip()
                if len(text) >= 50:
                    return text, "http"
    except Exception:
        pass

    return None, None


async def summarize_url(url, title=""):
    """Read URL content, then summarize with GLM. Returns (summary, error_msg)."""
    web_content, method = await read_url_content(url)

    if not web_content or len(web_content.strip()) < 50:
        return None, f"网页内容为空或过短 (抓取 {len(web_content.strip()) if web_content else 0} 字符, 方法: {method or '无'})"

    # Clean up
    web_content = re.sub(r'!\[.*?\]\(.*?\)', '', web_content)
    web_content = re.sub(r'\n{3,}', '\n\n', web_content).strip()
    web_content = web_content[:5000]

    # GLM summarize
    prompt = (
        "请对以下文章生成一份简洁的中文分析总结，严格按以下格式输出：\n\n"
        "🏷️ 关键词：3-5个关键词，逗号分隔\n"
        "📝 摘要：2-3句话概括核心内容\n"
        "💡 亮点：1-2个值得关注的要点\n\n"
        f"文章内容：\n{web_content}"
    )

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as s:
            async with s.post(
                "https://open.bigmodel.cn/api/paas/v4/chat/completions",
                headers={
                    "Authorization": f"Bearer {GLM_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "glm-4-flash",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 500,
                },
            ) as resp:
                data = await resp.json(content_type=None)
                if "error" in data:
                    return None, f"GLM API 错误: {data['error'].get('message', data['error'])}"
                return data["choices"][0]["message"]["content"].strip(), None
    except Exception as e:
        return None, f"GLM 请求失败: {e}"


async def process_task(session, task, saved_titles):
    """Process a single task: cubox save, dida delete, summarize. Returns stats dict."""
    task_id = task.get("id", "")
    project_id = task.get("projectId", INBOX_ID)
    title = task.get("title", "").strip()

    url, display_title = extract_url_and_title(task)
    if not url:
        return None

    # Dedup check
    if title in saved_titles:
        await delete_dida_task(session, project_id, task_id)
        return {"skipped": True, "deleted": True}

    # Save to Cubox + Delete from Dida365 (concurrent)
    cubox_ok, dida_ok = await asyncio.gather(
        save_to_cubox(session, url, display_title),
        delete_dida_task(session, project_id, task_id),
    )

    if cubox_ok:
        saved_titles.add(title)

    # Summarize
    print(f"Summarizing: {display_title[:50]}...")
    summary, error = await summarize_url(url, display_title)
    if summary:
        summary_text = summary
    else:
        summary_text = f"⚠️ 摘要生成失败\n\n{error}"

    return {
        "title": display_title,
        "summary": summary_text,
        "cubox_saved": cubox_ok,
        "deleted": dida_ok,
        "skipped": False,
    }


async def main():
    if not DIDA365_TOKEN or not CUBOX_API_KEY:
        print("ERROR: DIDA365_ACCESS_TOKEN or CUBOX_API_KEY not set")
        sys.exit(1)

    state = load_state()
    saved_titles = set(state["saved_titles"])

    # Get inbox tasks
    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        async with session.get(
            f"{DIDA365_API}/project/{INBOX_ID}/data",
            headers={"Authorization": f"Bearer {DIDA365_TOKEN}"},
        ) as resp:
            data = await resp.json(content_type=None)

    tasks = data.get("tasks", [])
    if not tasks:
        print("No tasks in inbox")
        return

    # Filter URL tasks
    url_tasks = [t for t in tasks if extract_url_and_title(t)[0] is not None]
    if not url_tasks:
        print("No URL tasks in inbox")
        return

    # Process all tasks concurrently with semaphore
    sem = asyncio.Semaphore(CONCURRENCY)

    async def guarded_process(session, task):
        async with sem:
            return await process_task(session, task, saved_titles)

    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        results = await asyncio.gather(
            *[guarded_process(session, t) for t in url_tasks],
            return_exceptions=True,
        )

    # Aggregate results
    cubox_saved = 0
    deleted = 0
    skipped = 0
    summaries = []

    for r in results:
        if isinstance(r, Exception):
            print(f"Task error: {r}")
            continue
        if r is None:
            continue
        if r.get("skipped"):
            skipped += 1
            if r.get("deleted"):
                deleted += 1
            continue
        if r.get("cubox_saved"):
            cubox_saved += 1
        if r.get("deleted"):
            deleted += 1
        summaries.append((r["title"], r["summary"]))

    # Save state
    state["saved_titles"] = list(saved_titles)
    state["last_sync"] = datetime.now().isoformat()
    save_state(state)

    # Build report
    if cubox_saved > 0 or skipped > 0:
        header = "📦 滴答清单 → Cubox 同步报告\n\n"
        stats = []
        if cubox_saved > 0:
            stats.append(f"✅ 转存 {cubox_saved} 条到 Cubox")
        if skipped > 0:
            stats.append(f"⏭️ 跳过 {skipped} 条重复")
        if deleted > 0:
            stats.append(f"🗑️ 清理 {deleted} 条滴答清单")
        report = header + "\n".join(stats)

        print(report)

        async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
            await send_telegram(session, report)
            for display_title, summary in summaries:
                msg = f"📄 {display_title}\n\n{summary}"
                print(f"Sending summary for: {display_title[:40]}...")
                await send_telegram(session, msg)
    else:
        print("Nothing to do")


if __name__ == "__main__":
    asyncio.run(main())
