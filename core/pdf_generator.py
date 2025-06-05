"""
PDF生成模块
负责将数据转换为Markdown格式并生成PDF
"""

import markdown2
from weasyprint import HTML, CSS


def convert_chunk_to_markdown(data_chunk, fields, tag="----"):
    """
    将数据块转换为 Markdown 格式
    Args:
        data_chunk: 数据块列表
        fields: 要提取的字段名列表
        tag: 分隔标记
    """
    md_lines = []
    for item in data_chunk:
        md_lines.append('<div class="record">')
        
        # 处理多个字段
        for field in fields:
            if field in item:
                field_content = str(item[field]).strip().replace('\n\n', '<br><br>').replace('\n', '<br>')
                md_lines.append(f"<h3>{field}:</h3>")
                md_lines.append(f"<p>{field_content}</p>")
        
        md_lines.append(tag)
        md_lines.append("</div>")
    return "\n".join(md_lines)


def markdown_to_pdf(markdown_content, pdf_path):
    """
    将Markdown内容转换为PDF文件
    Args:
        markdown_content: Markdown格式的内容
        pdf_path: 输出PDF文件路径
    """
    html_content = markdown2.markdown(markdown_content, extras=["fenced-code-blocks"])
    custom_css = CSS(string="""
        body {
            font-family: "Microsoft YaHei", sans-serif;
            line-height: 1.8;
            font-size: 14px;
            margin: 2cm;
        }
        h2 {
            color: #333;
            margin: 1em 0 0.5em;
        }
        h3 {
            color: #555;
            margin: 0.8em 0 0.3em;
            font-size: 16px;
        }
        p {
            text-align: justify;
            margin-bottom: 1em;
        }
        hr {
            border: none;
            border-top: 1px solid #ccc;
            margin: 1.5em 0;
        }
        .record {
            page-break-inside: avoid;
            break-inside: avoid;
            margin-bottom: 2em;
            padding: 1em;
            border-left: 3px solid #007acc;
            background-color: #f9f9f9;
        }
    """)
    HTML(string=html_content).write_pdf(pdf_path, stylesheets=[custom_css])
