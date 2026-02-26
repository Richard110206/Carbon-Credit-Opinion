# -*- coding: utf-8 -*-
"""
文本处理脚本：从CSV中提取内容和评论，进行分词处理
"""
import pandas as pd
import jieba
import re
from pathlib import Path

# 获取脚本所在目录
SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR / "data"
STOPWORDS_FILE = BASE_DIR / "stopwords_baidu.txt"
OUTPUT_DIR = SCRIPT_DIR / "output"

# 创建输出目录
OUTPUT_DIR.mkdir(exist_ok=True)

# 各平台数据文件配置
PLATFORM_CONFIG = {
    'weibo': {
        'content_file': BASE_DIR / 'weibo' / 'csv' / 'search_contents_2026-02-12.csv',
        'comment_file': BASE_DIR / 'weibo' / 'csv' / 'search_comments_2026-02-12.csv',
        'content_column': 'content',
        'comment_column': 'content'
    },
    'xhs': {
        'content_file': BASE_DIR / 'xhs' / 'csv' / 'search_contents_2026-02-12.csv',
        'comment_file': BASE_DIR / 'xhs' / 'csv' / 'search_comments_2026-02-12.csv',
        'content_column': 'desc',
        'comment_column': 'content'
    },
    'zhihu': {
        'content_file': BASE_DIR / 'zhihu' / 'csv' / 'search_contents_2026-02-12.csv',
        'comment_file': BASE_DIR / 'zhihu' / 'csv' / 'search_comments_2026-02-12.csv',
        'content_column': 'content_text',
        'comment_column': 'content'
    }
}


def load_stopwords(filepath):
    """加载停用词表"""
    with open(filepath, 'r', encoding='utf-8') as f:
        stopwords = set(line.strip() for line in f if line.strip())
    return stopwords


def is_numeric(text):
    """判断是否为纯数字"""
    return bool(re.match(r'^\d+(\.\d+)?$', text))


def extract_text_from_csv(filepath, text_column):
    """从CSV文件中提取文本列"""
        df = pd.read_csv(filepath, encoding='utf-8')
        texts = df[text_column].dropna().astype(str).tolist()
        return texts

def segment_and_filter(texts, stopwords):
    """使用jieba分词并过滤停用词和数字"""
    jieba.setLogLevel(jieba.logging.INFO)

    results = []
    for text in texts:
        text = text.strip()
        if not text:
            continue

        # 分词
        words = jieba.cut(text)

        # 过滤停用词、单字符和数字
        filtered_words = [w for w in words
                         if w not in stopwords
                         and len(w) > 1
                         and not is_numeric(w)]

        if filtered_words:
            results.append(' '.join(filtered_words))

    return results


def main():
    print("=" * 60)
    print("文本处理流程：提取内容/评论 → 分词 → 生成segmented_text.txt")
    print("=" * 60)

    # 1. 加载停用词
    print("\n[1/3] 加载停用词...")
    stopwords = load_stopwords(STOPWORDS_FILE)
    print(f"  加载了 {len(stopwords)} 个停用词")

    # 2. 提取各平台的内容和评论
    print("\n[2/3] 从CSV文件提取内容和评论...")

    all_texts = []
    content_count = 0
    comment_count = 0

    for platform, config in PLATFORM_CONFIG.items():
        print(f"\n  处理 {platform} 平台...")

        # 提取内容
        contents = extract_text_from_csv(config['content_file'], config['content_column'])
        all_texts.extend(contents)
        content_count += len(contents)
        print(f"    提取了 {len(contents)} 条内容")

        # 提取评论
        comments = extract_text_from_csv(config['comment_file'], config['comment_column'])
        all_texts.extend(comments)
        comment_count += len(comments)
        print(f"    提取了 {len(comments)} 条评论")

    print(f"\n  总计: {content_count} 条内容, {comment_count} 条评论, 共 {len(all_texts)} 条文本")

    # 3. 分词并过滤停用词和数字
    print("\n[3/3] jieba分词并过滤停用词和数字...")
    segmented_texts = segment_and_filter(all_texts, stopwords)
    print(f"  分词后剩余 {len(segmented_texts)} 条有效文本")

    # 保存分词结果
    segmented_file = OUTPUT_DIR / "segmented_text.txt"
    with open(segmented_file, 'w', encoding='utf-8') as f:
        for line in segmented_texts:
            f.write(line + '\n')
    print(f"  已保存到 {segmented_file}")

    # 统计信息
    print("\n" + "=" * 60)
    print("处理完成！生成文件:")
    print(f"  segmented_text.txt    - 分词后文本 ({len(segmented_texts)} 条)")
    print("=" * 60)


if __name__ == "__main__":
    main()
