#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社媒内容自动生成器
为每个AI生成的文章自动生成社交媒体推广文案
支持：Twitter/X、Facebook、LinkedIn、Instagram
"""

import os
import json
import urllib.request
import datetime
import re

API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
API_URL = 'https://api.deepseek.com/v1/chat/completions'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOCIAL_DIR = os.path.join(BASE_DIR, 'social-media-content')


def call_deepseek(prompt, max_tokens=500):
    """调用DeepSeek API"""
    if not API_KEY:
        print('未配置DEEPSEEK_API_KEY，跳过社媒内容生成')
        return None

    data = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': 'You are a social media marketing expert for B2B industrial companies. Write engaging, professional social media posts that drive engagement and leads. Use relevant hashtags, emojis, and clear calls to action.'},
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 0.8,
        'max_tokens': max_tokens
    }

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(data).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
    except Exception as e:
        print(f'DeepSeek API调用失败: {e}')
        return None


def generate_social_content(article_title, article_url, language='en'):
    """为一篇文章生成多平台社媒内容"""
    print(f'  生成社媒内容: {article_title[:50]}...')

    prompt = f"""Generate social media posts for this article:
Title: {article_title}
URL: {article_url}
Language: {language}

Generate 4 posts:

1. Twitter/X (280 chars max): Engaging hook + key benefit + link + 3-5 hashtags
2. Facebook (3-4 sentences): Storytelling approach + question to encourage comments + link
3. LinkedIn (professional B2B): Industry insight + data point + link + 3 hashtags
4. Instagram caption: Visual description + emoji + question + link in bio + 8-10 hashtags

Format each post with platform name as header."""

    content = call_deepseek(prompt, max_tokens=800)
    return content


def find_new_articles():
    """查找最近生成的AI文章"""
    articles = []
    today = datetime.date.today().strftime('%Y-%m-%d')

    for root, dirs, files in os.walk(BASE_DIR):
        for f in files:
            if f.startswith('news-ai-') and f.endswith('.html') and today in f:
                filepath = os.path.join(root, f)
                rel_path = os.path.relpath(filepath, BASE_DIR).replace('\\', '/')

                # 读取标题
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                        title_match = re.search(r'<title>(.*?)\s*\|', content)
                        title = title_match.group(1) if title_match else f.replace('.html', '')
                except:
                    title = f.replace('.html', '')

                # 确定URL和语言
                if rel_path.startswith('en/'):
                    url = f'https://topventus.com/{rel_path.replace(".html", "")}'
                    lang = 'en'
                elif rel_path.startswith('zh/'):
                    url = f'https://topventus.com/{rel_path.replace(".html", "")}'
                    lang = 'zh'
                else:
                    url = f'https://topventus.com/{rel_path.replace(".html", "")}'
                    lang = 'ru'

                articles.append({
                    'title': title,
                    'url': url,
                    'language': lang,
                    'file': rel_path
                })

    return articles


def main():
    """主函数"""
    print('=== 社媒内容自动生成器 ===')
    print(f'日期: {datetime.date.today()}')

    if not API_KEY:
        print('未配置DEEPSEEK_API_KEY，跳过')
        return

    # 创建输出目录
    os.makedirs(SOCIAL_DIR, exist_ok=True)

    # 查找新文章
    articles = find_new_articles()
    print(f'找到 {len(articles)} 篇新文章')

    if not articles:
        print('没有新文章需要生成社媒内容')
        return

    # 为每篇文章生成社媒内容
    today = datetime.date.today().strftime('%Y-%m-%d')
    all_content = []

    for article in articles:
        content = generate_social_content(article['title'], article['url'], article['language'])
        if content:
            all_content.append({
                'article': article,
                'content': content
            })

    # 保存为Markdown文件
    output_file = os.path.join(SOCIAL_DIR, f'social-media-posts-{today}.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f'# Social Media Content - {today}\n\n')
        f.write(f'Generated {len(all_content)} article promotion packages\n\n')
        f.write('---\n\n')

        for item in all_content:
            article = item['article']
            f.write(f'## {article["title"]}\n\n')
            f.write(f'**URL:** {article["url"]}\n')
            f.write(f'**Language:** {article["language"]}\n\n')
            f.write('### Social Media Posts\n\n')
            f.write(item['content'])
            f.write('\n\n---\n\n')

    print(f'\n✓ 社媒内容已保存: {output_file}')
    print(f'  共生成 {len(all_content)} 组推广文案')

    # 同时保存为JSON供后续自动发布使用
    json_file = os.path.join(SOCIAL_DIR, f'social-media-posts-{today}.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_content, f, ensure_ascii=False, indent=2)
    print(f'  JSON格式: {json_file}')

    print('\n=== 说明 ===')
    print('社媒文案已生成，可用于手动发布')
    print('如需自动发布，需要配置各平台API凭证:')
    print('  - Twitter/X: API Key + API Secret + Access Token + Access Secret')
    print('  - Facebook: Page Access Token + Page ID')
    print('  - LinkedIn: Client ID + Client Secret + Refresh Token')
    print('  - Instagram: Instagram Business Account ID + Facebook Access Token')


if __name__ == '__main__':
    main()
