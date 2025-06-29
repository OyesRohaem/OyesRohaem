#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة المدرسة الابتدائية
Elementary School Management System

الملف الرئيسي للتطبيق
Main application file
"""

import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from flask_migrate import Migrate
from config import config

# إنشاء التطبيق
def create_app(config_name=None):
    """إنشاء وتكوين تطبيق Flask"""
    app = Flask(__name__)
    
    # تحديد بيئة التشغيل
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'development')
    
    # تطبيق الإعدادات
    app.config.from_object(config[config_name])
    
    # تهيئة الإضافات
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # تسجيل المسارات
    register_blueprints(app)
    
    # إنشاء الجداول
    with app.app_context():
        db.create_all()
        create_default_admin()
    
    return app

# إعداد قاعدة البيانات
db = SQLAlchemy()
migrate = Migrate()

# إعداد نظام تسجيل الدخول
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'يرجى تسجيل الدخول للوصول إلى هذه الصفحة.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """تحميل المستخدم من قاعدة البيانات"""
    from models.user import User
    return User.query.get(int(user_id))

def register_blueprints(app):
    """تسجيل جميع المسارات"""
    # المسارات الأساسية
    @app.route('/')
    def index():
        """الصفحة الرئيسية"""
        if current_user.is_authenticated:
            # توجيه المستخدم حسب دوره
            if current_user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif current_user.role == 'teacher':
                return redirect(url_for('teacher.dashboard'))
            elif current_user.role == 'student':
                return redirect(url_for('student.dashboard'))
            elif current_user.role == 'parent':
                return redirect(url_for('parent.dashboard'))
        
        return render_template('index.html')
    
    @app.route('/about')
    def about():
        """صفحة حول النظام"""
        return render_template('about.html')
    
    # معالج الأخطاء
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # تسجيل المسارات الفرعية
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.teacher import teacher_bp
    from routes.student import student_bp
    from routes.parent import parent_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(parent_bp, url_prefix='/parent')

def create_default_admin():
    """إنشاء حساب المدير الافتراضي"""
    from models.user import User
    from werkzeug.security import generate_password_hash
    
    # التحقق من وجود مدير
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin_user = User(
            username='admin',
            email='admin@school.edu',
            first_name='مدير',
            last_name='النظام',
            role='admin',
            is_active=True
        )
        admin_user.password_hash = generate_password_hash('admin123')
        
        try:
            db.session.add(admin_user)
            db.session.commit()
            print("تم إنشاء حساب المدير الافتراضي:")
            print("اسم المستخدم: admin")
            print("كلمة المرور: admin123")
        except Exception as e:
            db.session.rollback()
            print(f"خطأ في إنشاء حساب المدير: {e}")

# إنشاء التطبيق
app = create_app()

if __name__ == '__main__':
    # تشغيل التطبيق في وضع التطوير
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
