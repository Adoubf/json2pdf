"""
JSON文件修复模块
负责修复格式不规范的JSON/JSONL文件
"""

import json
import os
from .data_loader import load_data_file


def fix_json_file(input_path, output_path=None, size_threshold_mb=10):
    """
    修复JSON/JSONL文件格式，将每行的JSON对象组合成一个数组
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径，如果为None且文件小于阈值，则返回修复后的数据
        size_threshold_mb: 文件大小阈值（MB），超过此大小将强制写入文件
    Returns:
        tuple: (是否写入文件, 文件路径或数据, 状态信息)
    """
    try:
        # 检查文件大小
        file_size_mb = os.path.getsize(input_path) / (1024 * 1024)
        
        # 先尝试直接加载数据（支持JSON和JSONL）
        try:
            data = load_data_file(input_path)
            
            # 如果成功加载，说明文件格式正确
            if file_size_mb <= size_threshold_mb and output_path is None:
                return False, data, f"✅ 文件格式正确，数据已加载到内存 (文件大小: {file_size_mb:.2f}MB)"
            
            # 如果需要输出或文件大，复制/转换文件
            if output_path:
                # 检查是否需要格式转换（JSONL -> JSON）
                if input_path.lower().endswith('.jsonl') and output_path.lower().endswith('.json'):
                    # JSONL转JSON
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    return True, output_path, f"✅ JSONL文件已转换为JSON格式: {output_path}"
                else:
                    # 直接复制
                    with open(input_path, 'r', encoding='utf-8') as src, open(output_path, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
                    return True, output_path, f"✅ 文件已复制到: {output_path}"
            else:
                return False, data, f"✅ 文件格式正确，数据已加载到内存"
                
        except Exception:
            # 如果直接加载失败，尝试修复
            pass

        # 尝试修复文件格式
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            raise ValueError("文件为空或没有有效内容")

        # 尝试修复JSONL格式（每行一个JSON对象）
        fixed_data = []
        for i, line in enumerate(lines):
            try:
                obj = json.loads(line)
                fixed_data.append(obj)
            except json.JSONDecodeError:
                # 如果不是有效的JSON行，尝试其他修复方式
                if not (line.startswith('{') and line.endswith('}')):
                    raise ValueError(f"格式错误，第{i+1}行不是有效的JSON对象：{line[:50]}...")
                
                # 尝试在每行末尾添加逗号的方式修复
                try:
                    obj = json.loads(line)
                    fixed_data.append(obj)
                except json.JSONDecodeError:
                    raise ValueError(f"无法修复第{i+1}行的JSON格式：{line[:50]}...")

        if not fixed_data:
            raise ValueError("没有找到有效的JSON数据")

        # 根据文件大小和是否提供输出路径决定处理方式
        if file_size_mb <= size_threshold_mb and output_path is None:
            # 小文件且无输出路径，返回数据
            return False, fixed_data, f"✅ 修复完成，数据已加载到内存 (文件大小: {file_size_mb:.2f}MB)"
        else:
            # 大文件或指定了输出路径，写入文件
            if not output_path:
                raise ValueError("大文件必须指定输出路径")
            
            # 写入为JSON数组格式
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(fixed_data, f, ensure_ascii=False, indent=2)
            
            return True, output_path, f"✅ 修复完成，输出文件为: {output_path} (文件大小: {file_size_mb:.2f}MB)"
        
    except Exception as e:
        error_msg = f"❌ 修复失败: {e}"
        print(error_msg)
        raise Exception(error_msg)
