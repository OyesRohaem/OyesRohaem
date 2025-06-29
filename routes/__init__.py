# -*- coding: utf-8 -*-
"""
مسارات التطبيق
Application Routes Package
"""

# تصدير جميع المسارات
from .auth import auth_bp
from .admin import admin_bp
from .teacher import teacher_bp
from .student import student_bp
from .parent import parent_bp

__all__ = [
    'auth_bp',
    'admin_bp', 
    'teacher_bp',
    'student_bp',
    'parent_bp'
]
