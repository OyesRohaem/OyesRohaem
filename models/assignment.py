# -*- coding: utf-8 -*-
"""
نموذج الواجبات
Assignment Model
"""

from datetime import datetime
from app import db

class Assignment(db.Model):
    """نموذج الواجبات"""
    
    __tablename__ = 'assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    max_score = db.Column(db.Float, default=100)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Assignment {self.title}>'
