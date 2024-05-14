"""librarymanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from library import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.home_view),
    path(
        "adminlogin",
        LoginView.as_view(template_name="library/adminlogin.html"),
        name="adminlogin",
    ),
    path("logout/", views.logout_view, name="logout"),
    path("afterlogin", views.after_login),
    path("search/", views.search_book_view, name="search_books"),
    # urls for books
    path("return_book/<int:id>/", views.return_book, name="return_book"),
    path("delete/book/<int:id>/", views.delete_book_view, name="delete_book"),
    path("update/book/<int:id>/", views.update_book_view, name="update_book"),
    path("addbook", views.add_book),
    path("viewbook", views.view_book, name="viewbook"),
    path("issuebook", views.issue_book),
    path("viewissuedbook", views.view_books_issued, name="viewissuedbook"),
    # urls for students
    path("delete/student/<int:id>/", views.delete_student_view, name="delete_student"),
    path("update/student/<int:id>/", views.update_student_view, name="update_student"),
    path("viewstudent", views.view_student, name="viewstudent"),
    path("addstudent", views.add_student, name="addstudent"),
]
