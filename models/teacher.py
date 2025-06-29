# -*- coding: utf-8 -*-
"""
نموذج المعلم
Teacher Model
"""

from datetime import datetime
from app import db

class Teacher(db.Model):
    """نموذج المعلم"""
    
    __tablename__ = 'teachers'
    
    # المعرف الأساسي
    id = db.Column(db.Integer, primary_key=True)
    
    # ربط مع المستخدم
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # رقم المعلم
    teacher_number = db.Column(db.String(20), unique=True, nullable=False)
    
    # المؤهلات
    qualification = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    experience_years = db.Column(db.Integer, default=0)
    
    # تاريخ التوظيف
    hire_date = db.Column(db.Date, default=datetime.utcnow)
    
    # حالة المعلم
    status = db.Column(db.String(20), default='active')  # active, inactive, retired
    
    # العلاقات
    user = db.relationship('User', backref='teacher_profile')
    
    def __repr__(self):
        return f'<Teacher {self.teacher_number}>'
