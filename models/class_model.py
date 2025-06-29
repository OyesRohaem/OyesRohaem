# -*- coding: utf-8 -*-
"""
نموذج الفصل
Class Model
"""

from datetime import datetime
from app import db

class Class(db.Model):
    """نموذج الفصل الدراسي"""
    
    __tablename__ = 'classes'
    
    # المعرف الأساسي
    id = db.Column(db.Integer, primary_key=True)
    
    # اسم الفصل
    name = db.Column(db.String(50), nullable=False)
    
    # الصف الدراسي
    grade_level = db.Column(db.String(10), nullable=False)
    
    # المعلم المسؤول
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    
    # السعة القصوى
    capacity = db.Column(db.Integer, default=30)
    
    # السنة الدراسية
    academic_year = db.Column(db.String(10), nullable=False)
    
    # حالة الفصل
    is_active = db.Column(db.Boolean, default=True)
    
    # تواريخ
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقات
    teacher = db.relationship('Teacher', backref='classes')
    students = db.relationship('Student', backref='class_info')
    
    def __repr__(self):
        return f'<Class {self.name}>'
