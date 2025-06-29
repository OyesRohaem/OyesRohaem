# -*- coding: utf-8 -*-
"""
نموذج الدرجات
Grade Model
"""

from datetime import datetime
from app import db

class Grade(db.Model):
    """نموذج الدرجات"""
    
    __tablename__ = 'grades'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    exam_type = db.Column(db.String(50), nullable=False)  # quiz, midterm, final
    score = db.Column(db.Float, nullable=False)
    max_score = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Grade {self.student_id} - {self.subject_id}>'
