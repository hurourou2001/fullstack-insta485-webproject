"""Views, one for each Insta485 page."""
from insta485.views.index import show_index
from insta485.views.explore import show_explore
from insta485.views.user import show_user
from insta485.views.user import uploaded_file
from insta485.views.follow import show_followers
from insta485.views.follow import show_following
from insta485.views.follow import follow_user
from insta485.views.likes import update_likes
from insta485.views.comments import update_comments
from insta485.views.posts import show_posts
from insta485.views.create import create
from insta485.views.delete import delete
from insta485.views.edit import edit
from insta485.views.password import password
from insta485.views.login import login
from insta485.views.accounts import accounts
from insta485.views.auth import auth
