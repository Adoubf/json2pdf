"""
主应用程序入口
使用重构后的模块化结构
"""

from web import create_interface


def main():
    """启动应用程序"""
    app = create_interface()
    app.launch(
        server_name="127.0.0.1",
        server_port=8000,
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    main()
