"""
数据加载模块
负责处理 JSON 和 JSONL 文件的加载
"""

import json


def load_json(json_path):
    """加载标准JSON文件"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_jsonl(jsonl_path):
    """加载JSONL文件"""
    data = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"警告: 跳过无效的JSON行: {line[:50]}... 错误: {e}")
                    continue
    return data


def load_data_file(file_path):
    """根据文件扩展名自动选择加载方式"""
    if file_path.lower().endswith('.jsonl'):
        return load_jsonl(file_path)
    else:
        return load_json(file_path)
