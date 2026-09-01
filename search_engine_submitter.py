#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动提交sitemap到搜索引擎
支持：Google Indexing API、Bing Webmaster API、Yandex Webmaster API
"""

import os
import json
import urllib.request
import urllib.parse
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITEMAP_URL = 'https://topventus.com/sitemap.xml'

# API凭证（从环境变量读取）
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')
GOOGLE_CLIENT_EMAIL = os.environ.get('GOOGLE_CLIENT_EMAIL', '')
GOOGLE_PRIVATE_KEY = os.environ.get('GOOGLE_PRIVATE_KEY', '')

BING_API_KEY = os.environ.get('BING_API_KEY', '')
BING_SITE_URL = 'https://topventus.com'

YANDEX_USERNAME = os.environ.get('YANDEX_USERNAME', '')
YANDEX_API_KEY = os.environ.get('YANDEX_API_KEY', '')
YANDEX_HOST = 'topventus.com'


def submit_to_google(urls):
    """提交URL到Google Indexing API"""
    print('\n=== 提交到Google ===')

    if not GOOGLE_API_KEY or not GOOGLE_CLIENT_EMAIL or not GOOGLE_PRIVATE_KEY:
        print('  ⚠ 未配置Google API凭证，跳过')
        print('  需要: GOOGLE_API_KEY, GOOGLE_CLIENT_EMAIL, GOOGLE_PRIVATE_KEY')
        return False

    try:
        # Google Indexing API需要JWT认证，这里简化处理
        # 实际使用时需要安装google-auth库
        print(f'  准备提交 {len(urls)} 个URL到Google')
        print('  ⚠ Google Indexing API需要服务账号认证')
        print('  建议手动提交: https://search.google.com/search-console')
        return False
    except Exception as e:
        print(f'  ✗ 提交失败: {e}')
        return False


def submit_to_bing(urls):
    """提交URL到Bing Webmaster API"""
    print('\n=== 提交到Bing ===')

    if not BING_API_KEY:
        print('  ⚠ 未配置BING_API_KEY，跳过')
        print('  获取API Key: https://www.bing.com/webmasters/about')
        return False

    try:
        # Bing URL Submission API
        api_url = f'https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlBatch?apikey={BING_API_KEY}'

        data = {
            'siteUrl': BING_SITE_URL,
            'urlList': urls[:100]  # Bing限制每次最多100个URL
        }

        req = urllib.request.Request(
            api_url,
            data=json.dumps(data).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'charset': 'utf-8'
            },
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f'  ✓ 成功提交 {len(urls[:100])} 个URL到Bing')
            return True

    except Exception as e:
        print(f'  ✗ 提交失败: {e}')
        return False


def submit_to_yandex(sitemap_url):
    """提交sitemap到Yandex Webmaster"""
    print('\n=== 提交到Yandex ===')

    if not YANDEX_USERNAME or not YANDEX_API_KEY:
        print('  ⚠ 未配置Yandex凭证，跳过')
        print('  需要: YANDEX_USERNAME (登录邮箱), YANDEX_API_KEY')
        print('  获取API Key: https://webmaster.yandex.ru/')
        return False

    try:
        # Yandex Webmaster API - 添加sitemap
        encoded_host = urllib.parse.quote(YANDEX_HOST, safe='')
        api_url = f'https://api.webmaster.yandex.net/v4/user/{YANDEX_USERNAME}/hosts/{encoded_host}/user-added-sitemaps'

        data = {
            'url': sitemap_url
        }

        req = urllib.request.Request(
            api_url,
            data=json.dumps(data).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'OAuth {YANDEX_API_KEY}'
            },
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f'  ✓ 成功提交sitemap到Yandex')
            print(f'    Sitemap ID: {result.get("sitemap_id", "N/A")}')
            return True

    except Exception as e:
        print(f'  ✗ 提交失败: {e}')
        return False


def get_all_urls_from_sitemap():
    """从sitemap.xml获取所有URL"""
    print('\n=== 读取sitemap.xml ===')
    try:
        req = urllib.request.Request(SITEMAP_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8')

            # 简单解析XML提取URL
            import re
            urls = re.findall(r'<loc>(.*?)</loc>', content)
            print(f'  ✓ 从sitemap获取 {len(urls)} 个URL')
            return urls
    except Exception as e:
        print(f'  ✗ 读取sitemap失败: {e}')
        return []


def main():
    """主函数"""
    print('=== 搜索引擎自动提交工具 ===')
    print(f'日期: {datetime.date.today()}')
    print(f'网站: https://topventus.com')

    # 获取所有URL
    urls = get_all_urls_from_sitemap()

    if not urls:
        print('没有获取到URL，退出')
        return

    results = {
        'google': False,
        'bing': False,
        'yandex': False
    }

    # 提交到各搜索引擎
    results['google'] = submit_to_google(urls)
    results['bing'] = submit_to_bing(urls)
    results['yandex'] = submit_to_yandex(SITEMAP_URL)

    # 总结
    print('\n=== 提交总结 ===')
    for engine, success in results.items():
        status = '✓ 成功' if success else '⚠ 未完成（需要配置API凭证）'
        print(f'  {engine.capitalize()}: {status}')

    print('\n=== 手动提交链接 ===')
    print('  Google Search Console: https://search.google.com/search-console')
    print('  Bing Webmaster Tools: https://www.bing.com/webmasters')
    print('  Yandex Webmaster: https://webmaster.yandex.ru/')

    print('\n=== 配置说明 ===')
    print('如需自动提交，请在GitHub Secrets中配置以下环境变量:')
    print('  Bing: BING_API_KEY')
    print('  Yandex: YANDEX_USERNAME, YANDEX_API_KEY')
    print('  Google: GOOGLE_API_KEY, GOOGLE_CLIENT_EMAIL, GOOGLE_PRIVATE_KEY (服务账号)')


if __name__ == '__main__':
    main()
