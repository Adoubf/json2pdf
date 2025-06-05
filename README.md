# JSON数据处理工具

这是一个用于处理JSON数据并生成PDF文件的工具，支持从JSON文件中提取指定字段并格式化渲染为PDF文档。

## 功能特性

- 📁 **文件上传**: 支持上传JSON格式的数据文件
- 🔧 **JSON修复**: 自动修复不规范的JSON文件格式
- 🎯 **字段选择**: 支持选择多个字段进行提取
- 📂 **路径配置**: 可自定义PDF输出路径
- 📊 **批量处理**: 支持调整batch size控制每个PDF文件的记录数量
- 🖥️ **Web界面**: 基于Gradio的直观Web界面

## 安装依赖

确保你的系统已安装Python 3.8+，然后安装项目依赖：

```bash
pip install -e .
```

或者直接安装依赖：

```bash
pip install gradio markdown2 weasyprint tqdm pandas
```

## 使用方法

### 1. 启动Web界面

```bash
python main.py
```

或安装后使用命令：

```bash
json-processor-web
```

然后在浏览器中访问 `http://localhost:8000`

### 2. 命令行使用

```bash
python cli.py input.json -f answer question -o ./output -b 1000
```

或安装后使用命令：

```bash
json-processor input.json -f answer question -o ./output -b 1000
```

命令行参数：
- `input_file`: 输入的JSON或JSONL文件路径
- `-f, --fields`: 要提取的字段名 (必需，可指定多个)
- `-o, --output`: PDF输出目录 (默认: ./output/pdfs)
- `-b, --batch-size`: 每个PDF文件包含的记录数量 (默认: 1500)
- `-t, --tag`: 记录分隔符 (默认: ----)
- `--fix`: 修复JSON文件格式
- `--fix-output`: 修复后的JSON文件输出路径

### 3. 使用Web界面

1. **上传JSON文件**: 点击"上传JSON文件"按钮选择你的JSON数据文件
2. **修复格式**: 如果JSON文件格式不规范，勾选"修复JSON文件格式"选项
3. **选择字段**: 上传文件后会自动显示可选字段，选择需要提取的字段
4. **设置输出**: 指定PDF文件的输出路径
5. **调整Batch Size**: 根据需要调整每个PDF文件包含的记录数量
6. **开始处理**: 点击"开始处理"按钮生成PDF文件

### 4. 模块化使用

你也可以直接导入模块使用：

```python
from core import process_in_batches, fix_json_file

# 修复JSON文件
is_file_output, result, status = fix_json_file("input.json", "fixed.json")
print(status)

# 处理数据生成PDF
batches = process_in_batches(
    json_path_or_data="fixed.json",
    output_dir="./output",
    fields=["answer", "question"],  # 指定要提取的字段
    batch_size=1500,
    tag="----"
)
print(f"生成了 {batches} 个PDF文件")
```

## JSON文件格式

支持的JSON文件格式：

```json
[
  {
    "question": "问题内容",
    "answer": "答案内容",
    "other_field": "其他字段"
  },
  {
    "question": "另一个问题",
    "answer": "另一个答案",
    "other_field": "其他内容"
  }
]
```

如果你的JSON文件是每行一个JSON对象的格式（JSONL），工具会自动检测并修复：

```json
{"question": "问题1", "answer": "答案1"}
{"question": "问题2", "answer": "答案2"}
```

## 项目结构

```
dataset_processing/
├── core/                   # 核心处理模块
│   ├── __init__.py        # 核心模块导出
│   ├── data_loader.py     # 数据加载器 (JSON/JSONL)
│   ├── json_repair.py     # JSON文件修复
│   ├── pdf_generator.py   # PDF生成器
│   └── processor.py       # 主处理器
├── web/                   # Web界面模块  
│   ├── __init__.py        # Web模块导出
│   ├── content.py         # 界面文字内容
│   ├── handlers.py        # 事件处理器
│   └── interface.py       # Gradio界面
├── main.py                # Web应用入口
├── cli.py                 # 命令行入口
├── pyproject.toml         # 项目配置和依赖
└── README.md              # 项目说明
```

## 系统要求

- Python 3.8+
- 足够的磁盘空间存储生成的PDF文件
- 如果处理大文件，建议有充足的内存

## 故障排除

### WeasyPrint安装问题

如果遇到WeasyPrint安装问题，请参考官方文档：

- **Ubuntu/Debian**: 
  ```bash
  sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
  ```

- **macOS**:
  ```bash
  brew install cairo pango gdk-pixbuf libffi
  ```

- **Windows**: 建议使用WSL或Docker

### 内存不足

如果处理大文件时遇到内存不足，可以：
- 减小batch_size的值
- 分批处理大文件

## 许可证

MIT License
