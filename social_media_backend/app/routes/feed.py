from flask_smorest import Blueprint
from flask.views import MethodView
from sqlalchemy import desc
from app.models import Post, Like, Comment
from app.schemas import PostSchema
from app.auth_utils import jwt_required

blp = Blueprint("Feed", "feed", url_prefix="/feed", description="Activity feed")

# PUBLIC_INTERFACE
@blp.route('/')
class Feed(MethodView):
    """Get recent posts on feed"""
    @blp.response(200, PostSchema(many=True))
    @jwt_required
    def get(self):
        posts = Post.query.order_by(desc(Post.timestamp)).limit(50).all()
        for post in posts:
            post.likes_count = Like.query.filter_by(post_id=post.id).count()
            post.comments_count = Comment.query.filter_by(post_id=post.id).count()
        return posts
