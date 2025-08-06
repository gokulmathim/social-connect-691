from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# PUBLIC_INTERFACE
class User(db.Model):
    """User model representing application users."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.String(256))
    image_url = db.Column(db.String(256))

    posts = relationship('Post', back_populates='author', cascade="all, delete-orphan")
    comments = relationship('Comment', back_populates='author', cascade="all, delete-orphan")
    likes = relationship('Like', back_populates='user', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"

# PUBLIC_INTERFACE
class Post(db.Model):
    """Post model for user posts in the feed."""
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text(), nullable=False)
    image_url = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    author = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post', cascade="all, delete-orphan")
    likes = relationship('Like', back_populates='post', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Post {self.id} by {self.author_id}>"

# PUBLIC_INTERFACE
class Comment(db.Model):
    """Comment model for storing comments on posts."""
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

    def __repr__(self):
        return f"<Comment {self.id} on post {self.post_id}>"

# PUBLIC_INTERFACE
class Like(db.Model):
    """Like model for storing 'likes' on posts."""
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    user = relationship('User', back_populates='likes')
    post = relationship('Post', back_populates='likes')

    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='_user_post_uc'),)

    def __repr__(self):
        return f"<Like user {self.user_id} post {self.post_id}>"
