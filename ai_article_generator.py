#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI文章生成器 - 多语言版本
使用DeepSeek API自动生成通风设备行业相关文章
"""

import os
import json
import urllib.request
import datetime
import random
import re

# 配置
API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
API_URL = 'https://api.deepseek.com/v1/chat/completions'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 文章主题库
TOPICS = [
    {
        'id': 'ventilation-design',
        'title_ru': 'Проектирование систем вентиляции для промышленных зданий',
        'title_en': 'Ventilation System Design for Industrial Buildings',
        'title_zh': '工业建筑通风系统设计要点',
        'keywords_ru': ['проектирование вентиляции', 'промышленная вентиляция', 'системы вентиляции'],
        'keywords_en': ['ventilation design', 'industrial ventilation', 'HVAC systems'],
        'keywords_zh': ['通风系统设计', '工业通风', 'HVAC系统'],
        'category': 'engineering'
    },
    {
        'id': 'fire-safety',
        'title_ru': 'Противопожарные клапаны: требования и монтаж',
        'title_en': 'Fire Dampers: Requirements and Installation',
        'title_zh': '防火阀：规范要求与安装指南',
        'keywords_ru': ['противопожарные клапаны', 'пожарная безопасность', 'монтаж клапанов'],
        'keywords_en': ['fire dampers', 'fire safety', 'damper installation'],
        'keywords_zh': ['防火阀', '消防安全', '阀门安装'],
        'category': 'safety'
    },
    {
        'id': 'smoke-control',
        'title_ru': 'Системы дымоудаления в многоэтажных зданиях',
        'title_en': 'Smoke Control Systems in High-Rise Buildings',
        'title_zh': '高层建筑排烟系统设计与应用',
        'keywords_ru': ['дымоудаление', 'системы дымоудаления', 'противодымная защита'],
        'keywords_en': ['smoke control', 'smoke extraction', 'fire protection'],
        'keywords_zh': ['排烟系统', '烟气控制', '消防保护'],
        'category': 'safety'
    },
    {
        'id': 'noise-reduction',
        'title_ru': 'Шумоглушители для вентиляционных систем',
        'title_en': 'Silencers for Ventilation Systems',
        'title_zh': '通风系统消声器选型与应用',
        'keywords_ru': ['шумоглушители', 'шум вентиляции', 'снижение шума'],
        'keywords_en': ['duct silencers', 'ventilation noise', 'noise reduction'],
        'keywords_zh': ['消声器', '通风噪音', '降噪'],
        'category': 'products'
    },
    {
        'id': 'energy-efficiency',
        'title_ru': 'Энергоэффективные системы вентиляции',
        'title_en': 'Energy-Efficient Ventilation Systems',
        'title_zh': '节能通风系统：原理与实践',
        'keywords_ru': ['энергоэффективность', 'энергосбережение', 'вентиляция'],
        'keywords_en': ['energy efficiency', 'energy saving', 'ventilation'],
        'keywords_zh': ['节能', '能效', '通风系统'],
        'category': 'engineering'
    },
    {
        'id': 'central-asia-market',
        'title_ru': 'Рынок вентиляционного оборудования в Центральной Азии',
        'title_en': 'Ventilation Equipment Market in Central Asia',
        'title_zh': '中亚通风设备市场分析与机遇',
        'keywords_ru': ['Центральная Азия', 'рынок вентиляции', 'Казахстан', 'Узбекистан'],
        'keywords_en': ['Central Asia', 'ventilation market', 'Kazakhstan', 'Uzbekistan'],
        'keywords_zh': ['中亚市场', '通风设备', '哈萨克斯坦', '乌兹别克斯坦'],
        'category': 'market'
    },
    {
        'id': 'maintenance-guide',
        'title_ru': 'Обслуживание систем вентиляции: чек-лист',
        'title_en': 'Ventilation System Maintenance: Checklist',
        'title_zh': '通风系统维护保养完整清单',
        'keywords_ru': ['обслуживание вентиляции', 'техническое обслуживание', 'чек-лист'],
        'keywords_en': ['ventilation maintenance', 'HVAC maintenance', 'checklist'],
        'keywords_zh': ['通风维护', '保养', '检查清单'],
        'category': 'guide'
    },
    {
        'id': 'air-quality',
        'title_ru': 'Обеспечение качества воздуха в помещениях',
        'title_en': 'Indoor Air Quality Assurance',
        'title_zh': '室内空气质量保障方案',
        'keywords_ru': ['качество воздуха', 'воздух в помещении', 'микроклимат'],
        'keywords_en': ['indoor air quality', 'IAQ', 'air quality'],
        'keywords_zh': ['室内空气质量', 'IAQ', '空气品质'],
        'category': 'engineering'
    },
    {
        'id': 'custom-projects',
        'title_ru': 'Индивидуальные проекты вентиляции под ключ',
        'title_en': 'Custom Turnkey Ventilation Projects',
        'title_zh': '定制化通风工程总承包服务',
        'keywords_ru': ['индивидуальные проекты', 'под ключ', 'вентиляция'],
        'keywords_en': ['custom projects', 'turnkey', 'ventilation'],
        'keywords_zh': ['定制项目', '总承包', '通风工程'],
        'category': 'services'
    },
    {
        'id': 'regulations',
        'title_ru': 'Нормативные требования к вентиляции в ЕАЭС',
        'title_en': 'Regulatory Requirements for Ventilation in EAEU',
        'title_zh': '欧亚经济联盟通风规范要求解读',
        'keywords_ru': ['нормативы', 'ЕАЭС', 'требования к вентиляции', 'сертификация'],
        'keywords_en': ['regulations', 'EAEU', 'ventilation standards', 'certification'],
        'keywords_zh': ['规范标准', '欧亚联盟', '通风要求', '认证'],
        'category': 'regulations'
    },
    {
        'id': 'project-case-hospital',
        'title_ru': 'Кейс: система вентиляции для медицинского центра',
        'title_en': 'Case Study: Ventilation System for a Medical Center',
        'title_zh': '项目案例：医疗中心通风系统设计与实施',
        'keywords_ru': ['медицинская вентиляция', 'кейс проекта', 'вентиляция больницы', 'чистые помещения'],
        'keywords_en': ['medical ventilation', 'case study', 'hospital ventilation', 'clean rooms'],
        'keywords_zh': ['医疗通风', '项目案例', '医院通风', '洁净室'],
        'category': 'case-study'
    },
    {
        'id': 'project-case-shopping',
        'title_ru': 'Кейс: вентиляция торгового центра площадью 50000 м²',
        'title_en': 'Case Study: Ventilation for 50,000 m² Shopping Mall',
        'title_zh': '项目案例：5万平米商业综合体通风系统',
        'keywords_ru': ['вентиляция ТЦ', 'торговый центр', 'кейс', 'приточная вентиляция'],
        'keywords_en': ['mall ventilation', 'shopping center', 'case study', 'supply ventilation'],
        'keywords_zh': ['商场通风', '商业中心', '案例', '送风系统'],
        'category': 'case-study'
    },
    {
        'id': 'tech-guide-damper-selection',
        'title_ru': 'Техническое руководство: как выбрать противопожарный клапан',
        'title_en': 'Technical Guide: How to Choose a Fire Damper',
        'title_zh': '技术指南：如何正确选择防火阀',
        'keywords_ru': ['выбор клапана', 'противопожарный клапан', 'техническое руководство', '70°C 280°C'],
        'keywords_en': ['damper selection', 'fire damper', 'technical guide', '70°C 280°C'],
        'keywords_zh': ['阀门选型', '防火阀', '技术指南', '70度 280度'],
        'category': 'tech-guide'
    },
    {
        'id': 'tech-guide-duct-sizing',
        'title_ru': 'Техническое руководство: расчет сечения воздуховодов',
        'title_en': 'Technical Guide: Duct Sizing Calculation',
        'title_zh': '技术指南：风管截面积计算方法',
        'keywords_ru': ['расчет воздуховодов', 'сечение воздуховода', 'скорость воздуха', 'техническое руководство'],
        'keywords_en': ['duct sizing', 'duct calculation', 'air velocity', 'technical guide'],
        'keywords_zh': ['风管计算', '风管尺寸', '风速', '技术指南'],
        'category': 'tech-guide'
    },
    {
        'id': 'market-analysis-2026',
        'title_ru': 'Анализ рынка вентиляционного оборудования 2026',
        'title_en': 'Ventilation Equipment Market Analysis 2026',
        'title_zh': '2026年通风设备市场分析与趋势预测',
        'keywords_ru': ['анализ рынка', '2026', 'тенденции', 'вентиляционное оборудование'],
        'keywords_en': ['market analysis', '2026', 'trends', 'ventilation equipment'],
        'keywords_zh': ['市场分析', '2026', '趋势', '通风设备'],
        'category': 'market'
    },
    {
        'id': 'installation-guide',
        'title_ru': 'Руководство по монтажу систем вентиляции',
        'title_en': 'Ventilation System Installation Guide',
        'title_zh': '通风系统安装施工完整指南',
        'keywords_ru': ['монтаж вентиляции', 'установка', 'руководство', 'воздуховоды'],
        'keywords_en': ['ventilation installation', 'setup', 'guide', 'ductwork'],
        'keywords_zh': ['通风安装', '施工', '指南', '风管'],
        'category': 'guide'
    },
    {
        'id': 'troubleshooting',
        'title_ru': 'Диагностика и устранение неисправностей вентиляции',
        'title_en': 'Ventilation System Troubleshooting and Repair',
        'title_zh': '通风系统常见故障诊断与排除方法',
        'keywords_ru': ['неисправности вентиляции', 'диагностика', 'ремонт', 'проблемы'],
        'keywords_en': ['ventilation problems', 'troubleshooting', 'repair', 'issues'],
        'keywords_zh': ['通风故障', '诊断', '维修', '问题'],
        'category': 'guide'
    },
    {
        'id': 'industry-trends-iot',
        'title_ru': 'Индустрия 4.0: умные системы вентиляции и IoT',
        'title_en': 'Industry 4.0: Smart Ventilation Systems and IoT',
        'title_zh': '工业4.0：智能通风系统与物联网技术应用',
        'keywords_ru': ['умная вентиляция', 'IoT', 'индустрия 4.0', 'автоматизация'],
        'keywords_en': ['smart ventilation', 'IoT', 'industry 4.0', 'automation'],
        'keywords_zh': ['智能通风', '物联网', '工业4.0', '自动化'],
        'category': 'trends'
    },
    {
        'id': 'product-comparison',
        'title_ru': 'Сравнение: круглые vs прямоугольные воздуховоды',
        'title_en': 'Comparison: Round vs Rectangular Ducts',
        'title_zh': '产品对比：圆形风管 vs 矩形风管的选择',
        'keywords_ru': ['круглые воздуховоды', 'прямоугольные воздуховоды', 'сравнение', 'выбор'],
        'keywords_en': ['round ducts', 'rectangular ducts', 'comparison', 'selection'],
        'keywords_zh': ['圆形风管', '矩形风管', '对比', '选型'],
        'category': 'products'
    },
    {
        'id': 'export-guide-central-asia',
        'title_ru': 'Экспорт вентиляционного оборудования в Центральную Азию: руководство',
        'title_en': 'Exporting Ventilation Equipment to Central Asia: A Guide',
        'title_zh': '通风设备出口中亚市场完整指南',
        'keywords_ru': ['экспорт', 'Центральная Азия', 'таможня', 'доставка', 'сертификация'],
        'keywords_en': ['export', 'Central Asia', 'customs', 'shipping', 'certification'],
        'keywords_zh': ['出口', '中亚', '清关', '物流', '认证'],
        'category': 'guide'
    },
    {
        'id': 'green-building',
        'title_ru': 'Зеленое строительство: энергоэффективная вентиляция',
        'title_en': 'Green Building: Energy-Efficient Ventilation Solutions',
        'title_zh': '绿色建筑：节能通风系统解决方案',
        'keywords_ru': ['зеленое строительство', 'энергоэффективность', 'экология', 'LEED'],
        'keywords_en': ['green building', 'energy efficiency', 'sustainability', 'LEED'],
        'keywords_zh': ['绿色建筑', '节能', '环保', 'LEED认证'],
        'category': 'trends'
    }
]


def call_deepseek(prompt, language='ru'):
    """调用DeepSeek API生成内容"""
    if not API_KEY:
        print('未配置DEEPSEEK_API_KEY，跳过AI生成')
        return None

    system_prompts = {
        'ru': 'Вы - эксперт по системам вентиляции и HVAC. Пишите профессиональные, информативные статьи на русском языке. Используйте ключевые слова естественно. Структура: введение, основная часть с подзаголовками, заключение.',
        'en': 'You are a ventilation and HVAC systems expert. Write professional, informative articles in English. Use keywords naturally. Structure: introduction, main body with subheadings, conclusion.',
        'zh': '你是通风和HVAC系统专家。用中文撰写专业、信息丰富的文章。自然地使用关键词。结构：引言、带小标题的正文、结论。'
    }

    data = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': system_prompts.get(language, system_prompts['en'])},
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 0.7,
        'max_tokens': 2000
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


def generate_article(topic, language='ru'):
    """生成单篇文章"""
    title_key = f'title_{language}'
    keywords_key = f'keywords_{language}'
    title = topic.get(title_key, topic['title_en'])
    keywords = topic.get(keywords_key, topic['keywords_en'])

    prompt = f"""Напишите подробную статью на тему: "{title}"

Ключевые слова для включения: {', '.join(keywords)}

Требования:
1. Объем 800-1200 слов
2. Структура с подзаголовками H2 и H3
3. Практические советы и рекомендации
4. Упоминание компании TopVentus как производителя
5. Призыв к действию в конце

Компания TopVentus производит: клапаны противопожарные, дымовые клапаны, шумоглушители, диффузоры, воздухораспределители, гибкие воздуховоды.
"""

    if language == 'en':
        prompt = f"""Write a detailed article on: "{title}"

Keywords to include: {', '.join(keywords)}

Requirements:
1. 800-1200 words
2. Structure with H2 and H3 subheadings
3. Practical tips and recommendations
4. Mention TopVentus as manufacturer
5. Call to action at the end

TopVentus manufactures: fire dampers, smoke dampers, silencers, diffusers, air distributors, flexible ducts.
"""
    elif language == 'zh':
        prompt = f"""撰写一篇关于"{title}"的详细文章

需要包含的关键词：{', '.join(keywords)}

要求：
1. 800-1200字
2. 使用H2和H3小标题结构
3. 实用建议和推荐
4. 提及TopVentus作为制造商
5. 结尾有行动号召

TopVentus生产：防火阀、排烟阀、消声器、散流器、风口、柔性风管。
"""

    print(f'  生成{language}文章: {title}')
    content = call_deepseek(prompt, language)
    return content


def create_article_html(topic, content, language='ru'):
    """创建文章HTML页面"""
    title_key = f'title_{language}'
    title = topic.get(title_key, topic['title_en'])
    today = datetime.date.today().strftime('%Y-%m-%d')
    article_id = f"news-ai-{topic['id']}-{today}"

    # 语言配置
    lang_config = {
        'ru': {'lang': 'ru', 'path': '', 'read_more': 'Читать далее', 'back': 'Назад к новостям', 'date_label': 'Дата публикации', 'category_label': 'Категория'},
        'en': {'lang': 'en', 'path': 'en/', 'read_more': 'Read more', 'back': 'Back to news', 'date_label': 'Publication date', 'category_label': 'Category'},
        'zh': {'lang': 'zh', 'path': 'zh/', 'read_more': '阅读更多', 'back': '返回新闻列表', 'date_label': '发布日期', 'category_label': '分类'}
    }
    cfg = lang_config.get(language, lang_config['en'])

    # 将内容转换为HTML段落
    paragraphs = content.split('\n\n') if content else ['<p>Article content coming soon.</p>']
    content_html = ''
    for p in paragraphs:
        p = p.strip()
        if p.startswith('# '):
            content_html += f'<h2>{p[2:]}</h2>\n'
        elif p.startswith('## '):
            content_html += f'<h3>{p[3:]}</h3>\n'
        elif p.startswith('### '):
            content_html += f'<h4>{p[4:]}</h4>\n'
        elif p:
            content_html += f'<p>{p}</p>\n'

    html = f'''<!DOCTYPE html>
<html lang="{cfg['lang']}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | TopVentus</title>
    <meta name="description" content="{title} - профессиональная статья от TopVentus">
    <meta name="keywords" content="{', '.join(topic.get(f'keywords_{language}', topic['keywords_en']))}">
    <link rel="canonical" href="https://topventus.com/{cfg['path']}{article_id}.html">
    <link rel="stylesheet" href="{cfg['path']}css/style.css">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{title}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://topventus.com/{cfg['path']}{article_id}.html">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{title}">
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="header-inner">
                <a href="{cfg['path']}index.html" class="logo">
                    <video class="logo-video" src="{cfg['path']}images/topventus-logo.mp4" autoplay muted loop playsinline></video>
                </a>
                <nav class="nav">
                    <a href="{cfg['path']}index.html">Главная</a>
                    <a href="{cfg['path']}products.html">Продукция</a>
                    <a href="{cfg['path']}projects.html">Проекты</a>
                    <a href="{cfg['path']}news.html">Новости</a>
                    <a href="{cfg['path']}about.html">О нас</a>
                    <a href="{cfg['path']}contact.html">Контакты</a>
                </nav>
            </div>
        </div>
    </header>

    <main>
        <article class="article-detail">
            <div class="container">
                <div class="article-meta">
                    <span>{cfg['date_label']}: {today}</span>
                    <span>{cfg['category_label']}: {topic['category']}</span>
                </div>
                <h1>{title}</h1>
                <div class="article-content">
                    {content_html}
                </div>
                <div class="article-cta">
                    <h3>Свяжитесь с нами</h3>
                    <p>TopVentus - профессиональный производитель вентиляционного оборудования. Получите консультацию и коммерческое предложение.</p>
                    <a href="{cfg['path']}contact.html" class="btn btn-primary">Связаться</a>
                </div>
                <a href="{cfg['path']}news.html" class="back-link">&larr; {cfg['back']}</a>
            </div>
        </article>
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2026 TopVentus. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>'''

    return article_id, html


def main():
    """主函数：生成2篇文章，每篇3个语言版本"""
    print('=== AI文章生成器 ===')
    print(f'当前日期: {datetime.date.today()}')

    if not API_KEY:
        print('未配置DEEPSEEK_API_KEY，跳过AI文章生成')
        return

    # 随机选择2个主题
    selected_topics = random.sample(TOPICS, min(2, len(TOPICS)))
    print(f'选择了 {len(selected_topics)} 个主题')

    generated_articles = []

    for topic in selected_topics:
        print(f'\n处理主题: {topic["id"]}')

        for language in ['ru', 'en', 'zh']:
            content = generate_article(topic, language)
            if content:
                article_id, html = create_article_html(topic, content, language)

                # 确定保存路径
                if language == 'ru':
                    save_dir = BASE_DIR
                elif language == 'en':
                    save_dir = os.path.join(BASE_DIR, 'en')
                else:
                    save_dir = os.path.join(BASE_DIR, 'zh')

                os.makedirs(save_dir, exist_ok=True)
                filepath = os.path.join(save_dir, f'{article_id}.html')

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html)

                print(f'  ✓ 已保存: {filepath}')
                generated_articles.append(article_id)
            else:
                print(f'  ✗ {language}文章生成失败')

    print(f'\n=== 生成完成 ===')
    print(f'共生成 {len(generated_articles)} 篇文章')
    for article_id in set(generated_articles):
        print(f'  - {article_id}')


if __name__ == '__main__':
    main()
