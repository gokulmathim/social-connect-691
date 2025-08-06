from marshmallow import Schema, fields  # Removed unused 'validate'

# PUBLIC_INTERFACE
class UserRegisterSchema(Schema):
    """Schema for new user registration."""
    username = fields.Str(required=True, description="Unique username")
    email = fields.Email(required=True, description="User email address")
    password = fields.Str(required=True, load_only=True, description="Password")

# PUBLIC_INTERFACE
class UserLoginSchema(Schema):
    """Schema for user login."""
    email = fields.Email(required=True, description="User email address")
    password = fields.Str(required=True, load_only=True, description="Password")

# PUBLIC_INTERFACE
class UserProfileSchema(Schema):
    """Schema for user profile (data returned to clients)."""
    id = fields.Int()
    username = fields.Str()
    email = fields.Email()
    bio = fields.Str()
    image_url = fields.Str()

# PUBLIC_INTERFACE
class PostCreateSchema(Schema):
    """Schema to create a new post."""
    body = fields.Str(required=True, description="Text content of the post")
    image_url = fields.Str(missing=None, allow_none=True, description="Optional image URL")

# PUBLIC_INTERFACE
class PostSchema(Schema):
    """Schema for returning post data including additional relations."""
    id = fields.Int()
    body = fields.Str()
    image_url = fields.Str()
    timestamp = fields.DateTime()
    author = fields.Nested(UserProfileSchema)
    likes_count = fields.Int()
    comments_count = fields.Int()

# PUBLIC_INTERFACE
class CommentCreateSchema(Schema):
    """Schema for creating a comment on a post."""
    body = fields.Str(required=True, description="Comment text")

# PUBLIC_INTERFACE
class CommentSchema(Schema):
    """Schema for returning a comment."""
    id = fields.Int()
    body = fields.Str()
    timestamp = fields.DateTime()
    author = fields.Nested(UserProfileSchema)

# PUBLIC_INTERFACE
class LikeSchema(Schema):
    """Schema for a like entry."""
    id = fields.Int()
    user = fields.Nested(UserProfileSchema)
