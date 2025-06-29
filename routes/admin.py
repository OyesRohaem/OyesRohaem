# -*- coding: utf-8 -*-
"""
مسارات لوحة الإدارة
Admin Dashboard Routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps

# إنشاء Blueprint
admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """ديكوريتر للتحقق من صلاحيات المدير"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.can_access_admin():
            flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """لوحة تحكم المدير"""
    return render_template('dashboard/admin.html')

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """إدارة المستخدمين"""
    return render_template('admin/users.html')

@admin_bp.route('/students')
@login_required
@admin_required
def students():
    """إدارة الطلاب"""
    return render_template('admin/students.html')

@admin_bp.route('/teachers')
@login_required
@admin_required
def teachers():
    """إدارة المعلمين"""
    return render_template('admin/teachers.html')

@admin_bp.route('/classes')
@login_required
@admin_required
def classes():
    """إدارة الفصول"""
    return render_template('admin/classes.html')

@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    """التقارير"""
    return render_template('admin/reports.html')
