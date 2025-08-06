from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from sqlalchemy import desc
from app.models import db, Post, Like, Comment  # Removed unused 'User'
from app.schemas import PostCreateSchema, PostSchema
from app.auth_utils import jwt_required

blp = Blueprint("Post", "post", url_prefix="/post", description="Post and feed management")

# PUBLIC_INTERFACE
@blp.route('/')
class PostList(MethodView):
    """Create a new post or get posts"""
    @blp.arguments(PostCreateSchema)
    @blp.response(201, PostSchema)
    @jwt_required
    def post(self, post_data):
        new_post = Post(
            body=post_data['body'],
            image_url=post_data.get('image_url'),
            author_id=request.user_id
        )
        db.session.add(new_post)
        db.session.commit()
        # Add like/comment counts for API doc compatibility
        new_post.likes_count = 0
        new_post.comments_count = 0
        return new_post

    @blp.response(200, PostSchema(many=True))
    @jwt_required
    def get(self):
        posts = Post.query.order_by(desc(Post.timestamp)).all()
        for post in posts:
            post.likes_count = Like.query.filter_by(post_id=post.id).count()
            post.comments_count = Comment.query.filter_by(post_id=post.id).count()
        return posts

# PUBLIC_INTERFACE
@blp.route('/<int:post_id>')
class PostDetail(MethodView):
    """Get, or delete a post"""
    @blp.response(200, PostSchema)
    @jwt_required
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        post.likes_count = Like.query.filter_by(post_id=post.id).count()
        post.comments_count = Comment.query.filter_by(post_id=post.id).count()
        return post

    @jwt_required
    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        if post.author_id != request.user_id:
            blp.abort(403, "You can delete only your own posts")
        db.session.delete(post)
        db.session.commit()
        return '', 204
