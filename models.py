from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='employee')  # admin, manager, employee
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    monthly_salary = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    manager = db.relationship('User', remote_side=[id], backref='team_members')
    attendances = db.relationship('Attendance', backref='employee', lazy='dynamic')
    regularization_requests = db.relationship('RegularizationRequest', 
                                              foreign_keys='RegularizationRequest.user_id',
                                              backref='employee', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def is_manager(self):
        return self.role in ['admin', 'manager']

    def __repr__(self):
        return f'<User {self.emp_id} - {self.name}>'


class Attendance(db.Model):
    __tablename__ = 'attendances'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    punch_in_time = db.Column(db.DateTime, nullable=True)
    punch_out_time = db.Column(db.DateTime, nullable=True)
    punch_in_lat = db.Column(db.Float, nullable=True)
    punch_in_lng = db.Column(db.Float, nullable=True)
    punch_out_lat = db.Column(db.Float, nullable=True)
    punch_out_lng = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), default='absent')  # present, absent, regularized, half-day
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'date', name='unique_user_date'),
    )

    def working_hours(self):
        if self.punch_in_time and self.punch_out_time:
            delta = self.punch_out_time - self.punch_in_time
            total_seconds = int(delta.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours}h {minutes}m"
        return "—"

    def __repr__(self):
        return f'<Attendance {self.user_id} on {self.date}>'


class Holiday(db.Model):
    __tablename__ = 'holidays'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    creator = db.relationship('User', backref='created_holidays')

    def __repr__(self):
        return f'<Holiday {self.name} on {self.date}>'


class RegularizationRequest(db.Model):
    __tablename__ = 'regularization_requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    requested_punch_in = db.Column(db.DateTime, nullable=True)
    requested_punch_out = db.Column(db.DateTime, nullable=True)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    manager_comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    reviewer = db.relationship('User', foreign_keys=[reviewed_by], backref='reviewed_requests')

    def __repr__(self):
        return f'<RegularizationRequest {self.id} by User {self.user_id}>'
