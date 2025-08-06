from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from app.models import db, User
from app.schemas import UserRegisterSchema, UserLoginSchema, UserProfileSchema
from app.auth_utils import (
    hash_password, verify_password, generate_jwt, jwt_required
)

blp = Blueprint("User", "user", url_prefix="/user", description="User authentication and profile management")

# PUBLIC_INTERFACE
@blp.route('/register')
class UserRegister(MethodView):
    """Register a new user"""
    @blp.arguments(UserRegisterSchema)
    @blp.response(201, UserProfileSchema)
    def post(self, user_data):
        if User.query.filter((User.username == user_data['username']) | (User.email == user_data['email'])).first():
            blp.abort(409, "User with this username or email already exists")
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            password_hash=hash_password(user_data['password'])
        )
        db.session.add(user)
        db.session.commit()
        return user

# PUBLIC_INTERFACE
@blp.route('/login')
class UserLogin(MethodView):
    """Login and retrieve JWT"""
    @blp.arguments(UserLoginSchema)
    def post(self, login_data):
        user = User.query.filter_by(email=login_data['email']).first()
        if user is None or not verify_password(login_data['password'], user.password_hash):
            blp.abort(401, "Invalid email or password")
        token = generate_jwt(user.id)
        return {"access_token": token}

# PUBLIC_INTERFACE
@blp.route('/profile')
class UserProfileView(MethodView):
    """Get or update user profile"""
    @blp.response(200, UserProfileSchema)
    @jwt_required
    def get(self):
        user = User.query.get(request.user_id)
        return user

    @blp.arguments(UserProfileSchema)
    @blp.response(200, UserProfileSchema)
    @jwt_required
    def put(self, profile_data):
        user = User.query.get(request.user_id)
        if 'bio' in profile_data:
            user.bio = profile_data['bio']
        if 'image_url' in profile_data:
            user.image_url = profile_data['image_url']
        db.session.commit()
        return user
