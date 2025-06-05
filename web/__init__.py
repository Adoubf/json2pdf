"""
Web界面模块
"""

from .interface import create_interface
from .handlers import (
    get_json_fields,
    process_json_to_pdf,
    update_fields_dropdown,
    toggle_fix_json_output,
    toggle_usage_guide
)
from .content import get_usage_guide
from .styles import get_header_html, get_help_button_js, get_custom_css

__all__ = [
    'create_interface',
    'get_json_fields',
    'process_json_to_pdf', 
    'update_fields_dropdown',
    'toggle_fix_json_output',
    'toggle_usage_guide',
    'get_usage_guide',
    'get_header_html',
    'get_help_button_js',
    'get_custom_css'
]
