#!/usr/bin/env python3
"""
IndexNow 自动提交脚本
自动提交新URL到Yandex和Bing（通过IndexNow协议）
"""
import os
import json
import urllib.request
import urllib.error
from datetime import datetime

# IndexNow API密钥（从环境变量读取）
INDEXNOW_KEY = os.environ.get("INDEXNOW_KEY", "")
KEY_LOCATION = os.environ.get("KEY_LOCATION", "")
SITE_URL = "https://topventus.com"

def submit_urls(urls, search_engine="api.indexnow.org"):
    """
    提交URL到IndexNow
    search_engine: api.indexnow.org (同时提交到所有支持的引擎)
                   yandex.com (仅Yandex)
                   bing.com (仅Bing)
    """
    if not INDEXNOW_KEY:
        print("未配置INDEXNOW_KEY，跳过提交")
        return False

    endpoint = f"https://{search_engine}/indexnow"
    
    payload = {
        "host": "topventus.com",
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION or f"{SITE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            status = response.status
            if status == 200:
                print(f"✓ 成功提交 {len(urls)} 个URL到 {search_engine}")
                return True
            elif status == 202:
                print(f"✓ 已接受提交 {len(urls)} 个URL到 {search_engine}（稍后处理）")
                return True
            else:
                print(f"⚠ 提交到 {search_engine} 返回状态码: {status}")
                return False
    except urllib.error.HTTPError as e:
        print(f"✗ 提交到 {search_engine} 失败: HTTP {e.code} - {e.reason}")
        if e.code == 400:
            print("  可能原因: 密钥验证文件不存在或URL格式错误")
        elif e.code == 403:
            print("  可能原因: 密钥无效或验证文件未正确放置")
        return False
    except Exception as e:
        print(f"✗ 提交到 {search_engine} 失败: {str(e)}")
        return False

def get_new_urls():
    """
    获取需要提交的新URL列表
    从最近生成的AI文章中提取
    """
    urls = []
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 扫描当前目录下今天生成的AI文章
    for root, dirs, files in os.walk("."):
        for f in files:
            if f.startswith("news-ai-") and f.endswith(".html") and today in f:
                path = os.path.join(root, f).replace("\\", "/").lstrip("./")
                if path == "index.html":
                    url = f"{SITE_URL}/"
                else:
                    url = f"{SITE_URL}/{path.replace('.html', '')}"
                urls.append(url)
    
    # 如果没有今天的新文章，提交sitemap中的前10个URL
    if not urls:
        print("没有发现今天的新AI文章，提交首页和主要页面")
        urls = [
            f"{SITE_URL}/",
            f"{SITE_URL}/products.html",
            f"{SITE_URL}/about.html",
            f"{SITE_URL}/contact.html",
            f"{SITE_URL}/news.html",
        ]
    
    return urls

def main():
    print("=" * 60)
    print("IndexNow 自动提交")
    print("=" * 60)
    
    if not INDEXNOW_KEY:
        print("✗ 未配置INDEXNOW_KEY环境变量")
        print("  请在GitHub Secrets中添加 INDEXNOW_KEY")
        return
    
    print(f"API密钥: {INDEXNOW_KEY[:8]}...{INDEXNOW_KEY[-4:]}")
    print(f"验证文件: {SITE_URL}/{INDEXNOW_KEY}.txt")
    
    # 获取需要提交的URL
    urls = get_new_urls()
    print(f"\n待提交URL数量: {len(urls)}")
    for url in urls:
        print(f"  - {url}")
    
    # 提交到IndexNow（同时提交到Yandex和Bing）
    print("\n--- 提交到 IndexNow（Yandex + Bing）---")
    submit_urls(urls, "api.indexnow.org")
    
    # 单独提交到Yandex（可选，提高可靠性）
    print("\n--- 单独提交到 Yandex ---")
    submit_urls(urls, "yandex.com")
    
    # 单独提交到Bing（可选，提高可靠性）
    print("\n--- 单独提交到 Bing ---")
    submit_urls(urls, "bing.com")
    
    print("\n" + "=" * 60)
    print("IndexNow 提交完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
