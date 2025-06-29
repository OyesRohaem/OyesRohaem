# -*- coding: utf-8 -*-
"""
نموذج المستخدم
User Model
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# استيراد قاعدة البيانات من التطبيق الرئيسي
from app import db

class User(UserMixin, db.Model):
    """نموذج المستخدم الأساسي"""
    
    __tablename__ = 'users'
    
    # المعرف الأساسي
    id = db.Column(db.Integer, primary_key=True)
    
    # بيانات تسجيل الدخول
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # البيانات الشخصية
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))  # male, female
    
    # صورة المستخدم
    profile_image = db.Column(db.String(255), default='default.jpg')
    
    # الدور والصلاحيات
    role = db.Column(db.String(20), nullable=False, default='student')
    # الأدوار: admin, teacher, student, parent
    
    # حالة الحساب
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    # تواريخ مهمة
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # العلاقات
    # سيتم إضافة العلاقات مع النماذج الأخرى لاحقاً
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    @property
    def full_name(self):
        """الاسم الكامل"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def password(self):
        """منع قراءة كلمة المرور"""
        raise AttributeError('كلمة المرور غير قابلة للقراءة')
    
    @password.setter
    def password(self, password):
        """تشفير كلمة المرور"""
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        """التحقق من كلمة المرور"""
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """تحديث وقت آخر تسجيل دخول"""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def is_admin(self):
        """التحقق من كون المستخدم مدير"""
        return self.role == 'admin'
    
    def is_teacher(self):
        """التحقق من كون المستخدم معلم"""
        return self.role == 'teacher'
    
    def is_student(self):
        """التحقق من كون المستخدم طالب"""
        return self.role == 'student'
    
    def is_parent(self):
        """التحقق من كون المستخدم ولي أمر"""
        return self.role == 'parent'
    
    def can_access_admin(self):
        """التحقق من صلاحية الوصول للوحة الإدارة"""
        return self.role in ['admin']
    
    def can_access_teacher(self):
        """التحقق من صلاحية الوصول للوحة المعلم"""
        return self.role in ['admin', 'teacher']
    
    def can_access_student(self):
        """التحقق من صلاحية الوصول للوحة الطالب"""
        return self.role in ['admin', 'teacher', 'student']
    
    def can_access_parent(self):
        """التحقق من صلاحية الوصول للوحة ولي الأمر"""
        return self.role in ['admin', 'parent']
    
    def to_dict(self):
        """تحويل البيانات إلى قاموس"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'phone': self.phone,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    @staticmethod
    def create_user(username, email, password, first_name, last_name, role='student', **kwargs):
        """إنشاء مستخدم جديد"""
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            **kwargs
        )
        user.password = password
        
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e
