# Import all route blueprints to expose them for Flask app registration

from .health import blp as health_blp
from .user import blp as user_blp
from .post import blp as post_blp
from .comment import blp as comment_blp
from .like import blp as like_blp
from .feed import blp as feed_blp
