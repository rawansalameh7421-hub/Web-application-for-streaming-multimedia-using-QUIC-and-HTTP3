# -*- coding: utf-8 -*-
# filename: DB.py

import sqlite3
from pathlib import Path
import bcrypt

# --- الإعدادات ---
# تحديد مسار ملف قاعدة البيانات في نفس مجلد السكربت
DATABASE_FILE = Path(__file__).resolve().parent / "users.db"

def setup_database():
    """
    تقوم بإنشاء قاعدة البيانات وجدول المستخدمين إذا لم يكونا موجودين.
    """
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        # إنشاء جدول المستخدمين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print("✅ Permanent SQLite database is setup and ready.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def add_user(username, password):
    """
    تضيف مستخدماً جديداً إلى قاعدة البيانات مع تشفير كلمة المرور.
    تعيد True عند النجاح، و False عند الفشل (إذا كان المستخدم موجوداً).
    """
    try:
        # تحويل كلمة المرور إلى بايت وتشفيرها
        password_bytes = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        # تخزين كلمة المرور المشفرة (كـ string)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password.decode('utf-8')))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:  # يحدث هذا الخطأ إذا كان اسم المستخدم مكرراً
        return False
    except Exception as e:
        print(f"An error occurred in add_user: {e}")
        return False


def find_user(username):
    """
    تبحث عن مستخدم في قاعدة البيانات باستخدام اسمه.
    تعيد بيانات المستخدم (بما في ذلك كلمة المرور المشفرة) إذا تم العثور عليه.
    """
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        return user
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def check_password(stored_password, provided_password):
    """
    تقارن كلمة المرور المقدمة مع النسخة المشفرة المخزنة.
    """
    try:
        stored_password_bytes = stored_password.encode('utf-8')
        provided_password_bytes = provided_password.encode('utf-8')
        return bcrypt.checkpw(provided_password_bytes, stored_password_bytes)
    except Exception:
        return False

