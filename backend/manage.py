#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""فایل اصلی اجرای پروژه Django"""

import os
import sys

def main():
    # تنظیم ماژول تنظیمات Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'propanalyzer_api.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django.") from exc
    
    # اجرای دستورات مدیریت Django
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()