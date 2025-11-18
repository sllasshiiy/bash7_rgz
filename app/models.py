from . import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import ENUM

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    PERIODICITY_CHOICES = ENUM('monthly', 'yearly', 'weekly', name='periodicity_enum')
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    periodicity = db.Column(PERIODICITY_CHOICES, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    next_billing_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('subscriptions', lazy=True))

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    table_name = db.Column(db.String(50), nullable=False)
    record_id = db.Column(db.Integer, nullable=False)
    old_values = db.Column(db.JSON)
    new_values = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('audit_logs', lazy=True))

class MigrationLog(db.Model):
    __tablename__ = 'migrations_log'
    
    id = db.Column(db.Integer, primary_key=True)
    migration_id = db.Column(db.Integer, nullable=False, unique=True)
    file_path = db.Column(db.String(255), nullable=False)
    executed_at = db.Column(db.DateTime, default=datetime.utcnow)
    checksum = db.Column(db.String(64), nullable=False)
