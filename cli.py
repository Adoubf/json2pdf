#!/usr/bin/env python3
"""
命令行入口
支持直接使用核心功能而不启动Web界面
"""

import argparse
import sys
from pathlib import Path

from core import process_in_batches, fix_json_file


def main():
    """命令行主函数"""
    parser = argparse.ArgumentParser(
        description="JSON数据处理工具 - 将JSON/JSONL文件转换为PDF"
    )
    
    parser.add_argument(
        "input_file",
        help="输入的JSON或JSONL文件路径"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="./output/pdfs",
        help="PDF输出目录 (默认: ./output/pdfs)"
    )
    
    parser.add_argument(
        "-f", "--fields",
        nargs="+",
        required=True,
        help="要提取的字段名 (可指定多个)"
    )
    
    parser.add_argument(
        "-b", "--batch-size",
        type=int,
        default=1500,
        help="每个PDF文件包含的记录数量 (默认: 1500)"
    )
    
    parser.add_argument(
        "-t", "--tag",
        default="----",
        help="记录分隔符 (默认: ----)"
    )
    
    parser.add_argument(
        "--fix",
        action="store_true",
        help="修复JSON文件格式"
    )
    
    parser.add_argument(
        "--fix-output",
        help="修复后的JSON文件输出路径"
    )
    
    args = parser.parse_args()
    
    # 检查输入文件是否存在
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"❌ 错误: 文件不存在 - {input_path}")
        sys.exit(1)
    
    try:
        json_data_or_path = str(input_path)
        
        # 如果需要修复JSON文件
        if args.fix:
            print("🔧 修复JSON文件...")
            is_file_output, result, status = fix_json_file(
                str(input_path), 
                args.fix_output
            )
            print(status)
            
            if is_file_output:
                json_data_or_path = result
            else:
                json_data_or_path = result
        
        # 处理数据生成PDF
        print(f"🚀 开始处理数据...")
        print(f"📁 输入文件: {input_path}")
        print(f"📂 输出目录: {args.output}")
        print(f"🎯 提取字段: {', '.join(args.fields)}")
        print(f"📊 批次大小: {args.batch_size}")
        print(f"🏷️  分隔符号: {args.tag}")
        
        batches = process_in_batches(
            json_path_or_data=json_data_or_path,
            output_dir=args.output,
            fields=args.fields,
            batch_size=args.batch_size,
            tag=args.tag
        )
        
        print(f"\n🎉 处理完成！共生成 {batches} 个PDF文件")
        
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
