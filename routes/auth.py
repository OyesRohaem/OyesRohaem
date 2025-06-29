# -*- coding: utf-8 -*-
"""
مسارات المصادقة
Authentication Routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from app import db

# إنشاء Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل الدخول"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        
        if not username or not password:
            flash('يرجى إدخال اسم المستخدم وكلمة المرور', 'error')
            return render_template('auth/login.html')
        
        # البحث عن المستخدم
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if user and user.verify_password(password):
            if not user.is_active:
                flash('حسابك غير مفعل. يرجى التواصل مع الإدارة', 'error')
                return render_template('auth/login.html')
            
            # تسجيل الدخول
            login_user(user, remember=remember)
            user.update_last_login()
            
            flash(f'مرحباً {user.full_name}', 'success')
            
            # التوجيه حسب الدور
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            if user.is_admin():
                return redirect(url_for('admin.dashboard'))
            elif user.is_teacher():
                return redirect(url_for('teacher.dashboard'))
            elif user.is_student():
                return redirect(url_for('student.dashboard'))
            elif user.is_parent():
                return redirect(url_for('parent.dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """تسجيل الخروج"""
    logout_user()
    flash('تم تسجيل الخروج بنجاح', 'info')
    return redirect(url_for('index'))

@auth_bp.route('/profile')
@login_required
def profile():
    """صفحة الملف الشخصي"""
    return render_template('auth/profile.html', user=current_user)

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """تغيير كلمة المرور"""
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not current_user.verify_password(current_password):
            flash('كلمة المرور الحالية غير صحيحة', 'error')
            return render_template('auth/change_password.html')
        
        if new_password != confirm_password:
            flash('كلمة المرور الجديدة غير متطابقة', 'error')
            return render_template('auth/change_password.html')
        
        if len(new_password) < 6:
            flash('كلمة المرور يجب أن تكون 6 أحرف على الأقل', 'error')
            return render_template('auth/change_password.html')
        
        # تحديث كلمة المرور
        current_user.password = new_password
        db.session.commit()
        
        flash('تم تغيير كلمة المرور بنجاح', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/change_password.html')
