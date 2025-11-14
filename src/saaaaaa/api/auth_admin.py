"""
Admin Authentication Module for AtroZ Dashboard

Provides secure authentication and authorization for the admin layer,
including PDF upload and pipeline execution capabilities.

Features:
- JWT-based authentication
- Secure password hashing with bcrypt
- Role-based access control (RBAC)
- Session management
- Rate limiting for login attempts

Author: AtroZ Dashboard Security Team
Version: 1.0.0
Python: 3.10+
"""

import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Dict, Optional, Tuple

import jwt
from werkzeug.security import check_password_hash, generate_password_hash


class AuthConfig:
    """Authentication configuration"""
    # JWT Settings
    JWT_SECRET = os.getenv('ATROZ_JWT_SECRET', 'jwt-secret-key-change-in-production')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_HOURS = int(os.getenv('ATROZ_JWT_EXPIRATION_HOURS', '24'))
    
    # Password Settings
    MIN_PASSWORD_LENGTH = 12
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_DIGITS = True
    REQUIRE_SPECIAL = True
    
    # Rate Limiting
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 15
    
    # Session Settings
    SESSION_TIMEOUT_MINUTES = 120  # 2 hours


class User:
    """User model for authentication"""
    
    def __init__(self, username: str, password_hash: str, role: str = 'admin',
                 email: Optional[str] = None, enabled: bool = True):
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.email = email
        self.enabled = enabled
        self.created_at = datetime.now(timezone.utc)
        self.last_login = None
    
    def verify_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.now(timezone.utc)
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary (without password)"""
        return {
            'username': self.username,
            'role': self.role,
            'email': self.email,
            'enabled': self.enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }


class UserStore:
    """In-memory user store (replace with database in production)"""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self._init_default_users()
    
    def _init_default_users(self):
        """Initialize default admin user"""
        # Default admin (CHANGE PASSWORD IN PRODUCTION!)
        default_admin = User(
            username='admin',
            password_hash=generate_password_hash('AtroZ_Admin_2024!', method='pbkdf2:sha256'),
            role='admin',
            email='admin@atroz.local'
        )
        self.users['admin'] = default_admin
    
    def get_user(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.users.get(username)
    
    def add_user(self, user: User) -> bool:
        """Add new user"""
        if user.username in self.users:
            return False
        self.users[user.username] = user
        return True
    
    def update_user(self, user: User) -> bool:
        """Update existing user"""
        if user.username not in self.users:
            return False
        self.users[user.username] = user
        return True
    
    def delete_user(self, username: str) -> bool:
        """Delete user"""
        if username not in self.users or username == 'admin':  # Protect default admin
            return False
        del self.users[username]
        return True


class LoginAttemptTracker:
    """Track and limit login attempts"""
    
    def __init__(self):
        self.attempts: Dict[str, list] = {}
        self.lockouts: Dict[str, datetime] = {}
    
    def is_locked_out(self, username: str) -> bool:
        """Check if user is currently locked out"""
        if username not in self.lockouts:
            return False
        
        lockout_until = self.lockouts[username]
        if datetime.now(timezone.utc) > lockout_until:
            # Lockout expired
            del self.lockouts[username]
            if username in self.attempts:
                del self.attempts[username]
            return False
        
        return True
    
    def record_attempt(self, username: str, success: bool):
        """Record login attempt"""
        if success:
            # Clear attempts on successful login
            if username in self.attempts:
                del self.attempts[username]
            if username in self.lockouts:
                del self.lockouts[username]
            return
        
        # Record failed attempt
        now = datetime.now(timezone.utc)
        if username not in self.attempts:
            self.attempts[username] = []
        
        self.attempts[username].append(now)
        
        # Remove attempts older than lockout duration
        cutoff = now - timedelta(minutes=AuthConfig.LOCKOUT_DURATION_MINUTES)
        self.attempts[username] = [
            attempt for attempt in self.attempts[username]
            if attempt > cutoff
        ]
        
        # Check if should lockout
        if len(self.attempts[username]) >= AuthConfig.MAX_LOGIN_ATTEMPTS:
            lockout_until = now + timedelta(minutes=AuthConfig.LOCKOUT_DURATION_MINUTES)
            self.lockouts[username] = lockout_until
    
    def get_remaining_attempts(self, username: str) -> int:
        """Get remaining login attempts before lockout"""
        if username not in self.attempts:
            return AuthConfig.MAX_LOGIN_ATTEMPTS
        
        return max(0, AuthConfig.MAX_LOGIN_ATTEMPTS - len(self.attempts[username]))


class AuthManager:
    """Main authentication manager"""
    
    def __init__(self):
        self.user_store = UserStore()
        self.attempt_tracker = LoginAttemptTracker()
        self.active_sessions: Dict[str, Dict] = {}
    
    def authenticate(self, username: str, password: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Authenticate user and return JWT token
        
        Returns:
            (success, token, error_message)
        """
        # Check if locked out
        if self.attempt_tracker.is_locked_out(username):
            remaining_time = self._get_lockout_remaining_time(username)
            return False, None, f"Account locked. Try again in {remaining_time} minutes."
        
        # Get user
        user = self.user_store.get_user(username)
        if not user:
            self.attempt_tracker.record_attempt(username, False)
            remaining = self.attempt_tracker.get_remaining_attempts(username)
            return False, None, f"Invalid credentials. {remaining} attempts remaining."
        
        # Check if enabled
        if not user.enabled:
            return False, None, "Account disabled."
        
        # Verify password
        if not user.verify_password(password):
            self.attempt_tracker.record_attempt(username, False)
            remaining = self.attempt_tracker.get_remaining_attempts(username)
            return False, None, f"Invalid credentials. {remaining} attempts remaining."
        
        # Authentication successful
        self.attempt_tracker.record_attempt(username, True)
        user.update_last_login()
        
        # Generate JWT token
        token = self._generate_token(user)
        
        # Create session
        session_id = secrets.token_urlsafe(32)
        self.active_sessions[session_id] = {
            'username': username,
            'role': user.role,
            'created_at': datetime.now(timezone.utc),
            'last_activity': datetime.now(timezone.utc),
            'token': token
        }
        
        return True, token, None
    
    def _generate_token(self, user: User) -> str:
        """Generate JWT token for user"""
        payload = {
            'username': user.username,
            'role': user.role,
            'exp': datetime.now(timezone.utc) + timedelta(hours=AuthConfig.JWT_EXPIRATION_HOURS),
            'iat': datetime.now(timezone.utc),
            'jti': secrets.token_urlsafe(16)  # Unique token ID
        }
        
        token = jwt.encode(
            payload,
            AuthConfig.JWT_SECRET,
            algorithm=AuthConfig.JWT_ALGORITHM
        )
        
        return token
    
    def verify_token(self, token: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Verify JWT token
        
        Returns:
            (valid, payload, error_message)
        """
        try:
            payload = jwt.decode(
                token,
                AuthConfig.JWT_SECRET,
                algorithms=[AuthConfig.JWT_ALGORITHM]
            )
            
            # Check if user still exists and is enabled
            user = self.user_store.get_user(payload['username'])
            if not user or not user.enabled:
                return False, None, "User no longer valid"
            
            return True, payload, None
            
        except jwt.ExpiredSignatureError:
            return False, None, "Token expired"
        except jwt.InvalidTokenError as e:
            return False, None, f"Invalid token: {str(e)}"
    
    def _get_lockout_remaining_time(self, username: str) -> int:
        """Get remaining lockout time in minutes"""
        if username not in self.attempt_tracker.lockouts:
            return 0
        
        lockout_until = self.attempt_tracker.lockouts[username]
        remaining = lockout_until - datetime.now(timezone.utc)
        return max(0, int(remaining.total_seconds() / 60))
    
    def logout(self, token: str) -> bool:
        """Logout user and invalidate token"""
        # Find and remove session
        for session_id, session in list(self.active_sessions.items()):
            if session.get('token') == token:
                del self.active_sessions[session_id]
                return True
        return False
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        now = datetime.now(timezone.utc)
        timeout = timedelta(minutes=AuthConfig.SESSION_TIMEOUT_MINUTES)
        
        for session_id, session in list(self.active_sessions.items()):
            last_activity = session.get('last_activity')
            if last_activity and (now - last_activity) > timeout:
                del self.active_sessions[session_id]


# Global auth manager instance
auth_manager = AuthManager()


def require_auth(role: Optional[str] = None):
    """
    Decorator to require authentication for Flask routes
    
    Usage:
        @app.route('/admin/upload')
        @require_auth(role='admin')
        def upload_pdf():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request, jsonify
            
            # Get token from header
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Missing or invalid authorization header'}), 401
            
            token = auth_header.split(' ')[1]
            
            # Verify token
            valid, payload, error = auth_manager.verify_token(token)
            if not valid:
                return jsonify({'error': error or 'Invalid token'}), 401
            
            # Check role if specified
            if role and payload.get('role') != role:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            # Add user info to request context
            request.current_user = payload
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """
    Validate password meets security requirements
    
    Returns:
        (valid, error_message)
    """
    if len(password) < AuthConfig.MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {AuthConfig.MIN_PASSWORD_LENGTH} characters"
    
    if AuthConfig.REQUIRE_UPPERCASE and not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    if AuthConfig.REQUIRE_LOWERCASE and not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    if AuthConfig.REQUIRE_DIGITS and not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    
    if AuthConfig.REQUIRE_SPECIAL and not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
        return False, "Password must contain at least one special character"
    
    return True, None


# Module-level cleanup task (should be called periodically)
def cleanup_auth_sessions():
    """Cleanup expired authentication sessions"""
    auth_manager.cleanup_expired_sessions()
