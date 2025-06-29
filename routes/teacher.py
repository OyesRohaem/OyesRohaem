# -*- coding: utf-8 -*-
"""
مسارات لوحة المعلم
Teacher Dashboard Routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps

# إنشاء Blueprint
teacher_bp = Blueprint('teacher', __name__)

def teacher_required(f):
    """ديكوريتر للتحقق من صلاحيات المعلم"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.can_access_teacher():
            flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@teacher_bp.route('/dashboard')
@login_required
@teacher_required
def dashboard():
    """لوحة تحكم المعلم"""
    return render_template('dashboard/teacher.html')

@teacher_bp.route('/classes')
@login_required
@teacher_required
def classes():
    """فصول المعلم"""
    return render_template('teacher/classes.html')

@teacher_bp.route('/attendance')
@login_required
@teacher_required
def attendance():
    """تسجيل الحضور"""
    return render_template('teacher/attendance.html')

@teacher_bp.route('/grades')
@login_required
@teacher_required
def grades():
    """إدارة الدرجات"""
    return render_template('teacher/grades.html')
