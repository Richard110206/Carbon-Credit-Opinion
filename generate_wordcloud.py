# -*- coding: utf-8 -*-
"""
词云图生成脚本：对segmented_text.txt生成词云图
"""
import jieba
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from pathlib import Path

# 获取脚本所在目录
SCRIPT_DIR = Path(__file__).parent
SEGMENTED_FILE = SCRIPT_DIR / "output" / "segmented_text.txt"
STOPWORDS_FILE = SCRIPT_DIR / "data" / "stopwords_baidu.txt"
OUTPUT_DIR = SCRIPT_DIR / "output"


def is_numeric(text):
    """判断是否为纯数字"""
    return bool(re.match(r'^\d+(\.\d+)?$', text))


def load_stopwords(filepath):
    """加载停用词"""
    with open(filepath, 'r', encoding='utf-8') as f:
        stopwords = set(line.strip() for line in f if line.strip())
    return stopwords


def generate_wordcloud_from_segmented():
    """从segmented_text.txt生成词云图"""
    print("=" * 60)
    print("词云图生成 - 基于 segmented_text.txt")
    print("=" * 60)

    # 1. 加载停用词
    print("\n[1/2] 加载停用词...")
    stopwords = load_stopwords(STOPWORDS_FILE)
    print(f"  停用词: {len(stopwords)} 个")

    # 2. 读取分词文本并统计词频
    print("\n[2/2] 读取分词文本并生成词云图...")

    all_words = []
    with open(SEGMENTED_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                words = line.split()
                # 过滤停用词、单字符和数字
                filtered = [w for w in words
                           if w not in stopwords
                           and len(w) > 1
                           and not is_numeric(w)]
                all_words.extend(filtered)

    # 统计词频
    word_counts = Counter(all_words)
    print(f"  共统计 {len(word_counts)} 个不同的词")
    print(f"  总词数: {sum(word_counts.values())}")

    # 显示前20个高频词
    top_words = word_counts.most_common(20)
    print("\n  前20高频词:")
    for word, count in top_words:
        print(f"    {word}: {count}")

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 生成词云图
    wordcloud = WordCloud(
        font_path="C:/Windows/Fonts/simhei.ttf",
        width=2000,
        height=1200,
        background_color='white',
        max_words=200,
        colormap='viridis',
        relative_scaling=0.5,
        min_font_size=10
    ).generate_from_frequencies(word_counts)

    # 保存词云图
    wordcloud_output = OUTPUT_DIR / "wordcloud.png"
    plt.figure(figsize=(20, 12))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('词云图 (基于 segmented_text.txt)', fontsize=28, pad=20)
    plt.tight_layout(pad=0)
    plt.savefig(wordcloud_output, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\n  词云图已保存到: {wordcloud_output}")

    print("\n" + "=" * 60)
    print("词云图生成完成！")
    print(f"  - wordcloud.png       (词云图)")
    print("=" * 60)

    return word_counts


if __name__ == "__main__":
    generate_wordcloud_from_segmented()
