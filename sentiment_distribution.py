# -*- coding: utf-8 -*-
"""
情感分布图生成脚本：对segmented_text.txt生成0-1之间的连续情感分析分布图
"""
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# 获取脚本所在目录
SCRIPT_DIR = Path(__file__).parent
SEGMENTED_TEXT_FILE = SCRIPT_DIR / "output" / "segmented_text.txt"
STOPWORDS_FILE = SCRIPT_DIR / "data" / "stopwords_baidu.txt"
OUTPUT_DIR = SCRIPT_DIR / "output"


def load_stopwords(filepath):
    """加载停用词"""
    with open(filepath, 'r', encoding='utf-8') as f:
        stopwords = set(line.strip() for line in f if line.strip())
    return stopwords


def analyze_segmented_text_sentiment():
    """分析分词文本的情感分布"""
    print("=" * 60)
    print("情感分布分析 - 基于 segmented_text.txt")
    print("=" * 60)

    # 1. 加载停用词
    print("\n[1/3] 加载停用词...")
    stopwords = load_stopwords(STOPWORDS_FILE)
    print(f"  停用词: {len(stopwords)} 个")

    # 2. 读取分词文本并分析情感
    print("\n[2/3] 读取分词文本并分析情感...")

    sentiments = []
    texts_count = 0

    with open(SEGMENTED_TEXT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and len(line) > 2:
                try:
                    s = SnowNLP(line)
                    sentiments.append(s.sentiments)
                    texts_count += 1
                    if texts_count % 100 == 0:
                        print(f"  已分析 {texts_count} 条文本...")
                except Exception as e:
                    pass

    print(f"  共分析 {len(sentiments)} 条文本的情感")

    # 3. 统计情感分布
    print("\n[3/3] 统计情感分布并生成图表...")

    # 按区间统计
    negative = sum(1 for s in sentiments if s < 0.3)
    neutral = sum(1 for s in sentiments if 0.3 <= s < 0.7)
    positive = sum(1 for s in sentiments if s >= 0.7)

    print(f"\n情感分布：")
    print(f"  负面 (0-0.3): {negative} ({negative/len(sentiments)*100:.1f}%)")
    print(f"  中性 (0.3-0.7): {neutral} ({neutral/len(sentiments)*100:.1f}%)")
    print(f"  正面 (0.7-1.0): {positive} ({positive/len(sentiments)*100:.1f}%)")
    print(f"  平均情感值: {np.mean(sentiments):.3f}")

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 生成情感分布直方图
    print("\n  生成情感分布直方图...")
    hist_output = OUTPUT_DIR / "sentiment_histogram.png"
    plt.figure(figsize=(14, 8))
    plt.hist(sentiments, bins=50, color='steelblue', edgecolor='black', alpha=0.7)

    # 添加分界线和平均值线
    plt.axvline(0.3, color='red', linestyle='--', linewidth=2, label='负面分界线 (0.3)')
    plt.axvline(0.7, color='green', linestyle='--', linewidth=2, label='正面分界线 (0.7)')
    plt.axvline(np.mean(sentiments), color='orange', linestyle='-',
                linewidth=3, label=f'平均值 ({np.mean(sentiments):.3f})')

    plt.xlabel('情感值', fontsize=14)
    plt.ylabel('文本数量', fontsize=14)
    plt.title('情感值分布直方图 (0-1连续分布)', fontsize=18, pad=15)
    plt.legend(fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(hist_output, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  已保存: {hist_output}")

    print("\n" + "=" * 60)
    print("情感分布图生成完成！")
    print("  - sentiment_histogram.png (情感分布直方图)")
    print("=" * 60)

    return sentiments


if __name__ == "__main__":
    analyze_segmented_text_sentiment()
