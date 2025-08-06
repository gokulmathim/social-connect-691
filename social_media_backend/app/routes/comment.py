from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from sqlalchemy import desc
from app.models import db, Comment, Post  # Removed unused 'User'
from app.schemas import CommentCreateSchema, CommentSchema
from app.auth_utils import jwt_required

blp = Blueprint("Comment", "comment", url_prefix="/comment", description="Commenting on posts")

# PUBLIC_INTERFACE
@blp.route('/post/<int:post_id>')
class CommentOnPost(MethodView):
    """Comments on a specific post"""
    @blp.arguments(CommentCreateSchema)
    @blp.response(201, CommentSchema)
    @jwt_required
    def post(self, comment_data, post_id):
        post = Post.query.get_or_404(post_id)
        comment = Comment(
            body=comment_data['body'],
            user_id=request.user_id,
            post_id=post.id
        )
        db.session.add(comment)
        db.session.commit()
        return comment

    @blp.response(200, CommentSchema(many=True))
    @jwt_required
    def get(self, post_id):
        comments = Comment.query.filter_by(post_id=post_id).order_by(desc(Comment.timestamp)).all()
        return comments
