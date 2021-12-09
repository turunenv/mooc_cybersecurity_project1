from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),

    path('', views.home, name='home'),

    path('<int:note_id>/', views.private_note, name='private_note'),
    path('public/', views.public, name='public'),

    path('create-note/', views.create_note, name='create-note'),
    path('delete-note/<int:note_id>/', views.delete_note, name='delete-note')
]