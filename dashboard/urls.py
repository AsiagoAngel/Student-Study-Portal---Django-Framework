from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from dashboard import views
from dashboard import views as dash_views
from .views import custom_logout
urlpatterns = [
    # -------- Notes Section ------------ #

    path('', views.home, name="home"),
    path('notes', views.notes, name="notes"),
    path('delete_note/<int:pk>', views.delete_note, name="delete-note"),
    path('notes_detail/<int:pk>', views.NotesDetailView.as_view(), name="notes-detail"),

    # -------- Homework Section ------------ #

    path('homework', views.homework, name="homework"),
    path('update_homework/<int:pk>', views.update_homework, name="update-homework"),
    path('delete_homework/<int:pk>', views.delete_homework, name="delete-homework"),


    # -------- To Do Section ------------ #

    path('todo', views.todo, name="todo"),
    path('update_todo/<int:pk>', views.update_todo, name="update-todo"),
    path('delete_todo/<int:pk>', views.delete_todo, name="delete-todo"),

    # -------- BOOK Section ------------ #

    path('books', views.books, name="books"),

    # -------- Dictionary Section ------------ #

    path('dictionary', views.dictionary, name="dictionary"),

    # -------- Wikipedia Section ------------ #

    path('wiki', views.wiki, name="wiki"),

    # -------- Conversion Section ------------ #
    path('login/',auth_views.LoginView.as_view(template_name="dashboard/login.html"), name='login'),
    path('profile',views.profile,name='profile'),
    path('register/',dash_views.register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name="dashboard/login.html"),name='login'), 
    path('profile/',dash_views.profile,name="profile"),
   path('logout/', custom_logout, name='logout'),  # Custom logout view

]

    # or
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Default Django logout view
