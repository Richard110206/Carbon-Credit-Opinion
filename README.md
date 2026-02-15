# 碳积分对Z世代绿色出行影响的舆论分析

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()

## 项目简介

本项目旨在分析碳积分、碳普惠等激励机制对Z世代绿色出行行为影响的机制。通过对三大社交媒体平台（微博、小红书、知乎）上相关话题的舆论数据进行采集和情感分析，探究年轻群体对绿色出行政策的认知态度和情感倾向，为政策制定和推广提供数据支持。

## 核心功能

- 📊 **多平台数据采集**: 支持微博、小红书、知乎三大社交平台
- 🔄 **中文文本预处理**: jieba分词、停用词过滤、数字过滤
- 💚 **情感倾向分析**: 基于SnowNLP的中文情感分析
- ☁️ **词云可视化**: 整体词云、积极/消极情感词云
- 📈 **情感分布统计**: 0-1连续情感值分布直方图

## 数据来源

数据使用 [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) 开源项目爬取，涵盖以下平台：

- **微博**: 86条内容 + 239条评论
- **小红书**: 140条内容 + 700条评论
- **知乎**: 110条内容 + 1317条评论

**总计**: 336条内容 + 2256条评论

### 爬取关键词

- 绿色出行
- 碳积分
- 碳普惠
- 低碳生活
- 环保出行

## 技术栈

### 后端处理
- **Python**: 3.x
- **pandas**: 数据处理和CSV文件读取
- **jieba**: 中文分词
- **SnowNLP**: 中文情感分析

### 数据可视化
- **matplotlib**: 图表绘制
- **wordcloud**: 词云图生成

### 辅助工具
- [词云工具](https://www.uciyun.com/cn/): 情感词云图在线生成

## 环境配置

### 系统要求
- Python 3.7+
- Windows / Linux / macOS

### 依赖安装

```bash
pip install pandas jieba snownlp matplotlib wordcloud
```

或使用 requirements.txt:

```bash
pip install -r requirements.txt
```

### requirements.txt

```
pandas>=1.3.0
jieba>=0.42.1
snownlp>=0.12.3
matplotlib>=3.3.0
wordcloud>=1.8.0
```

## 项目结构

```
carbon-credit-opinion/
├── data/
│   ├── stopwords_baidu.txt    # 百度停用词表
│   ├── weibo/                 # 微博爬取数据
│   │   └── csv/
│   ├── xhs/                   # 小红书爬取数据
│   │   └── csv/
│   └── zhihu/                 # 知乎爬取数据
│       └── csv/
├── output/                    # 输出结果目录
│   ├── segmented_text.txt     # 分词后文本
│   ├── positive_words.txt     # 积极词语列表
│   ├── negative_words.txt     # 消极词语列表
│   ├── wordcloud.png          # 整体词云图
│   ├── positive_wordcloud.png # 积极情感词云图
│   ├── negative_wordcloud.png # 消极情感词云图
│   ├── wordcloud_footprint.png # 词云足迹图
│   └── sentiment_histogram.png # 情感分布直方图
├── process_text.py            # 文本预处理脚本
├── generate_wordcloud.py      # 词云图生成脚本
├── sentiment_words.py         # 情感词提取脚本
├── sentiment_distribution.py  # 情感分布分析脚本
└── README.md                  # 项目说明文档
```

## 使用方法

### 1. 准备数据

确保 `data/` 目录下包含三个平台的CSV数据文件：

```
data/
├── weibo/csv/search_contents_*.csv
├── weibo/csv/search_comments_*.csv
├── xhs/csv/search_contents_*.csv
├── xhs/csv/search_comments_*.csv
├── zhihu/csv/search_contents_*.csv
└── zhihu/csv/search_comments_*.csv
```

### 2. 运行脚本

按顺序执行以下脚本：

```bash
# 步骤1: 文本预处理 - 提取内容/评论，分词，过滤停用词和数字
python process_text.py
```

输出: `output/segmented_text.txt`

```bash
# 步骤2: 生成整体词云图
python generate_wordcloud.py
```

输出: `output/wordcloud.png`

```bash
# 步骤3: 提取情感词 - 生成积极/消极词语列表
python sentiment_words.py
```

输出: `output/positive_words.txt`, `output/negative_words.txt`

```bash
# 步骤4: 生成情感分布图
python sentiment_distribution.py
```

输出: `output/sentiment_histogram.png`

### 3. 生成情感词云图（可选）

将 `positive_words.txt` 和 `negative_words.txt` 中的词语分别复制到 [词云工具](https://www.uciyun.com/cn/) 生成对应的词云图。

## 输出结果说明

### 文本文件

| 文件 | 说明 | 数量 |
|------|------|------|
| segmented_text.txt | 分词后文本（已过滤停用词和数字） | 2493条 |
| positive_words.txt | 积极词语列表（每行一个词） | 3729个 |
| negative_words.txt | 消极词语列表（每行一个词） | 1598个 |

### 可视化图表

| 图表 | 说明 | 生成方式 |
|------|------|----------|
| wordcloud.png | 整体词云图 | Python脚本生成 |
| positive_wordcloud.png | 积极情感词云图（绿色调） | [在线工具](https://www.uciyun.com/cn/) |
| negative_wordcloud.png | 消极情感词云图（红色调） | [在线工具](https://www.uciyun.com/cn/) |
| wordcloud_footprint.png | 词云足迹图 | [在线工具](https://www.uciyun.com/cn/) |
| sentiment_histogram.png | 情感值分布直方图（0-1连续分布） | Python脚本生成 |

## 注意事项

1. **停用词过滤**: 使用百度停用词表，可根据需要自定义停用词
2. **数字过滤**: 自动过滤纯数字词汇
3. **情感阈值**: 积极词语 ≥ 0.7，消极词语 ≤ 0.3，可根据需求调整
4. **字体设置**: 词云图生成使用黑体，确保系统中有该字体

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 致谢

- [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) - 数据爬取工具
- [SnowNLP](https://github.com/isnowfy/snownlp) - 中文情感分析库
- [词云工具](https://www.uciyun.com/cn/) - 在线词云可视化工具

## 许可证

[MIT License](LICENSE)

## 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 提交 [Issue](https://github.com/Richard110206/-Carbon-Credit-Opinion-/issues)
- 发送邮件至: your.email@example.com
