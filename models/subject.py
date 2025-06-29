# -*- coding: utf-8 -*-
"""
نموذج المادة الدراسية
Subject Model
"""

from app import db

class Subject(db.Model):
    """نموذج المادة الدراسية"""
    
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    grade_level = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Subject {self.name}>'
