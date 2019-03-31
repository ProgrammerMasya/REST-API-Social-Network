from django.urls import path
from home.views import PostsView, registration_view, login_view, profile_view, \
    like_view, dislike_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('home/', PostsView.as_view(), name='base'),
    path('registration/', registration_view, name='registration'),
    path('logout/', LogoutView.as_view(next_page='base'), name='logout'),
    path('login/', login_view, name='login'),
    path('like/', like_view, name='like'),
    path('dislike/', dislike_view, name='dislike'),
    path('profile/', profile_view, name='profile'),
]