# -*- coding: utf-8 -*-
"""
نماذج قاعدة البيانات
Database Models Package
"""

from flask_sqlalchemy import SQLAlchemy

# تصدير جميع النماذج
from .user import User
from .student import Student
from .teacher import Teacher
from .class_model import Class
from .subject import Subject
from .attendance import Attendance
from .grade import Grade
from .assignment import Assignment

__all__ = [
    'User',
    'Student', 
    'Teacher',
    'Class',
    'Subject',
    'Attendance',
    'Grade',
    'Assignment'
]
