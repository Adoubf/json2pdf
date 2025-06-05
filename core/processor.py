"""
主处理器模块
负责批量处理数据并生成PDF文件
"""

import math
import os
from datetime import datetime
from tqdm import tqdm

from .data_loader import load_data_file
from .pdf_generator import convert_chunk_to_markdown, markdown_to_pdf


def process_in_batches(json_path_or_data, output_dir, fields, batch_size=100, tag="----"):
    """
    批量处理JSON数据并生成PDF
    Args:
        json_path_or_data: JSON/JSONL文件路径或已加载的数据列表
        output_dir: 输出目录
        fields: 要提取的字段列表
        batch_size: 批处理大小
        tag: 分隔标记
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 判断输入是文件路径还是数据
    if isinstance(json_path_or_data, str):
        data = load_data_file(json_path_or_data)
    else:
        data = json_path_or_data
    
    total = len(data)
    batches = math.ceil(total / batch_size)

    for i in tqdm(range(batches), desc="生成PDF中", ncols=80):
        start = i * batch_size
        end = min(start + batch_size, total)
        chunk = data[start:end]

        markdown_content = convert_chunk_to_markdown(chunk, fields, tag)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        pdf_output_path = os.path.join(output_dir, f'医疗问诊_{timestamp}_batch{i+1}.pdf')

        markdown_to_pdf(markdown_content, pdf_output_path)

    print(f"\n✅ 全部完成，共生成 {batches} 个 PDF 文件，输出路径：{output_dir}")
    return batches
