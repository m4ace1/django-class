from . import views
from django.urls import path

urlpatterns = [
    path('blogs/', views.blogs),
    path('blog/', views.get_blog_post),
    path('signup/', views.signup),
    path('login/', views.login)
]