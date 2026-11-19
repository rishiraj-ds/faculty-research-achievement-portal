from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('records/add/', views.add_record, name='add_record'),
    path('records/<int:pk>/edit/', views.edit_record, name='edit_record'),
    path('records/<int:pk>/delete/', views.delete_record, name='delete_record'),

    path('review/', views.review, name='review'),
    path('review/<int:pk>/<str:action>/', views.decide, name='decide'),
    path('reports/', views.report, name='report'),
    path('reports/export.csv', views.export_csv, name='export_csv'),
]
