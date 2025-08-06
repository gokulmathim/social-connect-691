from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from app.models import db, Like
from app.schemas import LikeSchema
from app.auth_utils import jwt_required

blp = Blueprint("Like", "like", url_prefix="/like", description="Like/unlike posts")

# PUBLIC_INTERFACE
@blp.route('/post/<int:post_id>')
class LikePost(MethodView):
    """Like or unlike a post"""
    @blp.response(200, LikeSchema(many=True))
    @jwt_required
    def get(self, post_id):
        likes = Like.query.filter_by(post_id=post_id).all()
        return likes

    @jwt_required
    def post(self, post_id):
        # Unused: post = Post.query.get_or_404(post_id)
        like = Like.query.filter_by(post_id=post_id, user_id=request.user_id).first()
        if like:
            # Unlike
            db.session.delete(like)
            db.session.commit()
            return {'liked': False}
        else:
            # Like
            like = Like(post_id=post_id, user_id=request.user_id)
            db.session.add(like)
            db.session.commit()
            return {'liked': True}
