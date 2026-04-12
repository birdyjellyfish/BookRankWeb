from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("books/<int:pk>/", views.BookDetail.as_view(), name="book-detail"),
    path("books/<int:pk>/availability", views.BookAvailability.as_view(), name="book-availability"),
    path("genres/", views.GenreList.as_view(), name="genre-list"),
    path("genres/<int:pk>/", views.GenreDetail.as_view(), name="genre-detail"),
    path("genres/<int:pk>/books/", views.GenreBookList.as_view(), name="genre-book-list"),
    path("books", views.BookSearch.as_view(), name="book-search"),
    path("recommender/", views.Recommender.as_view(), name="recommender"),
    path("readlist/", views.BookUserList.as_view(), name="bookuser-list"),
    path("readlist/<int:book_id>/", views.BookUserDetail.as_view(), name="bookuser-detail"),
    path("users/", views.UserDetail.as_view(), name="user-detail"),
    path("users/all/", views.AdminUserList.as_view(), name="admin-user-list"),
    path("users/<int:pk>/", views.AdminUserDetail.as_view(), name="admin-user-detail"),
    path("users/register/", views.RegisterView.as_view(), name="register"),
    path("users/login/", views.LoginView.as_view(), name="login"),
    path("users/logout/", views.LogoutView.as_view(), name="logout"),
    path("users/resetpassword/", views.PasswordResetView.as_view(), name="reset-password"),
    path("set-csrf-token/", views.SetCSRFToken, name="set-csrf-token")
]

urlpatterns = format_suffix_patterns(urlpatterns)