# -*- coding: utf-8 -*-
"""
مسارات لوحة الطالب
Student Dashboard Routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps

# إنشاء Blueprint
student_bp = Blueprint('student', __name__)

def student_required(f):
    """ديكوريتر للتحقق من صلاحيات الطالب"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.can_access_student():
            flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    """لوحة تحكم الطالب"""
    return render_template('dashboard/student.html')

@student_bp.route('/grades')
@login_required
@student_required
def grades():
    """درجات الطالب"""
    return render_template('student/grades.html')

@student_bp.route('/attendance')
@login_required
@student_required
def attendance():
    """حضور الطالب"""
    return render_template('student/attendance.html')

@student_bp.route('/assignments')
@login_required
@student_required
def assignments():
    """واجبات الطالب"""
    return render_template('student/assignments.html')
