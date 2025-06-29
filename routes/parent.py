# -*- coding: utf-8 -*-
"""
مسارات لوحة ولي الأمر
Parent Dashboard Routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps

# إنشاء Blueprint
parent_bp = Blueprint('parent', __name__)

def parent_required(f):
    """ديكوريتر للتحقق من صلاحيات ولي الأمر"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.can_access_parent():
            flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@parent_bp.route('/dashboard')
@login_required
@parent_required
def dashboard():
    """لوحة تحكم ولي الأمر"""
    return render_template('dashboard/parent.html')

@parent_bp.route('/children')
@login_required
@parent_required
def children():
    """أطفال ولي الأمر"""
    return render_template('parent/children.html')

@parent_bp.route('/reports')
@login_required
@parent_required
def reports():
    """تقارير الأطفال"""
    return render_template('parent/reports.html')
