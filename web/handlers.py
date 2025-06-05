"""
Web界面处理器
负责处理用户交互逻辑
"""

import os
import tempfile
from core import load_data_file, fix_json_file, process_in_batches


def get_json_fields(json_file):
    """获取JSON/JSONL文件中的字段名"""
    if json_file is None:
        return []
    
    try:
        # 使用统一的数据加载函数
        data = load_data_file(json_file)
        
        if not data or not isinstance(data, list):
            return []
        
        # 获取第一个对象的字段名
        first_item = data[0] if data else {}
        fields = list(first_item.keys()) if isinstance(first_item, dict) else []
        return fields
    except Exception as e:
        print(f"读取文件错误: {e}")
        return []


def process_json_to_pdf(json_file, selected_fields, output_dir, batch_size, custom_tag, fix_json_checkbox, fix_json_output):
    """处理JSON文件并生成PDF"""
    if json_file is None:
        return "❌ 请先上传JSON文件"
    
    if not selected_fields:
        return "❌ 请选择至少一个字段"
    
    if not output_dir.strip():
        return "❌ 请指定输出路径"
    
    try:
        json_data_or_path = json_file
        status_messages = []
        
        # 如果需要修复JSON文件
        if fix_json_checkbox:
            # 确定修复文件的输出路径
            if fix_json_output and fix_json_output.strip():
                fix_output_path = fix_json_output.strip()
            else:
                # 默认使用PDF输出目录
                fix_output_path = os.path.join(output_dir, "fixed.json")
            
            # 检查文件大小并决定处理方式
            file_size_mb = os.path.getsize(json_file) / (1024 * 1024)
            
            if file_size_mb > 10:  # 大文件，必须输出到文件
                is_file_output, result, status = fix_json_file(json_file, fix_output_path)
                status_messages.append(status)
                if is_file_output:
                    json_data_or_path = result  # 使用修复后的文件路径
                else:
                    return f"❌ 大文件修复失败: {status}"
            else:  # 小文件，可以存储在内存中
                is_file_output, result, status = fix_json_file(json_file)
                status_messages.append(status)
                json_data_or_path = result  # 直接使用内存中的数据
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 处理数据并生成PDF
        batches = process_in_batches(
            json_path_or_data=json_data_or_path,
            output_dir=output_dir,
            fields=selected_fields,
            batch_size=batch_size,
            tag=custom_tag
        )
        
        final_message = "\n".join(status_messages) + f"\n✅ PDF生成完成！共生成 {batches} 个文件，输出路径: {output_dir}"
        return final_message
        
    except Exception as e:
        return f"❌ 处理失败: {str(e)}"


def update_fields_dropdown(json_file):
    """更新字段下拉菜单"""
    import gradio as gr
    fields = get_json_fields(json_file)
    return gr.CheckboxGroup(
        choices=fields,
        label="选择要提取的字段",
        info="可以选择多个字段",
        visible=True if fields else False
    )


def toggle_fix_json_output(fix_json_enabled):
    """根据是否启用修复JSON功能来显示/隐藏输出路径"""
    import gradio as gr
    return gr.Textbox(visible=fix_json_enabled)


def toggle_usage_guide(current_visibility):
    """切换使用说明的显示/隐藏状态"""
    import gradio as gr
    return gr.Markdown(visible=not current_visibility)
