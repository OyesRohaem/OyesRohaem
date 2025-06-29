# -*- coding: utf-8 -*-
"""
نموذج الحضور والغياب
Attendance Model
"""

from datetime import datetime
from app import db

class Attendance(db.Model):
    """نموذج الحضور والغياب"""
    
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # present, absent, late
    notes = db.Column(db.Text)
    recorded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Attendance {self.student_id} - {self.date}>'
