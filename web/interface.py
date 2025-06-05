"""
Gradio界面创建模块
负责创建和配置Web界面
"""

import gradio as gr
from .handlers import (
    process_json_to_pdf,
    update_fields_dropdown, 
    toggle_fix_json_output,
    toggle_usage_guide
)
from .content import get_usage_guide, get_app_title, get_app_description
from .styles import get_header_html, get_help_button_js, get_custom_css


def create_interface():
    """创建Gradio界面"""
    with gr.Blocks(title="JSON数据处理工具", theme=gr.themes.Soft()) as app:
        # 标题和帮助按钮在同一行
        with gr.Row():
            with gr.Column(scale=6):
                gr.HTML(get_header_html())
                gr.Markdown(get_app_description(), elem_classes=["description"])
            with gr.Column(scale=1, visible=False):
                help_btn = gr.Button(
                    "使用说明",
                    variant="primary",
                    size="sm",
                    elem_id="hidden-help-btn"
                )
        
        # 使用说明内容（默认隐藏）
        usage_guide = gr.Markdown(
            value=get_usage_guide(),
            visible=False,
            label="使用说明"
        )
        
        # 使用说明可见性状态（隐藏的状态变量）
        usage_guide_visible = gr.State(value=False)
        
        with gr.Row():
            with gr.Column(scale=1):
                # 文件上传
                json_file = gr.File(
                    label="📁 上传JSON/JSONL文件",
                    file_types=[".json", ".jsonl"],
                    type="filepath"
                )
                
                # 修复JSON选项
                fix_json_checkbox = gr.Checkbox(
                    label="🔧 修复JSON文件格式",
                    info="如果JSON文件格式不规范，选择此选项进行修复",
                    value=False
                )
                
                # 修复JSON文件输出路径（仅在选择修复时显示）
                fix_json_output = gr.Textbox(
                    label="📁 修复JSON文件输出路径",
                    placeholder="不填则使用PDF输出路径，大文件必须填写",
                    visible=False,
                    info="小文件会自动存储在内存中，大文件需要指定输出路径"
                )
                
                # 字段选择
                fields_dropdown = gr.CheckboxGroup(
                    choices=[],
                    label="选择要提取的字段",
                    info="可以选择多个字段",
                    visible=False
                )
                
                # 输出路径
                output_dir = gr.Textbox(
                    label="📂 输出路径",
                    placeholder="例如: ./output/pdfs",
                    value="",
                    info="生成的PDF文件将保存到此目录中。"
                )
                
                # Batch Size
                batch_size = gr.Number(
                    value=None,
                    label="📊 Batch Size",
                    info="每个PDF文件包含的记录数量"
                )
                # batch_size = gr.Slider(
                #     minimum=50,
                #     maximum=5000,
                #     value=1500,
                #     step=50,
                #     label="📊 Batch Size",
                #     info="每个PDF文件包含的记录数量"
                # )
                
                # 自定义标记符号
                custom_tag = gr.Textbox(
                    label="🏷️ 自定义标记符号",
                    placeholder="例如: ---- 或 === 或任何分隔符",
                    value="----",
                    info="用于分隔每条记录的标记符号"
                )
            
            with gr.Column(scale=1):
                # 状态显示
                status_output = gr.Textbox(
                    label="📋 处理状态",
                    lines=10,
                    interactive=False,
                    placeholder="状态信息将在这里显示..."
                )
        
        with gr.Row():
            # 处理按钮
            process_btn = gr.Button(
                "🚀 开始处理",
                variant="primary",
                size="lg"
            )
            
            # 清除按钮
            clear_btn = gr.Button(
                "🗑️ 清除",
                variant="secondary"
            )
        
        # 事件绑定
        json_file.change(
            fn=update_fields_dropdown,
            inputs=[json_file],
            outputs=[fields_dropdown]
        )
        
        fix_json_checkbox.change(
            fn=toggle_fix_json_output,
            inputs=[fix_json_checkbox],
            outputs=[fix_json_output]
        )
        
        process_btn.click(
            fn=process_json_to_pdf,
            inputs=[json_file, fields_dropdown, output_dir, batch_size, custom_tag, fix_json_checkbox, fix_json_output],
            outputs=[status_output]
        )
        
        clear_btn.click(
            fn=lambda: (None, [], "", 1500, "----", False, "", ""),
            outputs=[json_file, fields_dropdown, output_dir, batch_size, custom_tag, fix_json_checkbox, fix_json_output, status_output]
        )
        
        # 帮助按钮点击事件 - 切换使用说明的显示/隐藏
        def toggle_help_visibility(current_visible):
            new_visible = not current_visible
            return gr.Markdown(visible=new_visible), new_visible
        
        help_btn.click(
            fn=toggle_help_visibility,
            inputs=[usage_guide_visible],
            outputs=[usage_guide, usage_guide_visible]
        )
        
        # 添加 JavaScript 来连接 HTML 按钮和 Gradio 按钮
        app.load(
            fn=None,
            inputs=None,
            outputs=None,
            js=get_help_button_js()
        )
    
    return app
