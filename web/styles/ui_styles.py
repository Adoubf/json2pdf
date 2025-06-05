"""
样式相关的HTML和CSS代码
"""


def get_header_html():
    """获取页面头部的HTML代码，包含标题和帮助按钮"""
    return """
    <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 10px;">
        <h1 style="margin: 0; font-size: 24px; color: #333;">📄 JSON数据处理工具</h1>
        <button id="help-btn" style="
            background: #4A90E2; 
            color: white; 
            border: none; 
            padding: 6px 12px; 
            border-radius: 6px; 
            font-size: 12px; 
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 4px;
            font-weight: 500;
            transition: background-color 0.2s ease;
        " onmouseover="this.style.backgroundColor='#357ABD'" 
           onmouseout="this.style.backgroundColor='#4A90E2'">使用说明</button>
    </div>
    """


def get_help_button_js():
    """获取帮助按钮的JavaScript代码"""
    return """
    function() {
        // 连接 HTML 按钮和 Gradio 按钮
        setTimeout(function() {
            const htmlBtn = document.getElementById('help-btn');
            const gradioBtn = document.getElementById('hidden-help-btn');
            
            if (htmlBtn && gradioBtn) {
                htmlBtn.addEventListener('click', function() {
                    gradioBtn.click();
                });
            }
        }, 1000);
    }
    """


def get_custom_css():
    """获取自定义CSS样式"""
    return """
    <style>
    .description {
        color: #666;
        font-size: 14px;
        margin-top: 5px;
    }
    
    .gradio-container {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .help-section {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #4A90E2;
    }
    
    .help-section h2 {
        color: #2c3e50;
        margin-top: 0;
    }
    
    .help-section h3 {
        color: #34495e;
    }
    
    .help-section code {
        background: #e9ecef;
        padding: 2px 4px;
        border-radius: 3px;
        font-family: 'Courier New', monospace;
    }
    
    .help-section pre {
        background: #2d3748;
        color: #e2e8f0;
        padding: 15px;
        border-radius: 6px;
        overflow-x: auto;
    }
    
    .help-section pre code {
        background: transparent;
        color: inherit;
    }
    </style>
    """
