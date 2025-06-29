# -*- coding: utf-8 -*-
"""
نموذج الطالب
Student Model
"""

from datetime import datetime
from app import db

class Student(db.Model):
    """نموذج الطالب"""
    
    __tablename__ = 'students'
    
    # المعرف الأساسي
    id = db.Column(db.Integer, primary_key=True)
    
    # ربط مع المستخدم
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # رقم الطالب
    student_number = db.Column(db.String(20), unique=True, nullable=False)
    
    # معلومات أكاديمية
    grade_level = db.Column(db.String(10))  # الصف
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    
    # معلومات ولي الأمر
    parent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # تاريخ التسجيل
    enrollment_date = db.Column(db.Date, default=datetime.utcnow)
    
    # حالة الطالب
    status = db.Column(db.String(20), default='active')  # active, inactive, graduated
    
    # العلاقات
    user = db.relationship('User', foreign_keys=[user_id], backref='student_profile')
    parent = db.relationship('User', foreign_keys=[parent_id], backref='children')
    
    def __repr__(self):
        return f'<Student {self.student_number}>'
