# -*- coding: utf-8 -*-
"""
情感词提取脚本：对segmented_text.txt使用SnowNLP进行情感分析
生成positive_words.txt和negative_words.txt（每行一个词，不统计）
"""
from snownlp import SnowNLP
import re
from pathlib import Path

# 获取脚本所在目录
SCRIPT_DIR = Path(__file__).parent
SEGMENTED_TEXT_FILE = SCRIPT_DIR / "output" / "segmented_text.txt"
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


def analyze_word_sentiment(word):
    """分析单个词语的情感倾向"""
    try:
        s = SnowNLP(word)
        return s.sentiments
    except:
        return 0.5  # 默认中性


def main():
    print("=" * 60)
    print("情感词提取 - 基于 segmented_text.txt")
    print("=" * 60)

    # 1. 加载停用词
    print("\n[1/4] 加载停用词...")
    stopwords = load_stopwords(STOPWORDS_FILE)
    print(f"  停用词: {len(stopwords)} 个")

    # 2. 读取分词文本
    print("\n[2/4] 读取分词文本...")
    all_words = []
    with open(SEGMENTED_TEXT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                words = line.split()
                all_words.extend(words)

    print(f"  共 {len(all_words)} 个词语")

    # 3. 过滤停用词、数字并去重
    print("\n[3/4] 过滤停用词、数字并去重...")
    filtered_words = [w for w in all_words
                     if w not in stopwords
                     and len(w) > 1
                     and not is_numeric(w)]
    unique_words = list(set(filtered_words))  # 去重
    print(f"  过滤后剩余 {len(unique_words)} 个唯一词语")

    # 4. 分析每个词语的情感
    print("\n[4/4] 分析词语情感并分类...")

    positive_words = set()
    negative_words = set()

    # 情感阈值
    POSITIVE_THRESHOLD = 0.7
    NEGATIVE_THRESHOLD = 0.3

    for i, word in enumerate(unique_words):
        sentiment = analyze_word_sentiment(word)

        if sentiment >= POSITIVE_THRESHOLD:
            positive_words.add(word)
        elif sentiment <= NEGATIVE_THRESHOLD:
            negative_words.add(word)

        if (i + 1) % 100 == 0:
            print(f"  已分析 {i + 1}/{len(unique_words)} 个词语...")

    # 5. 保存积极词语（每行一个词）
    print("\n保存结果...")
    positive_file = OUTPUT_DIR / "positive_words.txt"
    with open(positive_file, 'w', encoding='utf-8') as f:
        for word in sorted(positive_words):
            f.write(word + '\n')
    print(f"  已保存 {len(positive_words)} 个积极词语到 {positive_file}")

    # 6. 保存消极词语（每行一个词）
    negative_file = OUTPUT_DIR / "negative_words.txt"
    with open(negative_file, 'w', encoding='utf-8') as f:
        for word in sorted(negative_words):
            f.write(word + '\n')
    print(f"  已保存 {len(negative_words)} 个消极词语到 {negative_file}")

    # 打印统计信息
    print("\n" + "=" * 60)
    print("情感词提取完成！")
    print(f"  积极词语: {len(positive_words)} 个")
    print(f"  消极词语: {len(negative_words)} 个")

    # 打印部分词语示例
    print("\n积极词语示例 (前20个):")
    for i, word in enumerate(sorted(positive_words)[:20]):
        print(f"  {word}")

    print("\n消极词语示例 (前20个):")
    for i, word in enumerate(sorted(negative_words)[:20]):
        print(f"  {word}")

    print("\n生成的文件:")
    print(f"  - positive_words.txt  (积极词语)")
    print(f"  - negative_words.txt  (消极词语)")
    print("=" * 60)


if __name__ == "__main__":
    main()
